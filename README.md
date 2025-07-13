# 🎬 Movie Recommendation System

A simple yet powerful movie recommendation system built in Python using PostgreSQL database. This project demonstrates various recommendation algorithms including collaborative filtering, content-based filtering, and hybrid approaches, with a complete user authentication system.

## ✨ Features

- **🔐 User Authentication**: Secure login/registration system with password hashing
- **👤 User Profiles**: Personalized user accounts with preferences and settings
- **🔑 Password Management**: Change passwords and manage account security
- **Collaborative Filtering**: Recommends movies based on similar users' preferences
- **Content-Based Filtering**: Recommends movies similar to a specific movie based on genres
- **Hybrid Recommendations**: Combines both collaborative and content-based approaches
- **Popular Movies**: Shows trending movies based on average ratings
- **Genre Browsing**: Browse movies by specific genres
- **User Rating History**: View all ratings for any user
- **Interactive CLI**: User-friendly command-line interface
- **PostgreSQL Database**: Robust data persistence with SQLAlchemy ORM

## 📊 Dataset

The system uses a comprehensive dataset containing:
- **49 Movies**: Popular movies with genres, years, ratings, descriptions, and directors
- **10 Users**: Users with different preferences and age groups
- **145+ Ratings**: User ratings on a 1-5 scale with realistic preference patterns

### Sample Movies
- The Shawshank Redemption (Drama, 1994) - Frank Darabont
- The Godfather (Crime, 1972) - Francis Ford Coppola
- The Dark Knight (Action, 2008) - Christopher Nolan
- Inception (Sci-Fi, 2010) - Christopher Nolan
- And many more...

## 🚀 Installation

### Prerequisites

1. **PostgreSQL Database**
   - Install PostgreSQL (version 12 or higher)
   - Create a database named `movie_recommendation`
   - Note down your database credentials

2. **Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Database Setup

1. **Initialize the database**:
   ```bash
   python init_database.py
   ```
   This will:
   - Create the `.env` file with default PostgreSQL credentials
   - Test the database connection
   - Create all necessary tables
   - Seed the database with sample data

   **Note**: The default credentials are:
   - Host: localhost
   - Port: 5432
   - Database: movie_recommendation
   - Username: postgres
   - Password: postgres

   You can edit the `.env` file to change these settings.

### Running the Application

1. **Start the main application**:
   ```bash
   python main.py
   ```

2. **Test the login system** (optional):
   ```bash
   python login_demo.py
   ```

3. **Reset database** (if needed):
   ```bash
   python database_seeder.py --clear
   python init_database.py
   ```

## 📋 Requirements

- Python 3.7+
- PostgreSQL 12+
- pandas
- numpy
- scikit-learn
- psycopg2-binary
- sqlalchemy
- python-dotenv

## 🎯 Usage

### Starting the Application

Run the main script:
```bash
python main.py
```

### Main Menu Options

1. **Login** - Authenticate with username and password
2. **Register** - Create a new user account
3. **Get personalized recommendations for a user** (requires login)
   - Uses your logged-in profile for recommendations
   - Get movie recommendations based on similar users

4. **Get content-based recommendations for a movie** (requires login)
   - Enter a movie ID (1-49)
   - Get movies similar based on genre and features

5. **Get hybrid recommendations** (requires login)
   - Combine collaborative and content-based filtering
   - Optionally specify a reference movie

6. **Show popular movies**
   - View trending movies based on average ratings

7. **Browse movies by genre**
   - Filter movies by specific genres (Action, Drama, Sci-Fi, etc.)

8. **View user ratings** (requires login)
   - See all movies rated by a specific user

9. **List all movies**
   - Browse the complete movie database

10. **List all users** (requires login)
    - View all users and their preferences

11. **View my profile** (requires login)
    - Display your account information and preferences

12. **Change password** (requires login)
    - Update your account password securely

13. **Logout** - Sign out of your account

14. **Exit** - Close the application

## 🔧 How It Works

### Collaborative Filtering
- Creates a user-movie rating matrix
- Calculates similarity between users using cosine similarity
- Recommends movies that similar users have rated highly

### Content-Based Filtering
- Analyzes movie features (genres, ratings)
- Creates a similarity matrix between movies
- Recommends movies similar to a reference movie

### Hybrid Approach
- Combines both collaborative and content-based scores
- Weights collaborative filtering more heavily (70% vs 30%)
- Provides more diverse and accurate recommendations

## 📁 Project Structure

```
movie-recommendation/
├── main.py                 # Main application with CLI and authentication
├── auth_system.py         # User authentication and session management
├── login_demo.py          # Demo script for testing login functionality
├── test_login.py          # Automated login tests
├── init_database.py       # Database initialization script
├── create_env.py          # Environment file creation utility
├── database_config.py     # PostgreSQL connection configuration
├── database_service.py    # Database operations service layer
├── database_adapter.py    # Adapter for pandas DataFrame compatibility
├── models.py              # SQLAlchemy database models
├── database_seeder.py     # Database seeding with sample data
├── recommendation_system.py # Core recommendation algorithms
├── movie_data.py          # Legacy dummy dataset generation
├── requirements.txt       # Python dependencies
├── .env                   # Database configuration (created by init)
└── README.md             # This file
```

## 🎨 Example Output

