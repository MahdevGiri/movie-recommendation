#!/usr/bin/env python3
"""
Login Demo Script

This script demonstrates the authentication system functionality
for the movie recommendation system.
"""

from auth_system import AuthSystem
import getpass

def demo_login_system():
    """Demonstrate the login system functionality."""
    print("🔐 MOVIE RECOMMENDATION SYSTEM - LOGIN DEMO")
    print("=" * 50)
    
    # Initialize authentication system
    auth = AuthSystem()
    
    while True:
        print("\n📋 DEMO MENU:")
        print("1. Login")
        print("2. Register new user")
        print("3. View current user info")
        print("4. Change password")
        print("5. Logout")
        print("6. List all users (admin only)")
        print("7. Exit demo")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            print("\n🔐 LOGIN")
            username = input("Username: ").strip()
            password = getpass.getpass("Password: ")
            auth.login(username, password)
            
        elif choice == "2":
            print("\n📝 REGISTRATION")
            username = input("Username: ").strip()
            password = getpass.getpass("Password: ")
            confirm_password = getpass.getpass("Confirm Password: ")
            
            if password != confirm_password:
                print("❌ Passwords do not match!")
                continue
                
            name = input("Full Name: ").strip()
            try:
                age = int(input("Age: "))
            except ValueError:
                print("❌ Age must be a number!")
                continue
                
            preferred_genre = input("Preferred Genre: ").strip()
            auth.register_user(username, password, name, age, preferred_genre)
            
        elif choice == "3":
            auth.display_user_info()
            
        elif choice == "4":
            if not auth.is_logged_in():
                print("❌ Please login first!")
                continue
                
            current_password = getpass.getpass("Current Password: ")
            new_password = getpass.getpass("New Password: ")
            confirm_password = getpass.getpass("Confirm New Password: ")
            
            if new_password != confirm_password:
                print("❌ Passwords do not match!")
                continue
                
            auth.change_password(current_password, new_password)
            
        elif choice == "5":
            auth.logout()
            
        elif choice == "6":
            auth.list_users()
            
        elif choice == "7":
            print("👋 Demo completed!")
            break
            
        else:
            print("❌ Invalid choice! Please enter 1-7.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    demo_login_system() 