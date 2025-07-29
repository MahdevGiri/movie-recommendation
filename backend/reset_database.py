#!/usr/bin/env python3
"""
Reset and recreate the database with the new schema.
"""

from database_config import db_config
from database_seeder import seed_database

def reset_database():
    """Reset the database and recreate all tables."""
    print("🔄 RESETTING DATABASE")
    print("=" * 50)
    
    # Drop all tables
    print("1. Dropping existing tables...")
    db_config.drop_tables()
    
    # Create all tables with new schema
    print("\n2. Creating new tables...")
    db_config.create_tables()
    
    # Seed the database
    print("\n3. Seeding database...")
    seed_database()
    
    print("\n✅ Database reset completed successfully!")

if __name__ == "__main__":
    reset_database() 