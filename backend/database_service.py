from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from typing import List, Optional, Dict, Any
import hashlib
import uuid
from datetime import datetime, timedelta

from database_config import db_config
from models import User, Movie, Rating, Genre, UserSession

class DatabaseService:
    """
    Service layer for database operations.
    
    This class handles all database interactions including:
    - User management (CRUD operations)
    - Movie management
    - Rating operations
    - Session management
    """
    
    def __init__(self):
        """Initialize the database service."""
        self.db_config = db_config
    
    def get_session(self) -> Session:
        """Get a database session."""
        return self.db_config.get_session()
    
    # User Operations
    def create_user(self, username: str, password: str, name: str, 
                   email: Optional[str] = None, age: Optional[int] = None, 
                   preferred_genre: Optional[str] = None, role: str = "user") -> Optional[User]:
        """
        Create a new user.
        
        Args:
            username: Unique username
            password: Plain text password
            name: User's full name
            email: User's email (optional)
            age: User's age (optional)
            preferred_genre: User's preferred genre (optional)
            role: User role (default: "user")
            
        Returns:
            User object if successful, None otherwise
        """
        session = self.get_session()
        try:
            # Check if username already exists
            existing_user = session.query(User).filter(User.username == username).first()
            if existing_user:
                return None
            
            # Hash password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Create user
            user = User(
                username=username,
                password_hash=password_hash,
                name=name,
                email=email,
                age=age,
                preferred_genre=preferred_genre,
                role=role
            )
            
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
            
        except Exception as e:
            session.rollback()
            print(f"Error creating user: {e}")
            return None
        finally:
            session.close()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        session = self.get_session()
        try:
            return session.query(User).filter(User.username == username).first()
        finally:
            session.close()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        session = self.get_session()
        try:
            return session.query(User).filter(User.id == user_id).first()
        finally:
            session.close()
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate user with username and password.
        
        Returns:
            User object if authentication successful, None otherwise
        """
        user = self.get_user_by_username(username)
        if user and user.password_hash == hashlib.sha256(password.encode()).hexdigest():
            return user
        return None
    
    def update_user(self, user_id: int, **kwargs) -> bool:
        """Update user information."""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            print(f"Error updating user: {e}")
            return False
        finally:
            session.close()
    
    def get_all_users(self) -> List[User]:
        """Get all users."""
        session = self.get_session()
        try:
            return session.query(User).all()
        finally:
            session.close()
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user and all their ratings."""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            
            # Delete all ratings by this user first (cascade)
            session.query(Rating).filter(Rating.user_id == user_id).delete()
            
            # Delete the user
            session.delete(user)
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            print(f"Error deleting user: {e}")
            return False
        finally:
            session.close()
    
    # Movie Operations
    def create_movie(self, title: str, genre: str, year: int, 
                    rating: Optional[float] = None, description: Optional[str] = None,
                    director: Optional[str] = None, cast: Optional[str] = None,
                    poster_url: Optional[str] = None, trailer_url: Optional[str] = None) -> Optional[Movie]:
        """Create a new movie."""
        session = self.get_session()
        try:
            movie = Movie(
                title=title,
                genre=genre,
                year=year,
                rating=rating,
                description=description,
                director=director,
                cast=cast,
                poster_url=poster_url,
                trailer_url=trailer_url
            )
            
            session.add(movie)
            session.commit()
            session.refresh(movie)
            return movie
            
        except Exception as e:
            session.rollback()
            print(f"Error creating movie: {e}")
            return None
        finally:
            session.close()
    
    def get_movie_by_id(self, movie_id: int) -> Optional[Movie]:
        """Get movie by ID."""
        session = self.get_session()
        try:
            return session.query(Movie).filter(Movie.id == movie_id).first()
        finally:
            session.close()
    
    def get_all_movies(self) -> List[Movie]:
        """Get all movies."""
        session = self.get_session()
        try:
            return session.query(Movie).all()
        finally:
            session.close()
    
    def get_movies_by_genre(self, genre: str, limit: int = 20) -> List[Movie]:
        """Get movies by genre."""
        session = self.get_session()
        try:
            return session.query(Movie).filter(Movie.genre == genre).limit(limit).all()
        finally:
            session.close()
    
    def get_popular_movies(self, limit: int = 20) -> List[Movie]:
        """Get popular movies based on average rating."""
        session = self.get_session()
        try:
            return session.query(Movie).order_by(desc(Movie.rating)).limit(limit).all()
        finally:
            session.close()
    
    def get_movies(self, page: int = 1, per_page: int = 20, genre: Optional[str] = None, 
                  search: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get movies with pagination and filtering."""
        session = self.get_session()
        try:
            query = session.query(Movie)
            
            if genre:
                query = query.filter(Movie.genre == genre)
            
            if search:
                query = query.filter(Movie.title.ilike(f'%{search}%'))
            
            # Debug: Check total count before pagination
            total_count = query.count()
            print(f"🔧 get_movies - Total movies in DB: {total_count}")
            print(f"🔧 get_movies - Parameters: page={page}, per_page={per_page}, genre={genre}, search={search}")
            
            # Apply pagination
            offset = (page - 1) * per_page
            movies = query.offset(offset).limit(per_page).all()
            
            print(f"🔧 get_movies - Returning {len(movies)} movies (offset={offset}, limit={per_page})")
            
            # Debug: Check for Inception specifically
            all_movies = session.query(Movie).all()
            inception_movies = [m for m in all_movies if 'inception' in m.title.lower()]
            if inception_movies:
                print(f"🔧 get_movies - Inception movies in DB: {[m.title for m in inception_movies]}")
            else:
                print("🔧 get_movies - No Inception movies found in DB")
            
            # Convert to dictionaries
            result = []
            for movie in movies:
                result.append({
                    'id': movie.id,
                    'title': movie.title,
                    'genre': movie.genre,
                    'year': movie.year,
                    'rating': movie.rating,
                    'description': movie.description,
                    'director': movie.director,
                    'cast': movie.cast,
                    'poster_url': movie.poster_url,
                    'trailer_url': movie.trailer_url
                })
            
            return result
        finally:
            session.close()
    
    def get_all_genres(self) -> List[str]:
        """Get all available genres."""
        session = self.get_session()
        try:
            genres = session.query(Movie.genre).distinct().all()
            return [genre[0] for genre in genres]
        finally:
            session.close()
    
    def add_rating(self, user_id: int, movie_id: int, rating: float, review: str = '') -> bool:
        """Add or update a rating."""
        session = self.get_session()
        try:
            # Check if rating already exists
            existing_rating = session.query(Rating).filter(
                and_(Rating.user_id == user_id, Rating.movie_id == movie_id)
            ).first()
            
            if existing_rating:
                # Update existing rating
                existing_rating.rating = rating
                existing_rating.review = review
                existing_rating.updated_at = datetime.now()
            else:
                # Create new rating
                new_rating = Rating(
                    user_id=user_id,
                    movie_id=movie_id,
                    rating=rating,
                    review=review
                )
                session.add(new_rating)
            
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            print(f"Error adding rating: {e}")
            return False
        finally:
            session.close()
    
    def update_rating(self, user_id: int, movie_id: int, rating: float, review: str = '') -> bool:
        """Update an existing rating."""
        session = self.get_session()
        try:
            existing_rating = session.query(Rating).filter(
                and_(Rating.user_id == user_id, Rating.movie_id == movie_id)
            ).first()
            
            if existing_rating:
                existing_rating.rating = rating
                existing_rating.review = review
                existing_rating.updated_at = datetime.now()
                session.commit()
                return True
            else:
                return False
                
        except Exception as e:
            session.rollback()
            print(f"Error updating rating: {e}")
            return False
        finally:
            session.close()
    
    def delete_rating(self, user_id: int, movie_id: int) -> bool:
        """Delete a rating."""
        session = self.get_session()
        try:
            rating = session.query(Rating).filter(
                and_(Rating.user_id == user_id, Rating.movie_id == movie_id)
            ).first()
            
            if rating:
                session.delete(rating)
                session.commit()
                return True
            else:
                return False
                
        except Exception as e:
            session.rollback()
            print(f"Error deleting rating: {e}")
            return False
        finally:
            session.close()
    
    def search_movies(self, query: str, limit: int = 20) -> List[Movie]:
        """Search movies by title."""
        session = self.get_session()
        try:
            return session.query(Movie).filter(
                Movie.title.ilike(f"%{query}%")
            ).limit(limit).all()
        finally:
            session.close()
    
    def update_movie(self, movie_id: int, **kwargs) -> bool:
        """Update movie information."""
        session = self.get_session()
        try:
            movie = session.query(Movie).filter(Movie.id == movie_id).first()
            if not movie:
                return False
            
            for key, value in kwargs.items():
                if hasattr(movie, key):
                    setattr(movie, key, value)
            
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            print(f"Error updating movie: {e}")
            return False
        finally:
            session.close()
    
    # Rating Operations
    def create_rating(self, user_id: int, movie_id: int, rating: float, 
                     review: Optional[str] = None) -> Optional[Rating]:
        """Create a new rating."""
        session = self.get_session()
        try:
            # Check if rating already exists
            existing_rating = session.query(Rating).filter(
                and_(Rating.user_id == user_id, Rating.movie_id == movie_id)
            ).first()
            
            if existing_rating:
                # Update existing rating
                existing_rating.rating = rating
                existing_rating.review = review
                session.commit()
                return existing_rating
            
            # Create new rating
            new_rating = Rating(
                user_id=user_id,
                movie_id=movie_id,
                rating=rating,
                review=review
            )
            
            session.add(new_rating)
            session.commit()
            session.refresh(new_rating)
            return new_rating
            
        except Exception as e:
            session.rollback()
            print(f"Error creating rating: {e}")
            return None
        finally:
            session.close()
    
    def get_user_ratings(self, user_id: int) -> List[Rating]:
        """Get all ratings for a user."""
        session = self.get_session()
        try:
            return session.query(Rating).filter(Rating.user_id == user_id).all()
        finally:
            session.close()
    
    def get_movie_ratings(self, movie_id: int) -> List[Rating]:
        """Get all ratings for a movie."""
        session = self.get_session()
        try:
            return session.query(Rating).filter(Rating.movie_id == movie_id).all()
        finally:
            session.close()
    
    def get_average_rating(self, movie_id: int) -> Optional[float]:
        """Get average rating for a movie."""
        session = self.get_session()
        try:
            result = session.query(func.avg(Rating.rating)).filter(
                Rating.movie_id == movie_id
            ).scalar()
            return float(result) if result else None
        finally:
            session.close()
    
    def get_rating_count(self, movie_id: int) -> int:
        """Get number of ratings for a movie."""
        session = self.get_session()
        try:
            return session.query(Rating).filter(Rating.movie_id == movie_id).count()
        finally:
            session.close()
    
    def get_rating_by_user_and_movie(self, user_id: int, movie_id: int) -> Optional[Rating]:
        """Get a specific rating by user and movie."""
        session = self.get_session()
        try:
            return session.query(Rating).filter(
                and_(Rating.user_id == user_id, Rating.movie_id == movie_id)
            ).first()
        finally:
            session.close()
    
    # Session Operations
    def create_session(self, user_id: int, expires_in_hours: int = 24) -> Optional[str]:
        """Create a new user session."""
        session = self.get_session()
        try:
            session_token = str(uuid.uuid4())
            expires_at = datetime.utcnow() + timedelta(hours=expires_in_hours)
            
            user_session = UserSession(
                user_id=user_id,
                session_token=session_token,
                expires_at=expires_at
            )
            
            session.add(user_session)
            session.commit()
            return session_token
            
        except Exception as e:
            session.rollback()
            print(f"Error creating session: {e}")
            return None
        finally:
            session.close()
    
    def get_session_user(self, session_token: str) -> Optional[User]:
        """Get user from session token."""
        session = self.get_session()
        try:
            user_session = session.query(UserSession).filter(
                and_(
                    UserSession.session_token == session_token,
                    UserSession.expires_at > datetime.utcnow()
                )
            ).first()
            
            if user_session:
                return self.get_user_by_id(user_session.user_id)
            return None
            
        finally:
            session.close()
    
    def delete_session(self, session_token: str) -> bool:
        """Delete a user session."""
        session = self.get_session()
        try:
            user_session = session.query(UserSession).filter(
                UserSession.session_token == session_token
            ).first()
            
            if user_session:
                session.delete(user_session)
                session.commit()
                return True
            return False
            
        except Exception as e:
            session.rollback()
            print(f"Error deleting session: {e}")
            return False
        finally:
            session.close()
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions and return count of deleted sessions."""
        session = self.get_session()
        try:
            expired_sessions = session.query(UserSession).filter(
                UserSession.expires_at <= datetime.utcnow()
            ).all()
            
            count = len(expired_sessions)
            for expired_session in expired_sessions:
                session.delete(expired_session)
            
            session.commit()
            return count
            
        except Exception as e:
            session.rollback()
            print(f"Error cleaning up sessions: {e}")
            return 0
        finally:
            session.close() 