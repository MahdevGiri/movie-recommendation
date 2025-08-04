import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from database_adapter import DatabaseAdapter

class MovieRecommendationSystem:
    """
    A comprehensive movie recommendation system that implements multiple recommendation algorithms.
    
    This class provides:
    - Collaborative filtering (user-based)
    - Content-based filtering (movie similarity)
    - Hybrid recommendations (combining both approaches)
    - Popular movies ranking
    - Genre-based filtering
    - User rating history
    
    The system uses cosine similarity for finding similar users and movies,
    and creates user-movie rating matrices for collaborative filtering.
    """
    
    def __init__(self):
        """
        Initialize the recommendation system with data and prepare similarity matrices.
        
        Loads all datasets from PostgreSQL database and creates:
        - User-movie rating matrix for collaborative filtering
        - Movie similarity matrix for content-based filtering
        - User similarity matrix for finding similar users
        """
        # Initialize database adapter
        self.db_adapter = DatabaseAdapter()
        
        # Load all datasets from database
        self.movies_df = self.db_adapter.get_movies_df()
        self.users_df = self.db_adapter.get_users_df()
        self.ratings_df = self.db_adapter.get_ratings_df()
        
        # Initialize similarity matrices (will be created in _prepare_data)
        self.user_movie_matrix = None      # Users x Movies matrix with ratings
        self.movie_similarity_matrix = None # Movies x Movies similarity matrix
        self.user_similarity_matrix = None  # Users x Users similarity matrix
        
        # Prepare data structures for recommendations
        self._prepare_data()
    
    def _prepare_data(self):
        """
        Prepare data structures for recommendation algorithms.
        
        This method:
        1. Creates a user-movie rating matrix (pivot table)
        2. Creates movie similarity matrix using content-based features
        3. Creates user similarity matrix using rating patterns
        """
        print(f"🔧 Preparing recommendation data...")
        print(f"🔧 Movies loaded: {len(self.movies_df)}")
        print(f"🔧 Users loaded: {len(self.users_df)}")
        print(f"🔧 Ratings loaded: {len(self.ratings_df)}")
        
        # Create user-movie rating matrix (pivot table)
        # Rows: users, Columns: movies, Values: ratings
        # Fill NaN values with 0 (unrated movies)
        self.user_movie_matrix = self.ratings_df.pivot(
            index='user_id', 
            columns='movie_id', 
            values='rating'
        ).fillna(0)
        
        print(f"🔧 User-movie matrix created: {self.user_movie_matrix.shape}")
        
        # Create similarity matrices for different recommendation approaches
        print(f"🔧 Creating movie similarity matrix...")
        self._create_movie_similarity_matrix()  # For content-based filtering
        print(f"🔧 Creating user similarity matrix...")
        self._create_user_similarity_matrix()   # For collaborative filtering
        print(f"🔧 Data preparation complete!")
    
    def refresh_data(self):
        """
        Refresh all data from the database.
        
        This method reloads all datasets from the database and recreates
        the similarity matrices. Use this after adding/updating ratings
        to ensure the recommendation system has the latest data.
        """
        # Reload all datasets from database
        self.movies_df = self.db_adapter.get_movies_df()
        self.users_df = self.db_adapter.get_users_df()
        self.ratings_df = self.db_adapter.get_ratings_df()
        
        # Recreate similarity matrices with updated data
        self._prepare_data()
    
    def _create_movie_similarity_matrix(self):
        """
        Create movie similarity matrix based on content features (genres and ratings).
        
        This method:
        1. Creates dummy variables for movie genres
        2. Combines genre features with movie ratings
        3. Calculates cosine similarity between all movie pairs
        
        The resulting matrix can be used to find movies similar to a given movie.
        """
        # Create feature matrix for movies (genre-based)
        movie_features = self.movies_df.copy()
        
        # Handle NaN values in rating field - replace with 0 or mean rating
        if movie_features['rating'].isna().any():
            print(f"🔧 Found {movie_features['rating'].isna().sum()} movies with NaN ratings")
            # Replace NaN ratings with 0 (neutral rating)
            movie_features['rating'] = movie_features['rating'].fillna(0)
        
        # Create genre dummy variables (one-hot encoding)
        # This converts categorical genre into numerical features
        genre_dummies = pd.get_dummies(movie_features['genre'], prefix='genre')
        movie_features = pd.concat([movie_features, genre_dummies], axis=1)
        
        # Select feature columns for similarity calculation
        # Include genre dummy variables and overall rating as features
        feature_cols = [col for col in movie_features.columns if col.startswith('genre_')]
        feature_cols.append('rating')  # Include overall rating as a feature
        
        print(f"🔧 Feature columns: {feature_cols}")
        print(f"🔧 Feature data types: {movie_features[feature_cols].dtypes}")
        
        # Calculate cosine similarity between all movie pairs
        movie_features_matrix = movie_features[feature_cols].values
        
        # Ensure the matrix is numeric and handle any non-numeric data
        try:
            # Convert to numeric, coercing errors to NaN
            movie_features_matrix = pd.DataFrame(movie_features_matrix, columns=feature_cols).astype(float).values
        except (ValueError, TypeError) as e:
            print(f"🔧 Error converting movie features to numeric: {e}")
            # Fallback: convert to numeric with errors='coerce' and fill NaN with 0
            movie_features_matrix = pd.DataFrame(movie_features_matrix, columns=feature_cols).apply(pd.to_numeric, errors='coerce').fillna(0).values
        
        # Additional check for any remaining NaN values
        if np.isnan(movie_features_matrix).any():
            print(f"🔧 Found NaN values in movie features matrix, replacing with 0")
            movie_features_matrix = np.nan_to_num(movie_features_matrix, nan=0.0)
        
        self.movie_similarity_matrix = cosine_similarity(movie_features_matrix)
    
    def _create_user_similarity_matrix(self):
        """
        Create user similarity matrix based on rating patterns.
        
        This method calculates cosine similarity between users based on how they
        rated the same movies. Users with similar rating patterns will have
        high similarity scores.
        """
        # Check for any NaN values in user-movie matrix
        if np.isnan(self.user_movie_matrix.values).any():
            print(f"🔧 Found NaN values in user-movie matrix, replacing with 0")
            self.user_movie_matrix = self.user_movie_matrix.fillna(0)
        
        # Calculate cosine similarity between users based on their rating patterns
        # This creates a matrix where each cell represents similarity between two users
        self.user_similarity_matrix = cosine_similarity(self.user_movie_matrix)
        print(f"🔧 User similarity matrix created: {self.user_similarity_matrix.shape}")
    
    def get_content_based_recommendations(self, movie_id, n_recommendations=5):
        """
        Get content-based recommendations based on movie similarity.
        
        This method finds movies similar to a given movie based on:
        - Genre similarity
        - Overall rating similarity
        
        Args:
            movie_id (int): ID of the reference movie
            n_recommendations (int): Number of recommendations to return
            
        Returns:
            list: List of dictionaries containing recommended movies with similarity scores
        """
        # Check if movie exists in our dataset
        if movie_id not in self.movies_df['movie_id'].values:
            return []
        
        # Find the index of the movie in our similarity matrix
        movie_idx = self.movies_df[self.movies_df['movie_id'] == movie_id].index[0]
        
        # Get similarity scores for this movie with all other movies
        movie_similarities = self.movie_similarity_matrix[movie_idx]
        
        # Get indices of most similar movies (excluding the movie itself)
        # Sort by similarity score in descending order, skip first (self-similarity)
        similar_indices = np.argsort(movie_similarities)[::-1][1:n_recommendations+1]
        
        # Get recommended movies with their details
        recommended_movies = []
        for idx in similar_indices:
            movie = self.movies_df.iloc[idx]
            similarity_score = movie_similarities[idx]
            recommended_movies.append({
                'movie_id': int(movie['movie_id']),
                'title': str(movie['title']),
                'genre': str(movie['genre']),
                'year': int(movie['year']),
                'description': str(movie['description']) if pd.notna(movie['description']) else None,
                'poster_url': str(movie['poster_url']) if pd.notna(movie['poster_url']) else None,
                'trailer_url': str(movie['trailer_url']) if pd.notna(movie['trailer_url']) else None,
                'similarity_score': float(round(similarity_score, 3))
            })
        
        return recommended_movies
    
    def get_collaborative_filtering_recommendations(self, user_id, n_recommendations=5):
        """
        Get collaborative filtering recommendations based on similar users.
        
        This method:
        1. Finds users similar to the target user
        2. Identifies movies rated highly by similar users
        3. Predicts ratings for unrated movies
        4. Gives preference to user's preferred genre
        5. Returns top recommendations
        
        Args:
            user_id (int): ID of the target user
            n_recommendations (int): Number of recommendations to return
            
        Returns:
            list: List of dictionaries containing recommended movies with predicted ratings
        """
        # Check if user exists in our dataset
        if user_id not in self.users_df['user_id'].values:
            return []
        
        # Get user's preferred genre
        user_info = self.users_df[self.users_df['user_id'] == user_id].iloc[0]
        preferred_genre = user_info['preferred_genre']
        
        # Check if user has any ratings (exists in user_movie_matrix)
        if user_id not in self.user_movie_matrix.index:
            # User has no ratings, return popular movies based on their preferred genre
            # Get popular movies in their preferred genre
            genre_movies = self.movies_df[self.movies_df['genre'] == preferred_genre]
            
            if len(genre_movies) == 0:
                # If no movies in preferred genre, get general popular movies
                genre_movies = self.movies_df
            
            # Sort by rating and return top recommendations
            top_movies = genre_movies.nlargest(n_recommendations, 'rating')
            
            recommended_movies = []
            for _, movie in top_movies.iterrows():
                            recommended_movies.append({
                'movie_id': int(movie['movie_id']),
                'title': str(movie['title']),
                'genre': str(movie['genre']),
                'year': int(movie['year']),
                'description': str(movie['description']) if pd.notna(movie['description']) else None,
                'poster_url': str(movie['poster_url']) if pd.notna(movie['poster_url']) else None,
                'trailer_url': str(movie['trailer_url']) if pd.notna(movie['trailer_url']) else None,
                'predicted_rating': float(round(min(movie['rating'], 5.0), 1))
            })
            
            return recommended_movies
        
        # Find the index of the user in our similarity matrix
        user_idx = self.user_movie_matrix.index.get_loc(user_id)
        
        # Get similarity scores for this user with all other users
        user_similarities = self.user_similarity_matrix[user_idx]
        
        # Get indices of most similar users (top 5 similar users)
        similar_user_indices = np.argsort(user_similarities)[::-1][1:6]
        
        # Get movies rated by similar users but not by the target user
        target_user_ratings = self.user_movie_matrix.iloc[user_idx]
        unrated_movies = target_user_ratings[target_user_ratings == 0].index
        
        # Calculate predicted ratings for unrated movies
        movie_scores = {}
        for movie_id in unrated_movies:
            score = 0
            total_similarity = 0
            
            # For each similar user, calculate weighted rating contribution
            for similar_user_idx in similar_user_indices:
                similar_user_id = self.user_movie_matrix.index[similar_user_idx]
                similarity = user_similarities[similar_user_idx]
                
                # Get rating from similar user for this movie
                rating = self.user_movie_matrix.loc[similar_user_id, movie_id]
                
                # Only consider positive ratings (users who actually rated the movie)
                if rating > 0:
                    score += similarity * rating  # Weighted contribution
                    total_similarity += similarity
            
            # Calculate predicted rating as weighted average
            if total_similarity > 0:
                predicted_rating = score / total_similarity
                
                # Apply genre preference boost
                movie_info = self.movies_df[self.movies_df['movie_id'] == movie_id].iloc[0]
                movie_genre = movie_info['genre']
                
                # Boost rating for movies in user's preferred genre
                if movie_genre == preferred_genre:
                    predicted_rating *= 1.3  # 30% boost for preferred genre
                
                # Cap the predicted rating at 5.0 to keep it within valid range
                predicted_rating = min(predicted_rating, 5.0)
                
                movie_scores[movie_id] = predicted_rating
        
        # If no collaborative filtering predictions were made (no similar users),
        # fall back to content-based recommendations based on user's rated movies
        if not movie_scores:
            # Get user's rated movies and their genres
            user_rated_movies = target_user_ratings[target_user_ratings > 0]
            user_genres = {}
            
            for movie_id, rating in user_rated_movies.items():
                movie_info = self.movies_df[self.movies_df['movie_id'] == movie_id].iloc[0]
                genre = movie_info['genre']
                if genre not in user_genres:
                    user_genres[genre] = []
                user_genres[genre].append(rating)
            
            # Calculate average rating per genre
            genre_avg_ratings = {}
            for genre, ratings in user_genres.items():
                genre_avg_ratings[genre] = sum(ratings) / len(ratings)
            
            # Sort genres by average rating (highest first)
            sorted_genres = sorted(genre_avg_ratings.items(), key=lambda x: x[1], reverse=True)
            
            # Get movies in user's preferred genres, excluding already rated movies
            for genre, avg_rating in sorted_genres:
                genre_movies = self.movies_df[
                    (self.movies_df['genre'] == genre) & 
                    (~self.movies_df['movie_id'].isin(user_rated_movies.index))
                ]
                
                if len(genre_movies) > 0:
                    # Sort by overall rating and take top movies
                    top_genre_movies = genre_movies.nlargest(n_recommendations, 'rating')
                    
                    for _, movie in top_genre_movies.iterrows():
                        movie_id = movie['movie_id']
                        # Use the average rating for this genre as predicted rating
                        predicted_rating = min(avg_rating, 5.0)
                        movie_scores[movie_id] = predicted_rating
                    
                    # If we have enough recommendations, break
                    if len(movie_scores) >= n_recommendations:
                        break
            
            # If still no recommendations, fall back to popular movies in preferred genre
            if not movie_scores:
                genre_movies = self.movies_df[self.movies_df['genre'] == preferred_genre]
                if len(genre_movies) > 0:
                    top_movies = genre_movies.nlargest(n_recommendations, 'rating')
                    for _, movie in top_movies.iterrows():
                        movie_id = movie['movie_id']
                        if movie_id not in user_rated_movies.index:  # Don't recommend already rated movies
                            movie_scores[movie_id] = min(movie['rating'], 5.0)
        
        # Sort movies by predicted rating (highest first)
        sorted_movies = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Get top recommendations with movie details
        recommended_movies = []
        for movie_id, predicted_rating in sorted_movies[:n_recommendations]:
            movie = self.movies_df[self.movies_df['movie_id'] == movie_id].iloc[0]
            recommended_movies.append({
                'movie_id': int(movie['movie_id']),
                'title': str(movie['title']),
                'genre': str(movie['genre']),
                'year': int(movie['year']),
                'description': str(movie['description']) if pd.notna(movie['description']) else None,
                'poster_url': str(movie['poster_url']) if pd.notna(movie['poster_url']) else None,
                'trailer_url': str(movie['trailer_url']) if pd.notna(movie['trailer_url']) else None,
                'predicted_rating': float(round(predicted_rating, 2))
            })
        
        return recommended_movies
    
    def get_hybrid_recommendations(self, user_id, movie_id=None, n_recommendations=5):
        """
        Get hybrid recommendations combining content-based and collaborative filtering.
        
        This method combines both approaches:
        - 70% weight to collaborative filtering (user preferences)
        - 30% weight to content-based filtering (movie similarity)
        
        Args:
            user_id (int): ID of the target user
            movie_id (int, optional): Reference movie for content-based filtering
            n_recommendations (int): Number of recommendations to return
            
        Returns:
            list: List of dictionaries containing recommended movies with hybrid scores
        """
        recommendations = []
        
        # Get collaborative filtering recommendations (always used)
        cf_recommendations = self.get_collaborative_filtering_recommendations(user_id, n_recommendations)
        
        # If a specific movie is provided, get content-based recommendations too
        if movie_id:
            cb_recommendations = self.get_content_based_recommendations(movie_id, n_recommendations)
            
            # Combine and rank recommendations from both approaches
            all_recommendations = {}
            
            # Add collaborative filtering recommendations
            for rec in cf_recommendations:
                movie_id = rec['movie_id']
                all_recommendations[movie_id] = {
                    'movie_id': movie_id,
                    'title': rec['title'],
                    'genre': rec['genre'],
                    'year': rec['year'],
                    'description': rec.get('description'),
                    'poster_url': rec.get('poster_url'),
                    'trailer_url': rec.get('trailer_url'),
                    'cf_score': rec['predicted_rating'],
                    'cb_score': 0,
                    'hybrid_score': rec['predicted_rating']  # Start with CF score
                }
            
            # Add content-based recommendations
            for rec in cb_recommendations:
                movie_id = rec['movie_id']
                if movie_id in all_recommendations:
                    # Movie appears in both approaches - combine scores
                    all_recommendations[movie_id]['cb_score'] = rec['similarity_score']
                    all_recommendations[movie_id]['hybrid_score'] = (
                        all_recommendations[movie_id]['cf_score'] * 0.7 +  # 70% CF weight
                        rec['similarity_score'] * 0.3                     # 30% CB weight
                    )
                else:
                    # Movie only appears in content-based - add with CB weight only
                    all_recommendations[movie_id] = {
                        'movie_id': movie_id,
                        'title': rec['title'],
                        'genre': rec['genre'],
                        'year': rec['year'],
                        'description': rec.get('description'),
                        'poster_url': rec.get('poster_url'),
                        'trailer_url': rec.get('trailer_url'),
                        'cf_score': 0,
                        'cb_score': rec['similarity_score'],
                        'hybrid_score': rec['similarity_score'] * 0.3  # Only CB contribution
                    }
            
            # Sort by hybrid score (highest first)
            sorted_recommendations = sorted(
                all_recommendations.values(), 
                key=lambda x: x['hybrid_score'], 
                reverse=True
            )
            
            recommendations = sorted_recommendations[:n_recommendations]
        else:
            # No reference movie provided - just use collaborative filtering
            recommendations = cf_recommendations
        
        return recommendations
    
    def get_popular_movies(self, n_recommendations=10):
        """
        Get popular movies based on average rating and number of ratings.
        
        This method calculates popularity using:
        - Average rating across all users
        - Number of ratings (more ratings = more reliable average)
        - Filters out movies with too few ratings
        
        Args:
            n_recommendations (int): Number of popular movies to return
            
        Returns:
            list: List of dictionaries containing popular movies with stats
        """
        # Calculate average rating and count for each movie
        movie_stats = self.ratings_df.groupby('movie_id').agg({
            'rating': ['mean', 'count']  # Average rating and number of ratings
        }).reset_index()
        
        # Flatten column names
        movie_stats.columns = ['movie_id', 'avg_rating', 'rating_count']
        
        # Filter movies with at least 3 ratings (more reliable averages)
        movie_stats = movie_stats[movie_stats['rating_count'] >= 3]
        
        # Sort by average rating (descending)
        movie_stats = movie_stats.sort_values('avg_rating', ascending=False)
        
        # Get top movies with their details
        popular_movies = []
        for _, row in movie_stats.head(n_recommendations).iterrows():
            movie = self.movies_df[self.movies_df['movie_id'] == row['movie_id']].iloc[0]
            popular_movies.append({
                'movie_id': int(movie['movie_id']),
                'title': str(movie['title']),
                'genre': str(movie['genre']),
                'year': int(movie['year']),
                'description': str(movie['description']) if pd.notna(movie['description']) else None,
                'poster_url': str(movie['poster_url']) if pd.notna(movie['poster_url']) else None,
                'trailer_url': str(movie['trailer_url']) if pd.notna(movie['trailer_url']) else None,
                'avg_rating': float(round(row['avg_rating'], 2)),
                'rating_count': int(row['rating_count'])
            })
        
        return popular_movies
    
    def get_movies_by_genre(self, genre, n_recommendations=10):
        """
        Get movies by specific genre, sorted by rating.
        
        Args:
            genre (str): Genre to filter by (e.g., 'Action', 'Drama', 'Sci-Fi')
            n_recommendations (int): Number of movies to return
            
        Returns:
            list: List of dictionaries containing movies in the specified genre
        """
        # Filter movies by the specified genre
        genre_movies = self.movies_df[self.movies_df['genre'] == genre].copy()
        
        if len(genre_movies) == 0:
            return []
        
        # Sort by rating (descending)
        genre_movies = genre_movies.sort_values('rating', ascending=False)
        
        # Get top movies in the genre
        recommended_movies = []
        for _, movie in genre_movies.head(n_recommendations).iterrows():
            recommended_movies.append({
                'movie_id': int(movie['movie_id']),
                'title': str(movie['title']),
                'genre': str(movie['genre']),
                'year': int(movie['year']),
                'description': str(movie['description']) if pd.notna(movie['description']) else None,
                'poster_url': str(movie['poster_url']) if pd.notna(movie['poster_url']) else None,
                'trailer_url': str(movie['trailer_url']) if pd.notna(movie['trailer_url']) else None,
                'rating': float(min(movie['rating'], 5.0))
            })
        
        return recommended_movies
    
    def get_user_ratings(self, user_id):
        """
        Get all ratings for a specific user.
        
        This method retrieves all movies rated by a user, along with movie details.
        The ratings are sorted by rating value (highest first).
        
        Args:
            user_id (int): ID of the user
            
        Returns:
            list: List of dictionaries containing user's rated movies with ratings
        """
        # Check if user exists in our dataset
        if user_id not in self.users_df['user_id'].values:
            return []
        
        # Get all ratings for this user
        user_ratings = self.ratings_df[self.ratings_df['user_id'] == user_id].copy()
        
        # Merge with movie information to get movie details
        user_ratings = user_ratings.merge(self.movies_df, on='movie_id')
        
        # Sort by rating (descending) - highest rated movies first
        user_ratings = user_ratings.sort_values('rating_x', ascending=False)
        
        # Rename 'rating_x' to 'rating' for output (rating_x is user's rating after merge)
        user_ratings = user_ratings.rename(columns={'rating_x': 'rating'})
        
        # Return selected columns as list of dictionaries
        return user_ratings[['movie_id', 'title', 'genre', 'year', 'rating']].to_dict('records') 