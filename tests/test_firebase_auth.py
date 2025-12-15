"""
Example usage of Firebase Authentication endpoints

This script demonstrates how to use the Firebase authentication endpoints
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def test_verify_token(firebase_token: str):
    """Test the /users/verify endpoint"""
    print("\n=== Testing /users/verify endpoint ===")
    
    url = f"{BASE_URL}/users/verify"
    headers = {"Content-Type": "application/json"}
    data = {"firebase_token": firebase_token}
    
    response = requests.post(url, headers=headers, json=data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.json()


def test_get_current_user(firebase_token: str):
    """Test the /users/me endpoint"""
    print("\n=== Testing /users/me endpoint ===")
    
    url = f"{BASE_URL}/users/me"
    headers = {"Authorization": f"Bearer {firebase_token}"}
    
    response = requests.get(url, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.json()


def test_protected_route_without_token():
    """Test accessing a protected route without a token"""
    print("\n=== Testing protected route without token ===")
    
    url = f"{BASE_URL}/users/me"
    
    response = requests.get(url)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_public_routes():
    """Test public routes that don't require authentication"""
    print("\n=== Testing public routes ===")
    
    # Test health endpoint
    response = requests.get("http://localhost:8000/health")
    print(f"Health endpoint - Status: {response.status_code}")
    
    # Test root endpoint
    response = requests.get("http://localhost:8000/")
    print(f"Root endpoint - Status: {response.status_code}")


if __name__ == "__main__":
    print("Firebase Authentication API Test")
    print("=" * 50)
    
    # Test public routes first
    test_public_routes()
    
    # Test protected route without token (should fail)
    test_protected_route_without_token()
    
    # To test authenticated endpoints, you need a real Firebase token
    # Get this from your client app after user signs in
    firebase_token = input("\nEnter your Firebase ID token (or press Enter to skip): ").strip()
    
    if firebase_token:
        # Test verify endpoint
        verify_result = test_verify_token(firebase_token)
        
        # Test get current user endpoint
        test_get_current_user(firebase_token)
    else:
        print("\nSkipping authenticated tests (no token provided)")
        print("\nTo get a Firebase token:")
        print("1. Use the Firebase Auth SDK in your client app")
        print("2. Sign in a user")
        print("3. Call user.getIdToken() to get the token")
    
    print("\n" + "=" * 50)
    print("Tests completed!")
