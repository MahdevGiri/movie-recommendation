#!/usr/bin/env python3
"""
Test script to verify poster URLs and trailer URLs are working correctly.
"""

from database_service import DatabaseService
from database_config import db_config

def test_movie_data():
    """Test that movies have poster and trailer URLs."""
    print("🧪 TESTING MOVIE DATA")
    print("=" * 50)
    
    # Initialize database service
    db_service = DatabaseService()
    
    # Get all movies
    movies = db_service.get_all_movies()
    
    print(f"Total movies: {len(movies)}")
    print("\nSample movies with poster and trailer URLs:")
    print("-" * 50)
    
    for i, movie in enumerate(movies[:5]):  # Show first 5 movies
        print(f"{i+1}. {movie.title} ({movie.year})")
        print(f"   Genre: {movie.genre}")
        print(f"   Description: {'✅' if movie.description else '❌'} {movie.description[:50] + '...' if movie.description and len(movie.description) > 50 else movie.description}")
        print(f"   Poster: {'✅' if movie.poster_url else '❌'} {movie.poster_url}")
        print(f"   Trailer: {'✅' if movie.trailer_url else '❌'} {movie.trailer_url}")
        print()
    
    # Count movies with poster URLs
    movies_with_posters = sum(1 for movie in movies if movie.poster_url)
    movies_with_trailers = sum(1 for movie in movies if movie.trailer_url)
    movies_with_descriptions = sum(1 for movie in movies if movie.description)
    
    print(f"Movies with poster URLs: {movies_with_posters}/{len(movies)}")
    print(f"Movies with trailer URLs: {movies_with_trailers}/{len(movies)}")
    print(f"Movies with descriptions: {movies_with_descriptions}/{len(movies)}")
    
    if movies_with_posters == len(movies) and movies_with_trailers == len(movies) and movies_with_descriptions == len(movies):
        print("✅ All movies have poster, trailer, and description!")
    else:
        print("❌ Some movies are missing poster, trailer, or description URLs.")

if __name__ == "__main__":
    test_movie_data() 