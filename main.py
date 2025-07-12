#!/usr/bin/env python3
"""
Movie Recommendation System - Main Application

This is the main entry point for the movie recommendation system.
It provides a command-line interface (CLI) for users to interact with
various recommendation features including collaborative filtering,
content-based filtering, hybrid recommendations, and more.

The application offers a menu-driven interface that allows users to:
1. Get personalized recommendations for specific users
2. Find movies similar to a given movie
3. Get hybrid recommendations combining multiple approaches
4. Browse popular movies
5. Filter movies by genre
6. View user rating histories
7. Explore the movie and user databases

Author: Movie Recommendation System
Version: 1.0
"""

import sys
from recommendation_system import MovieRecommendationSystem
from movie_data import load_all_data

def print_header():
    """
    Print the application header with title and decorative elements.
    
    This function creates a visually appealing header that introduces
    the movie recommendation system to users.
    """
    print("=" * 60)
    print("🎬 MOVIE RECOMMENDATION SYSTEM 🎬")
    print("=" * 60)
    print()

def print_menu():
    """
    Display the main menu options to the user.
    
    This function shows all available features of the recommendation system,
    numbered for easy selection. Each option corresponds to a different
    recommendation algorithm or data exploration feature.
    """
    print("📋 MAIN MENU:")
    print("1. Get personalized recommendations for a user")
    print("2. Get content-based recommendations for a movie")
    print("3. Get hybrid recommendations")
    print("4. Show popular movies")
    print("5. Browse movies by genre")
    print("6. View user ratings")
    print("7. List all movies")
    print("8. List all users")
    print("9. Exit")
    print()

def print_movie_list(movies, title="Movies"):
    """
    Print a formatted list of movies with their details.
    
    This function handles different types of movie data (recommendations,
    popular movies, genre lists, etc.) and formats them consistently
    for display to the user.
    
    Args:
        movies (list): List of movie dictionaries to display
        title (str): Title for the movie list section
    """
    print(f"\n🎭 {title.upper()}:")
    print("-" * 80)
    
    # Handle empty movie lists
    if not movies:
        print("No movies found.")
        return
    
    # Display each movie with appropriate formatting based on available data
    for i, movie in enumerate(movies, 1):
        if 'predicted_rating' in movie:
            # Collaborative filtering recommendations
            print(f"{i:2d}. {movie['title']} ({movie['year']}) - {movie['genre']} - Predicted Rating: {movie['predicted_rating']}")
        elif 'similarity_score' in movie:
            # Content-based recommendations
            print(f"{i:2d}. {movie['title']} ({movie['year']}) - {movie['genre']} - Similarity: {movie['similarity_score']}")
        elif 'avg_rating' in movie:
            # Popular movies with average ratings
            print(f"{i:2d}. {movie['title']} ({movie['year']}) - {movie['genre']} - Avg Rating: {movie['avg_rating']} ({movie['rating_count']} ratings)")
        elif 'hybrid_score' in movie:
            # Hybrid recommendations
            print(f"{i:2d}. {movie['title']} ({movie['year']}) - {movie['genre']} - Hybrid Score: {movie['hybrid_score']:.2f}")
        else:
            # General movie listings (genre browsing, user ratings, etc.)
            print(f"{i:2d}. {movie['title']} ({movie['year']}) - {movie['genre']} - Rating: {movie.get('rating', 'N/A')}")
    print()

def get_user_input(prompt, valid_range=None, input_type=int):
    """
    Get and validate user input with error handling.
    
    This function provides a robust way to get user input with:
    - Type validation (default: integer)
    - Range validation (optional)
    - Error handling for invalid input
    - Option to quit with 'q'
    
    Args:
        prompt (str): Message to display to the user
        valid_range (range, optional): Valid range for the input
        input_type (type): Expected data type (default: int)
        
    Returns:
        The validated user input, or None if user chooses to quit
    """
    while True:
        try:
            user_input = input(prompt)
            # Allow user to quit with 'q'
            if user_input.lower() == 'q':
                return None
            
            # Convert input to specified type
            value = input_type(user_input)
            
            # Validate range if specified
            if valid_range and value not in valid_range:
                print(f"Please enter a number between {min(valid_range)} and {max(valid_range)}")
                continue
            
            return value
            
        except ValueError:
            print("Please enter a valid number.")

