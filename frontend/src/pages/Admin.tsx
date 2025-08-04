import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import toast from 'react-hot-toast';
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Grid,
  Chip,
  Alert,
  CircularProgress,
  Pagination,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Tabs,
  Tab,
  Rating as MuiRating,
} from '@mui/material';
import { 
  Add as AddIcon, 
  Delete as DeleteIcon, 
  Edit as EditIcon,
  Person as PersonIcon,
  Movie as MovieIcon,
  Star as StarIcon
} from '@mui/icons-material';
import { Movie } from '../types';

interface User {
  id: number;
  username: string;
  name: string;
  email: string;
  age: number;
  preferred_genre: string;
  role: string;
  created_at: string;
}

interface UserFormData {
  username: string;
  password: string;
  name: string;
  email: string;
  age: number;
  preferred_genre: string;
  role: string;
}

interface MovieFormData {
  title: string;
  genre: string;
  year: number;
  rating: number;
  description: string;
  director: string;
  cast: string;
  poster_url: string;
  trailer_url: string;
}

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`admin-tabpanel-${index}`}
      aria-labelledby={`admin-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

const Admin: React.FC = () => {
  const { user } = useAuth();
  const [tabValue, setTabValue] = useState(0);
  
  // User management state
  const [users, setUsers] = useState<User[]>([]);
  const [userLoading, setUserLoading] = useState(true);
  const [openUserDialog, setOpenUserDialog] = useState(false);
  const [userFormData, setUserFormData] = useState<UserFormData>({
    username: '',
    password: '',
    name: '',
    email: '',
    age: 18,
    preferred_genre: 'Drama',
    role: 'user',
  });
  const [userSearchTerm, setUserSearchTerm] = useState('');
  const [selectedUserRole, setSelectedUserRole] = useState<string>('');

  // Movie management state
  const [movies, setMovies] = useState<Movie[]>([]);
  const [movieLoading, setMovieLoading] = useState(true);
  const [openMovieDialog, setOpenMovieDialog] = useState(false);
  const [editingMovie, setEditingMovie] = useState<Movie | null>(null);
  const [movieFormData, setMovieFormData] = useState<MovieFormData>({
    title: '',
    genre: 'Drama',
    year: new Date().getFullYear(),
    rating: 0,
    description: '',
    director: '',
    cast: '',
    poster_url: '',
    trailer_url: '',
  });
  const [movieSearchTerm, setMovieSearchTerm] = useState('');
  const [selectedMovieGenre, setSelectedMovieGenre] = useState<string>('');

  useEffect(() => {
    if (tabValue === 0) {
      fetchUsers();
    } else {
      fetchMovies();
    }
  }, [tabValue]); // Removed search terms from dependencies

  // Check if user is admin
  if (!user || user.role !== 'admin') {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error">
          Access denied. Admin privileges required.
        </Alert>
      </Box>
    );
  }

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  // User management functions
  const fetchUsers = async () => {
    try {
      setUserLoading(true);
      const response = await api.get('/users');
      setUsers(response.data.users);
    } catch (error: any) {
      toast.error('Failed to fetch users');
      console.error('Error fetching users:', error);
    } finally {
      setUserLoading(false);
    }
  };

  const handleUserSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
              await api.post('/users', userFormData);
      toast.success('User created successfully!');
      
      setOpenUserDialog(false);
      resetUserForm();
      fetchUsers();
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Operation failed');
    }
  };

  const handleUserDelete = async (userId: number, username: string) => {
    if (!window.confirm(`Are you sure you want to delete user "${username}"?`)) {
      return;
    }

    try {
              await api.delete(`/users/${userId}`);
      toast.success('User deleted successfully!');
      fetchUsers();
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Failed to delete user');
    }
  };

  const resetUserForm = () => {
    setUserFormData({
      username: '',
      password: '',
      name: '',
      email: '',
      age: 18,
      preferred_genre: 'Drama',
      role: 'user',
    });
  };

  const handleUserInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setUserFormData(prev => ({
      ...prev,
      [name]: name === 'age' ? parseInt(value) || 18 : value,
    }));
  };

  const handleUserSelectChange = (e: SelectChangeEvent) => {
    const { name, value } = e.target;
    setUserFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  // Movie management functions
  const fetchMovies = async () => {
    try {
      setMovieLoading(true);
      console.log('Fetching movies from admin endpoint...');
      const response = await api.get('/admin/movies');
      console.log('Movies response:', response.data);
      setMovies(response.data.movies);
      console.log('Movies state updated:', response.data.movies);
    } catch (error: any) {
      console.error('Error fetching movies:', error);
      toast.error('Failed to fetch movies');
    } finally {
      setMovieLoading(false);
    }
  };

  const handleMovieSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      if (editingMovie) {
        console.log('Updating movie:', editingMovie.id, 'with data:', movieFormData);
        const response = await api.put(`/admin/movies/${editingMovie.id}`, movieFormData);
        console.log('Update response:', response.data);
        toast.success('Movie updated successfully!');
        
        // Clear search and filter terms to ensure the updated movie shows up
        setMovieSearchTerm('');
        setSelectedMovieGenre('');
      } else {
        console.log('Creating new movie with data:', movieFormData);
        const response = await api.post('/admin/movies', movieFormData);
        console.log('Create response:', response.data);
        toast.success('Movie created successfully!');
      }
      
      setOpenMovieDialog(false);
      resetMovieForm();
      
      // Fetch updated movies list
      await fetchMovies();
      
      console.log('Movies after update:', movies);
    } catch (error: any) {
      console.error('Movie operation failed:', error);
      toast.error(error.response?.data?.error || 'Operation failed');
    }
  };

  const handleMovieDelete = async (movieId: number, title: string) => {
    if (!window.confirm(`Are you sure you want to delete movie "${title}"?`)) {
      return;
    }

    try {
      await api.delete(`/admin/movies/${movieId}`);
      toast.success('Movie deleted successfully!');
      fetchMovies();
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Failed to delete movie');
    }
  };

  const handleMovieEdit = (movie: Movie) => {
    setEditingMovie(movie);
    setMovieFormData({
      title: movie.title,
      genre: movie.genre,
      year: movie.year,
      rating: movie.rating || 0,
      description: movie.description || '',
      director: movie.director || '',
      cast: movie.cast || '',
      poster_url: movie.poster_url || '',
      trailer_url: movie.trailer_url || '',
    });
    setOpenMovieDialog(true);
  };

  const resetMovieForm = () => {
    setEditingMovie(null);
    setMovieFormData({
      title: '',
      genre: 'Drama',
      year: new Date().getFullYear(),
      rating: 0,
      description: '',
      director: '',
      cast: '',
      poster_url: '',
      trailer_url: '',
    });
  };

  const handleMovieInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setMovieFormData(prev => ({
      ...prev,
      [name]: name === 'year' ? parseInt(value) || new Date().getFullYear() : 
              name === 'rating' ? parseFloat(value) || 0 : value,
    }));
  };

  const handleMovieSelectChange = (e: SelectChangeEvent) => {
    const { name, value } = e.target;
    setMovieFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const getRoleColor = (role: string) => {
    return role === 'admin' ? 'error' : 'primary';
  };

  const filteredUsers = users.filter(user => {
    const matchesSearch = user.username.toLowerCase().includes(userSearchTerm.toLowerCase()) ||
                         user.name.toLowerCase().includes(userSearchTerm.toLowerCase()) ||
                         user.email.toLowerCase().includes(userSearchTerm.toLowerCase());
    const matchesRole = !selectedUserRole || user.role === selectedUserRole;
    return matchesSearch && matchesRole;
  });

  const filteredMovies = movies.filter(movie => {
    const matchesSearch = movie.title.toLowerCase().includes(movieSearchTerm.toLowerCase()) ||
                         (movie.director && movie.director.toLowerCase().includes(movieSearchTerm.toLowerCase()));
    const matchesGenre = !selectedMovieGenre || movie.genre === selectedMovieGenre;
    
    // Debug logging for movie filtering
    if (movie.title.toLowerCase().includes('inception')) {
      console.log('Inception movie found:', movie);
      console.log('Search term:', movieSearchTerm, 'Matches search:', matchesSearch);
      console.log('Selected genre:', selectedMovieGenre, 'Matches genre:', matchesGenre);
    }
    
    return matchesSearch && matchesGenre;
  });

  if (userLoading && tabValue === 0) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (movieLoading && tabValue === 1) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" sx={{ mb: 3 }}>
        👑 Admin Dashboard
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="admin tabs">
          <Tab 
            icon={<PersonIcon />} 
            label="User Management" 
            iconPosition="start"
          />
          <Tab 
            icon={<MovieIcon />} 
            label="Movie Management" 
            iconPosition="start"
          />
        </Tabs>
      </Box>

      {/* User Management Tab */}
      <TabPanel value={tabValue} index={0}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h5" component="h2">
            User Management
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setOpenUserDialog(true)}
          >
            Add User
          </Button>
        </Box>

        {/* User Search and Filter */}
        <Box sx={{ mb: 3 }}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Search users"
                value={userSearchTerm}
                onChange={(e) => setUserSearchTerm(e.target.value)}
                placeholder="Search by username, name, or email..."
                sx={{
                  '& .MuiInputLabel-root': {
                    color: 'text.primary',
                    fontWeight: 'medium',
                  },
                  '& .MuiInputLabel-root.Mui-focused': {
                    color: 'primary.main',
                    fontWeight: 'bold',
                  },
                  '& .MuiOutlinedInput-root': {
                    '& fieldset': {
                      borderColor: 'grey.400',
                    },
                    '&:hover fieldset': {
                      borderColor: 'primary.main',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: 'primary.main',
                      borderWidth: 2,
                    },
                  },
                }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth
                sx={{
                  '& .MuiInputLabel-root': {
                    color: 'text.primary',
                    fontWeight: 'medium',
                  },
                  '& .MuiInputLabel-root.Mui-focused': {
                    color: 'primary.main',
                    fontWeight: 'bold',
                  },
                  '& .MuiOutlinedInput-root': {
                    '& fieldset': {
                      borderColor: 'grey.400',
                    },
                    '&:hover fieldset': {
                      borderColor: 'primary.main',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: 'primary.main',
                      borderWidth: 2,
                    },
                  },
                }}
              >
                <InputLabel>Filter by Role</InputLabel>
                <Select
                  value={selectedUserRole}
                  label="Filter by Role"
                  onChange={(e) => setSelectedUserRole(e.target.value)}
                >
                  <MenuItem value="">All Roles</MenuItem>
                  <MenuItem value="user">User</MenuItem>
                  <MenuItem value="admin">Admin</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </Box>

        {/* Users Table */}
        <TableContainer component={Paper} sx={{ mb: 3 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary', backgroundColor: 'grey.100' }}>User</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary', backgroundColor: 'grey.100' }}>Email</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary', backgroundColor: 'grey.100' }}>Age</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary', backgroundColor: 'grey.100' }}>Preferred Genre</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary', backgroundColor: 'grey.100' }}>Role</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary', backgroundColor: 'grey.100' }}>Created</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary', backgroundColor: 'grey.100' }}>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredUsers.map((user) => (
                <TableRow key={user.id}>
                  <TableCell>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <PersonIcon color="primary" />
                      <Box>
                        <Typography variant="subtitle2">{user.name}</Typography>
                        <Typography variant="caption" color="text.secondary">
                          @{user.username}
                        </Typography>
                      </Box>
                    </Box>
                  </TableCell>
                  <TableCell>{user.email}</TableCell>
                  <TableCell>{user.age}</TableCell>
                  <TableCell>
                    <Chip label={user.preferred_genre} size="small" />
                  </TableCell>
                  <TableCell>
                    <Chip 
                      label={user.role} 
                      size="small" 
                      color={getRoleColor(user.role)}
                    />
                  </TableCell>
                  <TableCell>
                    {new Date(user.created_at).toLocaleDateString()}
                  </TableCell>
                  <TableCell>
                    <IconButton
                      size="small"
                      color="error"
                      onClick={() => handleUserDelete(user.id, user.username)}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      {/* Movie Management Tab */}
      <TabPanel value={tabValue} index={1}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h5" component="h2">
            Movie Management
          </Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              variant="outlined"
              onClick={() => {
                setMovieSearchTerm('');
                setSelectedMovieGenre('');
                fetchMovies();
              }}
            >
              Refresh
            </Button>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => setOpenMovieDialog(true)}
            >
              Add Movie
            </Button>
          </Box>
        </Box>

        {/* Movie Search and Filter */}
        <Box sx={{ mb: 3 }}>
          <Alert severity="info" sx={{ mb: 2 }}>
            <Typography variant="body2">
              💡 <strong>Tip:</strong> After updating a movie, use the "Refresh" button to see all movies. 
              Search and filter terms are automatically cleared after updates to ensure you can see the updated movie.
            </Typography>
          </Alert>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Search movies"
                value={movieSearchTerm}
                onChange={(e) => setMovieSearchTerm(e.target.value)}
                placeholder="Search by title or director..."
                sx={{
                  '& .MuiInputLabel-root': {
                    color: 'text.primary',
                    fontWeight: 'medium',
                  },
                  '& .MuiInputLabel-root.Mui-focused': {
                    color: 'primary.main',
                    fontWeight: 'bold',
                  },
                  '& .MuiOutlinedInput-root': {
                    '& fieldset': {
                      borderColor: 'grey.400',
                    },
                    '&:hover fieldset': {
                      borderColor: 'primary.main',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: 'primary.main',
                      borderWidth: 2,
                    },
                  },
                }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth
                sx={{
                  '& .MuiInputLabel-root': {
                    color: 'text.primary',
                    fontWeight: 'medium',
                  },
                  '& .MuiInputLabel-root.Mui-focused': {
                    color: 'primary.main',
                    fontWeight: 'bold',
                  },
                  '& .MuiOutlinedInput-root': {
                    '& fieldset': {
                      borderColor: 'grey.400',
                    },
                    '&:hover fieldset': {
                      borderColor: 'primary.main',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: 'primary.main',
                      borderWidth: 2,
                    },
                  },
                }}
              >
                <InputLabel>Filter by Genre</InputLabel>
                <Select
                  value={selectedMovieGenre}
                  label="Filter by Genre"
                  onChange={(e) => setSelectedMovieGenre(e.target.value)}
                >
                  <MenuItem value="">All Genres</MenuItem>
                  <MenuItem value="Drama">Drama</MenuItem>
                  <MenuItem value="Comedy">Comedy</MenuItem>
                  <MenuItem value="Action">Action</MenuItem>
                  <MenuItem value="Thriller">Thriller</MenuItem>
                  <MenuItem value="Romance">Romance</MenuItem>
                  <MenuItem value="Sci-Fi">Sci-Fi</MenuItem>
                  <MenuItem value="Horror">Horror</MenuItem>
                  <MenuItem value="Documentary">Documentary</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </Box>

        {/* Movies Table */}
        <TableContainer component={Paper} sx={{ mb: 3 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary', backgroundColor: 'grey.100' }}>Movie</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary', backgroundColor: 'grey.100' }}>Genre</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary', backgroundColor: 'grey.100' }}>Year</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary', backgroundColor: 'grey.100' }}>Director</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary', backgroundColor: 'grey.100' }}>Rating</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary', backgroundColor: 'grey.100' }}>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredMovies.map((movie) => (
                <TableRow key={movie.id}>
                  <TableCell>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <MovieIcon color="primary" />
                      <Box>
                        <Typography variant="subtitle2">{movie.title}</Typography>
                        {movie.description && (
                          <Typography variant="caption" color="text.secondary" sx={{ display: 'block' }}>
                            {movie.description.length > 50 ? `${movie.description.substring(0, 50)}...` : movie.description}
                          </Typography>
                        )}
                      </Box>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Chip label={movie.genre} size="small" />
                  </TableCell>
                  <TableCell>{movie.year}</TableCell>
                  <TableCell>{movie.director || '-'}</TableCell>
                  <TableCell>
                    {movie.rating ? (
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <MuiRating value={movie.rating} readOnly size="small" />
                        <Typography variant="caption">({movie.rating.toFixed(1)})</Typography>
                      </Box>
                    ) : (
                      <Typography variant="caption" color="text.secondary">No ratings</Typography>
                    )}
                  </TableCell>
                  <TableCell>
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <IconButton
                        size="small"
                        color="primary"
                        onClick={() => handleMovieEdit(movie)}
                      >
                        <EditIcon />
                      </IconButton>
                      <IconButton
                        size="small"
                        color="error"
                        onClick={() => handleMovieDelete(movie.id, movie.title)}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </Box>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      {/* Add/Edit User Dialog */}
      <Dialog open={openUserDialog} onClose={() => setOpenUserDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          Add New User
        </DialogTitle>
        <form onSubmit={handleUserSubmit}>
          <DialogContent>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Username"
                  name="username"
                  value={userFormData.username}
                  onChange={handleUserInputChange}
                  required
                  margin="normal"
                  sx={{
                    '& .MuiInputLabel-root': {
                      color: 'text.primary',
                      fontWeight: 'medium',
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                      color: 'primary.main',
                      fontWeight: 'bold',
                    },
                    '& .MuiOutlinedInput-root': {
                      '& fieldset': {
                        borderColor: 'grey.400',
                      },
                      '&:hover fieldset': {
                        borderColor: 'primary.main',
                      },
                      '&.Mui-focused fieldset': {
                        borderColor: 'primary.main',
                        borderWidth: 2,
                      },
                    },
                  }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Password"
                  name="password"
                  type="password"
                  value={userFormData.password}
                  onChange={handleUserInputChange}
                  required
                  margin="normal"
                  sx={{
                    '& .MuiInputLabel-root': {
                      color: 'text.primary',
                      fontWeight: 'medium',
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                      color: 'primary.main',
                      fontWeight: 'bold',
                    },
                    '& .MuiOutlinedInput-root': {
                      '& fieldset': {
                        borderColor: 'grey.400',
                      },
                      '&:hover fieldset': {
                        borderColor: 'primary.main',
                      },
                      '&.Mui-focused fieldset': {
                        borderColor: 'primary.main',
                        borderWidth: 2,
                      },
                    },
                  }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Full Name"
                  name="name"
                  value={userFormData.name}
                  onChange={handleUserInputChange}
                  required
                  margin="normal"
                  sx={{
                    '& .MuiInputLabel-root': {
                      color: 'text.primary',
                      fontWeight: 'medium',
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                      color: 'primary.main',
                      fontWeight: 'bold',
                    },
                    '& .MuiOutlinedInput-root': {
                      '& fieldset': {
                        borderColor: 'grey.400',
                      },
                      '&:hover fieldset': {
                        borderColor: 'primary.main',
                      },
                      '&.Mui-focused fieldset': {
                        borderColor: 'primary.main',
                        borderWidth: 2,
                      },
                    },
                  }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Email"
                  name="email"
                  type="email"
                  value={userFormData.email}
                  onChange={handleUserInputChange}
                  required
                  margin="normal"
                  sx={{
                    '& .MuiInputLabel-root': {
                      color: 'text.primary',
                      fontWeight: 'medium',
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                      color: 'primary.main',
                      fontWeight: 'bold',
                    },
                    '& .MuiOutlinedInput-root': {
                      '& fieldset': {
                        borderColor: 'grey.400',
                      },
                      '&:hover fieldset': {
                        borderColor: 'primary.main',
                      },
                      '&.Mui-focused fieldset': {
                        borderColor: 'primary.main',
                        borderWidth: 2,
                      },
                    },
                  }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Age"
                  name="age"
                  type="number"
                  value={userFormData.age}
                  onChange={handleUserInputChange}
                  required
                  margin="normal"
                  inputProps={{ min: 13, max: 120 }}
                  sx={{
                    '& .MuiInputLabel-root': {
                      color: 'text.primary',
                      fontWeight: 'medium',
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                      color: 'primary.main',
                      fontWeight: 'bold',
                    },
                    '& .MuiOutlinedInput-root': {
                      '& fieldset': {
                        borderColor: 'grey.400',
                      },
                      '&:hover fieldset': {
                        borderColor: 'primary.main',
                      },
                      '&.Mui-focused fieldset': {
                        borderColor: 'primary.main',
                        borderWidth: 2,
                      },
                    },
                  }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth margin="normal" required
                  sx={{
                    '& .MuiInputLabel-root': {
                      color: 'text.primary',
                      fontWeight: 'medium',
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                      color: 'primary.main',
                      fontWeight: 'bold',
                    },
                    '& .MuiOutlinedInput-root': {
                      '& fieldset': {
                        borderColor: 'grey.400',
                      },
                      '&:hover fieldset': {
                        borderColor: 'primary.main',
                      },
                      '&.Mui-focused fieldset': {
                        borderColor: 'primary.main',
                        borderWidth: 2,
                      },
                    },
                  }}
                >
                  <InputLabel>Preferred Genre</InputLabel>
                  <Select
                    name="preferred_genre"
                    value={userFormData.preferred_genre}
                    label="Preferred Genre"
                    onChange={handleUserSelectChange}
                  >
                    <MenuItem value="Drama">Drama</MenuItem>
                    <MenuItem value="Comedy">Comedy</MenuItem>
                    <MenuItem value="Action">Action</MenuItem>
                    <MenuItem value="Thriller">Thriller</MenuItem>
                    <MenuItem value="Romance">Romance</MenuItem>
                    <MenuItem value="Sci-Fi">Sci-Fi</MenuItem>
                    <MenuItem value="Horror">Horror</MenuItem>
                    <MenuItem value="Documentary">Documentary</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth margin="normal" required
                  sx={{
                    '& .MuiInputLabel-root': {
                      color: 'text.primary',
                      fontWeight: 'medium',
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                      color: 'primary.main',
                      fontWeight: 'bold',
                    },
                    '& .MuiOutlinedInput-root': {
                      '& fieldset': {
                        borderColor: 'grey.400',
                      },
                      '&:hover fieldset': {
                        borderColor: 'primary.main',
                      },
                      '&.Mui-focused fieldset': {
                        borderColor: 'primary.main',
                        borderWidth: 2,
                      },
                    },
                  }}
                >
                  <InputLabel>Role</InputLabel>
                  <Select
                    name="role"
                    value={userFormData.role}
                    label="Role"
                    onChange={handleUserSelectChange}
                  >
                    <MenuItem value="user">User</MenuItem>
                    <MenuItem value="admin">Admin</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenUserDialog(false)}>
              Cancel
            </Button>
            <Button type="submit" variant="contained">
              Create User
            </Button>
          </DialogActions>
        </form>
      </Dialog>

      {/* Add/Edit Movie Dialog */}
      <Dialog open={openMovieDialog} onClose={() => setOpenMovieDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingMovie ? 'Edit Movie' : 'Add New Movie'}
        </DialogTitle>
        <form onSubmit={handleMovieSubmit}>
          <DialogContent>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Title"
                  name="title"
                  value={movieFormData.title}
                  onChange={handleMovieInputChange}
                  required
                  margin="normal"
                  sx={{
                    '& .MuiInputLabel-root': {
                      color: 'text.primary',
                      fontWeight: 'medium',
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                      color: 'primary.main',
                      fontWeight: 'bold',
                    },
                    '& .MuiOutlinedInput-root': {
                      '& fieldset': {
                        borderColor: 'grey.400',
                      },
                      '&:hover fieldset': {
                        borderColor: 'primary.main',
                      },
                      '&.Mui-focused fieldset': {
                        borderColor: 'primary.main',
                        borderWidth: 2,
                      },
                    },
                  }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Year"
                  name="year"
                  type="number"
                  value={movieFormData.year}
                  onChange={handleMovieInputChange}
                  required
                  margin="normal"
                  inputProps={{ min: 1900, max: 2030 }}
                  sx={{
                    '& .MuiInputLabel-root': {
                      color: 'text.primary',
                      fontWeight: 'medium',
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                      color: 'primary.main',
                      fontWeight: 'bold',
                    },
                    '& .MuiOutlinedInput-root': {
                      '& fieldset': {
                        borderColor: 'grey.400',
                      },
                      '&:hover fieldset': {
                        borderColor: 'primary.main',
                      },
                      '&.Mui-focused fieldset': {
                        borderColor: 'primary.main',
                        borderWidth: 2,
                      },
                    },
                  }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth margin="normal" required
                  sx={{
                    '& .MuiInputLabel-root': {
                      color: 'text.primary',
                      fontWeight: 'medium',
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                      color: 'primary.main',
                      fontWeight: 'bold',
                    },
                    '& .MuiOutlinedInput-root': {
                      '& fieldset': {
                        borderColor: 'grey.400',
                      },
                      '&:hover fieldset': {
                        borderColor: 'primary.main',
                      },
                      '&.Mui-focused fieldset': {
                        borderColor: 'primary.main',
                        borderWidth: 2,
                      },
                    },
                  }}
                >
                  <InputLabel>Genre</InputLabel>
                  <Select
                    name="genre"
                    value={movieFormData.genre}
                    label="Genre"
                    onChange={handleMovieSelectChange}
                  >
                    <MenuItem value="Drama">Drama</MenuItem>
                    <MenuItem value="Comedy">Comedy</MenuItem>
                    <MenuItem value="Action">Action</MenuItem>
                    <MenuItem value="Thriller">Thriller</MenuItem>
                    <MenuItem value="Romance">Romance</MenuItem>
                    <MenuItem value="Sci-Fi">Sci-Fi</MenuItem>
                    <MenuItem value="Horror">Horror</MenuItem>
                    <MenuItem value="Documentary">Documentary</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Rating"
                  name="rating"
                  type="number"
                  value={movieFormData.rating}
                  onChange={handleMovieInputChange}
                  margin="normal"
                  inputProps={{ min: 0, max: 5, step: 0.1 }}
                  placeholder="0.0"
                  sx={{
                    '& .MuiInputLabel-root': {
                      color: 'text.primary',
                      fontWeight: 'medium',
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                      color: 'primary.main',
                      fontWeight: 'bold',
                    },
                    '& .MuiOutlinedInput-root': {
                      '& fieldset': {
                        borderColor: 'grey.400',
                      },
                      '&:hover fieldset': {
                        borderColor: 'primary.main',
                      },
                      '&.Mui-focused fieldset': {
                        borderColor: 'primary.main',
                        borderWidth: 2,
                      },
                    },
                  }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Director"
                  name="director"
                  value={movieFormData.director}
                  onChange={handleMovieInputChange}
                  margin="normal"
                  sx={{
                    '& .MuiInputLabel-root': {
                      color: 'text.primary',
                      fontWeight: 'medium',
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                      color: 'primary.main',
                      fontWeight: 'bold',
                    },
                    '& .MuiOutlinedInput-root': {
                      '& fieldset': {
                        borderColor: 'grey.400',
                      },
                      '&:hover fieldset': {
                        borderColor: 'primary.main',
                      },
                      '&.Mui-focused fieldset': {
                        borderColor: 'primary.main',
                        borderWidth: 2,
                      },
                    },
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Cast"
                  name="cast"
                  value={movieFormData.cast}
                  onChange={handleMovieInputChange}
                  margin="normal"
                  placeholder="Actor 1, Actor 2, Actor 3..."
                  sx={{
                    '& .MuiInputLabel-root': {
                      color: 'text.primary',
                      fontWeight: 'medium',
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                      color: 'primary.main',
                      fontWeight: 'bold',
                    },
                    '& .MuiOutlinedInput-root': {
                      '& fieldset': {
                        borderColor: 'grey.400',
                      },
                      '&:hover fieldset': {
                        borderColor: 'primary.main',
                      },
                      '&.Mui-focused fieldset': {
                        borderColor: 'primary.main',
                        borderWidth: 2,
                      },
                    },
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Description"
                  name="description"
                  value={movieFormData.description}
                  onChange={handleMovieInputChange}
                  margin="normal"
                  multiline
                  rows={3}
                  sx={{
                    '& .MuiInputLabel-root': {
                      color: 'text.primary',
                      fontWeight: 'medium',
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                      color: 'primary.main',
                      fontWeight: 'bold',
                    },
                    '& .MuiOutlinedInput-root': {
                      '& fieldset': {
                        borderColor: 'grey.400',
                      },
                      '&:hover fieldset': {
                        borderColor: 'primary.main',
                      },
                      '&.Mui-focused fieldset': {
                        borderColor: 'primary.main',
                        borderWidth: 2,
                      },
                    },
                  }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Poster URL"
                  name="poster_url"
                  value={movieFormData.poster_url}
                  onChange={handleMovieInputChange}
                  margin="normal"
                  placeholder="https://example.com/poster.jpg"
                  sx={{
                    '& .MuiInputLabel-root': {
                      color: 'text.primary',
                      fontWeight: 'medium',
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                      color: 'primary.main',
                      fontWeight: 'bold',
                    },
                    '& .MuiOutlinedInput-root': {
                      '& fieldset': {
                        borderColor: 'grey.400',
                      },
                      '&:hover fieldset': {
                        borderColor: 'primary.main',
                      },
                      '&.Mui-focused fieldset': {
                        borderColor: 'primary.main',
                        borderWidth: 2,
                      },
                    },
                  }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Trailer URL"
                  name="trailer_url"
                  value={movieFormData.trailer_url}
                  onChange={handleMovieInputChange}
                  margin="normal"
                  placeholder="https://youtube.com/watch?v=..."
                  sx={{
                    '& .MuiInputLabel-root': {
                      color: 'text.primary',
                      fontWeight: 'medium',
                    },
                    '& .MuiInputLabel-root.Mui-focused': {
                      color: 'primary.main',
                      fontWeight: 'bold',
                    },
                    '& .MuiOutlinedInput-root': {
                      '& fieldset': {
                        borderColor: 'grey.400',
                      },
                      '&:hover fieldset': {
                        borderColor: 'primary.main',
                      },
                      '&.Mui-focused fieldset': {
                        borderColor: 'primary.main',
                        borderWidth: 2,
                      },
                    },
                  }}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenMovieDialog(false)}>
              Cancel
            </Button>
            <Button type="submit" variant="contained">
              {editingMovie ? 'Update Movie' : 'Create Movie'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
};

export default Admin; 