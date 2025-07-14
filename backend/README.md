# 🎬 Movie Recommendation System - Backend

A Python Flask-based REST API for a movie recommendation system with JWT authentication, PostgreSQL database, and advanced recommendation algorithms.

## 🌟 Features

### 🔐 Authentication & Security
- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: SHA-256 hashing for password security
- **CORS Support**: Cross-origin resource sharing enabled
- **Input Validation**: Server-side validation of all inputs
- **SQL Injection Protection**: Parameterized queries with SQLAlchemy

### 🎯 Recommendation Algorithms
- **Collaborative Filtering**: Based on similar users' preferences
- **Content-Based Filtering**: Based on movie features and genres
- **Hybrid Approach**: Combines both methods for better accuracy
- **Genre-Focused Recommendations**: Top-rated movies in user's preferred genre
- **Smart Personalization**: Boosts recommendations based on user's preferred genre

### 📊 Database & Data Management
- **PostgreSQL Database**: Robust data persistence
- **SQLAlchemy ORM**: Object-relational mapping
- **Database Seeding**: Pre-populated with sample data
- **User Profiles**: Personalized user accounts with preferences

## 🏗️ Project Structure

```
backend/
├── api_server.py              # Main Flask application
├── auth_system.py             # JWT authentication logic
├── recommendation_system.py   # Recommendation algorithms
├── database_service.py        # Database operations
├── models.py                  # SQLAlchemy models
├── database_config.py         # Database configuration
├── database_seeder.py         # Database seeding script
├── init_database.py           # Database initialization
├── requirements.txt           # Python dependencies
├── test_login.py              # Authentication tests
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.7+** and **pip**
2. **PostgreSQL 12+** database
3. **Git** (for cloning)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd movie-recommendation/backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL database:**
   - Create a new PostgreSQL database
   - Update database connection in `database_config.py` if needed

4. **Initialize the database:**
   ```bash
   python init_database.py
   ```

5. **Start the development server:**
   ```bash
   python api_server.py
   ```

The API will be available at: **http://localhost:5000**

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile

### Movies
- `GET /api/movies` - List all movies (with pagination)
- `GET /api/movies/{id}` - Get specific movie details

### Ratings
- `POST /api/ratings` - Rate a movie
- `GET /api/ratings` - Get user's ratings

### Recommendations
- `GET /api/recommendations/personalized` - Get smart collaborative recommendations
- `GET /api/recommendations/genre-focused` - Get top-rated movies in preferred genre
- `GET /api/recommendations/popular` - Get popular movies

## 🔧 Development

### Available Scripts

```bash
python api_server.py          # Start development server
python init_database.py       # Initialize database
python test_login.py          # Run authentication tests
```

### Environment Variables

The following environment variables can be configured:

- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret key for JWT token generation
- `FLASK_ENV`: Development/production environment

### Database Schema

#### Users Table
- `id`: Primary key
- `username`: Unique username
- `password_hash`: Hashed password
- `email`: User email
- `preferred_genre`: User's preferred movie genre
- `age`: User age
- `created_at`: Account creation timestamp

#### Movies Table
- `id`: Primary key
- `title`: Movie title
- `genre`: Movie genre
- `year`: Release year
- `description`: Movie description
- `average_rating`: Average user rating
- `rating_count`: Number of ratings

#### Ratings Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `movie_id`: Foreign key to movies
- `rating`: Rating value (1-5)
- `created_at`: Rating timestamp

## 🎯 Recommendation Algorithms

### Collaborative Filtering
- Finds users with similar preferences
- Calculates similarity using Pearson correlation
- Predicts ratings based on similar users' ratings
- Handles cold start with fallback strategies

### Content-Based Filtering
- Analyzes movie features (genre, year, description)
- Creates user preference profiles
- Recommends movies similar to previously rated ones
- Uses TF-IDF for text analysis

### Hybrid Approach
- Combines collaborative and content-based methods
- Weights recommendations based on data availability
- Provides fallback strategies for new users
- Balances personalization with diversity

### Genre-Focused Recommendations
- Identifies user's preferred genre from profile
- Returns top-rated movies in that genre
- Provides genre-specific discovery
- Complements personalized recommendations

### Smart Personalization
- Boosts predicted ratings for preferred genre movies
- Maintains collaborative filtering accuracy
- Balances genre preference with user similarity
- Adapts to user's evolving preferences

## 📊 Sample Data

The system includes comprehensive sample data:

### Movies (49 movies)
- Popular movies across different genres
- Years ranging from 1972 to 2020
- Various genres: Action, Drama, Comedy, Sci-Fi, etc.
- Realistic descriptions and ratings

### Users (10 users)
- Different age groups and preferences
- Various preferred genres
- Realistic rating patterns

### Ratings (145+ ratings)
- User ratings on 1-5 scale
- Realistic rating distributions
- Covers different movie genres

## 🔒 Security Features

- **JWT Tokens**: Secure authentication without server-side sessions
- **Password Hashing**: SHA-256 hashing for password security
- **Input Validation**: Comprehensive validation of all API inputs
- **SQL Injection Protection**: Parameterized queries with SQLAlchemy
- **CORS Configuration**: Proper cross-origin resource sharing
- **Error Handling**: Secure error responses without information leakage

## 🧪 Testing

Run the authentication tests:
```bash
python test_login.py
```

The tests verify:
- User registration
- User login
- JWT token validation
- Profile access
- Error handling

## 🚀 Deployment

### Production Setup

1. **Set up PostgreSQL database**
2. **Configure environment variables**
3. **Install production dependencies**
4. **Run database migrations**
5. **Start with production WSGI server**

### Environment Variables for Production

```bash
export FLASK_ENV=production
export JWT_SECRET_KEY=your-secure-secret-key
export DATABASE_URL=postgresql://user:password@host:port/database
```

## 📝 API Documentation

### Request/Response Examples

#### Register User
```bash
POST /api/auth/register
Content-Type: application/json

{
  "username": "newuser",
  "password": "password123",
  "email": "user@example.com",
  "preferred_genre": "Action",
  "age": 25
}
```

#### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "username": "user",
  "password": "password123"
}
```

#### Rate Movie
```bash
POST /api/ratings
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "movie_id": 1,
  "rating": 5
}
```

#### Get Recommendations
```bash
GET /api/recommendations/personalized?limit=12
Authorization: Bearer <jwt-token>
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Flask** for the robust web framework
- **SQLAlchemy** for the excellent ORM
- **PostgreSQL** for the reliable database
- **JWT** for secure authentication

---

**Happy Coding! 🚀✨** 