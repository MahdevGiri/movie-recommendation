# 👑 Admin Functionality Setup Guide

This guide provides comprehensive documentation for the admin functionality in the Movie Recommendation System.

## 🚀 Quick Setup

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python init_database.py
python create_admin.py  # Creates admin user
python api_server.py
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 3. Access Admin Panel
1. Open http://localhost:3000 in your browser
2. Login with admin credentials:
   - **Username**: `admin`
   - **Password**: `admin123`
3. Click "Admin" in the navigation bar
4. You'll be redirected to `/admin` page

## 🎯 Admin Features

### Movie Management
- **Add Movies**: Create new movies with full details
- **Edit Movies**: Update existing movie information
- **Delete Movies**: Remove movies and their ratings
- **Search Movies**: Find movies by title
- **Filter by Genre**: View movies by specific genre
- **Pagination**: Navigate through large collections

### Admin Dashboard
- **Movie Grid**: Visual display of all movies
- **Action Buttons**: Edit and delete buttons on each movie card
- **Add Movie Button**: Quick access to create new movies
- **Search Bar**: Real-time search functionality
- **Genre Filter**: Dropdown to filter by genre
- **Pagination Controls**: Navigate through pages

## 🔧 API Endpoints

### Admin Movie Management
```
GET    /api/admin/movies          # Get all movies (admin only)
POST   /api/admin/movies          # Create new movie (admin only)
PUT    /api/admin/movies/{id}     # Update movie (admin only)
DELETE /api/admin/movies/{id}     # Delete movie (admin only)
```

### User Management
```
GET    /api/users                 # Get all users (admin only)
```

### Authentication
```
POST   /api/auth/login           # Login (returns JWT token)
GET    /api/auth/profile         # Get current user profile
```

## 🛡️ Security Implementation

### Backend Security
```python
# Admin role verification
def require_admin():
    user_id = get_jwt_identity()
    current_user = db_service.get_user_by_id(user_id)
    
    if not current_user or current_user.role != 'admin':
        return False, 'Admin access required'
    return True, current_user

# Protected admin endpoints
@app.route('/api/admin/movies', methods=['GET'])
@jwt_required()
def admin_get_movies():
    is_admin, current_user = require_admin()
    if not is_admin:
        return jsonify({'error': current_user}), 403
    # ... admin logic
```

### Frontend Security
```typescript
// Role-based access control
if (!user || user.role !== 'admin') {
  return (
    <Box sx={{ p: 3 }}>
      <Alert severity="error">
        Access denied. Admin privileges required.
      </Alert>
    </Box>
  );
}

// Conditional navigation
{user.role === 'admin' && (
  <Button component={RouterLink} to="/admin">
    Admin
  </Button>
)}
```

## 📊 Database Schema

### User Model
```python
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    age = Column(Integer)
    preferred_genre = Column(String(50))
    role = Column(String(20), default="user")  # "user" or "admin"
```

### Movie Model
```python
class Movie(Base):
    __tablename__ = 'movies'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    genre = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float)
    description = Column(Text)
    director = Column(String(100))
    cast = Column(Text)
    poster_url = Column(String(500))
    trailer_url = Column(String(500))
```

## 🎨 Frontend Components

### Admin Page Structure
```typescript
const Admin: React.FC = () => {
  // State management
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(true);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingMovie, setEditingMovie] = useState<Movie | null>(null);
  
  // Role-based access control
  if (!user || user.role !== 'admin') {
    return <AccessDenied />;
  }
  
  // API calls
  const fetchMovies = async () => {
    const response = await api.get('/admin/movies');
    setMovies(response.data.movies);
  };
  
  // CRUD operations
  const handleSubmit = async (formData) => {
    if (editingMovie) {
      await api.put(`/admin/movies/${editingMovie.id}`, formData);
    } else {
      await api.post('/admin/movies', formData);
    }
  };
  
  const handleDelete = async (movieId) => {
    await api.delete(`/admin/movies/${movieId}`);
  };
};
```

