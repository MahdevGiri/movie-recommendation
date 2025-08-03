# 🎬 Movie Recommendation System

A comprehensive movie recommendation system with a Python Flask backend and React frontend, featuring smart recommendation algorithms and a modern user interface.

## 🌟 Features

### 🎯 Smart Recommendations
- **💡 Smart Recommendations**: Personalized movie suggestions
- **🎭 Content-Based Filtering**: Find movies similar to your favorites
- **👥 Collaborative Filtering**: Get recommendations based on similar users
- **🔀 Hybrid Approach**: Combines multiple recommendation algorithms
- **🎨 Genre-Focused**: Discover top movies in your preferred genre
- **🚫 Admin Restrictions**: Admin users cannot access movie recommendations (focused on management)

### 🖼️ Rich Movie Information
- **📸 Movie Posters**: High-quality poster images for all movies
- **🎬 YouTube Trailers**: Direct links to official movie trailers
- **📝 Movie Descriptions**: Comprehensive movie plot summaries
- **📊 Detailed Ratings**: User ratings and predicted ratings
- **🎭 Genre Classification**: Movies categorized by genre

### 🔐 User Authentication & Management
- **🔒 Secure Login**: JWT-based authentication
- **👤 User Profiles**: Personalized user accounts
- **⭐ Rating System**: Rate movies and see your history
- **🎯 Preferences**: Set your preferred movie genre
- **📧 Required Fields**: Email and age are now required during registration
- **👑 Enhanced Admin Panel**: Comprehensive user and movie management system

### 📱 Modern UI/UX
- **📱 Responsive Design**: Works on all devices
- **🎨 Material-UI**: Beautiful, modern interface with improved contrast
- **⚡ Fast Loading**: Optimized performance
- **🔍 Enhanced Search**: Smooth search experience without losing focus
- **🎨 Better Visibility**: Improved contrast and readability for all labels and text

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Node.js 16+
- PostgreSQL 12+

### Backend Setup
```bash
create database named 'movie_recommendation'
cd backend
pip install -r requirements.txt
python init_database.py
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
- `email`: Email address (unique, required)
- `age`: User age (required, 13-120)
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
- `POST /api/auth/register` - User registration (auto-login after signup)
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile

### Admin Endpoints (Admin Only)
- `GET /api/admin/movies` - Get all movies for admin management
- `POST /api/admin/movies` - Create a new movie
- `PUT /api/admin/movies/{id}` - Update an existing movie
- `DELETE /api/admin/movies/{id}` - Delete a movie and its ratings
- `GET /api/users` - Get all users (admin only)
- `POST /api/users` - Create new user (admin only)
- `DELETE /api/users/{id}` - Delete user (admin only)

## 🎯 Demo Accounts

| Username | Password | Role | Preferred Genre |
|----------|----------|------|-----------------|
| admin    | admin123 | Admin | Drama |
| alice    | alice123 | User | Drama |
| bob      | bob123   | User | Action |

## 👑 Enhanced Admin Functionality

### 🎛️ Tabbed Admin Dashboard
- **👥 User Management Tab**: Complete user administration
- **🎬 Movie Management Tab**: Comprehensive movie management
- **🔄 Easy Switching**: Seamless navigation between user and movie management

### 👥 User Management Features
- **📋 User List**: View all users in a comprehensive table
- **🔍 Smart Search**: Search users by username, name, or email
- **🎭 Role Filtering**: Filter users by role (user/admin)
- **➕ Add Users**: Create new users with all required fields
- **🗑️ Delete Users**: Remove users with confirmation
- **📊 User Details**: View email, age, preferred genre, role, and creation date
- **🎨 Visual Indicators**: Color-coded role chips and user icons

### 🎬 Movie Management Features
- **📋 Movie List**: View all movies with ratings and details
- **🔍 Smart Search**: Search movies by title or director
- **🎭 Genre Filtering**: Filter movies by genre
- **➕ Add Movies**: Create new movies with comprehensive details
- **✏️ Edit Movies**: Update existing movie information
- **🗑️ Delete Movies**: Remove movies with confirmation
- **⭐ Rating Display**: Show movie ratings with star icons
- **📊 Movie Details**: Title, genre, year, director, description, cast, poster URL, trailer URL

### 🎨 Enhanced UI/UX
- **🎨 Better Contrast**: Improved visibility for all labels and text
- **📱 Responsive Design**: Works perfectly on all screen sizes
- **⚡ Smooth Interactions**: No focus loss during search and typing
- **🎯 Clear Visual Hierarchy**: Bold headers, proper spacing, and visual organization
- **🔍 Instant Search**: Real-time filtering without API calls
- **💫 Professional Appearance**: Clean, modern interface with Material-UI

### 🔒 Security & Validation
- **🔐 JWT Authentication**: Secure token-based authentication
- **👑 Role Verification**: Server-side admin role checking
- **✅ Input Validation**: Comprehensive validation for all forms
- **🛡️ Data Integrity**: Proper cascade deletion and data cleanup
- **📧 Required Fields**: Email and age validation during registration

### 📊 Form Features
- **📝 Comprehensive Forms**: All necessary fields for users and movies
- **✅ Real-time Validation**: Immediate feedback on form inputs
- **🎨 Enhanced Styling**: Better contrast and visibility for all form elements
- **🔄 Auto-login**: New users are automatically logged in after registration
- **📱 Mobile-Friendly**: Responsive forms that work on all devices

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

## 🔧 Recent Improvements

### ✅ Enhanced Admin Dashboard
- **Tabbed Interface**: Separate tabs for user and movie management
- **Comprehensive User Management**: Add, view, and delete users
- **Advanced Movie Management**: Full CRUD operations for movies
- **Better Search Experience**: Smooth search without losing focus
- **Improved Contrast**: Better visibility for all UI elements

### ✅ User Registration Improvements
- **Required Fields**: Email and age are now mandatory
- **Auto-login**: New users are automatically logged in after registration
- **Better Validation**: Enhanced form validation and error handling
- **Improved UX**: Clear labels and better form styling

### ✅ UI/UX Enhancements
- **Better Contrast**: All labels and text are now more visible
- **Smooth Interactions**: No focus loss during typing
- **Professional Styling**: Enhanced visual hierarchy and spacing
- **Responsive Design**: Perfect functionality on all devices

### ✅ Security & Performance
- **Enhanced Security**: Better role verification and data validation
- **Improved Performance**: Client-side filtering for instant results
- **Data Integrity**: Proper cascade deletion and cleanup
- **Better Error Handling**: Comprehensive error messages and validation

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