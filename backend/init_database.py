#!/usr/bin/env python3
"""
Initialize PostgreSQL Database for Movie Recommendation System
"""

import os
from create_env import create_env_file
from database_config import db_config
from database_seeder import seed_database

def main():
    """Initialize the database."""
    print("🚀 INITIALIZING POSTGRESQL DATABASE")
    print("=" * 50)
    
    # Step 1: Create .env file
    print("1. Creating .env file...")
    create_env_file()
    
    # Step 2: Test database connection
    print("\n2. Testing database connection...")
    if not db_config.test_connection():
        print("❌ Database connection failed!")
        print("Please make sure:")
        print("- PostgreSQL is running")
        print("- Database 'movie_recommendation' exists")
        print("- Username: postgres, Password: postgres")
        return False
    
    print("✅ Database connection successful!")
    
    # Step 3: Create tables
    print("\n3. Creating database tables...")
    db_config.create_tables()
    
    # Step 4: Seed data
    print("\n4. Seeding database with sample data...")
    if not seed_database():
        print("❌ Failed to seed database!")
        return False
    
    print("\n🎉 DATABASE INITIALIZATION COMPLETED!")
    print("=" * 50)
    print("You can now run the movie recommendation system:")
    print("   python api_server.py")
    print("\nDefault login credentials:")
    print("   Username: admin, Password: admin123")
    print("   Username: alice, Password: alice123")
    print("   Username: bob, Password: bob123")
    print("   Username: charlie, Password: charlie123")
    
    return True

if __name__ == "__main__":
    main() 