from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database_config import db_config

Base = db_config.Base

class User(Base):
    """
    User model for storing user information and authentication data.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    age = Column(Integer, nullable=True)
    preferred_genre = Column(String(50), nullable=True)
    role = Column(String(20), default="user")  # user, admin
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    ratings = relationship("Rating", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', name='{self.name}')>"

class Movie(Base):
    """
    Movie model for storing movie information.
    """
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    genre = Column(String(100), nullable=False, index=True)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=True)  # Overall rating
    description = Column(Text, nullable=True)
    director = Column(String(100), nullable=True)
    cast = Column(Text, nullable=True)  # JSON string of cast members
    poster_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    ratings = relationship("Rating", back_populates="movie")
    
    def __repr__(self):
        return f"<Movie(id={self.id}, title='{self.title}', year={self.year})>"

class Rating(Base):
    """
    Rating model for storing user ratings of movies.
    """
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False, index=True)
    rating = Column(Float, nullable=False)  # Rating value (1-5)
    review = Column(Text, nullable=True)  # Optional review text
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")
    
    def __repr__(self):
        return f"<Rating(id={self.id}, user_id={self.user_id}, movie_id={self.movie_id}, rating={self.rating})>"

class Genre(Base):
    """
    Genre model for storing available movie genres.
    """
    __tablename__ = "genres"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Genre(id={self.id}, name='{self.name}')>"

class UserSession(Base):
    """
    User session model for storing active user sessions.
    """
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    
    def __repr__(self):
        return f"<UserSession(id={self.id}, user_id={self.user_id}, expires_at={self.expires_at})>" 