# 🎬 Movie Recommendation System

A comprehensive movie recommendation system with a Python Flask backend and React frontend, featuring smart recommendation algorithms and a modern user interface.

## 🌟 Features

### 🎯 Smart Recommendations
- **💡 Smart Recommendations**: Personalized movie suggestions
- **🎭 Content-Based Filtering**: Find movies similar to your favorites
- **👥 Collaborative Filtering**: Get recommendations based on similar users
- **🔀 Hybrid Approach**: Combines multiple recommendation algorithms
- **🎨 Genre-Focused**: Discover top movies in your preferred genre

### 🖼️ Rich Movie Information
- **📸 Movie Posters**: High-quality poster images for all movies
- **🎬 YouTube Trailers**: Direct links to official movie trailers
- **📝 Movie Descriptions**: Comprehensive movie plot summaries
- **📊 Detailed Ratings**: User ratings and predicted ratings
- **🎭 Genre Classification**: Movies categorized by genre

### 🔐 User Authentication
- **🔒 Secure Login**: JWT-based authentication
- **👤 User Profiles**: Personalized user accounts
- **⭐ Rating System**: Rate movies and see your history
- **🎯 Preferences**: Set your preferred movie genre
- **👑 Admin Panel**: Full movie management system for administrators

### 📱 Modern UI/UX
- **📱 Responsive Design**: Works on all devices
- **🎨 Material-UI**: Beautiful, modern interface
- **⚡ Fast Loading**: Optimized performance
- **🔍 Search & Filter**: Find movies easily

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Node.js 16+
- PostgreSQL 12+

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python init_database.py
python create_admin.py  # Create admin user
python api_server.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Admin Access
1. Start both backend and frontend servers
2. Open http://localhost:3000 in your browser
3. Login with admin credentials:
   - Username: `admin`
   - Password: `admin123`
4. Click "Admin" in the navigation to access the admin panel

## 🎬 Movie Features

### Poster Images
- All movies now include high-quality poster images from IMDb
- Posters are displayed prominently on movie cards
- Responsive design ensures optimal viewing on all devices

### YouTube Trailers
- Direct links to official movie trailers on YouTube
- "🎬 Trailer" button opens trailers in a new tab
- Available on both movie browsing and recommendation pages

### Enhanced Movie Cards
- **Poster Display**: Movie posters at the top of each card
- **Movie Descriptions**: Plot summaries with text truncation
- **Trailer Button**: Quick access to official trailers
- **Rating System**: Rate movies directly from the card
- **Responsive Layout**: Optimized for mobile and desktop

## 🎯 Recommendation Algorithms

### Smart Personalization
- **Genre Preference Boost**: 30% rating boost for preferred genres
- **Collaborative Filtering**: Based on similar users' preferences
- **Content-Based Filtering**: Based on movie features and genres
- **Hybrid Approach**: Combines multiple algorithms for accuracy

### Recommendation Types
1. **Personalized Recommendations**: Based on your rating history
2. **Genre-Focused**: Top movies in your preferred genre
3. **Popular Movies**: Highest-rated movies overall
4. **Similar Movies**: Movies like the one you're viewing

## 📊 Database Schema

### Movies Table
- `id`: Primary key
- `title`: Movie title
- `genre`: Movie genre
- `year`: Release year
- `rating`: Overall rating
- `description`: Movie description
- `director`: Movie director
- `cast`: Cast information
- `poster_url`: High-quality poster image URL
- `trailer_url`: YouTube trailer link

### Users Table
- `id`: Primary key
- `username`: Unique username
- `password_hash`: Hashed password
- `name`: Full name
- `email`: Email address (unique)
- `age`: User age
- `preferred_genre`: Favorite movie genre
- `role`: User role (user/admin)

## 🎨 Frontend Components

### Movie Cards
- **Poster Images**: Displayed prominently at the top
- **Movie Information**: Title, year, genre, description
- **Rating System**: Interactive star ratings
- **Action Buttons**: View details and watch trailer
- **Responsive Design**: Adapts to screen size

### Recommendation Cards
- **Ranking**: Shows recommendation position (#1, #2, etc.)
- **Predicted Rating**: AI-predicted user rating
- **Poster Display**: Movie poster for visual appeal
- **Movie Descriptions**: Plot summaries for better context
- **Trailer Access**: Quick trailer viewing
- **Genre Information**: Movie genre and preferences

## 🔧 API Endpoints

### Movies
- `GET /api/movies` - List all movies with pagination
- `GET /api/movies/{id}` - Get specific movie details
- `GET /api/movies/popular` - Get popular movies
- `GET /api/movies/genre/{genre}` - Get movies by genre

### Recommendations
- `GET /api/recommendations/personalized` - Smart collaborative recommendations
- `GET /api/recommendations/genre-focused` - Genre-specific recommendations
- `GET /api/recommendations/content-based/{id}` - Similar movies
- `GET /api/recommendations/hybrid` - Combined approach

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile

### Admin Endpoints (Admin Only)
- `GET /api/admin/movies` - Get all movies for admin management
- `POST /api/admin/movies` - Create a new movie
- `PUT /api/admin/movies/{id}` - Update an existing movie
- `DELETE /api/admin/movies/{id}` - Delete a movie and its ratings
- `GET /api/users` - Get all users (admin only)

## 🎯 Demo Accounts

| Username | Password | Role | Preferred Genre |
|----------|----------|------|-----------------|
| admin    | admin123 | Admin | Drama |
| alice    | alice123 | User | Drama |
| bob      | bob123   | User | Action |

## 👑 Admin Functionality

### Admin Dashboard Features
- **🎬 Movie Management**: Add, edit, and delete movies
- **🔍 Search & Filter**: Find movies by title or genre
- **📊 Pagination**: Navigate through large movie collections
- **🖼️ Rich Media**: Support for poster URLs and trailer links
- **⚡ Real-time Updates**: Changes reflect immediately
- **🔒 Role-based Access**: Only admin users can access

### Admin Capabilities
- **Create Movies**: Add new movies with full details (title, genre, year, description, director, cast, poster URL, trailer URL)
- **Edit Movies**: Update any movie information
- **Delete Movies**: Remove movies and their associated ratings
- **Search Movies**: Find specific movies by title
- **Filter by Genre**: View movies by specific genre
- **Bulk Management**: Handle large collections efficiently

### Security Features
- **JWT Authentication**: Secure token-based authentication
- **Role Verification**: Server-side admin role checking
- **Input Validation**: Proper validation for all movie data
- **Cascade Deletion**: Proper cleanup when deleting movies

## 🚀 Deployment

### Backend Deployment
1. Set up PostgreSQL database
2. Configure environment variables
3. Install Python dependencies
4. Run database initialization
5. Start with production WSGI server

### Frontend Deployment
1. Build the React application
2. Deploy to static hosting (Netlify, Vercel, etc.)
3. Configure API endpoint URLs

## 🛠️ Development

### Backend Development
```bash
cd backend
python api_server.py  # Development server
python test_images.py  # Test poster/trailer functionality
```

### Frontend Development
```bash
cd frontend
npm start  # Development server
npm test   # Run tests
npm build  # Production build
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**🎬 Enjoy discovering your next favorite movie with our smart recommendation system!** 