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
        ("The Shawshank Redemption", "Drama", 1994, 9.3, "Two imprisoned men bond over a number of years...", "Frank Darabont", 
         "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_.jpg",
         "https://www.youtube.com/watch?v=6hB3S9bIaco"),
        ("Forrest Gump", "Drama", 1994, 8.8, "The presidencies of Kennedy and Johnson...", "Robert Zemeckis",
         "https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg",
         "https://www.youtube.com/watch?v=bLvqoHBptjg"),
        ("The Green Mile", "Drama", 1999, 8.6, "The lives of guards on Death Row...", "Frank Darabont",
         "https://m.media-amazon.com/images/M/MV5BMTUxMzQyNjA5Nl5BMl5BanBnXkFtZTYwOTU2NTY3._V1_.jpg",
         "https://www.youtube.com/watch?v=Ki4haFrqSrw"),
        ("Good Will Hunting", "Drama", 1997, 8.3, "Will Hunting, a janitor at M.I.T...", "Gus Van Sant",
         "https://m.media-amazon.com/images/M/MV5BOTI0MzcxMTYtZDVkMy00NjY1LTgyMTYtZmUxN2M3NmQ2NWJhXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg",
         "https://www.youtube.com/watch?v=PaZVjZEFkRs"),
        ("The Social Network", "Biography", 2010, 7.7, "As Harvard student Mark Zuckerberg...", "David Fincher",
         "https://m.media-amazon.com/images/M/MV5BOGUyZWExNGYtYjFiYy00MzEzLTllNjYtYTFhMjI0YjM5MjFjXkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_.jpg",
         "https://www.youtube.com/watch?v=lB95KLmpLR4"),
        ("La La Land", "Musical", 2016, 8.0, "A jazz pianist falls for an aspiring actress...", "Damien Chazelle",
         "https://m.media-amazon.com/images/M/MV5BMzUzNDM2NzM2MV5BMl5BanBnXkFtZTgwNTM3NTg4OTE@._V1_.jpg",
         "https://www.youtube.com/watch?v=0pdqf4P9MB8"),
        ("Moonlight", "Drama", 2016, 7.4, "A chronicle of the childhood, adolescence...", "Barry Jenkins",
         "https://m.media-amazon.com/images/M/MV5BNzQxNTIyODAxMV5BMl5BanBnXkFtZTgwNzQyMDA3OTE@._V1_.jpg",
         "https://www.youtube.com/watch?v=9NJj12tJzqc"),
        ("Parasite", "Thriller", 2019, 8.5, "Greed and class discrimination...", "Bong Joon-ho",
         "https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_.jpg",
         "https://www.youtube.com/watch?v=5xH0HfJHsaY"),
        
        # Action movies
        ("The Dark Knight", "Action", 2008, 9.0, "When the menace known as the Joker...", "Christopher Nolan",
         "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_.jpg",
         "https://www.youtube.com/watch?v=EXeTwQWrcwY"),
        ("Gladiator", "Action", 2000, 8.5, "A former Roman General sets out...", "Ridley Scott",
         "https://m.media-amazon.com/images/M/MV5BMDliMmNhNDEtODUyOS00MjNkLTgxODEtN2U3NzIxMGVkZTA1L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg",
         "https://www.youtube.com/watch?v=owK1qxDselE"),
        ("The Avengers", "Action", 2012, 8.0, "Earth's mightiest heroes must learn...", "Joss Whedon",
         "https://m.media-amazon.com/images/M/MV5BNDYxNjQyMjAtNTdiOS00NGYwLWFmNTAtN2IxYWIxZTY1ZTMyXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg",
         "https://www.youtube.com/watch?v=eOrNdBpGMv8"),
        ("Iron Man", "Action", 2008, 7.9, "After being held captive in an Afghan cave...", "Jon Favreau",
         "https://m.media-amazon.com/images/M/MV5BMTczNTI2ODUwOF5BMl5BanBnXkFtZTcwMTU0NTIzMw@@._V1_.jpg",
         "https://www.youtube.com/watch?v=8ugaeA-nMTc"),
        ("Spider-Man", "Action", 2002, 7.4, "When bitten by a genetically modified spider...", "Sam Raimi",
         "https://m.media-amazon.com/images/M/MV5BZDEyN2NhMjgtMjdhNi00MmNlLWE5YTgtZGE4MzNjYTRlNzgxXkEyXkFqcGdeQXVyNDUyOTg3Njg@._V1_.jpg",
         "https://www.youtube.com/watch?v=TYMMOjBUPMM"),
        ("Batman Begins", "Action", 2005, 8.2, "After training with his mentor...", "Christopher Nolan",
         "https://m.media-amazon.com/images/M/MV5BOTY4YjI2N2MtYmFlMC00ZjcyLTg3YjEtMDQyM2ZjYzQ5YWFkXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg",
         "https://www.youtube.com/watch?v=vak9ZLfhGo5"),
        ("Mad Max: Fury Road", "Action", 2015, 8.1, "In a post-apocalyptic wasteland...", "George Miller",
         "https://m.media-amazon.com/images/M/MV5BN2EwM2I5OWMtMGQyMi00Zjg1LWJkNTctZTcwYWM4OWI4MGQyXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg",
         "https://www.youtube.com/watch?v=hA2ple9k0Ic"),
        ("Wonder Woman", "Action", 2017, 7.4, "When a pilot crashes and tells of conflict...", "Patty Jenkins",
         "https://m.media-amazon.com/images/M/MV5BOGYzYWI3ZjItZmQ1Yy00YjA5LWI3ZjEtYzFjOTYzNWNlY2ZlXkEyXkFqcGdeQXVyNTI4MzE4MDU@._V1_.jpg",
         "https://www.youtube.com/watch?v=VSB4wGIdDwo"),
        
        # Sci-Fi movies
        ("Inception", "Sci-Fi", 2010, 8.8, "A thief who steals corporate secrets...", "Christopher Nolan",
         "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg",
         "https://www.youtube.com/watch?v=YoHD9XEInc0"),
        ("The Matrix", "Sci-Fi", 1999, 8.7, "A computer programmer discovers...", "Lana Wachowski",
         "https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg",
         "https://www.youtube.com/watch?v=vKQi3bBA1y8"),
        ("Interstellar", "Sci-Fi", 2014, 8.6, "A team of explorers travel through...", "Christopher Nolan",
         "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg",
         "https://www.youtube.com/watch?v=2LqzF5WauAw"),
        ("Star Wars", "Sci-Fi", 1977, 8.6, "Luke Skywalker joins forces with...", "George Lucas",
         "https://m.media-amazon.com/images/M/MV5BNzVlY2MwMjktM2E4OS00Y2Y3LWE3ZjctYzhkZGM3YzA1ZWM2XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg",
         "https://www.youtube.com/watch?v=vZ734NWnAHA"),
        ("Back to the Future", "Sci-Fi", 1985, 8.5, "Marty McFly, a 17-year-old high school student...", "Robert Zemeckis",
         "https://m.media-amazon.com/images/M/MV5BZmU0M2Y1OGUtZjIxNi00ZjBkLTg1MjgtOWIyN2Q3ZWNkOWE2XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg",
         "https://www.youtube.com/watch?v=qvsgGtivCgs"),
        ("E.T.", "Family", 1982, 7.8, "A troubled child summons the courage...", "Steven Spielberg",
         "https://m.media-amazon.com/images/M/MV5BMTQ2ODFlMDAtNmU2ZC00ZjYzLWE1Y2MtYTVjMzQ4MTk2ZWM4XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg",
         "https://www.youtube.com/watch?v=qYAETtIIClk"),
        ("2001: A Space Odyssey", "Sci-Fi", 1968, 8.8, "After discovering a mysterious artifact...", "Stanley Kubrick",
         "https://m.media-amazon.com/images/M/MV5BMmNlYzRiNDctZWNhMi00MzI4LThkZTctMTUzMmZkMmFmMWNhXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg",
         "https://www.youtube.com/watch?v=Z2UWOeBcsJI"),
        ("Her", "Romance", 2013, 8.0, "A lonely writer develops an unlikely relationship...", "Spike Jonze",
         "https://m.media-amazon.com/images/M/MV5BMjA1Nzk0OTM2OF5BMl5BanBnXkFtZTgwNjU2NjEwODE@._V1_.jpg",
         "https://www.youtube.com/watch?v=WzV6mXIOVl4"),
        
        # Crime/Thriller movies
        ("The Godfather", "Crime", 1972, 9.2, "The aging patriarch of an organized crime dynasty...", "Francis Ford Coppola",
         "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg",
         "https://www.youtube.com/watch?v=sY1S34973zA"),
        ("Pulp Fiction", "Crime", 1994, 8.9, "The lives of two mob hitmen...", "Quentin Tarantino",
         "https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg",
         "https://www.youtube.com/watch?v=s7EdQ4FqbhY"),
        ("Goodfellas", "Crime", 1990, 8.7, "The story of Henry Hill and his life...", "Martin Scorsese",
         "https://m.media-amazon.com/images/M/MV5BY2NkZjEzMDgtN2RjYy00YzM1LWI4ZmQtMmIwYzIwYzM0MDYzXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg",
         "https://www.youtube.com/watch?v=qo5jJpHtI1Y"),
        ("The Silence of the Lambs", "Thriller", 1991, 8.6, "A young F.B.I. cadet must receive...", "Jonathan Demme",
         "https://m.media-amazon.com/images/M/MV5BNjNhZTk0ZmEtNjJhMi00YzFlLGE1MmEtYzM1M2ZmMGMwMTU4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg",
         "https://www.youtube.com/watch?v=W6Mm8Sbe__o"),
        ("The Departed", "Crime", 2006, 8.5, "An undercover cop and a mole in the police...", "Martin Scorsese",
         "https://m.media-amazon.com/images/M/MV5BMTI1MTY2OTIxNV5BMl5BanBnXkFtZTYwNjQ4NjY3._V1_.jpg",
         "https://www.youtube.com/watch?v=auYbpnJw61g"),
        ("Taxi Driver", "Crime", 1976, 8.2, "A mentally unstable Vietnam War veteran...", "Martin Scorsese",
         "https://m.media-amazon.com/images/M/MV5BM2M1MmVmNDEtNmQ0Yy00NGU4LWIwNzgtM2ZmNjcwNzg2MjZkXkEyXkFqcGdeQXVyMzUyOTU0OTM@._V1_.jpg",
         "https://www.youtube.com/watch?v=UUxD4-dEzn0"),
        ("Raging Bull", "Biography", 1980, 8.2, "The life of boxer Jake LaMotta...", "Martin Scorsese",
         "https://m.media-amazon.com/images/M/MV5BYjRmODkzNDItMTNhNi00YjExLTJjNzQtMWVmNWVmODIwODVmXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_.jpg",
         "https://www.youtube.com/watch?v=mHhzOM4gBIA"),
        ("Get Out", "Horror", 2017, 7.7, "A young African-American visits...", "Jordan Peele",
         "https://m.media-amazon.com/images/M/MV5BMjUxMjQ5ODI1NF5BMl5BanBnXkFtZTgwNjk2OTg2NTE@._V1_.jpg",
         "https://www.youtube.com/watch?v=D9sjwJxhvVM"),
        
        # Comedy movies
        ("The Grand Budapest Hotel", "Comedy", 2014, 8.1, "A writer encounters the owner of an old hotel...", "Wes Anderson",
         "https://m.media-amazon.com/images/M/MV5BMzM5NjUxOTEyMl5BMl5BanBnXkFtZTgwNjEyMDM0MDE@._V1_.jpg",
         "https://www.youtube.com/watch?v=1Fg5iWmQjwk"),
        ("Birdman", "Drama", 2014, 7.7, "A washed-up superhero actor attempts...", "Alejandro González Iñárritu",
         "https://m.media-amazon.com/images/M/MV5BODAzNDMxMzAzOV5BMl5BanBnXkFtZTgwMDMxMjA4MjE@._V1_.jpg",
         "https://www.youtube.com/watch?v=uJfLoE6hanc"),
        ("Whiplash", "Drama", 2014, 8.5, "A promising young drummer enrolls...", "Damien Chazelle",
         "https://m.media-amazon.com/images/M/MV5BOTA5NDZlZGUtMjE5NC00YWQ3LThmMWUtZWVjYTAyMWVjMjZiXkEyXkFqcGdeQXVyNTM4OTYyMDI@._V1_.jpg",
         "https://www.youtube.com/watch?v=7d_jQycdQGo"),
        
        # Horror movies
        ("The Shining", "Horror", 1980, 8.4, "A family heads to an isolated hotel...", "Stanley Kubrick",
         "https://m.media-amazon.com/images/M/MV5BZWFlYmY2MGEtZjVkYS00YzU4LTJmY2ItZjZiZGRmZGRmZGRmXkEyXkFqcGdeQXVyNDUyOTg3Njg@._V1_.jpg",
         "https://www.youtube.com/watch?v=S014oGjAqnM"),
        ("A Clockwork Orange", "Crime", 1971, 8.3, "In the future, a sadistic gang leader...", "Stanley Kubrick",
         "https://m.media-amazon.com/images/M/MV5BMTY3MjM1Mzc4N15BMl5BanBnXkFtZTgwODM0NzAxMDE@._V1_.jpg",
         "https://www.youtube.com/watch?v=SPRzm8ibDQ8"),
        ("The Exorcist", "Horror", 1973, 8.0, "When a 12-year-old girl is possessed...", "William Friedkin",
         "https://m.media-amazon.com/images/M/MV5BYjhmMGMxZDYtY2QwYS00NTBmLTk3NDItYmRkY2VlN2JhNzM4XkEyXkFqcGdeQXVyNzQ1ODk3MTQ@._V1_.jpg",
         "https://www.youtube.com/watch?v=YDGw1yEe5B4"),
        ("Jaws", "Thriller", 1975, 8.0, "When a killer shark unleashes chaos...", "Steven Spielberg",
         "https://m.media-amazon.com/images/M/MV5BMmVmODY1MzEtYTMwZC00MzNhLWFkNDMtZjAwM2EwODUxZTA5XkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_.jpg",
         "https://www.youtube.com/watch?v=U1fu_sA7XhE"),
        
        # Adventure/Fantasy movies
        ("The Lord of the Rings", "Fantasy", 2001, 8.9, "A meek Hobbit from the Shire...", "Peter Jackson",
         "https://m.media-amazon.com/images/M/MV5BN2EyZjM3NzUtNWUzMi00MTgxLWIyNTctN2M0N2Y3MWQ5ZTgxXkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_.jpg",
         "https://www.youtube.com/watch?v=V75dMMIW2B4"),
        ("Harry Potter", "Fantasy", 2001, 7.6, "An orphaned boy enrolls in a school...", "Chris Columbus",
         "https://m.media-amazon.com/images/M/MV5BNmQ0ODBhMjUtNDRhOC00MGQzLTk5MTAtZDliODg5NmU5MjZhXkEyXkFqcGdeQXVyNDUyOTg3Njg@._V1_.jpg",
         "https://www.youtube.com/watch?v=eKSB0gXW9J0"),
        ("Indiana Jones", "Adventure", 1981, 8.4, "Archaeology professor Indiana Jones...", "Steven Spielberg",
         "https://m.media-amazon.com/images/M/MV5BMjNkMzc2N2QtNjVlNS00ZTk1LTg2YTItNjU2OTY0ZWFhMDI5L2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_.jpg",
         "https://www.youtube.com/watch?v=XkkzKHCx154"),
        ("The Lion King", "Animation", 1994, 8.5, "Lion prince Simba and his father...", "Roger Allers",
         "https://m.media-amazon.com/images/M/MV5BYTYxNGMyZTYtMjE3MS00MzYyLWEyY2YtOGQ3Y2IzZmExOWM4XkEyXkFqcGdeQXVyNjg0NTcxMTg@._V1_.jpg",
         "https://www.youtube.com/watch?v=4sj1MT05lAA"),
        ("Titanic", "Romance", 1997, 7.9, "A seventeen-year-old aristocrat...", "James Cameron",
         "https://m.media-amazon.com/images/M/MV5BMDdmZGU3NDQtY2E5My00ZTliLWIzOTUtMTY4ZGI1YjI6MGJhXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg",
         "https://www.youtube.com/watch?v=2e-eXJ0HgkU"),
        ("Avatar", "Sci-Fi", 2009, 7.8, "A paraplegic Marine dispatched...", "James Cameron",
         "https://m.media-amazon.com/images/M/MV5BMTYwOTEwNjAzMl5BMl5BanBnXkFtZTcwODc5MTUwMw@@._V1_.jpg",
         "https://www.youtube.com/watch?v=5PSNL1qE6VY"),
        ("Jurassic Park", "Adventure", 1993, 8.5, "A pragmatic paleontologist visiting...", "Steven Spielberg",
         "https://m.media-amazon.com/images/M/MV5BMjM2MDgxMDg0Nl5BMl5BanBnXkFtZTgwNTM2OTM5NDE@._V1_.jpg",
         "https://www.youtube.com/watch?v=lc0UehYemQA"),
        
        # Additional movies
        ("Apocalypse Now", "War", 1979, 8.4, "A U.S. Army officer serving in Vietnam...", "Francis Ford Coppola",
         "https://m.media-amazon.com/images/M/MV5BMDdhODg0MjYtYzBiOS00ZmI5LWEwZGYtZDEyNDU4MmQyNzFkXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg",
         "https://www.youtube.com/watch?v=IkRhSXxMhjI"),
        ("Black Panther", "Action", 2018, 7.3, "T'Challa, heir to the hidden but advanced...", "Ryan Coogler",
         "https://m.media-amazon.com/images/M/MV5BMTg1MTY2MjYzNV5BMl5BanBnXkFtZTgwMTc4NTMwNDI@._V1_.jpg",
         "https://www.youtube.com/watch?v=xjDjIWPwcPU"),
        ("The Godfather Part II", "Crime", 1974, 9.0, "The early life and career of Vito Corleone...", "Francis Ford Coppola",
         "https://m.media-amazon.com/images/M/MV5BMWMwMGQzZTItY2JlNC00OWZiLWIyMDctNDk2ZDQ2YjRjMWQ0XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg",
         "https://www.youtube.com/watch?v=9O1Iy9od7-A"),
    ]
    
    created_movies = []
    for title, genre, year, rating, description, director, poster_url, trailer_url in movies_data:
        # Convert IMDb rating (1-10) to our rating scale (1-5)
        rating_1_5 = (rating / 2.0) if rating else None
        
        movie = db_service.create_movie(
            title=title,
            genre=genre,
            year=year,
            rating=rating_1_5,
            description=description,
            director=director,
            poster_url=poster_url,
            trailer_url=trailer_url
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