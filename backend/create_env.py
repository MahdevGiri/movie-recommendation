#!/usr/bin/env python3
"""
Create .env file with database configuration
"""

import os
import platform

def create_env_file():
    """
    Create a .env file with default PostgreSQL database configuration.
    """
    # Detect operating system
    system = platform.system()
    
    if system == "Darwin":  # macOS
        env_content = """# PostgreSQL Database Configuration (macOS)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=movie_recommendation
DB_USER=postgres
DB_PASSWORD=

# Optional: Set to True for SQL query logging
DB_ECHO=False
"""
        print("📝 macOS detected - using empty password (trust authentication)")
    else:
        env_content = """# PostgreSQL Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=movie_recommendation
DB_USER=postgres
DB_PASSWORD=postgres

# Optional: Set to True for SQL query logging
DB_ECHO=False
"""
        print("📝 Windows/Linux detected - using password authentication")
    
    # Check if .env file already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists. Skipping creation.")
        return True
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully")
        print("📝 Default database configuration:")
        print("   Host: localhost")
        print("   Port: 5432")
        print("   Database: movie_recommendation")
        print("   Username: postgres")
        if system == "Darwin":
            print("   Password: (empty - trust authentication)")
        else:
            print("   Password: postgres")
        print("\n💡 You can edit the .env file to change these settings.")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

if __name__ == "__main__":
    create_env_file() 