def get_personalized_recommendations(recommender):
    """
    Handle personalized recommendations for a specific user.
    
    This function implements collaborative filtering by:
    1. Showing available users with their preferences
    2. Getting user selection and number of recommendations
    3. Calling the collaborative filtering algorithm
    4. Displaying results
    
    Args:
        recommender (MovieRecommendationSystem): The recommendation system instance
    """
    print("\n👤 PERSONALIZED RECOMMENDATIONS")
    print("-" * 40)
    
    # Display available users with their preferences
    users = recommender.users_df[['user_id', 'name', 'preferred_genre']].to_dict('records')
    print("Available users:")
    for user in users:
        print(f"{user['user_id']:2d}. {user['name']} (Prefers: {user['preferred_genre']})")
    
    # Get user selection
    user_id = get_user_input("\nEnter user ID (or 'q' to quit): ", range(1, 21))
    if user_id is None:
        return
    
    # Get number of recommendations
    n_recommendations = get_user_input("Number of recommendations (1-10): ", range(1, 11))
    if n_recommendations is None:
        return
    
    # Get and display recommendations
    recommendations = recommender.get_collaborative_filtering_recommendations(user_id, n_recommendations)
    print_movie_list(recommendations, f"Personalized Recommendations for User {user_id}")

def get_content_based_recommendations(recommender):
    """
    Handle content-based recommendations for a specific movie.
    
    This function implements content-based filtering by:
    1. Showing available movies (first 20 for brevity)
    2. Getting movie selection and number of recommendations
    3. Calling the content-based filtering algorithm
    4. Displaying similar movies
    
    Args:
        recommender (MovieRecommendationSystem): The recommendation system instance
    """
    print("\n🎭 CONTENT-BASED RECOMMENDATIONS")
    print("-" * 40)
    
    # Display available movies (first 20 to avoid overwhelming output)
    movies = recommender.movies_df[['movie_id', 'title', 'genre']].to_dict('records')
    print("Available movies:")
    for movie in movies[:20]:  # Show first 20 movies
        print(f"{movie['movie_id']:2d}. {movie['title']} ({movie['genre']})")
    print("... (showing first 20 movies)")
    
    # Get movie selection
    movie_id = get_user_input("\nEnter movie ID (or 'q' to quit): ", range(1, 51))
    if movie_id is None:
        return
    
    # Get number of recommendations
    n_recommendations = get_user_input("Number of recommendations (1-10): ", range(1, 11))
    if n_recommendations is None:
        return
    
    # Get and display recommendations
    recommendations = recommender.get_content_based_recommendations(movie_id, n_recommendations)
    print_movie_list(recommendations, f"Movies Similar to Movie {movie_id}")

def get_hybrid_recommendations(recommender):
    """
    Handle hybrid recommendations combining multiple approaches.
    
    This function implements hybrid filtering by:
    1. Getting user selection
    2. Optionally getting a reference movie for content-based filtering
    3. Combining collaborative and content-based approaches
    4. Displaying hybrid recommendations
    
    Args:
        recommender (MovieRecommendationSystem): The recommendation system instance
    """
    print("\n🔀 HYBRID RECOMMENDATIONS")
    print("-" * 40)
    
    # Display available users
    users = recommender.users_df[['user_id', 'name']].to_dict('records')
    print("Available users:")
    for user in users:
        print(f"{user['user_id']:2d}. {user['name']}")
    
    # Get user selection
    user_id = get_user_input("\nEnter user ID (or 'q' to quit): ", range(1, 21))
    if user_id is None:
        return
    
    # Optional: ask for a specific movie for content-based filtering
    print("\nOptional: Enter a specific movie ID for content-based filtering")
    print("(Press Enter to skip and use only collaborative filtering)")
    movie_id = input("Movie ID (or Enter to skip): ").strip()
    
    # Validate movie ID if provided
    if movie_id:
        try:
            movie_id = int(movie_id)
            if movie_id not in range(1, 51):
                print("Invalid movie ID. Using collaborative filtering only.")
                movie_id = None
        except ValueError:
            print("Invalid input. Using collaborative filtering only.")
            movie_id = None
    
    # Get number of recommendations
    n_recommendations = get_user_input("Number of recommendations (1-10): ", range(1, 11))
    if n_recommendations is None:
        return
    
    # Get and display hybrid recommendations
    recommendations = recommender.get_hybrid_recommendations(user_id, movie_id, n_recommendations)
    print_movie_list(recommendations, f"Hybrid Recommendations for User {user_id}")

def show_popular_movies(recommender):
    """
    Show popular movies based on average ratings.
    
    This function displays trending movies by:
    1. Getting the number of movies to show
    2. Calling the popular movies algorithm
    3. Displaying movies with their average ratings and rating counts
    
    Args:
        recommender (MovieRecommendationSystem): The recommendation system instance
    """
    print("\n🔥 POPULAR MOVIES")
    print("-" * 40)
    
    # Get number of popular movies to display
    n_recommendations = get_user_input("Number of popular movies to show (1-20): ", range(1, 21))
    if n_recommendations is None:
        return
    
    # Get and display popular movies
    popular_movies = recommender.get_popular_movies(n_recommendations)
    print_movie_list(popular_movies, "Popular Movies")