```
============================================================
🎬 MOVIE RECOMMENDATION SYSTEM 🎬
============================================================

Loading movie recommendation system...
✅ System loaded successfully!
Loading authentication system...
✅ Authentication system loaded successfully!

👤 Not logged in

📋 MAIN MENU:
1. Login
2. Register
3. Get personalized recommendations for a user
4. Get content-based recommendations for a movie
5. Get hybrid recommendations
6. Show popular movies
7. Browse movies by genre
8. View user ratings
9. List all movies
10. List all users
11. View my profile
12. Change password
13. Logout
14. Exit

Enter your choice (1-14): 1

🔐 LOGIN
----------------------------------------
Username: alice
Password: ****
✅ Welcome back, Alice Johnson!

👤 Logged in as: Alice Johnson (alice)

Enter your choice (1-14): 3

👤 PERSONALIZED RECOMMENDATIONS
----------------------------------------
Getting recommendations for: Alice Johnson (User ID: 2)
Preferred genre: Drama
Number of recommendations (1-10): 5

🎭 PERSONALIZED RECOMMENDATIONS FOR ALICE JOHNSON:
--------------------------------------------------------------------------------
 1. The Shawshank Redemption (1994) - Drama - Predicted Rating: 4.3
 2. Forrest Gump (1994) - Drama - Predicted Rating: 4.2
 3. The Green Mile (1999) - Drama - Predicted Rating: 4.1
 4. Good Will Hunting (1997) - Drama - Predicted Rating: 4.0
 5. The Social Network (2010) - Biography - Predicted Rating: 3.9
```

## 🔐 Security Features

### Password Security
- **SHA-256 Hashing**: All passwords are securely hashed before storage
- **No Plain Text**: Passwords are never stored in readable format
- **Secure Authentication**: Login verification uses hash comparison
- **Session Management**: Secure session tokens for logged-in users

### Data Protection
- **Unique Usernames**: Prevents duplicate account creation
- **Input Validation**: Age and password length requirements
- **SQL Injection Protection**: Uses SQLAlchemy ORM with parameterized queries

## 🔐 Default Login Credentials

The system comes with pre-configured demo accounts:

| Username | Password | Role | Preferred Genre |
|----------|----------|------|-----------------|
| admin    | admin123 | Admin | Drama |
| alice    | alice123 | User | Drama |
| bob      | bob123   | User | Action |
| charlie  | charlie123 | User | Sci-Fi |
| diana    | diana123 | User | Romance |
| eve      | eve123   | User | Horror |
| frank    | frank123 | User | Crime |
| grace    | grace123 | User | Comedy |
| henry    | henry123 | User | Action |
| ivy      | ivy123   | User | Drama |

## 🔍 Algorithm Details

### Similarity Calculation
- **Cosine Similarity**: Used for both user and movie similarity
- **Feature Vector**: Movies represented by genre dummies and ratings
- **Rating Matrix**: Users × Movies matrix with ratings

### Recommendation Scoring
- **Collaborative**: Weighted average of similar users' ratings
- **Content-Based**: Direct similarity scores
- **Hybrid**: Weighted combination (70% CF + 30% CB)

## 🛠️ Customization

### Adding New Movies
Edit the `movies_data` list in `database_seeder.py`:
```python
movies_data = [
    ("Your Movie Title", "Genre", 2024, 8.5, "Description...", "Director Name"),
    # Add more movies here
]
```

### Adding New Users
Edit the `users_data` list in `database_seeder.py`:
```python
users_data = [
    ("username", "password", "Full Name", "email@example.com", 25, "Preferred Genre", "role"),
    # Add more users here
]
```

## 🐛 Troubleshooting

### Common Issues

1. **"User object is not subscriptable" error**
   - ✅ **FIXED**: This has been resolved in the latest version
   - The application now properly handles User objects from the database

2. **New users getting "No movies found" for recommendations**
   - ✅ **FIXED**: New users without ratings now get genre-based recommendations
   - The system automatically provides popular movies in their preferred genre

3. **Registration not automatically logging in users**
   - ✅ **FIXED**: Users are now automatically logged in after successful registration
   - No need to manually login after registration

4. **Database connection issues**
   - Ensure PostgreSQL is running
   - Check your `.env` file configuration
   - Verify database credentials

5. **Password input not visible**
   - This is normal behavior for security
   - Type your password and press Enter
   - If using PowerShell, try Command Prompt instead

6. **Import errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check that all files are in the correct directory

## 🎓 Learning Objectives

This project demonstrates:
- **Database Design**: PostgreSQL with SQLAlchemy ORM
- **Data Preprocessing**: Creating and manipulating pandas DataFrames
- **Machine Learning**: Implementing recommendation algorithms
- **Similarity Metrics**: Using cosine similarity for recommendations
- **Matrix Operations**: Working with user-item matrices
- **Software Design**: Modular code structure and clean interfaces
- **Authentication**: Secure user management with password hashing

## 🤝 Contributing

Feel free to enhance this project by:
- Adding more sophisticated algorithms
- Implementing additional similarity metrics
- Creating a web interface
- Adding more movie features (director, cast, etc.)
- Implementing real-time rating updates
- Adding unit tests
- Improving error handling

## 📝 License

This project is open source and available under the MIT License.

## 🎯 Future Enhancements

- Web-based user interface
- Real-time rating system
- More sophisticated algorithms (SVD, neural networks)
- Movie poster integration
- Enhanced user authentication (email verification, password reset)
- User rating submission system
- Movie watchlist functionality
- API endpoints for external integration
- Docker containerization
- Automated testing suite

## 📈 Recent Updates

- **v2.2**: Fixed new user recommendation system and auto-login after registration
- **v2.1**: Fixed User object access issues in main.py
- **v2.0**: Migrated to PostgreSQL database with SQLAlchemy ORM
- **v1.0**: Initial release with in-memory data storage

---

**Enjoy exploring the world of movie recommendations! 🍿** 