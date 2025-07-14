# 🎬 Movie Recommendation System - Complete Setup Guide

This guide will help you set up both the Python backend API and React frontend for the Movie Recommendation System.

## 📋 Prerequisites

- **Python 3.7+**
- **Node.js 16+**
- **PostgreSQL 12+**
- **npm or yarn**

## 🚀 Quick Setup

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Initialize database (creates .env file and seeds data)
python init_database.py

# Start the API server
python api_server.py
```

The backend will be available at: http://localhost:5000

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the React development server
npm start
```

The frontend will be available at: http://localhost:3000

## 🔧 Detailed Setup

### Backend Configuration

1. **Database Setup:**
   - Install PostgreSQL
   - Create database: `movie_recommendation`
   - Update `.env` file with your database credentials

2. **API Endpoints Available:**
   - `GET /api/health` - Health check
   - `POST /api/auth/login` - User login
   - `POST /api/auth/register` - User registration
   - `GET /api/movies` - Get movies
   - `GET /api/recommendations/personalized` - Get recommendations
   - And many more...

### Frontend Features

- **Authentication System** - Login/Register with JWT
- **Movie Browsing** - Browse and search movies
- **Recommendations** - Personalized movie suggestions
- **User Profiles** - Manage preferences
- **Responsive Design** - Works on all devices

## 🎯 Demo Accounts

Use these pre-configured accounts to test the system:

| Username | Password | Role | Preferred Genre |
|----------|----------|------|-----------------|
| admin    | admin123 | Admin | Drama |
| alice    | alice123 | User | Drama |
| bob      | bob123   | User | Action |
| charlie  | charlie123 | User | Sci-Fi |

## 🛠️ Development

### Backend Development
```bash
cd backend
# The API server runs in debug mode by default
python api_server.py
```

### Frontend Development
```bash
cd frontend
npm start
# Hot reload enabled
```

### Database Management
```bash
cd backend
# Reset database
python database_seeder.py --clear
python init_database.py
```

## 📁 Project Structure

```
movie-recommendation/
├── backend/                 # Python Flask API
│   ├── api_server.py       # Main API server
│   ├── models.py           # Database models
│   ├── recommendation_system.py # Core algorithms
│   ├── auth_system.py      # Authentication
│   ├── database_service.py # Database operations
│   └── requirements.txt    # Python dependencies
├── frontend/               # React TypeScript app
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── contexts/      # React contexts
│   │   └── types/         # TypeScript types
│   ├── package.json       # Node.js dependencies
│   └── tsconfig.json      # TypeScript config
└── README.md              # Main documentation
```

## 🔐 Security Features

- **JWT Authentication** - Secure token-based auth
- **Password Hashing** - SHA-256 encryption
- **CORS Protection** - Cross-origin security
- **Input Validation** - Server-side validation

## 🎨 UI/UX Features

- **Dark Theme** - Modern dark interface
- **Material-UI** - Professional components
- **Responsive Design** - Mobile-friendly
- **Toast Notifications** - User feedback
- **Loading States** - Better UX

## 🚀 Production Deployment

### Backend (Python)
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api_server:app
```

### Frontend (React)
```bash
# Build for production
npm run build

# Serve with nginx or similar
```

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check PostgreSQL is running
   - Verify `.env` file credentials
   - Ensure database exists

2. **Frontend Build Errors**
   - Clear node_modules: `rm -rf node_modules && npm install`
   - Check Node.js version: `node --version`

3. **API Connection Issues**
   - Verify backend is running on port 5000
   - Check CORS settings
   - Ensure proxy configuration in package.json

## 📞 Support

If you encounter any issues:
1. Check the console for error messages
2. Verify all prerequisites are installed
3. Ensure both backend and frontend are running
4. Check the database connection

---

**🎬 Enjoy exploring the Movie Recommendation System!** 