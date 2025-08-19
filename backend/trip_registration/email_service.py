from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class RegistrationEmailService:
    """Service for sending registration-related emails"""
    
    @staticmethod
    def send_customer_confirmation(registration_data, passengers):
        """Send confirmation email to customer"""
        try:
            primary_passenger = next((p for p in passengers if p.get('is_primary')), passengers[0])
            
            # Prepare email context
            context = {
                'primary_passenger': primary_passenger,
                'trip_title': registration_data['trip_title'],
                'registration_id': registration_data.get('id', 'TMP' + str(timezone.now().timestamp())),
                'registration_date': timezone.now().strftime('%B %d, %Y at %I:%M %p'),
                'passengers': passengers,
                'trip_price': registration_data['trip_price'],
                'processing_fee': round(registration_data['trip_price'] * 0.03, 2),
                'total_amount': registration_data['payment']['total_amount'],
                'payment_type_display': RegistrationEmailService._get_payment_type_display(
                    registration_data['payment']['payment_type']
                ),
                'payment_plan_display': RegistrationEmailService._get_payment_plan_display(
                    registration_data['payment']['payment_plan']
                ),
                'customer_notes': registration_data.get('customer_notes', ''),
                'frontend_url': getattr(settings, 'FRONTEND_URL', 'http://localhost:3000'),
                'current_year': timezone.now().year
            }
            
            # Render email templates
            html_content = render_to_string('emails/customer_confirmation.html', context)
            text_content = f"""
Registration Confirmation - Nativity Pilgrimage

Dear {primary_passenger['title']} {primary_passenger['last_name']},

Thank you for registering for {registration_data['trip_title']}!

Registration Details:
- Registration ID: #{context['registration_id']}
- Trip: {registration_data['trip_title']}
- Passengers: {len(passengers)}
- Total Amount: ${registration_data['payment']['total_amount']}

We will contact you soon with additional details.

Contact us: info@nativitypilgrimage.com | (555) 123-4567

Blessings,
The Nativity Pilgrimage Team
            """
            
            # Send email
            subject = f"Registration Confirmed: {registration_data['trip_title']}"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [primary_passenger['email']]
            
            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            logger.info(f"Customer confirmation email sent to {primary_passenger['email']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send customer confirmation email: {str(e)}")
            return False
    
    @staticmethod
    def send_admin_notification(registration_data, passengers):
        """Send notification email to admin staff"""
        try:
            primary_passenger = next((p for p in passengers if p.get('is_primary')), passengers[0])
            
            # Prepare email context
            context = {
                'primary_passenger': primary_passenger,
                'trip_title': registration_data['trip_title'],
                'registration_id': registration_data.get('id', 'TMP' + str(timezone.now().timestamp())),
                'registration_date': timezone.now().strftime('%B %d, %Y at %I:%M %p'),
                'pilgrimage_id': registration_data['pilgrimage_id'],
                'passengers': passengers,
                'trip_price': registration_data['trip_price'],
                'processing_fee': round(registration_data['trip_price'] * 0.03, 2),
                'total_amount': registration_data['payment']['total_amount'],
                'payment_type': registration_data['payment']['payment_type'],
                'payment_type_display': RegistrationEmailService._get_payment_type_display(
                    registration_data['payment']['payment_type']
                ),
                'payment_plan_display': RegistrationEmailService._get_payment_plan_display(
                    registration_data['payment']['payment_plan']
                ),
                'customer_notes': registration_data.get('customer_notes', ''),
                'admin_url': getattr(settings, 'ADMIN_URL', 'http://127.0.0.1:8000'),
                'primary_email': primary_passenger['email'],
                'primary_phone': primary_passenger['phone'],
                'credit_card_last4': registration_data['payment'].get('credit_card_number', '')[-4:] 
                    if registration_data['payment'].get('credit_card_number') else ''
            }
            
            # Render email templates
            html_content = render_to_string('emails/admin_notification.html', context)
            text_content = f"""
NEW REGISTRATION ALERT - Nativity Pilgrimage

Trip: {registration_data['trip_title']}
Registration ID: #{context['registration_id']}
Passengers: {len(passengers)}
Total Amount: ${registration_data['payment']['total_amount']}

Primary Contact:
{primary_passenger['title']} {primary_passenger['first_name']} {primary_passenger['last_name']}
Email: {primary_passenger['email']}
Phone: {primary_passenger['phone']}

Payment: {context['payment_type_display']} - {context['payment_plan_display']}

IMMEDIATE ACTIONS REQUIRED:
1. Verify payment processing
2. Update trip capacity
3. Send welcome packet
4. Review documentation

Admin Dashboard: {context['admin_url']}/admin/
            """
            
            # Send to admin emails
            subject = f"🚨 NEW REGISTRATION: {registration_data['trip_title']} - {len(passengers)} passengers"
            from_email = settings.DEFAULT_FROM_EMAIL
            
            # Admin email addresses (configure in settings)
            admin_emails = getattr(settings, 'ADMIN_EMAIL_ADDRESSES', [
                'admin@nativitypilgrimage.com',
                'reservations@nativitypilgrimage.com'
            ])
            
            msg = EmailMultiAlternatives(subject, text_content, from_email, admin_emails)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            logger.info(f"Admin notification email sent to {admin_emails}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send admin notification email: {str(e)}")
            return False
    
    @staticmethod
    def _get_payment_type_display(payment_type):
        """Convert payment type code to display name"""
        payment_types = {
            'cc': 'Credit Card',
            'check': 'Check',
            'bank_transfer': 'Bank Transfer',
            'cash': 'Cash',
            'other': 'Other'
        }
        return payment_types.get(payment_type, payment_type.title())
    
    @staticmethod
    def _get_payment_plan_display(payment_plan):
        """Convert payment plan code to display name"""
        payment_plans = {
            'full': 'Full Payment',
            'deposit': 'Deposit Only',
            'installments': 'Installment Plan',
            'other': 'Other'
        }
        return payment_plans.get(payment_plan, payment_plan.title())
