"""
Trip Registration Serializers
Handles serialization of registration form data to match PHP form structure
"""
from rest_framework import serializers
from .models import ClientTmp, PilgrimageClientTmp, Country, Pilgrimage
import json
from datetime import datetime, timedelta
from django.utils import timezone


class CountrySerializer(serializers.ModelSerializer):
    """Serializer for country lookup"""
    class Meta:
        model = Country
        fields = ['id', 'nombre', 'codigo']


class PilgrimageSerializer(serializers.ModelSerializer):
    """Serializer for pilgrimage lookup"""
    class Meta:
        model = Pilgrimage
        fields = ['id', 'name', 'description', 'cost', 'departure_date', 
                 'return_date', 'registration_deadline', 'slug']


class PassengerDataSerializer(serializers.Serializer):
    """Serializer for individual passenger data (PHP array structure)"""
    firstname = serializers.CharField(max_length=100)
    lastname = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=50, required=False, allow_blank=True)
    fax = serializers.CharField(max_length=50, required=False, allow_blank=True)
    country = serializers.CharField(max_length=100, required=False, allow_blank=True)
    state = serializers.CharField(max_length=100, required=False, allow_blank=True)
    city = serializers.CharField(max_length=100, required=False, allow_blank=True)
    address = serializers.CharField(max_length=200, required=False, allow_blank=True)
    zipcode = serializers.CharField(max_length=20, required=False, allow_blank=True)
    birthday = serializers.CharField(max_length=20, required=False, allow_blank=True)
    gender = serializers.CharField(max_length=1, required=False, allow_blank=True)
    occupation = serializers.CharField(max_length=100, required=False, allow_blank=True)
    passport = serializers.CharField(max_length=50, required=False, allow_blank=True)
    passport_exp = serializers.CharField(max_length=20, required=False, allow_blank=True)
    passport_country = serializers.CharField(max_length=100, required=False, allow_blank=True)
    nationality = serializers.CharField(max_length=100, required=False, allow_blank=True)
    emergency_contact = serializers.CharField(max_length=100, required=False, allow_blank=True)
    emergency_contact_phone = serializers.CharField(max_length=50, required=False, allow_blank=True)
    shirt_size = serializers.CharField(max_length=10, required=False, allow_blank=True)
    dietary_restrictions = serializers.CharField(required=False, allow_blank=True)
    medical_conditions = serializers.CharField(required=False, allow_blank=True)
    room_preference = serializers.CharField(max_length=100, required=False, allow_blank=True)
    roommate_preference = serializers.CharField(max_length=100, required=False, allow_blank=True)
    previous_traveler = serializers.CharField(max_length=10, required=False, allow_blank=True)
    preferred_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    middle_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    suffix = serializers.CharField(max_length=20, required=False, allow_blank=True)
    title = serializers.CharField(max_length=10, required=False, allow_blank=True)
    address2 = serializers.CharField(max_length=200, required=False, allow_blank=True)
    mobile_phone = serializers.CharField(max_length=50, required=False, allow_blank=True)
    work_phone = serializers.CharField(max_length=50, required=False, allow_blank=True)
    business_email = serializers.EmailField(required=False, allow_blank=True)
    personal_email = serializers.EmailField(required=False, allow_blank=True)
    social_security = serializers.CharField(max_length=20, required=False, allow_blank=True)
    employer = serializers.CharField(max_length=200, required=False, allow_blank=True)
    business_address = serializers.CharField(max_length=200, required=False, allow_blank=True)
    business_city = serializers.CharField(max_length=100, required=False, allow_blank=True)
    business_state = serializers.CharField(max_length=100, required=False, allow_blank=True)
    business_zip = serializers.CharField(max_length=20, required=False, allow_blank=True)
    business_country = serializers.CharField(max_length=100, required=False, allow_blank=True)
    special_assistance = serializers.CharField(required=False, allow_blank=True)


