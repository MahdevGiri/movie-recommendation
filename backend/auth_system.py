import hashlib
import getpass
from typing import Optional, Dict, Any
from database_service import DatabaseService
from models import User

class AuthSystem:
    """
    Authentication system for the movie recommendation application.
    
    This class handles:
    - User registration with password hashing
    - User login with password verification
    - Session management
    - User data persistence using PostgreSQL database
    """
    
    def __init__(self):
        """Initialize the authentication system."""
        self.db_service = DatabaseService()
        self.current_user: Optional[User] = None
    
    def _hash_password(self, password: str) -> str:
        """
        Hash a password using SHA-256.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username: str, password: str, name: str, age: int, preferred_genre: str, email: Optional[str] = None) -> bool:
        """
        Register a new user.
        
        Args:
            username: Unique username
            password: Plain text password
            name: User's full name
            age: User's age
            preferred_genre: User's preferred movie genre
            email: User's email (optional)
            
        Returns:
            True if registration successful, False otherwise
        """
        if len(password) < 6:
            print("❌ Password must be at least 6 characters long!")
            return False
        
        if age < 13 or age > 120:
            print("❌ Invalid age! Must be between 13 and 120.")
            return False
        
        # Create user in database
        user = self.db_service.create_user(
            username=username,
            password=password,
            name=name,
            email=email,
            age=age,
            preferred_genre=preferred_genre,
            role="user"
        )
        
        if user:
            print("✅ Registration successful!")
            return True
        else:
            print("❌ Username already exists!")
            return False
    
    def login(self, username: str, password: str) -> bool:
        """
        Authenticate a user login.
        
        Args:
            username: Username to authenticate
            password: Plain text password
            
        Returns:
            True if login successful, False otherwise
        """
        user = self.db_service.authenticate_user(username, password)
        if user:
            self.current_user = user
            print(f"✅ Welcome back, {user.name}!")
            return True
        else:
            print("❌ Invalid username or password!")
            return False
    
    def logout(self) -> None:
        """Log out the current user."""
        if self.current_user:
            print(f"👋 Goodbye, {self.current_user.name}!")
            self.current_user = None
        else:
            print("No user is currently logged in.")
    
    def is_logged_in(self) -> bool:
        """
        Check if a user is currently logged in.
        
        Returns:
            True if user is logged in, False otherwise
        """
        return self.current_user is not None
    
    def get_current_user(self) -> Optional[User]:
        """
        Get the current logged-in user's information.
        
        Returns:
            User object if logged in, None otherwise
        """
        return self.current_user
    
    def get_user_id(self) -> Optional[int]:
        """
        Get the current user's ID for the recommendation system.
        
        Returns:
            User ID if logged in, None otherwise
        """
        if not self.current_user:
            return None
        
        return self.current_user.id
    
    def change_password(self, current_password: str, new_password: str) -> bool:
        """
        Change the current user's password.
        
        Args:
            current_password: Current password for verification
            new_password: New password to set
            
        Returns:
            True if password change successful, False otherwise
        """
        if not self.is_logged_in():
            print("❌ No user is currently logged in!")
            return False
        
        if len(new_password) < 6:
            print("❌ New password must be at least 6 characters long!")
            return False
        
        # Verify current password
        if not self.db_service.authenticate_user(self.current_user.username, current_password):
            print("❌ Current password is incorrect!")
            return False
        
        # Update password in database
        success = self.db_service.update_user(
            self.current_user.id, 
            password_hash=self._hash_password(new_password)
        )
        
        if success:
            print("✅ Password changed successfully!")
            return True
        else:
            print("❌ Failed to update password!")
            return False
    
    def display_user_info(self) -> None:
        """Display current user's information."""
        if not self.is_logged_in():
            print("❌ No user is currently logged in!")
            return
        
        user = self.current_user
        print(f"\n👤 USER INFORMATION:")
        print(f"Username: {user.username}")
        print(f"Name: {user.name}")
        print(f"Age: {user.age}")
        print(f"Preferred Genre: {user.preferred_genre}")
        print(f"Role: {user.role}")
        if user.email:
            print(f"Email: {user.email}")
    
    def list_users(self) -> None:
        """List all registered users (admin only)."""
        if not self.is_logged_in():
            print("❌ Access denied! Admin privileges required.")
            return
        
        if self.current_user.role != "admin":
            print("❌ Access denied! Admin privileges required.")
            return
        
        users = self.db_service.get_all_users()
        print(f"\n👥 REGISTERED USERS:")
        print("-" * 50)
        for user in users:
            print(f"Username: {user.username}")
            print(f"Name: {user.name}")
            print(f"Age: {user.age}")
            print(f"Preferred Genre: {user.preferred_genre}")
            print(f"Role: {user.role}")
            if user.email:
                print(f"Email: {user.email}")
            print("-" * 30) 