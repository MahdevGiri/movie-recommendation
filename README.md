# 🎬 Movie Recommendation System

A full-stack movie recommendation system with a Python Flask backend and React TypeScript frontend. This project demonstrates modern web development practices with user authentication, personalized recommendations, and a responsive UI.

## 🌟 Features

### Backend (Python Flask)
- **🔐 JWT Authentication**: Secure login/registration with JWT tokens
- **🎯 Recommendation Algorithms**: Collaborative filtering, content-based filtering, and hybrid approaches
- **📊 PostgreSQL Database**: Robust data persistence with SQLAlchemy ORM
- **🔄 RESTful API**: Complete REST endpoints for all functionality
- **🔒 CORS Support**: Cross-origin resource sharing enabled
- **📈 User Profiles**: Personalized user accounts with preferences

### Frontend (React TypeScript)
- **🎨 Modern UI**: Material-UI components with dark theme
- **📱 Responsive Design**: Works seamlessly on desktop and mobile
- **🔐 Authentication**: Login/register with JWT token management
- **🎬 Movie Browsing**: Browse, search, and rate movies
- **💡 Smart Recommendations**: Personalized movie suggestions
- **👤 User Profiles**: Manage preferences and view rating history
- **⚡ TypeScript**: Full type safety and better development experience

## 🏗️ Project Structure

```
movie-recommendation/
├── backend/                 # Python Flask API
│   ├── api_server.py       # Main Flask application
│   ├── auth_system.py      # JWT authentication
│   ├── recommendation_system.py # Recommendation algorithms
│   ├── database_service.py # Database operations
│   ├── models.py           # SQLAlchemy models
│   ├── requirements.txt    # Python dependencies
│   └── README.md          # Backend documentation
├── frontend/               # React TypeScript app
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── contexts/      # React contexts
│   │   ├── types/         # TypeScript definitions
│   │   └── App.tsx        # Main app component
│   ├── package.json       # Node.js dependencies
│   └── README.md          # Frontend documentation
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Node.js 16+** and **npm** (for frontend)
2. **Python 3.7+** and **pip** (for backend)
3. **PostgreSQL 12+** database

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd movie-recommendation
   ```

2. **Set up the backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   python init_database.py
   ```

3. **Set up the frontend:**
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

1. **Start the backend server:**
   ```bash
   cd backend
   python api_server.py
   ```
   The API will be available at: http://localhost:5000

2. **Start the frontend development server:**
   ```bash
   cd frontend
   npm start
   ```
   The frontend will be available at: http://localhost:3000

3. **Open your browser:**
   Navigate to http://localhost:3000 to access the application

## 🔐 Default Login Credentials

Use any of these demo accounts:
- **Username:** `admin`, **Password:** `admin123`
- **Username:** `alice`, **Password:** `alice123`
- **Username:** `bob`, **Password:** `bob123`

## 📊 Dataset

The system includes a comprehensive dataset with:
- **49 Movies**: Popular movies with genres, years, ratings, and descriptions
- **10 Users**: Users with different preferences and age groups
- **145+ Ratings**: User ratings on a 1-5 scale with realistic patterns

### Sample Movies
- The Shawshank Redemption (Drama, 1994)
- The Godfather (Crime, 1972)
- The Dark Knight (Action, 2008)
- Inception (Sci-Fi, 2010)
- And many more...

## 🎯 API Endpoints

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
- `GET /api/recommendations/personalized` - Get personalized recommendations
- `GET /api/recommendations/popular` - Get popular movies

## 🔧 Development

### Backend Development
- **Framework**: Flask with Flask-CORS
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens
- **Recommendation Algorithms**: Collaborative filtering, content-based filtering, hybrid approach

### Frontend Development
- **Framework**: React 18 with TypeScript
- **UI Library**: Material-UI (MUI)
- **State Management**: React Context API
- **HTTP Client**: Axios
- **Routing**: React Router

### Available Scripts

**Backend:**
```bash
cd backend
python api_server.py          # Start development server
python init_database.py       # Initialize database
python test_login.py          # Run authentication tests
```

**Frontend:**
```bash
cd frontend
npm start                     # Start development server
npm build                     # Build for production
npm test                      # Run tests
```

## 🎨 Features in Detail

### User Authentication
- Secure JWT-based authentication
- User registration and login
- Password hashing with SHA-256
- Session management

### Movie Recommendations
- **Collaborative Filtering**: Based on similar users' preferences
- **Content-Based Filtering**: Based on movie features and genres
- **Hybrid Approach**: Combines both methods for better accuracy
- **Popular Movies**: Trending movies based on average ratings

### User Interface
- **Responsive Design**: Works on all screen sizes
- **Dark Theme**: Modern dark UI with Material-UI
- **Movie Cards**: Beautiful movie presentation with ratings
- **Search & Filter**: Find movies by title, genre, or year
- **Pagination**: Efficient browsing of large movie collections

### User Experience
- **Real-time Updates**: Instant feedback on ratings and recommendations
- **Loading States**: Smooth loading indicators
- **Error Handling**: User-friendly error messages
- **Navigation**: Intuitive navigation between pages

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: SHA-256 hashing for password security
- **CORS Configuration**: Proper cross-origin resource sharing
- **Input Validation**: Server-side validation of all inputs
- **SQL Injection Protection**: Parameterized queries with SQLAlchemy

## 📱 Responsive Design

The frontend is fully responsive and works on:
- **Desktop**: Full-featured experience with all controls
- **Tablet**: Optimized layout for medium screens
- **Mobile**: Touch-friendly interface for small screens

## 🚀 Deployment

### Backend Deployment
1. Set up a PostgreSQL database
2. Configure environment variables
3. Install Python dependencies
4. Run database migrations
5. Start the Flask application

### Frontend Deployment
1. Build the production version: `npm run build`
2. Deploy the `build` folder to your web server
3. Configure API endpoint URLs for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Material-UI** for the beautiful UI components
- **Flask** for the robust backend framework
- **PostgreSQL** for the reliable database
- **React** for the modern frontend framework

## 📞 Support

If you encounter any issues or have questions:
1. Check the documentation in the `backend/README.md` and `frontend/README.md` files
2. Review the API endpoints and their usage
3. Check the console for error messages
4. Ensure both backend and frontend servers are running

---

**Happy Movie Watching! 🎬✨** 