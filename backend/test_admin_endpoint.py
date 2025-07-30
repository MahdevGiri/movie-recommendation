#!/usr/bin/env python3
"""
Test Admin Endpoint Script

This script tests the admin endpoint to verify it's working correctly.
"""

import requests
import json

def test_admin_endpoint():
    """Test the admin endpoint"""
    
    base_url = "http://localhost:5000/api"
    
    print("🧪 Testing Admin Endpoint")
    print("=" * 40)
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 2: Try to access admin endpoint without auth
    print("2. Testing admin endpoint without authentication...")
    try:
        response = requests.get(f"{base_url}/admin/movies")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 3: Login as admin
    print("3. Testing admin login...")
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            login_response = response.json()
            token = login_response.get('token')
            user = login_response.get('user')
            print(f"   Login successful!")
            print(f"   User: {user.get('username')}")
            print(f"   Role: {user.get('role')}")
            print(f"   Token: {token[:20]}..." if token else "No token")
            
            # Test 4: Access admin endpoint with auth
            print()
            print("4. Testing admin endpoint with authentication...")
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{base_url}/admin/movies", headers=headers)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                admin_response = response.json()
                movies = admin_response.get('movies', [])
                pagination = admin_response.get('pagination', {})
                print(f"   Movies found: {len(movies)}")
                print(f"   Total movies: {pagination.get('total', 0)}")
                print(f"   Page: {pagination.get('page', 1)}")
                
                if movies:
                    print("   First movie:")
                    first_movie = movies[0]
                    print(f"     Title: {first_movie.get('title')}")
                    print(f"     Year: {first_movie.get('year')}")
                    print(f"     Genre: {first_movie.get('genre')}")
            else:
                print(f"   Error: {response.json()}")
        else:
            print(f"   Login failed: {response.json()}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    print("✅ Test completed!")

if __name__ == "__main__":
    test_admin_endpoint() 