class TripRegistrationSerializer(serializers.Serializer):
    """
    Main registration form serializer - matches PHP form structure exactly
    """
    # Trip Information
    pilgrimage_id = serializers.IntegerField()
    ap = serializers.CharField(max_length=50)  # Trip public code
    gsv = serializers.CharField(max_length=10, default='142')  # Form submission ID
    
    # Payment Information
    departurecity_id = serializers.IntegerField(required=False, allow_null=True)
    landonly = serializers.CharField(max_length=10, required=False, allow_blank=True)
    totalcost = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)
    coupon = serializers.CharField(max_length=50, required=False, allow_blank=True)
    paymentoption = serializers.CharField(max_length=50)
    
    # Lead passenger information (from first passenger in arrays)
    lead_firstname = serializers.CharField(max_length=100)
    lead_lastname = serializers.CharField(max_length=100)
    lead_email = serializers.EmailField()
    lead_phone = serializers.CharField(max_length=50, required=False, allow_blank=True)
    
    # Emergency contact (usually from first passenger)
    emergency_contact = serializers.CharField(max_length=100, required=False, allow_blank=True)
    emergency_contact_phone = serializers.CharField(max_length=50, required=False, allow_blank=True)
    
    # How they heard about us
    know_us = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    # Passenger data arrays (PHP structure: firstname[], lastname[], etc.)
    passengers = PassengerDataSerializer(many=True)
    
    # Credit card information (for Authorize.Net)
    card_number = serializers.CharField(max_length=20, write_only=True, required=False)
    card_expiry_month = serializers.CharField(max_length=2, write_only=True, required=False)
    card_expiry_year = serializers.CharField(max_length=4, write_only=True, required=False)
    card_cvv = serializers.CharField(max_length=4, write_only=True, required=False)
    billing_firstname = serializers.CharField(max_length=50, write_only=True, required=False)
    billing_lastname = serializers.CharField(max_length=50, write_only=True, required=False)
    billing_address = serializers.CharField(max_length=200, write_only=True, required=False)
    billing_city = serializers.CharField(max_length=100, write_only=True, required=False)
    billing_state = serializers.CharField(max_length=100, write_only=True, required=False)
    billing_zip = serializers.CharField(max_length=20, write_only=True, required=False)
    billing_country = serializers.CharField(max_length=100, write_only=True, required=False)
    
    def validate(self, data):
        """Validate the registration data"""
        # Check if pilgrimage exists
        try:
            pilgrimage = Pilgrimage.objects.get(id=data['pilgrimage_id'])
        except Pilgrimage.DoesNotExist:
            raise serializers.ValidationError("Invalid pilgrimage ID")
        
        # Validate passengers array is not empty
        if not data.get('passengers'):
            raise serializers.ValidationError("At least one passenger is required")
        
        # Validate payment option requires card details (except pay by mail)
        if data.get('paymentoption') != 'pay_in_email':
            required_card_fields = ['card_number', 'card_expiry_month', 'card_expiry_year', 'card_cvv']
            for field in required_card_fields:
                if not data.get(field):
                    raise serializers.ValidationError(f"{field} is required for credit card payments")
        
        return data
    
    def create(self, validated_data):
        """
        Create temporary registration records in client_tmp and pilgrimage_client_tmp
        matching the PHP system's two-phase commit approach
        """
        passengers_data = validated_data.pop('passengers')
        card_data = {
            'card_number': validated_data.pop('card_number', ''),
            'card_expiry_month': validated_data.pop('card_expiry_month', ''),
            'card_expiry_year': validated_data.pop('card_expiry_year', ''),
            'card_cvv': validated_data.pop('card_cvv', ''),
            'billing_firstname': validated_data.pop('billing_firstname', ''),
            'billing_lastname': validated_data.pop('billing_lastname', ''),
            'billing_address': validated_data.pop('billing_address', ''),
            'billing_city': validated_data.pop('billing_city', ''),
            'billing_state': validated_data.pop('billing_state', ''),
            'billing_zip': validated_data.pop('billing_zip', ''),
            'billing_country': validated_data.pop('billing_country', ''),
        }
        
        # Lead passenger extraction
        lead_data = {
            'firstname': validated_data.pop('lead_firstname'),
            'lastname': validated_data.pop('lead_lastname'),
            'email': validated_data.pop('lead_email'),
            'phone': validated_data.pop('lead_phone', ''),
            'emergency_contact': validated_data.pop('emergency_contact', ''),
            'emergency_contact_phone': validated_data.pop('emergency_contact_phone', ''),
        }
        
        # Generate session ID for tracking
        session_id = f"reg_{timezone.now().strftime('%Y%m%d_%H%M%S')}_{validated_data['pilgrimage_id']}"
        expires_at = timezone.now() + timedelta(hours=2)  # 2-hour expiration
        
        # Step 1: Create temporary client record
        # Convert passengers to PHP-style serialized arrays
        passenger_arrays = {}
        for field in ['firstname', 'lastname', 'email', 'phone', 'fax', 'country', 'state', 'city', 
                     'address', 'zipcode', 'birthday', 'gender', 'occupation', 'passport', 
                     'passport_exp', 'passport_country', 'nationality', 'emergency_contact',
                     'emergency_contact_phone', 'shirt_size', 'dietary_restrictions', 
                     'medical_conditions', 'room_preference', 'roommate_preference', 
                     'previous_traveler', 'preferred_name', 'middle_name', 'suffix', 'title',
                     'address2', 'mobile_phone', 'work_phone', 'business_email', 'personal_email',
                     'social_security', 'employer', 'business_address', 'business_city',
                     'business_state', 'business_zip', 'business_country', 'special_assistance']:
            passenger_arrays[field] = json.dumps([p.get(field, '') for p in passengers_data])
        
        # Create pilgrimage_client_tmp record
        pilgrimage_client_tmp = PilgrimageClientTmp.objects.create(
            pilgrimage_id=validated_data['pilgrimage_id'],
            client_id=None,  # Will be set after client_tmp is created
            ap=validated_data['ap'],
            gsv=validated_data['gsv'],
            departurecity_id=validated_data.get('departurecity_id'),
            landonly=validated_data.get('landonly', ''),
            totalcost=validated_data['totalcost'],
            payed=0,  # Will be updated after payment
            discount=validated_data.get('discount', 0),
            coupon=validated_data.get('coupon', ''),
            paymentoption=validated_data['paymentoption'],
            know_us=validated_data.get('know_us', ''),
            session_id=session_id,
            expires_at=expires_at,
            payment_attempted=False,
            **passenger_arrays
        )
        
        return {
            'registration_id': pilgrimage_client_tmp.id,
            'session_id': session_id,
            'expires_at': expires_at,
            'payment_required': validated_data['paymentoption'] != 'pay_in_email',
            'card_data': card_data if validated_data['paymentoption'] != 'pay_in_email' else None,
            'total_amount': validated_data['totalcost'],
            'passengers_count': len(passengers_data)
        }


class PaymentProcessSerializer(serializers.Serializer):
    """Serializer for processing payments via Authorize.Net"""
    registration_id = serializers.IntegerField()
    session_id = serializers.CharField(max_length=100)
    
    def validate(self, data):
        """Validate the payment request"""
        try:
            registration = PilgrimageClientTmp.objects.get(
                id=data['registration_id'],
                session_id=data['session_id'],
                payment_attempted=False
            )
            if registration.expires_at < timezone.now():
                raise serializers.ValidationError("Registration has expired")
        except PilgrimageClientTmp.DoesNotExist:
            raise serializers.ValidationError("Invalid registration or session")
        
        return data