def browse_by_genre(recommender):
    """
    Browse movies by specific genre.
    
    This function allows genre-based exploration by:
    1. Displaying available genres
    2. Getting genre selection and number of movies
    3. Filtering movies by the selected genre
    4. Displaying results sorted by rating
    
    Args:
        recommender (MovieRecommendationSystem): The recommendation system instance
    """
    print("\n🎭 BROWSE BY GENRE")
    print("-" * 40)
    
    # Get unique genres and display them
    genres = sorted(recommender.movies_df['genre'].unique())
    print("Available genres:")
    for i, genre in enumerate(genres, 1):
        print(f"{i:2d}. {genre}")
    
    # Get genre selection
    genre_choice = get_user_input("\nEnter genre number (or 'q' to quit): ", range(1, len(genres) + 1))
    if genre_choice is None:
        return
    
    # Get selected genre
    selected_genre = genres[genre_choice - 1]
    
    # Get number of movies to display
    n_recommendations = get_user_input("Number of movies to show (1-20): ", range(1, 21))
    if n_recommendations is None:
        return
    
    # Get and display movies in the selected genre
    genre_movies = recommender.get_movies_by_genre(selected_genre, n_recommendations)
    print_movie_list(genre_movies, f"{selected_genre} Movies")

def view_user_ratings(recommender):
    """
    View ratings for a specific user.
    
    This function shows a user's rating history by:
    1. Displaying available users
    2. Getting user selection
    3. Retrieving and displaying the user's rated movies
    
    Args:
        recommender (MovieRecommendationSystem): The recommendation system instance
    """
    print("\n⭐ USER RATINGS")
    print("-" * 40)
    
    # Display available users
    users = recommender.users_df[['user_id', 'name']].to_dict('records')
    print("Available users:")
    for user in users:
        print(f"{user['user_id']:2d}. {user['name']}")
    
    # Get user selection
    user_id = get_user_input("\nEnter user ID (or 'q' to quit): ", range(1, 21))
    if user_id is None:
        return
    
    # Get and display user's ratings
    user_ratings = recommender.get_user_ratings(user_id)
    print_movie_list(user_ratings, f"Ratings for User {user_id}")

def list_all_movies(recommender):
    """
    List all movies in the database.
    
    This function provides a complete view of the movie database,
    useful for exploration and understanding the available data.
    
    Args:
        recommender (MovieRecommendationSystem): The recommendation system instance
    """
    print("\n📚 ALL MOVIES")
    print("-" * 40)
    
    # Get all movies and display them
    movies = recommender.movies_df.to_dict('records')
    print_movie_list(movies, "All Movies in Database")

def list_all_users(recommender):
    """
    List all users in the database.
    
    This function provides a complete view of the user database,
    showing user details including age and preferred genres.
    
    Args:
        recommender (MovieRecommendationSystem): The recommendation system instance
    """
    print("\n👥 ALL USERS")
    print("-" * 40)
    
    # Get all users and display them in a formatted table
    users = recommender.users_df.to_dict('records')
    print("Users in the system:")
    print("-" * 50)
    for user in users:
        print(f"ID: {user['user_id']:2d} | Name: {user['name']:10s} | Age: {user['age']:2d} | Preferred Genre: {user['preferred_genre']}")
    print()

def main():
    """
    Main application function.
    
    This function:
    1. Initializes the recommendation system
    2. Displays the main menu
    3. Handles user input and navigation
    4. Calls appropriate functions based on user selection
    5. Provides error handling and graceful exit
    
    The application runs in a loop until the user chooses to exit.
    """
    # Display application header
    print_header()
    
    try:
        # Initialize the recommendation system
        print("Loading movie recommendation system...")
        recommender = MovieRecommendationSystem()
        print("✅ System loaded successfully!")
        print()
        
        # Main application loop
        while True:
            # Display menu and get user choice
            print_menu()
            choice = get_user_input("Enter your choice (1-9): ", range(1, 10))
            
            # Handle user quit
            if choice is None:
                break
            
            # Route to appropriate function based on user choice
            if choice == 1:
                get_personalized_recommendations(recommender)
            elif choice == 2:
                get_content_based_recommendations(recommender)
            elif choice == 3:
                get_hybrid_recommendations(recommender)
            elif choice == 4:
                show_popular_movies(recommender)
            elif choice == 5:
                browse_by_genre(recommender)
            elif choice == 6:
                view_user_ratings(recommender)
            elif choice == 7:
                list_all_movies(recommender)
            elif choice == 8:
                list_all_users(recommender)
            elif choice == 9:
                print("\n👋 Thank you for using the Movie Recommendation System!")
                break
            
            # Wait for user to continue before showing menu again
            input("\nPress Enter to continue...")
            print("\n" + "=" * 60)
    
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\n👋 Goodbye!")
    except Exception as e:
        # Handle any unexpected errors
        print(f"\n❌ An error occurred: {e}")
        print("Please check your installation and try again.")

if __name__ == "__main__":
    main() 