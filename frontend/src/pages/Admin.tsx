import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Movie } from '../types';
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
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import MovieImage from '../components/MovieImage';

interface MovieFormData {
  title: string;
  genre: string;
  year: number;
  description: string;
  director: string;
  cast: string;
  poster_url: string;
  trailer_url: string;
}

const Admin: React.FC = () => {
  const { user } = useAuth();
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(true);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingMovie, setEditingMovie] = useState<Movie | null>(null);
  const [formData, setFormData] = useState<MovieFormData>({
    title: '',
    genre: '',
    year: new Date().getFullYear(),
    description: '',
    director: '',
    cast: '',
    poster_url: '',
    trailer_url: '',
  });
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedGenre, setSelectedGenre] = useState<string>('');
  const [genres, setGenres] = useState<string[]>([]);

  useEffect(() => {
    fetchMovies();
    fetchGenres();
  }, [page, searchTerm, selectedGenre]);

  // Check if user is admin - moved after hooks
  if (!user || user.role !== 'admin') {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error">
          Access denied. Admin privileges required.
        </Alert>
      </Box>
    );
  }

  const fetchMovies = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams({
        page: page.toString(),
        per_page: '10',
      });
      
      if (searchTerm) params.append('search', searchTerm);
      if (selectedGenre) params.append('genre', selectedGenre);

      const response = await api.get(`/admin/movies?${params}`);
      setMovies(response.data.movies);
      setTotalPages(Math.ceil(response.data.pagination.total / 10));
    } catch (error: any) {
      toast.error('Failed to fetch movies');
      console.error('Error fetching movies:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchGenres = async () => {
    try {
      const response = await api.get('/movies/genres');
      setGenres(response.data.genres);
    } catch (error) {
      console.error('Error fetching genres:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      if (editingMovie) {
        await api.put(`/admin/movies/${editingMovie.id}`, formData);
        toast.success('Movie updated successfully!');
      } else {
        await api.post('/admin/movies', formData);
        toast.success('Movie created successfully!');
      }
      
      setOpenDialog(false);
      resetForm();
      fetchMovies();
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Operation failed');
    }
  };

  const handleDelete = async (movieId: number) => {
    if (!window.confirm('Are you sure you want to delete this movie?')) {
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

  const handleEdit = (movie: Movie) => {
    setEditingMovie(movie);
    setFormData({
      title: movie.title,
      genre: movie.genre,
      year: movie.year,
      description: movie.description || '',
      director: movie.director || '',
      cast: movie.cast || '',
      poster_url: movie.poster_url || '',
      trailer_url: movie.trailer_url || '',
    });
    setOpenDialog(true);
  };

  const handleAdd = () => {
    setEditingMovie(null);
    resetForm();
    setOpenDialog(true);
  };

  const resetForm = () => {
    setFormData({
      title: '',
      genre: '',
      year: new Date().getFullYear(),
      description: '',
      director: '',
      cast: '',
      poster_url: '',
      trailer_url: '',
    });
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'year' ? parseInt(value) || 0 : value,
    }));
  };

  const handleGenreChange = (e: SelectChangeEvent) => {
    setFormData(prev => ({
      ...prev,
      genre: e.target.value,
    }));
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Admin Dashboard
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleAdd}
        >
          Add Movie
        </Button>
      </Box>

      {/* Search and Filter */}
      <Box sx={{ mb: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Search movies"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search by title..."
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Filter by Genre</InputLabel>
              <Select
                value={selectedGenre}
                label="Filter by Genre"
                onChange={(e) => setSelectedGenre(e.target.value)}
              >
                <MenuItem value="">All Genres</MenuItem>
                {genres.map((genre) => (
                  <MenuItem key={genre} value={genre}>
                    {genre}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Box>

      {/* Movies Grid */}
      <Grid container spacing={3}>
        {movies.map((movie) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={movie.id}>
            <Card>
              <MovieImage 
                posterUrl={movie.poster_url}
                title={movie.title}
                genre={movie.genre}
                year={movie.year}
              />
              <CardContent>
                <Typography variant="h6" component="h2" noWrap>
                  {movie.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {movie.year} • {movie.genre}
                </Typography>
                {movie.rating && (
                  <Chip
                    label={`${movie.rating.toFixed(1)} ⭐`}
                    size="small"
                    color="primary"
                    sx={{ mb: 1 }}
                  />
                )}
                <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
                  <IconButton
                    size="small"
                    color="primary"
                    onClick={() => handleEdit(movie)}
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    size="small"
                    color="error"
                    onClick={() => handleDelete(movie.id)}
                  >
                    <DeleteIcon />
                  </IconButton>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Pagination */}
      {totalPages > 1 && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
          <Pagination
            count={totalPages}
            page={page}
            onChange={(_, value) => setPage(value)}
            color="primary"
          />
        </Box>
      )}

      {/* Add/Edit Movie Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingMovie ? 'Edit Movie' : 'Add New Movie'}
        </DialogTitle>
        <form onSubmit={handleSubmit}>
          <DialogContent>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Title"
                  name="title"
                  value={formData.title}
                  onChange={handleInputChange}
                  required
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth margin="normal" required>
                  <InputLabel>Genre</InputLabel>
                  <Select
                    name="genre"
                    value={formData.genre}
                    label="Genre"
                    onChange={handleGenreChange}
                  >
                    {genres.map((genre) => (
                      <MenuItem key={genre} value={genre}>
                        {genre}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Year"
                  name="year"
                  type="number"
                  value={formData.year}
                  onChange={handleInputChange}
                  required
                  margin="normal"
                  inputProps={{ min: 1900, max: 2030 }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Director"
                  name="director"
                  value={formData.director}
                  onChange={handleInputChange}
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Cast"
                  name="cast"
                  value={formData.cast}
                  onChange={handleInputChange}
                  margin="normal"
                  placeholder="Actor 1, Actor 2, Actor 3..."
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Description"
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  margin="normal"
                  multiline
                  rows={3}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Poster URL"
                  name="poster_url"
                  value={formData.poster_url}
                  onChange={handleInputChange}
                  margin="normal"
                  placeholder="https://example.com/poster.jpg"
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Trailer URL"
                  name="trailer_url"
                  value={formData.trailer_url}
                  onChange={handleInputChange}
                  margin="normal"
                  placeholder="https://youtube.com/watch?v=..."
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenDialog(false)}>
              Cancel
            </Button>
            <Button type="submit" variant="contained">
              {editingMovie ? 'Update' : 'Create'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
};

export default Admin; 