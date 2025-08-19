import requests
import json
from datetime import datetime

# Test the registration endpoints
base_url = "http://127.0.0.1:8000/api/registration"

def test_get_countries():
    print("Testing GET countries endpoint...")
    response = requests.get(f"{base_url}/countries/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Countries: {response.json()}")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

def test_get_pilgrimage():
    print("Testing GET pilgrimage endpoint...")
    response = requests.get(f"{base_url}/pilgrimage/1/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Pilgrimage: {response.json()}")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

def test_submit_registration():
    print("Testing POST registration endpoint...")
    
    registration_data = {
        "pilgrimage_id": 1,
        "trip_title": "Holy Land Pilgrimage 2024",
        "trip_price": 3299.00,
        "customer_notes": "Looking forward to this spiritual journey",
        "passengers": [
            {
                "title": "Mr.",
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1980-05-15",
                "gender": "M",
                "phone": "555-123-4567",
                "email": "john.doe@example.com",
                "address": "123 Main St",
                "city": "Anytown",
                "state": "CA",
                "zip": "12345",
                "country_id": 1,
                "passport_number": "123456789",
                "passport_exp": "2025-05-15",
                "passport_country_id": 1,
                "emergency_contact_name": "Jane Doe",
                "emergency_contact_relationship": "Wife",
                "emergency_contact_phone": "555-987-6543",
                "dietary_restrictions": "",
                "medical_conditions": "",
                "special_requests": "",
                "is_primary": True
            }
        ],
        "payment": {
            "payment_type": "cc",
            "payment_plan": "full",
            "total_amount": 3399.97,  # Including 3% processing fee
            "credit_card_number": "4111111111111111",
            "exp_month": "12",
            "exp_year": "2025",
            "cvv": "123",
            "cardholder_name": "John Doe"
        }
    }
    
    response = requests.post(
        f"{base_url}/submit/",
        data=json.dumps(registration_data),
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code in [200, 201]:
        print(f"Success: {response.json()}")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

if __name__ == "__main__":
    try:
        test_get_countries()
        test_get_pilgrimage()
        test_submit_registration()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Django server. Make sure it's running on port 8000.")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