### Movie Form Dialog
```typescript
<Dialog open={openDialog} maxWidth="md" fullWidth>
  <DialogTitle>
    {editingMovie ? 'Edit Movie' : 'Add New Movie'}
  </DialogTitle>
  <form onSubmit={handleSubmit}>
    <DialogContent>
      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <TextField
            name="title"
            label="Title"
            required
            fullWidth
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <FormControl fullWidth required>
            <InputLabel>Genre</InputLabel>
            <Select name="genre">
              {genres.map(genre => (
                <MenuItem key={genre} value={genre}>
                  {genre}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        {/* More form fields */}
      </Grid>
    </DialogContent>
    <DialogActions>
      <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
      <Button type="submit" variant="contained">
        {editingMovie ? 'Update' : 'Create'}
      </Button>
    </DialogActions>
  </form>
</Dialog>
```

## 🔍 Search and Filtering

### Backend Implementation
```python
def admin_get_movies():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    genre = request.args.get('genre')
    search = request.args.get('search')
    
    movies = db_service.get_movies(
        page=page, 
        per_page=per_page, 
        genre=genre, 
        search=search
    )
    
    return jsonify({
        'movies': movies,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total
        }
    })
```

### Frontend Implementation
```typescript
const fetchMovies = async () => {
  const params = new URLSearchParams({
    page: page.toString(),
    per_page: '10',
  });
  
  if (searchTerm) params.append('search', searchTerm);
  if (selectedGenre) params.append('genre', selectedGenre);
  
  const response = await api.get(`/admin/movies?${params}`);
  setMovies(response.data.movies);
  setTotalPages(Math.ceil(response.data.pagination.total / 10));
};
```

## 🧪 Testing

### Create Admin User
```bash
cd backend
python create_admin.py
```

### Test Admin Endpoints
```bash
# Test admin login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Test admin movie access
curl -X GET http://localhost:5000/api/admin/movies \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Manual Testing Checklist
- [ ] Login as admin user
- [ ] Access admin dashboard
- [ ] View all movies
- [ ] Search for specific movies
- [ ] Filter by genre
- [ ] Add a new movie
- [ ] Edit an existing movie
- [ ] Delete a movie
- [ ] Test pagination
- [ ] Verify role-based access (try accessing as non-admin)

## 🚨 Troubleshooting

### Common Issues

#### 1. Admin User Not Found
```bash
# Solution: Create admin user
cd backend
python create_admin.py
```

#### 2. Frontend Compilation Errors
```bash
# Solution: Fix import issues
# Change: import { api } from '../services/api';
# To: import api from '../services/api';
```

#### 3. API Connection Errors
```bash
# Check if backend is running
netstat -an | findstr :5000

# Check if frontend is running
netstat -an | findstr :3000
```

#### 4. Permission Denied Errors
- Ensure you're logged in as admin user
- Check that user has `role: "admin"` in database
- Verify JWT token is valid

### Debug Commands
```bash
# Check admin user in database
python -c "from backend.database_service import DatabaseService; db = DatabaseService(); admin = db.get_user_by_username('admin'); print(f'Admin: {admin.username}, Role: {admin.role}')"

# Test admin authentication
python -c "from backend.auth_system import AuthSystem; auth = AuthSystem(); success = auth.login('admin', 'admin123'); print(f'Login success: {success}')"
```

## 🔄 Future Enhancements

### Planned Features
- **Bulk Operations**: Select multiple movies for batch operations
- **Movie Import**: Import movies from CSV/JSON files
- **Advanced Search**: Search by director, cast, year range
- **Image Upload**: Direct image upload for movie posters
- **Audit Log**: Track admin actions and changes
- **User Management**: Admin ability to manage user accounts
- **Analytics Dashboard**: View system usage statistics

### Technical Improvements
- **Caching**: Implement Redis caching for better performance
- **File Upload**: Add support for direct file uploads
- **API Rate Limiting**: Implement rate limiting for admin endpoints
- **Enhanced Validation**: More comprehensive input validation
- **Backup System**: Automated database backups

## 📚 Additional Resources

- [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/)
- [Material-UI Components](https://mui.com/material-ui/)
- [React Router Documentation](https://reactrouter.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)

---

**🎬 The admin functionality is now fully operational! Enjoy managing your movie collection with ease and security.** 