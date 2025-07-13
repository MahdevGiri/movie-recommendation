#!/usr/bin/env python3
"""
Test script for the login system
"""

from auth_system import AuthSystem

def test_login_system():
    """Test the basic login functionality."""
    print("🧪 TESTING LOGIN SYSTEM")
    print("=" * 40)
    
    # Initialize auth system
    auth = AuthSystem()
    
    # Test 1: Login with default admin account
    print("\n1. Testing admin login...")
    success = auth.login("admin", "admin123")
    if success:
        print("✅ Admin login successful")
        auth.display_user_info()
    else:
        print("❌ Admin login failed")
    
    # Test 2: Login with alice account
    print("\n2. Testing alice login...")
    auth.logout()  # Clear previous session
    success = auth.login("alice", "alice123")
    if success:
        print("✅ Alice login successful")
        user_id = auth.get_user_id()
        print(f"User ID for recommendations: {user_id}")
    else:
        print("❌ Alice login failed")
    
    # Test 3: Test invalid login
    print("\n3. Testing invalid login...")
    auth.logout()
    success = auth.login("invalid", "password")
    if not success:
        print("✅ Invalid login correctly rejected")
    else:
        print("❌ Invalid login should have been rejected")
    
    # Test 4: Test password change
    print("\n4. Testing password change...")
    auth.login("bob", "bob123")
    if auth.is_logged_in():
        print("✅ Bob logged in successfully")
        # Change password temporarily for testing
        success = auth.change_password("bob123", "newpassword123")
        if success:
            print("✅ Password changed successfully")
            # Change it back
            auth.change_password("newpassword123", "bob123")
            print("✅ Password changed back to original")
        else:
            print("❌ Password change failed")
    else:
        print("❌ Bob login failed")
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    test_login_system() 