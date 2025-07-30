#!/usr/bin/env python3
"""
Simple Admin Test - No external dependencies
"""

import sys
import os
sys.path.append('backend')

def test_admin_user():
    """Test if admin user exists and can be authenticated"""
    try:
        from backend.database_service import DatabaseService
        from backend.auth_system import AuthSystem
        
        print("🧪 Testing Admin User Setup")
        print("=" * 40)
        
        # Test 1: Check if admin user exists
        db = DatabaseService()
        admin = db.get_user_by_username('admin')
        
        if admin:
            print("✅ Admin user exists!")
            print(f"   Username: {admin.username}")
            print(f"   Role: {admin.role}")
            print(f"   User ID: {admin.id}")
        else:
            print("❌ Admin user not found!")
            return False
        
        # Test 2: Test admin authentication
        auth = AuthSystem()
        login_success = auth.login('admin', 'admin123')
        
        if login_success:
            print("✅ Admin authentication successful!")
            user = auth.get_current_user()
            print(f"   Logged in as: {user.username}")
            print(f"   Role: {user.role}")
        else:
            print("❌ Admin authentication failed!")
            return False
        
        # Test 3: Check if movies exist
        movies = db.get_all_movies()
        print(f"✅ Found {len(movies)} movies in database")
        
        if movies:
            print("   Sample movies:")
            for i, movie in enumerate(movies[:3]):
                print(f"     {i+1}. {movie.title} ({movie.year}) - {movie.genre}")
        
        print()
        print("🎉 All tests passed! Admin functionality should work.")
        print()
        print("📋 Next steps:")
        print("   1. Make sure backend server is running: python backend/api_server.py")
        print("   2. Make sure frontend is running: cd frontend && npm start")
        print("   3. Login with admin/admin123 in the frontend")
        print("   4. Navigate to /admin page")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_admin_user() 