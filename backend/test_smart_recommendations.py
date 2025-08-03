#!/usr/bin/env python3
"""
Comprehensive test suite for the smart recommendation system.
Tests all logical scenarios and edge cases.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from recommendation_system import MovieRecommendationSystem
from database_adapter import DatabaseAdapter
import pandas as pd
import numpy as np

class TestSmartRecommendations:
    """Test suite for the smart recommendation system."""
    
    def __init__(self):
        """Initialize the test suite."""
        self.recommender = MovieRecommendationSystem()
        self.db_adapter = DatabaseAdapter()
        
    def test_data_loading(self):
        """Test that data is loaded correctly."""
        print("=== TESTING DATA LOADING ===")
        
        # Test that all dataframes are loaded
        assert self.recommender.movies_df is not None, "Movies dataframe not loaded"
        assert self.recommender.users_df is not None, "Users dataframe not loaded"
        assert self.recommender.ratings_df is not None, "Ratings dataframe not loaded"
        
        # Test that dataframes are not empty
        assert len(self.recommender.movies_df) > 0, "Movies dataframe is empty"
        assert len(self.recommender.users_df) > 0, "Users dataframe is empty"
        assert len(self.recommender.ratings_df) > 0, "Ratings dataframe is empty"
        
        # Test that user-movie matrix is created
        assert self.recommender.user_movie_matrix is not None, "User-movie matrix not created"
        assert self.recommender.user_movie_matrix.shape[0] > 0, "User-movie matrix has no users"
        assert self.recommender.user_movie_matrix.shape[1] > 0, "User-movie matrix has no movies"
        
        print("✅ Data loading tests passed")
        
    def test_user_with_no_ratings(self):
        """Test recommendations for a user with no ratings."""
        print("\n=== TESTING USER WITH NO RATINGS ===")
        
        # Create a test user with no ratings
        test_user_id = 999  # Non-existent user
        
        recommendations = self.recommender.get_collaborative_filtering_recommendations(test_user_id, 5)
        
        # Should return empty list for non-existent user
        assert len(recommendations) == 0, f"Expected empty list for non-existent user, got {len(recommendations)}"
        
        print("✅ User with no ratings test passed")
        
    def test_user_with_ratings_but_no_similar_users(self):
        """Test the fallback mechanism for users with ratings but no similar users."""
        print("\n=== TESTING USER WITH RATINGS BUT NO SIMILAR USERS ===")
        
        # User 3 has ratings but no similar users (as we discovered)
        user_id = 3
        
        recommendations = self.recommender.get_collaborative_filtering_recommendations(user_id, 5)
        
        # Should return recommendations using fallback mechanism
        assert len(recommendations) > 0, f"Expected recommendations using fallback, got {len(recommendations)}"
        
        # Check that recommendations are based on user's rated genres
        user_ratings = self.recommender.ratings_df[self.recommender.ratings_df['user_id'] == user_id]
        user_genres = set()
        for _, rating in user_ratings.iterrows():
            movie_info = self.recommender.movies_df[self.recommender.movies_df['movie_id'] == rating['movie_id']]
            if not movie_info.empty:
                user_genres.add(movie_info.iloc[0]['genre'])
        
        # At least some recommendations should be from genres the user has rated
        recommended_genres = set(rec['genre'] for rec in recommendations)
        genre_overlap = user_genres.intersection(recommended_genres)
        
        print(f"User rated genres: {user_genres}")
        print(f"Recommended genres: {recommended_genres}")
        print(f"Genre overlap: {genre_overlap}")
        
        # Should have some overlap or be from user's preferred genre
        user_info = self.recommender.users_df[self.recommender.users_df['user_id'] == user_id].iloc[0]
        preferred_genre = user_info['preferred_genre']
        
        assert len(genre_overlap) > 0 or preferred_genre in recommended_genres, \
            f"No genre overlap and preferred genre {preferred_genre} not in recommendations"
        
        print("✅ User with ratings but no similar users test passed")
        
    def test_user_with_similar_users(self):
        """Test recommendations for users who have similar users."""
        print("\n=== TESTING USER WITH SIMILAR USERS ===")
        
        # Test with user 1 or 2 who have some overlap
        for user_id in [1, 2]:
            recommendations = self.recommender.get_collaborative_filtering_recommendations(user_id, 5)
            
            # Should return recommendations
            assert len(recommendations) > 0, f"Expected recommendations for user {user_id}, got {len(recommendations)}"
            
            # Check that recommendations have predicted ratings
            for rec in recommendations:
                assert 'predicted_rating' in rec, f"Recommendation missing predicted_rating: {rec}"
                assert 0 <= rec['predicted_rating'] <= 5, f"Predicted rating out of range: {rec['predicted_rating']}"
            
            print(f"✅ User {user_id} recommendations test passed")
        
    def test_content_based_recommendations(self):
        """Test content-based recommendations."""
        print("\n=== TESTING CONTENT-BASED RECOMMENDATIONS ===")
        
        # Test with a movie that exists
        test_movie_id = 1
        recommendations = self.recommender.get_content_based_recommendations(test_movie_id, 5)
        
        # Should return recommendations
        assert len(recommendations) > 0, f"Expected content-based recommendations, got {len(recommendations)}"
        
        # Check that recommendations have similarity scores
        for rec in recommendations:
            assert 'similarity_score' in rec, f"Recommendation missing similarity_score: {rec}"
            assert 0 <= rec['similarity_score'] <= 1, f"Similarity score out of range: {rec['similarity_score']}"
        
        # Check that recommended movies are different from the input movie
        for rec in recommendations:
            assert rec['movie_id'] != test_movie_id, f"Recommended movie is the same as input movie"
        
        print("✅ Content-based recommendations test passed")
        
    def test_hybrid_recommendations(self):
        """Test hybrid recommendations."""
        print("\n=== TESTING HYBRID RECOMMENDATIONS ===")
        
        user_id = 3  # User with ratings
        movie_id = 1  # Reference movie
        
        recommendations = self.recommender.get_hybrid_recommendations(user_id, movie_id, 5)
        
        # Should return recommendations
        assert len(recommendations) > 0, f"Expected hybrid recommendations, got {len(recommendations)}"
        
        # Check that recommendations have hybrid scores
        for rec in recommendations:
            assert 'hybrid_score' in rec, f"Recommendation missing hybrid_score: {rec}"
            assert rec['hybrid_score'] >= 0, f"Hybrid score negative: {rec['hybrid_score']}"
        
        print("✅ Hybrid recommendations test passed")
        
    def test_popular_movies(self):
        """Test popular movies recommendations."""
        print("\n=== TESTING POPULAR MOVIES ===")
        
        recommendations = self.recommender.get_popular_movies(10)
        
        # Should return recommendations
        assert len(recommendations) > 0, f"Expected popular movies, got {len(recommendations)}"
        
        # Check that recommendations have required fields
        for rec in recommendations:
            assert 'avg_rating' in rec, f"Recommendation missing avg_rating: {rec}"
            assert 'rating_count' in rec, f"Recommendation missing rating_count: {rec}"
            assert rec['avg_rating'] >= 0, f"Average rating negative: {rec['avg_rating']}"
            assert rec['rating_count'] > 0, f"Rating count zero: {rec['rating_count']}"
        
        # Check that movies are sorted by average rating (descending)
        ratings = [rec['avg_rating'] for rec in recommendations]
        assert ratings == sorted(ratings, reverse=True), "Popular movies not sorted by rating"
        
        print("✅ Popular movies test passed")
        
    def test_genre_based_recommendations(self):
        """Test genre-based recommendations."""
        print("\n=== TESTING GENRE-BASED RECOMMENDATIONS ===")
        
        test_genre = "Action"
        recommendations = self.recommender.get_movies_by_genre(test_genre, 5)
        
        # Should return recommendations
        assert len(recommendations) > 0, f"Expected {test_genre} movies, got {len(recommendations)}"
        
        # Check that all recommendations are from the specified genre
        for rec in recommendations:
            assert rec['genre'] == test_genre, f"Movie {rec['title']} is not {test_genre}"
        
        # Check that movies are sorted by rating (descending)
        ratings = [rec['rating'] for rec in recommendations]
        assert ratings == sorted(ratings, reverse=True), f"{test_genre} movies not sorted by rating"
        
        print("✅ Genre-based recommendations test passed")
        
    def test_user_ratings_retrieval(self):
        """Test user ratings retrieval."""
        print("\n=== TESTING USER RATINGS RETRIEVAL ===")
        
        user_id = 3
        user_ratings = self.recommender.get_user_ratings(user_id)
        
        # Should return user's ratings
        assert len(user_ratings) > 0, f"Expected user ratings, got {len(user_ratings)}"
        
        # Check that ratings are sorted by rating (descending)
        ratings = [rec['rating'] for rec in user_ratings]
        assert ratings == sorted(ratings, reverse=True), "User ratings not sorted by rating"
        
        # Check that all ratings are for the correct user
        for rec in user_ratings:
            # Verify this movie was actually rated by this user
            user_rating_check = self.recommender.ratings_df[
                (self.recommender.ratings_df['user_id'] == user_id) & 
                (self.recommender.ratings_df['movie_id'] == rec['movie_id'])
            ]
            assert len(user_rating_check) > 0, f"Movie {rec['movie_id']} not rated by user {user_id}"
        
        print("✅ User ratings retrieval test passed")
        
    def test_data_refresh(self):
        """Test that data refresh works correctly."""
        print("\n=== TESTING DATA REFRESH ===")
        
        # Store original data
        original_movies_count = len(self.recommender.movies_df)
        original_users_count = len(self.recommender.users_df)
        original_ratings_count = len(self.recommender.ratings_df)
        
        # Refresh data
        self.recommender.refresh_data()
        
        # Check that data is still loaded
        assert len(self.recommender.movies_df) == original_movies_count, "Movies count changed after refresh"
        assert len(self.recommender.users_df) == original_users_count, "Users count changed after refresh"
        assert len(self.recommender.ratings_df) == original_ratings_count, "Ratings count changed after refresh"
        
        # Check that matrices are still valid
        assert self.recommender.user_movie_matrix is not None, "User-movie matrix lost after refresh"
        assert self.recommender.user_similarity_matrix is not None, "User similarity matrix lost after refresh"
        assert self.recommender.movie_similarity_matrix is not None, "Movie similarity matrix lost after refresh"
        
        print("✅ Data refresh test passed")
        
    def test_edge_cases(self):
        """Test edge cases and error handling."""
        print("\n=== TESTING EDGE CASES ===")
        
        # Test with invalid movie ID
        invalid_movie_id = 99999
        recommendations = self.recommender.get_content_based_recommendations(invalid_movie_id, 5)
        assert len(recommendations) == 0, f"Expected empty list for invalid movie, got {len(recommendations)}"
        
        # Test with invalid user ID
        invalid_user_id = 99999
        recommendations = self.recommender.get_collaborative_filtering_recommendations(invalid_user_id, 5)
        assert len(recommendations) == 0, f"Expected empty list for invalid user, got {len(recommendations)}"
        
        # Test with invalid genre
        invalid_genre = "NonExistentGenre"
        recommendations = self.recommender.get_movies_by_genre(invalid_genre, 5)
        assert len(recommendations) == 0, f"Expected empty list for invalid genre, got {len(recommendations)}"
        
        # Test with zero recommendations requested
        recommendations = self.recommender.get_popular_movies(0)
        assert len(recommendations) == 0, f"Expected empty list for zero count, got {len(recommendations)}"
        
        print("✅ Edge cases test passed")
        
    def test_recommendation_quality(self):
        """Test the quality and logic of recommendations."""
        print("\n=== TESTING RECOMMENDATION QUALITY ===")
        
        # Test that recommendations don't include already rated movies
        user_id = 3
        user_ratings = self.recommender.get_user_ratings(user_id)
        rated_movie_ids = set(rec['movie_id'] for rec in user_ratings)
        
        recommendations = self.recommender.get_collaborative_filtering_recommendations(user_id, 10)
        
        # Check that no recommended movie is already rated
        for rec in recommendations:
            assert rec['movie_id'] not in rated_movie_ids, \
                f"Recommended movie {rec['title']} is already rated by user"
        
        # Test that recommendations have reasonable predicted ratings
        for rec in recommendations:
            assert 0 <= rec['predicted_rating'] <= 5, \
                f"Predicted rating {rec['predicted_rating']} is out of range for {rec['title']}"
        
        # Test that recommendations are diverse (not all same genre)
        recommended_genres = set(rec['genre'] for rec in recommendations)
        assert len(recommended_genres) > 1, f"All recommendations are same genre: {recommended_genres}"
        
        print("✅ Recommendation quality test passed")
        
    def run_all_tests(self):
        """Run all tests and report results."""
        print("🧪 RUNNING SMART RECOMMENDATION SYSTEM TESTS")
        print("=" * 60)
        
        tests = [
            self.test_data_loading,
            self.test_user_with_no_ratings,
            self.test_user_with_ratings_but_no_similar_users,
            self.test_user_with_similar_users,
            self.test_content_based_recommendations,
            self.test_hybrid_recommendations,
            self.test_popular_movies,
            self.test_genre_based_recommendations,
            self.test_user_ratings_retrieval,
            self.test_data_refresh,
            self.test_edge_cases,
            self.test_recommendation_quality
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                test()
                passed += 1
            except Exception as e:
                print(f"❌ {test.__name__} failed: {e}")
                failed += 1
        
        print("\n" + "=" * 60)
        print(f"📊 TEST RESULTS: {passed} passed, {failed} failed")
        
        if failed == 0:
            print("🎉 ALL TESTS PASSED! The smart recommendation system is working correctly.")
        else:
            print(f"⚠️  {failed} test(s) failed. Please review the issues above.")
        
        return passed, failed

def main():
    """Run the test suite."""
    tester = TestSmartRecommendations()
    passed, failed = tester.run_all_tests()
    
    # Exit with appropriate code
    if failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main() 