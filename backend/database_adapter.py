import pandas as pd
from typing import List, Optional
from database_service import DatabaseService
from models import User, Movie, Rating

class DatabaseAdapter:
    """
    Adapter class to convert PostgreSQL data to pandas DataFrames
    for compatibility with the existing recommendation system.
    """
    
    def __init__(self):
        """Initialize the database adapter."""
        self.db_service = DatabaseService()
    
    def get_movies_df(self) -> pd.DataFrame:
        """
        Get movies as a pandas DataFrame.
        
        Returns:
            DataFrame with columns: movie_id, title, genre, year, rating, description, poster_url, trailer_url
        """
        movies = self.db_service.get_all_movies()
        
        data = []
        for movie in movies:
            data.append({
                'movie_id': movie.id,
                'title': movie.title,
                'genre': movie.genre,
                'year': movie.year,
                'rating': movie.rating,
                'description': movie.description,
                'poster_url': movie.poster_url,
                'trailer_url': movie.trailer_url
            })
        
        return pd.DataFrame(data)
    
    def get_users_df(self) -> pd.DataFrame:
        """
        Get users as a pandas DataFrame.
        
        Returns:
            DataFrame with columns: user_id, name, age, preferred_genre
        """
        users = self.db_service.get_all_users()
        
        data = []
        for user in users:
            data.append({
                'user_id': user.id,
                'name': user.name,
                'age': user.age,
                'preferred_genre': user.preferred_genre
            })
        
        return pd.DataFrame(data)
    
    def get_ratings_df(self) -> pd.DataFrame:
        """
        Get ratings as a pandas DataFrame.
        
        Returns:
            DataFrame with columns: user_id, movie_id, rating
        """
        # Get all ratings from database
        session = self.db_service.get_session()
        try:
            ratings = session.query(Rating).all()
            
            data = []
            for rating in ratings:
                data.append({
                    'user_id': rating.user_id,
                    'movie_id': rating.movie_id,
                    'rating': rating.rating
                })
            
            return pd.DataFrame(data)
        finally:
            session.close()
    
    def get_user_ratings(self, user_id: int) -> pd.DataFrame:
        """
        Get ratings for a specific user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            DataFrame with user's ratings including movie details
        """
        ratings = self.db_service.get_user_ratings(user_id)
        
        data = []
        for rating in ratings:
            movie = self.db_service.get_movie_by_id(rating.movie_id)
            if movie:
                data.append({
                    'movie_id': movie.id,
                    'title': movie.title,
                    'genre': movie.genre,
                    'year': movie.year,
                    'rating': rating.rating
                })
        
        return pd.DataFrame(data)
    
    def get_movies_by_genre(self, genre: str, limit: int = 20) -> pd.DataFrame:
        """
        Get movies by genre.
        
        Args:
            genre: Genre to filter by
            limit: Maximum number of movies to return
            
        Returns:
            DataFrame with movies in the specified genre
        """
        movies = self.db_service.get_movies_by_genre(genre, limit)
        
        data = []
        for movie in movies:
            # Get average rating from user ratings
            avg_rating = self.db_service.get_average_rating(movie.id)
            rating_count = self.db_service.get_rating_count(movie.id)
            
            data.append({
                'movie_id': movie.id,
                'title': movie.title,
                'genre': movie.genre,
                'year': movie.year,
                'rating': movie.rating,
                'avg_rating': avg_rating,
                'rating_count': rating_count
            })
        
        return pd.DataFrame(data)
    
    def get_popular_movies(self, limit: int = 20) -> pd.DataFrame:
        """
        Get popular movies based on average ratings.
        
        Args:
            limit: Maximum number of movies to return
            
        Returns:
            DataFrame with popular movies
        """
        movies = self.db_service.get_popular_movies(limit)
        
        data = []
        for movie in movies:
            # Get average rating from user ratings
            avg_rating = self.db_service.get_average_rating(movie.id)
            rating_count = self.db_service.get_rating_count(movie.id)
            
            data.append({
                'movie_id': movie.id,
                'title': movie.title,
                'genre': movie.genre,
                'year': movie.year,
                'rating': movie.rating,
                'avg_rating': avg_rating,
                'rating_count': rating_count
            })
        
        return pd.DataFrame(data)
    
    def search_movies(self, query: str, limit: int = 20) -> pd.DataFrame:
        """
        Search movies by title.
        
        Args:
            query: Search query
            limit: Maximum number of movies to return
            
        Returns:
            DataFrame with matching movies
        """
        movies = self.db_service.search_movies(query, limit)
        
        data = []
        for movie in movies:
            data.append({
                'movie_id': movie.id,
                'title': movie.title,
                'genre': movie.genre,
                'year': movie.year,
                'rating': movie.rating
            })
        
        return pd.DataFrame(data)
    
    def create_rating(self, user_id: int, movie_id: int, rating: float, 
                     review: Optional[str] = None) -> bool:
        """
        Create a new rating.
        
        Args:
            user_id: ID of the user
            movie_id: ID of the movie
            rating: Rating value (1-5)
            review: Optional review text
            
        Returns:
            True if successful, False otherwise
        """
        db_rating = self.db_service.create_rating(user_id, movie_id, rating, review)
        return db_rating is not None
    
    def get_movie_details(self, movie_id: int) -> Optional[dict]:
        """
        Get detailed information about a movie.
        
        Args:
            movie_id: ID of the movie
            
        Returns:
            Dictionary with movie details or None if not found
        """
        movie = self.db_service.get_movie_by_id(movie_id)
        if not movie:
            return None
        
        avg_rating = self.db_service.get_average_rating(movie_id)
        rating_count = self.db_service.get_rating_count(movie_id)
        
        return {
            'id': movie.id,
            'title': movie.title,
            'genre': movie.genre,
            'year': movie.year,
            'rating': movie.rating,
            'description': movie.description,
            'director': movie.director,
            'cast': movie.cast,
            'poster_url': movie.poster_url,
            'avg_rating': avg_rating,
            'rating_count': rating_count
        }
    
    def get_user_details(self, user_id: int) -> Optional[dict]:
        """
        Get detailed information about a user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            Dictionary with user details or None if not found
        """
        user = self.db_service.get_user_by_id(user_id)
        if not user:
            return None
        
        return {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'age': user.age,
            'preferred_genre': user.preferred_genre,
            'role': user.role
        } 