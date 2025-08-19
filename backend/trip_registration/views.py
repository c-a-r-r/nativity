"""
Trip Registration Views
API endpoints for handling trip registration and payment processing
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from django.conf import settings
import json
import logging

from .models import (
    ClientTmp, PilgrimageClientTmp, Client, PilgrimageClient, 
    Country, Pilgrimage
)
from .serializers import (
    TripRegistrationSerializer, PaymentProcessSerializer,
    CountrySerializer, PilgrimageSerializer
)
from .services import AuthorizeNetService
from .email_service import RegistrationEmailService

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_countries(request):
    """Get list of all countries for the registration form"""
    countries = Country.objects.all().order_by('nombre')
    serializer = CountrySerializer(countries, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_pilgrimage(request, pilgrimage_id):
    """Get pilgrimage details for registration"""
    try:
        pilgrimage = Pilgrimage.objects.get(id=pilgrimage_id, status='active')
        serializer = PilgrimageSerializer(pilgrimage)
        return Response(serializer.data)
    except Pilgrimage.DoesNotExist:
        return Response(
            {'error': 'Pilgrimage not found or not available for registration'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def submit_registration(request):
    """
    Submit trip registration form
    Creates temporary records and initiates payment process
    """
    serializer = TripRegistrationSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {'error': 'Invalid registration data', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        with transaction.atomic():
            # Create temporary registration
            result = serializer.save()
            
            # If payment by mail, mark as submitted
            if not result['payment_required']:
                # Send confirmation emails for non-credit card payments
                try:
                    # Get temp registration for email data
                    temp_registration = PilgrimageClientTmp.objects.get(id=result['registration_id'])
                    
                    # Prepare email data
                    registration_data = {
                        'id': result['registration_id'],
                        'pilgrimage_id': serializer.validated_data['pilgrimage_id'],
                        'trip_title': serializer.validated_data['trip_title'],
                        'trip_price': float(serializer.validated_data['trip_price']),
                        'customer_notes': serializer.validated_data.get('customer_notes', ''),
                        'payment': {
                            'payment_type': serializer.validated_data['payment']['payment_type'],
                            'payment_plan': serializer.validated_data['payment']['payment_plan'],
                            'total_amount': float(serializer.validated_data['payment']['total_amount'])
                        }
                    }
                    
                    # Prepare passenger data for email
                    passengers_for_email = []
                    for i, passenger in enumerate(serializer.validated_data['passengers']):
                        passenger_email_data = passenger.copy()
                        passenger_email_data['is_primary'] = (i == 0)
                        passengers_for_email.append(passenger_email_data)
                    
                    # Send customer confirmation email
                    RegistrationEmailService.send_customer_confirmation(registration_data, passengers_for_email)
                    
                    # Send admin notification email
                    RegistrationEmailService.send_admin_notification(registration_data, passengers_for_email)
                    
                except Exception as email_error:
                    logger.error(f"Failed to send confirmation emails for non-CC payment: {str(email_error)}")
                
                return Response({
                    'success': True,
                    'message': 'Registration submitted successfully. You will receive payment instructions by email.',
                    'registration_id': result['registration_id'],
                    'payment_method': 'mail'
                })
            
            # For credit card payments, return payment processing info
            return Response({
                'success': True,
                'message': 'Registration created. Please proceed with payment.',
                'registration_id': result['registration_id'],
                'session_id': result['session_id'],
                'payment_required': True,
                'total_amount': float(result['total_amount']),
                'passengers_count': result['passengers_count'],
                'expires_at': result['expires_at'].isoformat()
            })
            
    except Exception as e:
        logger.error(f"Registration submission error: {str(e)}")
        return Response(
            {'error': 'An error occurred while processing your registration. Please try again.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def process_payment(request):
    """
    Process credit card payment via Authorize.Net
    Moves data from temp tables to permanent tables upon success
    """
    serializer = PaymentProcessSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {'error': 'Invalid payment request', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    registration_id = serializer.validated_data['registration_id']
    session_id = serializer.validated_data['session_id']
    
    try:
        # Get the temporary registration
        temp_registration = PilgrimageClientTmp.objects.get(
            id=registration_id,
            session_id=session_id
        )
        
        # Mark payment as attempted
        temp_registration.payment_attempted = True
        temp_registration.save()
        
        # Initialize Authorize.Net service
        auth_service = AuthorizeNetService()
        
        # Calculate total with processing fee (3% for credit cards)
        base_amount = float(temp_registration.totalcost - temp_registration.discount)
        processing_fee = base_amount * 0.03  # 3% processing fee
        total_amount = base_amount + processing_fee
        
        # Process payment (this would integrate with actual Authorize.Net)
        payment_result = auth_service.process_payment(
            amount=total_amount,
            card_data=request.data.get('card_data', {}),
            billing_data=request.data.get('billing_data', {}),
            order_id=f"REG-{registration_id}"
        )
        
        if payment_result['success']:
            # Payment successful - move to permanent tables
            with transaction.atomic():
                # Create permanent client record(s)
                # Parse passenger arrays from temp record
                passenger_count = len(json.loads(temp_registration.firstname or '[]'))
                
                for i in range(passenger_count):
                    # Extract passenger data from arrays
                    passenger_data = {}
                    for field in ['firstname', 'lastname', 'email', 'phone', 'fax', 'country', 
                                'state', 'city', 'address', 'zipcode', 'birthday', 'gender',
                                'occupation', 'passport', 'passport_exp', 'passport_country',
                                'nationality', 'emergency_contact', 'emergency_contact_phone',
                                'shirt_size', 'dietary_restrictions', 'medical_conditions',
                                'room_preference', 'roommate_preference', 'previous_traveler',
                                'preferred_name', 'middle_name', 'suffix', 'title', 'address2',
                                'mobile_phone', 'work_phone', 'business_email', 'personal_email',
                                'social_security', 'employer', 'business_address', 'business_city',
                                'business_state', 'business_zip', 'business_country', 'special_assistance']:
                        
                        field_data = getattr(temp_registration, field)
                        if field_data:
                            try:
                                field_array = json.loads(field_data)
                                passenger_data[field] = field_array[i] if i < len(field_array) else ''
                            except (json.JSONDecodeError, IndexError):
                                passenger_data[field] = ''
                        else:
                            passenger_data[field] = ''
                    
                    # Create permanent client record
                    client = Client.objects.create(
                        title=passenger_data.get('title', ''),
                        name=passenger_data.get('firstname', ''),
                        lastname=passenger_data.get('lastname', ''),
                        email=passenger_data.get('email', ''),
                        phone=passenger_data.get('phone', ''),
                        fax=passenger_data.get('fax', ''),
                        country=passenger_data.get('country', ''),
                        state=passenger_data.get('state', ''),
                        city=passenger_data.get('city', ''),
                        address=passenger_data.get('address', ''),
                        zipcode=passenger_data.get('zipcode', ''),
                        birthday=passenger_data.get('birthday') or None,
                        gender=passenger_data.get('gender', ''),
                        occupation=passenger_data.get('occupation', ''),
                        passport=passenger_data.get('passport', ''),
                        passport_exp=passenger_data.get('passport_exp') or None,
                        passport_country=passenger_data.get('passport_country', ''),
                        nationality=passenger_data.get('nationality', ''),
                        emergency_contact=passenger_data.get('emergency_contact', ''),
                        emergency_contact_phone=passenger_data.get('emergency_contact_phone', ''),
                        shirt_size=passenger_data.get('shirt_size', ''),
                        dietary_restrictions=passenger_data.get('dietary_restrictions', ''),
                        medical_conditions=passenger_data.get('medical_conditions', ''),
                        know_us=temp_registration.know_us,
                        room_preference=passenger_data.get('room_preference', ''),
                        roommate_preference=passenger_data.get('roommate_preference', ''),
                        previous_traveler=passenger_data.get('previous_traveler', ''),
                        preferred_name=passenger_data.get('preferred_name', ''),
                        middle_name=passenger_data.get('middle_name', ''),
                        suffix=passenger_data.get('suffix', ''),
                        address2=passenger_data.get('address2', ''),
                        mobile_phone=passenger_data.get('mobile_phone', ''),
                        work_phone=passenger_data.get('work_phone', ''),
                        business_email=passenger_data.get('business_email', ''),
                        personal_email=passenger_data.get('personal_email', ''),
                        social_security=passenger_data.get('social_security', ''),
                        employer=passenger_data.get('employer', ''),
                        business_address=passenger_data.get('business_address', ''),
                        business_city=passenger_data.get('business_city', ''),
                        business_state=passenger_data.get('business_state', ''),
                        business_zip=passenger_data.get('business_zip', ''),
                        business_country=passenger_data.get('business_country', ''),
                        special_assistance=passenger_data.get('special_assistance', '')
                    )
                
                # Create permanent pilgrimage_client record
                pilgrimage_client = PilgrimageClient.objects.create(
                    pilgrimage_id=temp_registration.pilgrimage_id,
                    client_id=client.id,  # Link to first passenger as primary
                    ap=temp_registration.ap,
                    gsv=temp_registration.gsv,
                    departurecity_id=temp_registration.departurecity_id,
                    landonly=temp_registration.landonly,
                    totalcost=temp_registration.totalcost,
                    payed=total_amount,
                    discount=temp_registration.discount,
                    coupon=temp_registration.coupon,
                    paymentoption=temp_registration.paymentoption,
                    firstname=temp_registration.firstname,
                    lastname=temp_registration.lastname,
                    email=temp_registration.email,
                    phone=temp_registration.phone,
                    fax=temp_registration.fax,
                    country=temp_registration.country,
                    state=temp_registration.state,
                    city=temp_registration.city,
                    address=temp_registration.address,
                    zipcode=temp_registration.zipcode,
                    birthday=temp_registration.birthday,
                    gender=temp_registration.gender,
                    occupation=temp_registration.occupation,
                    passport=temp_registration.passport,
                    passport_exp=temp_registration.passport_exp,
                    passport_country=temp_registration.passport_country,
                    nationality=temp_registration.nationality,
                    emergency_contact=temp_registration.emergency_contact,
                    emergency_contact_phone=temp_registration.emergency_contact_phone,
                    shirt_size=temp_registration.shirt_size,
                    dietary_restrictions=temp_registration.dietary_restrictions,
                    medical_conditions=temp_registration.medical_conditions,
                    know_us=temp_registration.know_us,
                    observations=temp_registration.observations,
                    room_preference=temp_registration.room_preference,
                    roommate_preference=temp_registration.roommate_preference,
                    previous_traveler=temp_registration.previous_traveler,
                    preferred_name=temp_registration.preferred_name,
                    middle_name=temp_registration.middle_name,
                    suffix=temp_registration.suffix,
                    title=temp_registration.title,
                    address2=temp_registration.address2,
                    mobile_phone=temp_registration.mobile_phone,
                    work_phone=temp_registration.work_phone,
                    business_email=temp_registration.business_email,
                    personal_email=temp_registration.personal_email,
                    social_security=temp_registration.social_security,
                    employer=temp_registration.employer,
                    business_address=temp_registration.business_address,
                    business_city=temp_registration.business_city,
                    business_state=temp_registration.business_state,
                    business_zip=temp_registration.business_zip,
                    business_country=temp_registration.business_country,
                    special_assistance=temp_registration.special_assistance
                )
                
                # Store transaction ID for reference
                temp_registration.authorize_net_transaction_id = payment_result['transaction_id']
                temp_registration.payment_response = json.dumps(payment_result)
                temp_registration.save()
                
                # Send confirmation emails
                try:
                    # Prepare email data
                    registration_data = {
                        'id': pilgrimage_client.id,
                        'pilgrimage_id': temp_registration.pilgrimage_id,
                        'trip_title': getattr(temp_registration.pilgrimage, 'title', 'Holy Land Pilgrimage'),
                        'trip_price': float(temp_registration.totalcost - temp_registration.discount),
                        'customer_notes': temp_registration.observations or '',
                        'payment': {
                            'payment_type': 'cc',
                            'payment_plan': 'full',
                            'total_amount': total_amount,
                            'credit_card_number': request.data.get('card_data', {}).get('card_number', '')
                        }
                    }
                    
                    # Parse passenger data for email
                    passengers_for_email = []
                    passenger_count = len(json.loads(temp_registration.firstname or '[]'))
                    
                    for i in range(passenger_count):
                        passenger_email_data = {}
                        for field_map in [
                            ('title', 'title'), ('first_name', 'firstname'), ('last_name', 'lastname'),
                            ('email', 'email'), ('phone', 'phone'), ('date_of_birth', 'birthday'),
                            ('gender', 'gender'), ('address', 'address'), ('city', 'city'),
                            ('state', 'state'), ('zip', 'zipcode'), ('country_id', 'country'),
                            ('passport_number', 'passport'), ('passport_exp', 'passport_exp'),
                            ('passport_country_id', 'passport_country'),
                            ('emergency_contact_name', 'emergency_contact'),
                            ('emergency_contact_relationship', 'emergency_contact_relationship'),
                            ('emergency_contact_phone', 'emergency_contact_phone'),
                            ('dietary_restrictions', 'dietary_restrictions'),
                            ('medical_conditions', 'medical_conditions'),
                            ('special_requests', 'special_assistance')
                        ]:
                            email_field, db_field = field_map
                            field_data = getattr(temp_registration, db_field)
                            if field_data:
                                try:
                                    field_array = json.loads(field_data)
                                    passenger_email_data[email_field] = field_array[i] if i < len(field_array) else ''
                                except (json.JSONDecodeError, IndexError):
                                    passenger_email_data[email_field] = ''
                            else:
                                passenger_email_data[email_field] = ''
                        
                        passenger_email_data['is_primary'] = (i == 0)  # First passenger is primary
                        passengers_for_email.append(passenger_email_data)
                    
                    # Send customer confirmation email
                    RegistrationEmailService.send_customer_confirmation(registration_data, passengers_for_email)
                    
                    # Send admin notification email
                    RegistrationEmailService.send_admin_notification(registration_data, passengers_for_email)
                    
                except Exception as email_error:
                    logger.error(f"Failed to send confirmation emails: {str(email_error)}")
                    # Don't fail the registration if email fails
                
                # Clean up - delete temp records after successful migration
                temp_registration.delete()
                
            return Response({
                'success': True,
                'message': 'Payment processed successfully! Your registration is confirmed.',
                'transaction_id': payment_result['transaction_id'],
                'confirmation_number': f"CONF-{pilgrimage_client.id}",
                'amount_charged': total_amount,
                'processing_fee': processing_fee
            })
        
        else:
            # Payment failed
            temp_registration.payment_response = json.dumps(payment_result)
            temp_registration.save()
            
            return Response({
                'success': False,
                'error': 'Payment was declined. Please check your card information and try again.',
                'decline_reason': payment_result.get('message', 'Unknown error')
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except PilgrimageClientTmp.DoesNotExist:
        return Response(
            {'error': 'Registration not found or has expired'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Payment processing error: {str(e)}")
        return Response(
            {'error': 'An error occurred while processing your payment. Please try again.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def check_registration_status(request, session_id):
    """Check the status of a registration by session ID"""
    try:
        temp_registration = PilgrimageClientTmp.objects.get(session_id=session_id)
        
        # Check if expired
        if temp_registration.expires_at < timezone.now():
            return Response({
                'status': 'expired',
                'message': 'Registration has expired. Please start over.'
            })
        
        # Check payment status
        if temp_registration.payment_attempted:
            if temp_registration.authorize_net_transaction_id:
                return Response({
                    'status': 'completed',
                    'message': 'Registration completed successfully.',
                    'transaction_id': temp_registration.authorize_net_transaction_id
                })
            else:
                return Response({
                    'status': 'failed',
                    'message': 'Payment failed. Please try again.'
                })
        
        return Response({
            'status': 'pending',
            'message': 'Registration created, payment pending.',
            'expires_at': temp_registration.expires_at.isoformat()
        })
        
    except PilgrimageClientTmp.DoesNotExist:
        return Response({
            'status': 'not_found',
            'message': 'Registration not found.'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def cleanup_expired_registrations(request):
    """Clean up expired temporary registrations (cron job endpoint)"""
    try:
        expired_count = PilgrimageClientTmp.objects.filter(
            expires_at__lt=timezone.now()
        ).count()
        
        PilgrimageClientTmp.objects.filter(
            expires_at__lt=timezone.now()
        ).delete()
        
        return Response({
            'success': True,
            'message': f'Cleaned up {expired_count} expired registrations.'
        })
        
    except Exception as e:
        logger.error(f"Cleanup error: {str(e)}")
        return Response(
            {'error': 'An error occurred during cleanup.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
