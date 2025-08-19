#!/usr/bin/env python
"""
Test script for registration email functionality
Run this to test the email sending after registration
"""
import os
import sys
import django

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nativity_crm.settings')
django.setup()

from trip_registration.email_service import RegistrationEmailService

def test_email_functionality():
    """Test the email service with sample data"""
    print("Testing Registration Email Service...")
    
    # Sample registration data
    registration_data = {
        'id': 'TEST123',
        'pilgrimage_id': 1,
        'trip_title': 'Holy Land Pilgrimage 2024',
        'trip_price': 3299.00,
        'customer_notes': 'Looking forward to this spiritual journey',
        'payment': {
            'payment_type': 'cc',
            'payment_plan': 'full',
            'total_amount': 3399.97,
            'credit_card_number': '4111111111111111'
        }
    }
    
    # Sample passenger data
    passengers = [
        {
            'title': 'Mr.',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',  # Change this to a real email for testing
            'phone': '555-123-4567',
            'date_of_birth': '1980-05-15',
            'gender': 'M',
            'address': '123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'zip': '12345',
            'country_id': 1,
            'passport_number': '123456789',
            'passport_exp': '2025-05-15',
            'passport_country_id': 1,
            'emergency_contact_name': 'Jane Doe',
            'emergency_contact_relationship': 'Wife',
            'emergency_contact_phone': '555-987-6543',
            'dietary_restrictions': '',
            'medical_conditions': '',
            'special_requests': '',
            'is_primary': True
        }
    ]
    
    # Test customer confirmation email
    print("\n1. Testing customer confirmation email...")
    customer_result = RegistrationEmailService.send_customer_confirmation(
        registration_data, passengers
    )
    print(f"Customer email result: {customer_result}")
    
    # Test admin notification email
    print("\n2. Testing admin notification email...")
    admin_result = RegistrationEmailService.send_admin_notification(
        registration_data, passengers
    )
    print(f"Admin email result: {admin_result}")
    
    if customer_result and admin_result:
        print("\n✅ All emails sent successfully!")
    else:
        print("\n❌ Some emails failed to send. Check the logs for details.")
    
    print("\nNote: For actual email sending, configure EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in your .env file")

if __name__ == "__main__":
    test_email_functionality()
