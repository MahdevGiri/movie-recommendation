#!/usr/bin/env python3
"""
Movie Recommendation System - API Server

This Flask API server exposes the movie recommendation system functionality
as REST endpoints for the React frontend. It provides endpoints for:
- User authentication (login, register, logout)
- Movie recommendations (collaborative, content-based, hybrid)
- Movie browsing and filtering
- User profile management
- Rating management

Author: Movie Recommendation System
Version: 2.0
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta
import json
import hashlib
import pandas as pd
import re

# Import existing modules
from recommendation_system import MovieRecommendationSystem
from auth_system import AuthSystem
from database_service import DatabaseService
from models import User, Movie, Rating, Genre, UserSession
from database_config import db_config

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-jwt-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
CORS(app)  # Enable CORS for all routes
jwt = JWTManager(app)

# JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    print(f"JWT token expired: {jwt_payload}")
    return jsonify({'error': 'Token has expired'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    print(f"Invalid JWT token: {error}")
    return jsonify({'error': 'Invalid token'}), 422

@jwt.unauthorized_loader
def missing_token_callback(error):
    print(f"Missing JWT token: {error}")
    return jsonify({'error': 'Missing token'}), 401

# Initialize services
recommender = MovieRecommendationSystem()
auth_system = AuthSystem()
db_service = DatabaseService()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Movie Recommendation API is running',
        'timestamp': datetime.now().isoformat()
    })

# Authentication endpoints
@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        # Use existing auth system
        login_success = auth_system.login(username, password)
        
        if login_success:
            # Get the current user after successful login
            user = auth_system.get_current_user()
            # Create JWT token (identity must be a string)
            access_token = create_access_token(identity=str(user.id))
            
            return jsonify({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'name': user.name,
                    'email': user.email,
                    'age': user.age,
                    'preferred_genre': user.preferred_genre,
                    'role': user.role
                },
                'access_token': access_token
            }), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        name = data.get('name')
        email = data.get('email')
        age = data.get('age')
        preferred_genre = data.get('preferred_genre', 'Drama')
        
        if not username or not password or not name or not email or age is None:
            return jsonify({'error': 'Username, password, name, email, and age are required'}), 400
        
        # Validate email format
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            return jsonify({'error': 'Please enter a valid email address'}), 400
        
        # Validate age
        if not isinstance(age, int) or age < 13 or age > 120:
            return jsonify({'error': 'Age must be between 13 and 120'}), 400
        
        # Use existing auth system
        registration_success = auth_system.register_user(username, password, name, age, preferred_genre, email)
        
        if registration_success:
            # Automatically log in the newly registered user
            login_success = auth_system.login(username, password)
            if login_success:
                user = auth_system.get_current_user()
            else:
                # Fallback: get user by username if login fails
                user = db_service.get_user_by_username(username)
            
            if user:
                # Create JWT token (identity must be a string)
                access_token = create_access_token(identity=str(user.id))
                
                return jsonify({
                    'message': 'Registration successful',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'name': user.name,
                        'email': user.email,
                        'age': user.age,
                        'preferred_genre': user.preferred_genre,
                        'role': user.role
                    },
                    'access_token': access_token
                }), 201
            else:
                return jsonify({'error': 'Registration successful but failed to log in user'}), 500
        else:
            return jsonify({'error': 'Username already exists'}), 409
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        user_id = get_jwt_identity()
        print(f"Profile request for user_id: {user_id}")
        
        user = db_service.get_user_by_id(user_id)
        
        if user:
            return jsonify({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'name': user.name,
                    'email': user.email,
                    'age': user.age,
                    'preferred_genre': user.preferred_genre,
                    'role': user.role
                }
            }), 200
        else:
            print(f"User not found for ID: {user_id}")
            return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        print(f"Profile endpoint error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Current and new password are required'}), 400
        
        # Get user and verify current password
        user = db_service.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Verify current password
        if not db_service.authenticate_user(user.username, current_password):
            return jsonify({'error': 'Invalid current password'}), 400
        
        # Update password
        success = db_service.update_user(user_id, password_hash=hashlib.sha256(new_password.encode()).hexdigest())
        
        if success:
            return jsonify({'message': 'Password changed successfully'}), 200
        else:
            return jsonify({'error': 'Invalid current password'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Movie endpoints
@app.route('/api/movies', methods=['GET'])
def get_movies():
    """Get all movies with optional filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        genre = request.args.get('genre')
        search = request.args.get('search')
        
        movies = db_service.get_movies(page=page, per_page=per_page, genre=genre, search=search)
        # Get the total number of movies for pagination
        session = db_service.get_session()
        query = session.query(Movie)
        if genre:
            query = query.filter(Movie.genre == genre)
        if search:
            query = query.filter(Movie.title.ilike(f'%{search}%'))
        total = query.count()
        session.close()
        
        return jsonify({
            'movies': movies,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Get specific movie details"""
    try:
        movie = db_service.get_movie_by_id(movie_id)
        
        if movie:
            movie_data = {
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
            }
            return jsonify({'movie': movie_data}), 200
        else:
            return jsonify({'error': 'Movie not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/movies/popular', methods=['GET'])
def get_popular_movies():
    """Get popular movies"""
    try:
        limit = request.args.get('limit', 10, type=int)
        popular_movies = recommender.get_popular_movies(limit)
        
        return jsonify({
            'movies': popular_movies,
            'count': len(popular_movies)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/movies/genres', methods=['GET'])
def get_genres():
    """Get all available genres"""
    try:
        genres = db_service.get_all_genres()
        
        return jsonify({
            'genres': genres
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/movies/genre/<genre>', methods=['GET'])
def get_movies_by_genre(genre):
    """Get movies by specific genre"""
    try:
        limit = request.args.get('limit', 10, type=int)
        movies = recommender.get_movies_by_genre(genre, limit)
        
        return jsonify({
            'movies': movies,
            'genre': genre,
            'count': len(movies)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Recommendation endpoints
@app.route('/api/recommendations/personalized', methods=['GET'])
@jwt_required()
def get_personalized_recommendations():
    """Get personalized recommendations for current user"""
    try:
        user_id = int(get_jwt_identity())
        limit = request.args.get('limit', 5, type=int)
        
        # Get user info for context
        user = db_service.get_user_by_id(user_id)
        
        # Check if user is admin - admins don't get recommendations
        if user.role == 'admin':
            return jsonify({'error': 'Admin users do not have access to movie recommendations'}), 403
        
        recommendations = recommender.get_collaborative_filtering_recommendations(user_id, limit)
        
        return jsonify({
            'recommendations': recommendations,
            'type': 'collaborative',
            'user_preferred_genre': user.preferred_genre,
            'algorithm_info': 'Uses collaborative filtering with genre preference boost',
            'count': len(recommendations)
        }), 200
        
    except Exception as e:
        print("Error in /api/recommendations/personalized:", e)
        import traceback; traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations/genre-focused', methods=['GET'])
@jwt_required()
def get_genre_focused_recommendations():
    """Get genre-focused personalized recommendations for current user"""
    try:
        user_id = int(get_jwt_identity())
        limit = request.args.get('limit', 5, type=int)
        
        # Get user info
        user = db_service.get_user_by_id(user_id)
        
        # Check if user is admin - admins don't get recommendations
        if user.role == 'admin':
            return jsonify({'error': 'Admin users do not have access to movie recommendations'}), 403
        
        preferred_genre = user.preferred_genre
        
        # Get movies in user's preferred genre, sorted by rating
        genre_movies = recommender.movies_df[recommender.movies_df['genre'] == preferred_genre]
        top_genre_movies = genre_movies.nlargest(limit, 'rating')
        
        recommendations = []
        for _, movie in top_genre_movies.iterrows():
            recommendations.append({
                'movie_id': int(movie['movie_id']),
                'title': str(movie['title']),
                'genre': str(movie['genre']),
                'year': int(movie['year']),
                'description': str(movie['description']) if pd.notna(movie['description']) else None,
                'poster_url': str(movie['poster_url']) if pd.notna(movie['poster_url']) else None,
                'trailer_url': str(movie['trailer_url']) if pd.notna(movie['trailer_url']) else None,
                'predicted_rating': float(round(min(movie['rating'], 5.0), 1)),
                'reason': f'Top rated {preferred_genre} movie'
            })
        
        return jsonify({
            'recommendations': recommendations,
            'type': 'genre-focused',
            'user_preferred_genre': preferred_genre,
            'algorithm_info': f'Top rated movies in your preferred genre ({preferred_genre})',
            'count': len(recommendations)
        }), 200
        
    except Exception as e:
        print("Error in /api/recommendations/genre-focused:", e)
        import traceback; traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations/content-based/<int:movie_id>', methods=['GET'])
def get_content_based_recommendations(movie_id):
    """Get content-based recommendations for a specific movie"""
    try:
        limit = request.args.get('limit', 5, type=int)
        
        recommendations = recommender.get_content_based_recommendations(movie_id, limit)
        
        return jsonify({
            'recommendations': recommendations,
            'type': 'content-based',
            'reference_movie_id': movie_id,
            'count': len(recommendations)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations/hybrid', methods=['GET'])
@jwt_required()
def get_hybrid_recommendations():
    """Get hybrid recommendations for current user"""
    try:
        user_id = get_jwt_identity()
        movie_id = request.args.get('movie_id', type=int)
        limit = request.args.get('limit', 5, type=int)
        
        # Get user info to check role
        user = db_service.get_user_by_id(int(user_id))
        
        # Check if user is admin - admins don't get recommendations
        if user.role == 'admin':
            return jsonify({'error': 'Admin users do not have access to movie recommendations'}), 403
        
        recommendations = recommender.get_hybrid_recommendations(user_id, movie_id, limit)
        
        return jsonify({
            'recommendations': recommendations,
            'type': 'hybrid',
            'count': len(recommendations)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rating endpoints
@app.route('/api/ratings', methods=['GET'])
@jwt_required()
def get_user_ratings():
    """Get ratings for current user"""
    try:
        user_id = int(get_jwt_identity())
        ratings = recommender.get_user_ratings(user_id)
        
        return jsonify({
            'ratings': ratings,
            'count': len(ratings)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ratings', methods=['POST'])
@jwt_required()
def add_rating():
    """Add a new rating"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        movie_id = data.get('movie_id')
        rating = data.get('rating')
        review = data.get('review', '')
        
        if not movie_id or not rating:
            return jsonify({'error': 'Movie ID and rating are required'}), 400
        
        if not (1 <= rating <= 5):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        success = db_service.add_rating(user_id, movie_id, rating, review)
        
        if success:
            recommender.refresh_data()
            return jsonify({'message': 'Rating added successfully'}), 201
        else:
            return jsonify({'error': 'Failed to add rating'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ratings/<int:movie_id>', methods=['PUT'])
@jwt_required()
def update_rating(movie_id):
    """Update an existing rating"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        rating = data.get('rating')
        review = data.get('review', '')
        
        if not rating:
            return jsonify({'error': 'Rating is required'}), 400
        
        if not (1 <= rating <= 5):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        success = db_service.update_rating(user_id, movie_id, rating, review)
        
        if success:
            recommender.refresh_data()
            return jsonify({'message': 'Rating updated successfully'}), 200
        else:
            return jsonify({'error': 'Rating not found or update failed'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ratings/<int:movie_id>', methods=['DELETE'])
@jwt_required()
def delete_rating(movie_id):
    """Delete a rating"""
    try:
        user_id = int(get_jwt_identity())
        
        success = db_service.delete_rating(user_id, movie_id)
        
        if success:
            recommender.refresh_data()
            return jsonify({'message': 'Rating deleted successfully'}), 200
        else:
            return jsonify({'error': 'Rating not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin helper function
def require_admin():
    """Helper function to require admin access"""
    user_id = get_jwt_identity()
    # Convert string to int if needed
    if isinstance(user_id, str):
        try:
            user_id = int(user_id)
        except ValueError:
            return False, 'Invalid user ID'
    
    current_user = db_service.get_user_by_id(user_id)
    
    if not current_user or current_user.role != 'admin':
        return False, 'Admin access required'
    return True, current_user

# User management endpoints
@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users (admin only)"""
    try:
        is_admin, result = require_admin()
        if not is_admin:
            return jsonify({'error': result}), 403
        
        users = db_service.get_all_users()
        
        # Convert users to serializable format
        user_list = []
        for user in users:
            user_list.append({
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'email': user.email,
                'age': user.age,
                'preferred_genre': user.preferred_genre,
                'role': user.role,
                'created_at': user.created_at.isoformat() if user.created_at else None
            })
        
        return jsonify({
            'users': user_list,
            'count': len(user_list)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users', methods=['POST'])
@jwt_required()
def admin_create_user():
    """Create a new user (admin only)"""
    try:
        is_admin, current_user = require_admin()
        if not is_admin:
            return jsonify({'error': current_user}), 403
        
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        name = data.get('name')
        email = data.get('email')
        age = data.get('age')
        preferred_genre = data.get('preferred_genre', 'Drama')
        role = data.get('role', 'user')
        
        if not username or not password or not name or not email or age is None:
            return jsonify({'error': 'Username, password, name, email, and age are required'}), 400
        
        # Validate email format
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            return jsonify({'error': 'Please enter a valid email address'}), 400
        
        # Validate age
        if not isinstance(age, int) or age < 13 or age > 120:
            return jsonify({'error': 'Age must be between 13 and 120'}), 400
        
        # Validate role
        if role not in ['user', 'admin']:
            return jsonify({'error': 'Role must be either "user" or "admin"'}), 400
        
        user = db_service.create_user(
            username=username,
            password=password,
            name=name,
            email=email,
            age=age,
            preferred_genre=preferred_genre,
            role=role
        )
        
        if user:
            return jsonify({
                'message': 'User created successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'name': user.name,
                    'email': user.email,
                    'age': user.age,
                    'preferred_genre': user.preferred_genre,
                    'role': user.role
                }
            }), 201
        else:
            return jsonify({'error': 'Username or email already exists'}), 409
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_user(user_id):
    """Delete a user (admin only)"""
    try:
        is_admin, current_user = require_admin()
        if not is_admin:
            return jsonify({'error': current_user}), 403
        
        # Prevent admin from deleting themselves
        if user_id == current_user.id:
            return jsonify({'error': 'Cannot delete your own account'}), 400
        
        # Check if user exists
        user = db_service.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Delete user (this will cascade to ratings)
        success = db_service.delete_user(user_id)
        
        if success:
            return jsonify({'message': 'User deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete user'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin movie management endpoints
@app.route('/api/admin/movies', methods=['POST'])
@jwt_required()
def admin_create_movie():
    """Create a new movie (admin only)"""
    try:
        is_admin, current_user = require_admin()
        if not is_admin:
            return jsonify({'error': current_user}), 403
        
        data = request.get_json()
        title = data.get('title')
        genre = data.get('genre')
        year = data.get('year')
        description = data.get('description')
        director = data.get('director')
        cast = data.get('cast')
        poster_url = data.get('poster_url')
        trailer_url = data.get('trailer_url')
        
        if not title or not genre or not year:
            return jsonify({'error': 'Title, genre, and year are required'}), 400
        
        # Validate year
        if not isinstance(year, int) or year < 1900 or year > 2030:
            return jsonify({'error': 'Year must be between 1900 and 2030'}), 400
        
        movie = db_service.create_movie(
            title=title,
            genre=genre,
            year=year,
            description=description,
            director=director,
            cast=cast,
            poster_url=poster_url,
            trailer_url=trailer_url
        )
        
        if movie:
            return jsonify({
                'message': 'Movie created successfully',
                'movie': {
                    'id': movie.id,
                    'title': movie.title,
                    'genre': movie.genre,
                    'year': movie.year,
                    'description': movie.description,
                    'director': movie.director,
                    'cast': movie.cast,
                    'poster_url': movie.poster_url,
                    'trailer_url': movie.trailer_url
                }
            }), 201
        else:
            return jsonify({'error': 'Failed to create movie'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/movies/<int:movie_id>', methods=['PUT'])
@jwt_required()
def admin_update_movie(movie_id):
    """Update a movie (admin only)"""
    try:
        is_admin, current_user = require_admin()
        if not is_admin:
            return jsonify({'error': current_user}), 403
        
        data = request.get_json()
        
        # Validate required fields if provided
        if 'year' in data and (not isinstance(data['year'], int) or data['year'] < 1900 or data['year'] > 2030):
            return jsonify({'error': 'Year must be between 1900 and 2030'}), 400
        
        success = db_service.update_movie(movie_id, **data)
        
        if success:
            # Get updated movie
            movie = db_service.get_movie_by_id(movie_id)
            return jsonify({
                'message': 'Movie updated successfully',
                'movie': {
                    'id': movie.id,
                    'title': movie.title,
                    'genre': movie.genre,
                    'year': movie.year,
                    'description': movie.description,
                    'director': movie.director,
                    'cast': movie.cast,
                    'poster_url': movie.poster_url,
                    'trailer_url': movie.trailer_url
                }
            }), 200
        else:
            return jsonify({'error': 'Movie not found or update failed'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/movies/<int:movie_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_movie(movie_id):
    """Delete a movie (admin only)"""
    try:
        is_admin, current_user = require_admin()
        if not is_admin:
            return jsonify({'error': current_user}), 403
        
        # First check if movie exists
        movie = db_service.get_movie_by_id(movie_id)
        if not movie:
            return jsonify({'error': 'Movie not found'}), 404
        
        # Delete associated ratings first
        session = db_service.get_session()
        try:
            # Delete all ratings for this movie
            ratings = session.query(Rating).filter(Rating.movie_id == movie_id).all()
            for rating in ratings:
                session.delete(rating)
            
            # Delete the movie
            session.delete(movie)
            session.commit()
            
            return jsonify({'message': 'Movie deleted successfully'}), 200
            
        except Exception as e:
            session.rollback()
            return jsonify({'error': f'Failed to delete movie: {str(e)}'}), 500
        finally:
            session.close()
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/movies', methods=['GET'])
@jwt_required()
def admin_get_movies():
    """Get all movies with admin details (admin only)"""
    try:
        is_admin, current_user = require_admin()
        if not is_admin:
            return jsonify({'error': current_user}), 403
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        genre = request.args.get('genre')
        search = request.args.get('search')
        
        movies = db_service.get_movies(page=page, per_page=per_page, genre=genre, search=search)
        
        # Get total count for pagination
        session = db_service.get_session()
        query = session.query(Movie)
        if genre:
            query = query.filter(Movie.genre == genre)
        if search:
            query = query.filter(Movie.title.ilike(f'%{search}%'))
        total = query.count()
        session.close()
        
        return jsonify({
            'movies': movies,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🎬 Starting Movie Recommendation API Server...")
    print("📡 API will be available at: http://localhost:5000")
    print("🔗 Frontend can connect to: http://localhost:5000/api")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000) 