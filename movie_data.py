import pandas as pd
import numpy as np

def create_dummy_movies():
    """
    Create a dummy dataset of movies with genres and basic information.
    
    This function creates a DataFrame containing 50 popular movies with:
    - movie_id: Unique identifier for each movie
    - title: Movie title
    - genre: Primary genre of the movie
    - year: Release year
    - rating: Overall rating (1-10 scale)
    
    Returns:
        pandas.DataFrame: DataFrame containing movie information
    """
    movies_data = {
        'movie_id': range(1, 51),  # IDs from 1 to 50
        'title': [
            'The Shawshank Redemption', 'The Godfather', 'The Dark Knight', 'Pulp Fiction',
            'Fight Club', 'Inception', 'Forrest Gump', 'The Matrix', 'Goodfellas', 'The Silence of the Lambs',
            'Interstellar', 'The Departed', 'The Green Mile', 'Gladiator', 'The Lion King',
            'Titanic', 'Avatar', 'Jurassic Park', 'The Avengers', 'Iron Man',
            'Spider-Man', 'Batman Begins', 'The Lord of the Rings', 'Harry Potter', 'Star Wars',
            'Indiana Jones', 'Back to the Future', 'E.T.', 'Jaws', 'The Exorcist',
            'The Shining', 'A Clockwork Orange', '2001: A Space Odyssey', 'The Godfather Part II', 'Apocalypse Now',
            'Taxi Driver', 'Raging Bull', 'Good Will Hunting', 'The Social Network', 'La La Land',
            'Moonlight', 'Parasite', 'Get Out', 'Black Panther', 'Wonder Woman',
            'Mad Max: Fury Road', 'The Grand Budapest Hotel', 'Birdman', 'Whiplash', 'Her'
        ],
        'genre': [
            'Drama', 'Crime', 'Action', 'Crime', 'Drama', 'Sci-Fi', 'Drama', 'Sci-Fi', 'Crime', 'Thriller',
            'Sci-Fi', 'Crime', 'Drama', 'Action', 'Animation', 'Romance', 'Sci-Fi', 'Adventure', 'Action', 'Action',
            'Action', 'Action', 'Fantasy', 'Fantasy', 'Sci-Fi', 'Adventure', 'Sci-Fi', 'Family', 'Thriller', 'Horror',
            'Horror', 'Crime', 'Sci-Fi', 'Crime', 'War', 'Crime', 'Biography', 'Drama', 'Biography', 'Musical',
            'Drama', 'Thriller', 'Horror', 'Action', 'Action', 'Action', 'Comedy', 'Drama', 'Drama', 'Romance'
        ],
        'year': [
            1994, 1972, 2008, 1994, 1999, 2010, 1994, 1999, 1990, 1991,
            2014, 2006, 1999, 2000, 1994, 1997, 2009, 1993, 2012, 2008,
            2002, 2005, 2001, 2001, 1977, 1981, 1985, 1982, 1975, 1973,
            1980, 1971, 1968, 1974, 1979, 1976, 1980, 1997, 2010, 2016,
            2016, 2019, 2017, 2018, 2017, 2015, 2014, 2014, 2014, 2013
        ],
        'rating': [
            9.3, 9.2, 9.0, 8.9, 8.8, 8.8, 8.8, 8.7, 8.7, 8.6,
            8.6, 8.5, 8.6, 8.5, 8.5, 7.9, 7.8, 8.5, 8.0, 7.9,
            7.4, 8.2, 8.9, 7.6, 8.6, 8.4, 8.5, 7.8, 8.0, 8.0,
            8.4, 8.3, 8.8, 9.0, 8.4, 8.2, 8.2, 8.3, 7.7, 8.0,
            7.4, 8.5, 7.7, 7.3, 7.4, 8.1, 8.1, 7.7, 8.5, 8.0
        ]
    }
    return pd.DataFrame(movies_data)

def create_dummy_users():
    """
    Create a dummy dataset of users with preferences.
    
    This function creates a DataFrame containing 20 users with:
    - user_id: Unique identifier for each user
    - name: User's name
    - age: User's age
    - preferred_genre: User's favorite movie genre
    
    Returns:
        pandas.DataFrame: DataFrame containing user information
    """
    users_data = {
        'user_id': range(1, 21),  # IDs from 1 to 20
        'name': [
            'Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack',
            'Kate', 'Liam', 'Mia', 'Noah', 'Olivia', 'Paul', 'Quinn', 'Ruby', 'Sam', 'Tina'
        ],
        'age': [
            25, 30, 35, 28, 22, 40, 27, 33, 29, 31,
            26, 24, 32, 38, 23, 36, 34, 28, 30, 27
        ],
        'preferred_genre': [
            'Drama', 'Action', 'Sci-Fi', 'Romance', 'Horror', 'Crime', 'Comedy', 'Action', 'Drama', 'Sci-Fi',
            'Romance', 'Action', 'Fantasy', 'War', 'Animation', 'Thriller', 'Comedy', 'Drama', 'Action', 'Romance'
        ]
    }
    return pd.DataFrame(users_data)

def create_dummy_ratings():
    """
    Create a dummy dataset of user ratings for movies.
    
    This function generates realistic user ratings by:
    1. Having each user rate 10-20 random movies
    2. Using a normal distribution centered around 3.5 for realistic ratings
    3. Ensuring ratings are between 1 and 5
    
    Returns:
        pandas.DataFrame: DataFrame containing user ratings with columns:
            - user_id: ID of the user who gave the rating
            - movie_id: ID of the movie being rated
            - rating: Rating value (1-5 scale)
    """
    np.random.seed(42)  # For reproducible results - same ratings every time
    
    ratings_data = []
    users = range(1, 21)  # All 20 users
    movies = range(1, 51)  # All 50 movies
    
    # Generate random ratings for each user
    for user_id in users:
        # Each user rates 10-20 random movies (realistic variation)
        num_ratings = np.random.randint(10, 21)
        rated_movies = np.random.choice(movies, num_ratings, replace=False)
        
        for movie_id in rated_movies:
            # Generate rating based on normal distribution (more realistic than uniform)
            # Mean of 3.5, standard deviation of 1.0
            base_rating = np.random.normal(3.5, 1.0)
            # Ensure rating is between 1 and 5, and round to nearest integer
            rating = max(1, min(5, round(base_rating)))
            ratings_data.append({
                'user_id': user_id,
                'movie_id': movie_id,
                'rating': rating
            })
    
    return pd.DataFrame(ratings_data)

def load_all_data():
    """
    Load all dummy datasets for the recommendation system.
    
    This function creates and returns all three datasets needed for the
    movie recommendation system: movies, users, and ratings.
    
    Returns:
        tuple: (movies_df, users_df, ratings_df) - Three pandas DataFrames
    """
    movies_df = create_dummy_movies()
    users_df = create_dummy_users()
    ratings_df = create_dummy_ratings()
    
    return movies_df, users_df, ratings_df

if __name__ == "__main__":
    # Test the data creation functions
    movies, users, ratings = load_all_data()
    
    print("Movies dataset:")
    print(movies.head())
    print(f"\nTotal movies: {len(movies)}")
    
    print("\nUsers dataset:")
    print(users.head())
    print(f"\nTotal users: {len(users)}")
    
    print("\nRatings dataset:")
    print(ratings.head())
    print(f"\nTotal ratings: {len(ratings)}") 