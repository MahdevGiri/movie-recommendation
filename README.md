# 🎬 Movie Recommendation System

A simple yet powerful movie recommendation system built in Python using dummy data. This project demonstrates various recommendation algorithms including collaborative filtering, content-based filtering, and hybrid approaches.

## ✨ Features

- **Collaborative Filtering**: Recommends movies based on similar users' preferences
- **Content-Based Filtering**: Recommends movies similar to a specific movie based on genres
- **Hybrid Recommendations**: Combines both collaborative and content-based approaches
- **Popular Movies**: Shows trending movies based on average ratings
- **Genre Browsing**: Browse movies by specific genres
- **User Rating History**: View all ratings for any user
- **Interactive CLI**: User-friendly command-line interface

## 📊 Dataset

The system uses a dummy dataset containing:
- **50 Movies**: Popular movies with genres, years, and ratings
- **20 Users**: Users with different preferences and age groups
- **300+ Ratings**: User ratings on a 1-5 scale

### Sample Movies
- The Shawshank Redemption (Drama, 1994)
- The Godfather (Crime, 1972)
- The Dark Knight (Action, 2008)
- Inception (Sci-Fi, 2010)
- And many more...

## 🚀 Installation

1. **Clone or download the project files**

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## 📋 Requirements

- Python 3.7+
- pandas
- numpy
- scikit-learn

## 🎯 Usage

### Starting the Application

Run the main script:
```bash
python main.py
```

### Main Menu Options

1. **Get personalized recommendations for a user**
   - Enter a user ID (1-20)
   - Get movie recommendations based on similar users

2. **Get content-based recommendations for a movie**
   - Enter a movie ID (1-50)
   - Get movies similar based on genre and features

3. **Get hybrid recommendations**
   - Combine collaborative and content-based filtering
   - Optionally specify a reference movie

4. **Show popular movies**
   - View trending movies based on average ratings

5. **Browse movies by genre**
   - Filter movies by specific genres (Action, Drama, Sci-Fi, etc.)

6. **View user ratings**
   - See all movies rated by a specific user

7. **List all movies**
   - Browse the complete movie database

8. **List all users**
   - View all users and their preferences

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
FirstProject/
├── main.py                 # Main application with CLI
├── movie_data.py          # Dummy dataset generation
├── recommendation_system.py # Core recommendation algorithms
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🎨 Example Output

```
============================================================
🎬 MOVIE RECOMMENDATION SYSTEM 🎬
============================================================

Loading movie recommendation system...
✅ System loaded successfully!

📋 MAIN MENU:
1. Get personalized recommendations for a user
2. Get content-based recommendations for a movie
3. Get hybrid recommendations
4. Show popular movies
5. Browse movies by genre
6. View user ratings
7. List all movies
8. List all users
9. Exit

Enter your choice (1-9): 1

👤 PERSONALIZED RECOMMENDATIONS
----------------------------------------
Available users:
 1. Alice (Prefers: Drama)
 2. Bob (Prefers: Action)
 3. Charlie (Prefers: Sci-Fi)
...

Enter user ID (or 'q' to quit): 1
Number of recommendations (1-10): 5

🎭 PERSONALIZED RECOMMENDATIONS FOR USER 1:
--------------------------------------------------------------------------------
 1. The Dark Knight (2008) - Action - Predicted Rating: 4.2
 2. Inception (2010) - Sci-Fi - Predicted Rating: 4.1
 3. The Matrix (1999) - Sci-Fi - Predicted Rating: 4.0
 4. Pulp Fiction (1994) - Crime - Predicted Rating: 3.9
 5. Goodfellas (1990) - Crime - Predicted Rating: 3.8
```

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
Edit the `create_dummy_movies()` function in `movie_data.py`:
```python
def create_dummy_movies():
    movies_data = {
        'movie_id': range(1, 51),
        'title': ['Your Movie Title', ...],
        'genre': ['Your Genre', ...],
        'year': [2024, ...],
        'rating': [8.5, ...]
    }
    return pd.DataFrame(movies_data)
```

### Adding New Users
Edit the `create_dummy_users()` function:
```python
def create_dummy_users():
    users_data = {
        'user_id': range(1, 21),
        'name': ['New User', ...],
        'age': [25, ...],
        'preferred_genre': ['Action', ...]
    }
    return pd.DataFrame(users_data)
```

## 🎓 Learning Objectives

This project demonstrates:
- **Data Preprocessing**: Creating and manipulating pandas DataFrames
- **Machine Learning**: Implementing recommendation algorithms
- **Similarity Metrics**: Using cosine similarity for recommendations
- **Matrix Operations**: Working with user-item matrices
- **Software Design**: Modular code structure and clean interfaces

## 🤝 Contributing

Feel free to enhance this project by:
- Adding more sophisticated algorithms
- Implementing additional similarity metrics
- Creating a web interface
- Adding more movie features (director, cast, etc.)
- Implementing real-time rating updates

## 📝 License

This project is open source and available under the MIT License.

## 🎯 Future Enhancements

- Web-based user interface
- Real-time rating system
- More sophisticated algorithms (SVD, neural networks)
- Movie poster integration
- User authentication system
- Database integration (SQLite/PostgreSQL)

---

**Enjoy exploring the world of movie recommendations! 🍿** 