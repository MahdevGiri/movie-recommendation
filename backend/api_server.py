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
        
        if not username or not password or not name:
            return jsonify({'error': 'Username, password, and name are required'}), 400
        
        # Use existing auth system
        registration_success = auth_system.register_user(username, password, name, age, preferred_genre, email)
        
        if registration_success:
            # Get the newly created user
            user = auth_system.get_current_user()
            if not user:
                # If not logged in, get user by username
                user = db_service.get_user_by_username(username)
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
            return jsonify({'movie': movie}), 200
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
                'rating': float(round(movie['rating'], 1)),
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

# User management endpoints
@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users (admin only)"""
    try:
        user_id = get_jwt_identity()
        current_user = db_service.get_user_by_id(user_id)
        
        if current_user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        users = db_service.get_all_users()
        
        return jsonify({
            'users': users,
            'count': len(users)
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