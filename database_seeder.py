#!/usr/bin/env python3
"""
Database Seeder for Movie Recommendation System

This script populates the PostgreSQL database with initial data including:
- Sample movies with genres and ratings
- Default users with authentication
- Sample ratings for recommendation algorithms
"""

import numpy as np
from database_service import DatabaseService
from database_config import db_config

def seed_database():
    """
    Seed the database with initial data.
    """
    print("🌱 SEEDING DATABASE")
    print("=" * 50)
    
    # Initialize database service
    db_service = DatabaseService()
    
    # Test database connection
    if not db_config.test_connection():
        print("❌ Cannot connect to database. Please check your configuration.")
        return False
    
    # Create tables
    print("Creating database tables...")
    db_config.create_tables()
    
    # Seed movies
    print("\n📽️ Seeding movies...")
    movies_data = [
        # Drama movies
        ("The Shawshank Redemption", "Drama", 1994, 9.3, "Two imprisoned men bond over a number of years...", "Frank Darabont"),
        ("Forrest Gump", "Drama", 1994, 8.8, "The presidencies of Kennedy and Johnson...", "Robert Zemeckis"),
        ("The Green Mile", "Drama", 1999, 8.6, "The lives of guards on Death Row...", "Frank Darabont"),
        ("Good Will Hunting", "Drama", 1997, 8.3, "Will Hunting, a janitor at M.I.T...", "Gus Van Sant"),
        ("The Social Network", "Biography", 2010, 7.7, "As Harvard student Mark Zuckerberg...", "David Fincher"),
        ("La La Land", "Musical", 2016, 8.0, "A jazz pianist falls for an aspiring actress...", "Damien Chazelle"),
        ("Moonlight", "Drama", 2016, 7.4, "A chronicle of the childhood, adolescence...", "Barry Jenkins"),
        ("Parasite", "Thriller", 2019, 8.5, "Greed and class discrimination...", "Bong Joon-ho"),
        
        # Action movies
        ("The Dark Knight", "Action", 2008, 9.0, "When the menace known as the Joker...", "Christopher Nolan"),
        ("Gladiator", "Action", 2000, 8.5, "A former Roman General sets out...", "Ridley Scott"),
        ("The Avengers", "Action", 2012, 8.0, "Earth's mightiest heroes must learn...", "Joss Whedon"),
        ("Iron Man", "Action", 2008, 7.9, "After being held captive in an Afghan cave...", "Jon Favreau"),
        ("Spider-Man", "Action", 2002, 7.4, "When bitten by a genetically modified spider...", "Sam Raimi"),
        ("Batman Begins", "Action", 2005, 8.2, "After training with his mentor...", "Christopher Nolan"),
        ("Mad Max: Fury Road", "Action", 2015, 8.1, "In a post-apocalyptic wasteland...", "George Miller"),
        ("Wonder Woman", "Action", 2017, 7.4, "When a pilot crashes and tells of conflict...", "Patty Jenkins"),
        
        # Sci-Fi movies
        ("Inception", "Sci-Fi", 2010, 8.8, "A thief who steals corporate secrets...", "Christopher Nolan"),
        ("The Matrix", "Sci-Fi", 1999, 8.7, "A computer programmer discovers...", "Lana Wachowski"),
        ("Interstellar", "Sci-Fi", 2014, 8.6, "A team of explorers travel through...", "Christopher Nolan"),
        ("Star Wars", "Sci-Fi", 1977, 8.6, "Luke Skywalker joins forces with...", "George Lucas"),
        ("Back to the Future", "Sci-Fi", 1985, 8.5, "Marty McFly, a 17-year-old high school student...", "Robert Zemeckis"),
        ("E.T.", "Family", 1982, 7.8, "A troubled child summons the courage...", "Steven Spielberg"),
        ("2001: A Space Odyssey", "Sci-Fi", 1968, 8.8, "After discovering a mysterious artifact...", "Stanley Kubrick"),
        ("Her", "Romance", 2013, 8.0, "A lonely writer develops an unlikely relationship...", "Spike Jonze"),
        
        # Crime/Thriller movies
        ("The Godfather", "Crime", 1972, 9.2, "The aging patriarch of an organized crime dynasty...", "Francis Ford Coppola"),
        ("Pulp Fiction", "Crime", 1994, 8.9, "The lives of two mob hitmen...", "Quentin Tarantino"),
        ("Goodfellas", "Crime", 1990, 8.7, "The story of Henry Hill and his life...", "Martin Scorsese"),
        ("The Silence of the Lambs", "Thriller", 1991, 8.6, "A young F.B.I. cadet must receive...", "Jonathan Demme"),
        ("The Departed", "Crime", 2006, 8.5, "An undercover cop and a mole in the police...", "Martin Scorsese"),
        ("Taxi Driver", "Crime", 1976, 8.2, "A mentally unstable Vietnam War veteran...", "Martin Scorsese"),
        ("Raging Bull", "Biography", 1980, 8.2, "The life of boxer Jake LaMotta...", "Martin Scorsese"),
        ("Get Out", "Horror", 2017, 7.7, "A young African-American visits...", "Jordan Peele"),
        
        # Comedy movies
        ("The Grand Budapest Hotel", "Comedy", 2014, 8.1, "A writer encounters the owner of an old hotel...", "Wes Anderson"),
        ("Birdman", "Drama", 2014, 7.7, "A washed-up superhero actor attempts...", "Alejandro González Iñárritu"),
        ("Whiplash", "Drama", 2014, 8.5, "A promising young drummer enrolls...", "Damien Chazelle"),
        
        # Horror movies
        ("The Shining", "Horror", 1980, 8.4, "A family heads to an isolated hotel...", "Stanley Kubrick"),
        ("A Clockwork Orange", "Crime", 1971, 8.3, "In the future, a sadistic gang leader...", "Stanley Kubrick"),
        ("The Exorcist", "Horror", 1973, 8.0, "When a 12-year-old girl is possessed...", "William Friedkin"),
        ("Jaws", "Thriller", 1975, 8.0, "When a killer shark unleashes chaos...", "Steven Spielberg"),
        
        # Adventure/Fantasy movies
        ("The Lord of the Rings", "Fantasy", 2001, 8.9, "A meek Hobbit from the Shire...", "Peter Jackson"),
        ("Harry Potter", "Fantasy", 2001, 7.6, "An orphaned boy enrolls in a school...", "Chris Columbus"),
        ("Indiana Jones", "Adventure", 1981, 8.4, "Archaeology professor Indiana Jones...", "Steven Spielberg"),
        ("The Lion King", "Animation", 1994, 8.5, "Lion prince Simba and his father...", "Roger Allers"),
        ("Titanic", "Romance", 1997, 7.9, "A seventeen-year-old aristocrat...", "James Cameron"),
        ("Avatar", "Sci-Fi", 2009, 7.8, "A paraplegic Marine dispatched...", "James Cameron"),
        ("Jurassic Park", "Adventure", 1993, 8.5, "A pragmatic paleontologist visiting...", "Steven Spielberg"),
        
        # Additional movies
        ("Apocalypse Now", "War", 1979, 8.4, "A U.S. Army officer serving in Vietnam...", "Francis Ford Coppola"),
        ("Black Panther", "Action", 2018, 7.3, "T'Challa, heir to the hidden but advanced...", "Ryan Coogler"),
        ("The Godfather Part II", "Crime", 1974, 9.0, "The early life and career of Vito Corleone...", "Francis Ford Coppola"),
    ]
    
    created_movies = []
    for title, genre, year, rating, description, director in movies_data:
        movie = db_service.create_movie(
            title=title,
            genre=genre,
            year=year,
            rating=rating,
            description=description,
            director=director
        )
        if movie:
            created_movies.append(movie)
            print(f"✅ Created: {title} ({year})")
        else:
            print(f"❌ Failed to create: {title}")
    
    print(f"\n📽️ Created {len(created_movies)} movies")
    
    # Seed users
    print("\n👥 Seeding users...")
    users_data = [
        ("admin", "admin123", "Administrator", "admin@example.com", 30, "Drama", "admin"),
        ("alice", "alice123", "Alice Johnson", "alice@example.com", 25, "Drama", "user"),
        ("bob", "bob123", "Bob Smith", "bob@example.com", 30, "Action", "user"),
        ("charlie", "charlie123", "Charlie Brown", "charlie@example.com", 35, "Sci-Fi", "user"),
        ("diana", "diana123", "Diana Prince", "diana@example.com", 28, "Romance", "user"),
        ("eve", "eve123", "Eve Wilson", "eve@example.com", 22, "Horror", "user"),
        ("frank", "frank123", "Frank Miller", "frank@example.com", 40, "Crime", "user"),
        ("grace", "grace123", "Grace Kelly", "grace@example.com", 27, "Comedy", "user"),
        ("henry", "henry123", "Henry Ford", "henry@example.com", 33, "Action", "user"),
        ("ivy", "ivy123", "Ivy Chen", "ivy@example.com", 29, "Drama", "user"),
    ]
    
    created_users = []
    for username, password, name, email, age, preferred_genre, role in users_data:
        # Check if user already exists
        existing_user = db_service.get_user_by_username(username)
        if existing_user:
            created_users.append(existing_user)
            print(f"✅ Found existing: {name} ({username})")
        else:
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
                created_users.append(user)
                print(f"✅ Created: {name} ({username})")
            else:
                print(f"❌ Failed to create: {name}")
    
    print(f"\n👥 Created {len(created_users)} users")
    
    # Seed ratings
    print("\n⭐ Seeding ratings...")
    np.random.seed(42)  # For reproducible results
    
    rating_count = 0
    for user in created_users:
        # Each user rates 10-20 random movies
        num_ratings = np.random.randint(10, 21)
        rated_movies = np.random.choice(created_movies, num_ratings, replace=False)
        
        for movie in rated_movies:
            # Generate rating based on user's preferred genre
            if user.preferred_genre == movie.genre:
                # Higher ratings for preferred genre
                base_rating = np.random.normal(4.0, 0.8)
            else:
                # Lower ratings for non-preferred genres
                base_rating = np.random.normal(3.0, 1.0)
            
            # Ensure rating is between 1 and 5
            rating = max(1, min(5, round(base_rating)))
            
            # Add some randomness based on movie's overall rating
            if movie.rating and movie.rating > 8.0:
                rating = min(5, rating + np.random.randint(0, 2))
            elif movie.rating and movie.rating < 6.0:
                rating = max(1, rating - np.random.randint(0, 2))
            
            # Check if rating already exists
            existing_rating = db_service.get_rating_by_user_and_movie(user.id, movie.id)
            if existing_rating:
                # Skip if rating already exists
                continue
            
            # Create rating
            db_rating = db_service.create_rating(
                user_id=user.id,
                movie_id=movie.id,
                rating=rating
            )
            
            if db_rating:
                rating_count += 1
    
    print(f"\n⭐ Created {rating_count} ratings")
    
    # Update movie average ratings
    print("\n📊 Updating movie average ratings...")
    for movie in created_movies:
        avg_rating = db_service.get_average_rating(movie.id)
        if avg_rating:
            db_service.update_movie(movie.id, rating=round(avg_rating, 1))
    
    print("\n🎉 Database seeding completed successfully!")
    print(f"📊 Summary:")
    print(f"   - Movies: {len(created_movies)}")
    print(f"   - Users: {len(created_users)}")
    print(f"   - Ratings: {rating_count}")
    
    return True

def clear_database():
    """
    Clear all data from the database (use with caution!).
    """
    print("🗑️ CLEARING DATABASE")
    print("=" * 50)
    
    db_config.drop_tables()
    db_config.create_tables()
    print("✅ Database cleared successfully!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        clear_database()
    else:
        seed_database() 