#!/usr/bin/env python3
"""
Create Admin User Script

This script creates an admin user in the movie recommendation system.
Run this script to set up an admin account for managing movies.

Usage:
    python create_admin.py
"""

import hashlib
from database_service import DatabaseService
from database_config import db_config

def create_admin_user():
    """Create an admin user in the database."""
    
    # Initialize database service
    db_service = DatabaseService()
    
    # Admin user details
    admin_username = "admin"
    admin_password = "admin123"  # Change this in production
    admin_name = "System Administrator"
    admin_email = "admin@movie-recommendation.com"
    admin_role = "admin"
    
    print("🔧 Creating admin user...")
    
    # Check if admin already exists
    existing_admin = db_service.get_user_by_username(admin_username)
    if existing_admin:
        print(f"⚠️  Admin user '{admin_username}' already exists!")
        print(f"   User ID: {existing_admin.id}")
        print(f"   Role: {existing_admin.role}")
        return False
    
    # Create admin user
    admin_user = db_service.create_user(
        username=admin_username,
        password=admin_password,
        name=admin_name,
        email=admin_email,
        role=admin_role
    )
    
    if admin_user:
        print("✅ Admin user created successfully!")
        print(f"   Username: {admin_username}")
        print(f"   Password: {admin_password}")
        print(f"   Role: {admin_role}")
        print(f"   User ID: {admin_user.id}")
        print()
        print("⚠️  IMPORTANT: Change the admin password in production!")
        return True
    else:
        print("❌ Failed to create admin user!")
        return False

if __name__ == "__main__":
    print("🎬 Movie Recommendation System - Admin User Creation")
    print("=" * 50)
    
    try:
        success = create_admin_user()
        if success:
            print("🎉 Admin user setup complete!")
        else:
            print("💥 Admin user setup failed!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Make sure the database is initialized and running.") 