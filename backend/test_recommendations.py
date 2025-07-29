#!/usr/bin/env python3
"""
Test script to verify that the recommendation system is working with new fields.
"""

from recommendation_system import MovieRecommendationSystem

def test_recommendations():
    """Test that recommendations include all required fields."""
    print("🧪 TESTING RECOMMENDATION SYSTEM")
    print("=" * 50)
    
    try:
        # Initialize recommendation system
        recommender = MovieRecommendationSystem()
        
        print("✅ Recommendation system initialized successfully")
        
        # Test collaborative filtering recommendations
        print("\n📊 Testing collaborative filtering recommendations...")
        cf_recommendations = recommender.get_collaborative_filtering_recommendations(1, 3)
        
        if cf_recommendations:
            print(f"✅ Got {len(cf_recommendations)} collaborative filtering recommendations")
            
            # Check if all required fields are present
            sample_rec = cf_recommendations[0]
            required_fields = ['movie_id', 'title', 'genre', 'year', 'description', 'poster_url', 'trailer_url']
            
            missing_fields = []
            for field in required_fields:
                if field not in sample_rec:
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"❌ Missing fields: {missing_fields}")
            else:
                print("✅ All required fields are present")
                print(f"Sample movie: {sample_rec['title']} ({sample_rec['year']})")
                print(f"Description: {sample_rec['description'][:50]}...")
                print(f"Poster URL: {'✅' if sample_rec['poster_url'] else '❌'}")
                print(f"Trailer URL: {'✅' if sample_rec['trailer_url'] else '❌'}")
        else:
            print("❌ No collaborative filtering recommendations returned")
        
        # Test content-based recommendations
        print("\n🎭 Testing content-based recommendations...")
        cb_recommendations = recommender.get_content_based_recommendations(1, 3)
        
        if cb_recommendations:
            print(f"✅ Got {len(cb_recommendations)} content-based recommendations")
            
            # Check if all required fields are present
            sample_rec = cb_recommendations[0]
            required_fields = ['movie_id', 'title', 'genre', 'year', 'description', 'poster_url', 'trailer_url']
            
            missing_fields = []
            for field in required_fields:
                if field not in sample_rec:
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"❌ Missing fields: {missing_fields}")
            else:
                print("✅ All required fields are present")
        else:
            print("❌ No content-based recommendations returned")
        
        print("\n🎉 Recommendation system test completed!")
        
    except Exception as e:
        print(f"❌ Error testing recommendation system: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_recommendations() 