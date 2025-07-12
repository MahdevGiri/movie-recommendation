#!/usr/bin/env python3
"""
Demo script for the Movie Recommendation System

This script demonstrates various features of the recommendation system by
running through different scenarios and showing the results. It serves as
both a testing tool and a showcase of the system's capabilities.

The demo covers:
- Basic system functionality and data statistics
- Collaborative filtering recommendations
- Content-based filtering recommendations
- Popular movies ranking
- Genre-based browsing
- Hybrid recommendations
- User rating histories

Each demo function shows realistic examples and explains what the system
is doing behind the scenes.

Author: Movie Recommendation System
Version: 1.0
"""

import sys

from recommendation_system import MovieRecommendationSystem
from movie_data import load_all_data

def demo_basic_functionality():
    """
    Demonstrate basic functionality of the recommendation system.
    
    This function shows:
    - System initialization
    - Dataset statistics
    - Sample data from movies and users
    - Basic system capabilities
    
    This serves as an introduction to the system and verifies that
    all data is loaded correctly.
    """
    print("🎬 MOVIE RECOMMENDATION SYSTEM DEMO")
    print("=" * 50)
    
    # Initialize the recommendation system
    print("Loading recommendation system...")
    recommender = MovieRecommendationSystem()
    print("✅ System loaded successfully!")
    print()
    
    # Display dataset statistics
    print("📊 DATASET STATISTICS:")
    print(f"Total Movies: {len(recommender.movies_df)}")
    print(f"Total Users: {len(recommender.users_df)}")
    print(f"Total Ratings: {len(recommender.ratings_df)}")
    print()
    
    # Show sample movies to demonstrate data quality
    print("🎭 SAMPLE MOVIES:")
    sample_movies = recommender.movies_df.head(5)
    for _, movie in sample_movies.iterrows():
        print(f"  • {movie['title']} ({movie['year']}) - {movie['genre']} - Rating: {movie['rating']}")
    print()
    
    # Show sample users to demonstrate user data
    print("👥 SAMPLE USERS:")
    sample_users = recommender.users_df.head(5)
    for _, user in sample_users.iterrows():
        print(f"  • {user['name']} (ID: {user['user_id']}) - Age: {user['age']} - Prefers: {user['preferred_genre']}")
    print()

def demo_collaborative_filtering():
    """
    Demonstrate collaborative filtering recommendations.
    
    This function shows how the system recommends movies based on
    similar users' preferences. It uses user 1 (Alice) as an example
    and shows the top 5 recommended movies with predicted ratings.
    
    The collaborative filtering algorithm:
    1. Finds users similar to Alice based on rating patterns
    2. Identifies movies that similar users rated highly
    3. Predicts Alice's likely rating for unrated movies
    4. Returns the top recommendations
    """
    print("🔍 COLLABORATIVE FILTERING DEMO")
    print("-" * 40)
    
    # Initialize the recommendation system
    recommender = MovieRecommendationSystem()
    
    # Get recommendations for user 1 (Alice)
    user_id = 1
    recommendations = recommender.get_collaborative_filtering_recommendations(user_id, 5)
    
    # Display results with user context
    user_name = recommender.users_df[recommender.users_df['user_id'] == user_id]['name'].iloc[0]
    print(f"Top 5 recommendations for User {user_id} ({user_name}):")
    for i, movie in enumerate(recommendations, 1):
        print(f"  {i}. {movie['title']} ({movie['year']}) - {movie['genre']} - Predicted Rating: {movie['predicted_rating']}")
    print()

def demo_content_based_filtering():
    """
    Demonstrate content-based filtering recommendations.
    
    This function shows how the system finds movies similar to a
    given movie based on content features (genres, ratings). It uses
    "The Dark Knight" as the reference movie and shows similar movies
    with similarity scores.
    
    The content-based filtering algorithm:
    1. Analyzes movie features (genres, ratings)
    2. Calculates similarity between movies
    3. Finds movies most similar to the reference movie
    4. Returns recommendations with similarity scores
    """
    print("🎭 CONTENT-BASED FILTERING DEMO")
    print("-" * 40)
    
    # Initialize the recommendation system
    recommender = MovieRecommendationSystem()
    
    # Get recommendations similar to "The Dark Knight" (movie_id = 3)
    movie_id = 3  # The Dark Knight
    movie_title = recommender.movies_df[recommender.movies_df['movie_id'] == movie_id]['title'].iloc[0]
    
    # Get content-based recommendations
    recommendations = recommender.get_content_based_recommendations(movie_id, 5)
    
    # Display results with movie context
    print(f"Top 5 movies similar to '{movie_title}':")
    for i, movie in enumerate(recommendations, 1):
        print(f"  {i}. {movie['title']} ({movie['year']}) - {movie['genre']} - Similarity: {movie['similarity_score']}")
    print()

def demo_popular_movies():
    """
    Demonstrate popular movies feature.
    
    This function shows how the system ranks movies by popularity
    based on average ratings and number of ratings. It displays
    the top 10 most popular movies with their statistics.
    
    The popularity algorithm:
    1. Calculates average rating for each movie
    2. Counts number of ratings for reliability
    3. Filters out movies with too few ratings
    4. Sorts by average rating (highest first)
    """
    print("🔥 POPULAR MOVIES DEMO")
    print("-" * 40)
    
    # Initialize the recommendation system
    recommender = MovieRecommendationSystem()
    
    # Get top 10 popular movies
    popular_movies = recommender.get_popular_movies(10)
    
    # Display results with popularity statistics
    print("Top 10 popular movies based on average ratings:")
    for i, movie in enumerate(popular_movies, 1):
        print(f"  {i}. {movie['title']} ({movie['year']}) - {movie['genre']} - Avg Rating: {movie['avg_rating']} ({movie['rating_count']} ratings)")
    print()

