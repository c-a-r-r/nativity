"""
Quick test script to verify our API endpoints
"""
import requests
import json

def test_registration_endpoints():
    base_url = "http://127.0.0.1:8000/api/registration"
    
    print("🧪 Testing Trip Registration API Endpoints")
    print("=" * 50)
    
    # Test 1: Get countries
    print("\n1️⃣ Testing GET /countries/")
    try:
        response = requests.get(f"{base_url}/countries/")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            countries = response.json()
            print(f"✅ Success: Found {len(countries)} countries")
            print(f"Sample: {countries[:3] if countries else 'No countries'}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    
    # Test 2: Get pilgrimage (we'll use ID 1 as a test)
    print("\n2️⃣ Testing GET /pilgrimage/1/")
    try:
        response = requests.get(f"{base_url}/pilgrimage/1/")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            pilgrimage = response.json()
            print(f"✅ Success: {pilgrimage.get('name', 'Unknown Trip')}")
            print(f"Cost: ${pilgrimage.get('cost', 'N/A')}")
        elif response.status_code == 404:
            print("⚠️  No pilgrimage with ID 1 found - this is expected if no data exists")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    
    # Test 3: Submit registration (basic validation test)
    print("\n3️⃣ Testing POST /submit/ (validation test)")
    try:
        test_data = {
            "pilgrimage_id": 1,
            "ap": "TEST-TRIP",
            "paymentoption": "pay_in_email",
            "totalcost": 2500.00,
            "passengers": [
                {
                    "firstname": "John",
                    "lastname": "Doe",
                    "email": "john.doe@example.com",
                    "phone": "555-123-4567"
                }
            ],
            "lead_firstname": "John",
            "lead_lastname": "Doe",
            "lead_email": "john.doe@example.com"
        }
        
        response = requests.post(
            f"{base_url}/submit/",
            headers={"Content-Type": "application/json"},
            json=test_data
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        
        if response.status_code == 200:
            print("✅ Registration submission successful!")
            print(f"Message: {result.get('message', 'No message')}")
        elif response.status_code == 400:
            print("⚠️  Validation error (expected):")
            print(f"Details: {result.get('details', result.get('error', 'Unknown error'))}")
        else:
            print(f"❌ Unexpected error: {result}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    
    print("\n" + "=" * 50)
    print("✨ API Test Complete!")
    print("\n💡 Next Steps:")
    print("   1. Add sample data to your database")
    print("   2. Test the registration form in the browser")
    print("   3. Verify customer authentication works")

if __name__ == "__main__":
    test_registration_endpoints()