def demo_genre_browsing():
    """
    Demonstrate genre browsing feature.
    
    This function shows how users can browse movies by genre.
    It demonstrates the feature with two popular genres: Action and Drama.
    For each genre, it shows the top 5 movies sorted by rating.
    
    The genre browsing feature:
    1. Filters movies by the specified genre
    2. Sorts by overall rating (highest first)
    3. Returns the top movies in that genre
    """
    print("🎭 GENRE BROWSING DEMO")
    print("-" * 40)
    
    # Initialize the recommendation system
    recommender = MovieRecommendationSystem()
    
    # Get top Action movies
    action_movies = recommender.get_movies_by_genre('Action', 5)
    print("Top 5 Action movies:")
    for i, movie in enumerate(action_movies, 1):
        print(f"  {i}. {movie['title']} ({movie['year']}) - Rating: {movie['rating']}")
    print()
    
    # Get top Drama movies
    drama_movies = recommender.get_movies_by_genre('Drama', 5)
    print("Top 5 Drama movies:")
    for i, movie in enumerate(drama_movies, 1):
        print(f"  {i}. {movie['title']} ({movie['year']}) - Rating: {movie['rating']}")
    print()

def demo_hybrid_recommendations():
    """
    Demonstrate hybrid recommendations.
    
    This function shows how the system combines collaborative filtering
    and content-based filtering to provide more diverse and accurate
    recommendations. It uses user 1 and "The Dark Knight" as examples.
    
    The hybrid algorithm:
    1. Gets collaborative filtering recommendations (70% weight)
    2. Gets content-based recommendations (30% weight)
    3. Combines scores for movies that appear in both
    4. Sorts by hybrid score and returns top recommendations
    """
    print("🔀 HYBRID RECOMMENDATIONS DEMO")
    print("-" * 40)
    
    # Initialize the recommendation system
    recommender = MovieRecommendationSystem()
    
    # Get hybrid recommendations for user 1 with movie 3 as reference
    user_id = 1
    movie_id = 3  # The Dark Knight
    movie_title = recommender.movies_df[recommender.movies_df['movie_id'] == movie_id]['title'].iloc[0]
    
    # Get hybrid recommendations
    recommendations = recommender.get_hybrid_recommendations(user_id, movie_id, 5)
    
    # Display results with hybrid context
    print(f"Hybrid recommendations for User {user_id} based on '{movie_title}':")
    for i, movie in enumerate(recommendations, 1):
        print(f"  {i}. {movie['title']} ({movie['year']}) - {movie['genre']} - Hybrid Score: {movie['hybrid_score']:.2f}")
    print()

def demo_user_ratings():
    """
    Demonstrate user ratings feature.
    
    This function shows how to view a user's rating history.
    It displays the movies rated by user 1 (Alice) with their ratings,
    sorted by rating value (highest first). This helps understand
    user preferences and verify the rating data.
    
    The user ratings feature:
    1. Retrieves all ratings for a specific user
    2. Merges with movie information for context
    3. Sorts by rating value (highest first)
    4. Displays user's movie preferences
    """
    print("⭐ USER RATINGS DEMO")
    print("-" * 40)
    
    # Initialize the recommendation system
    recommender = MovieRecommendationSystem()
    
    # Get ratings for user 1 (Alice)
    user_id = 1
    user_name = recommender.users_df[recommender.users_df['user_id'] == user_id]['name'].iloc[0]
    user_ratings = recommender.get_user_ratings(user_id)
    
    # Display user's rating history
    print(f"Movies rated by {user_name} (User {user_id}):")
    if not user_ratings:
        print("  No ratings found for this user.")
        return
    
    # Show first 10 ratings (to avoid overwhelming output)
    for i, rating in enumerate(user_ratings[:10], 1):
        print(f"  {i}. {rating['title']} ({rating['year']}) - {rating['genre']} - Rating: {rating['rating']}")
    
    # Show summary if there are more ratings
    if len(user_ratings) > 10:
        print(f"... and {len(user_ratings) - 10} more movies")
    print()

def main():
    """
    Main demo function that runs all demonstration scenarios.
    
    This function orchestrates the entire demo by:
    1. Running each demo function in sequence
    2. Providing clear separation between demos
    3. Handling any errors that might occur
    4. Providing instructions for running the full application
    
    The demo serves as both a test of system functionality and
    a showcase of the recommendation system's capabilities.
    """
    try:
        # Run all demo functions in sequence
        print("Starting comprehensive demo of the Movie Recommendation System...")
        print()
        
        # Basic functionality and data overview
        demo_basic_functionality()
        
        # Recommendation algorithms
        demo_collaborative_filtering()
        demo_content_based_filtering()
        demo_popular_movies()
        demo_genre_browsing()
        demo_hybrid_recommendations()
        demo_user_ratings()
        
        # Demo completion message
        print("🎉 DEMO COMPLETED SUCCESSFULLY!")
        print("\nTo run the interactive application, use:")
        print("python main.py")
        
    except Exception as e:
        # Handle any errors during demo execution
        print(f"❌ Error during demo: {e}")
        print("Please check your installation and try again.")

if __name__ == "__main__":
    main() 