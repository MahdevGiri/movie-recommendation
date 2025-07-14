import React, { useEffect, useState } from 'react';
import { Container, Typography, CircularProgress, Card, CardContent, Box, Button, Snackbar, Alert, Stack, Grid } from '@mui/material';
import Rating from '@mui/material/Rating';
import api from '../services/api';

interface Movie {
  id: number;
  title: string;
  genre: string;
  year: number;
  rating?: number;
  description?: string;
}

interface Pagination {
  page: number;
  per_page: number;
  total: number;
}

const Movies: React.FC = () => {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [ratingSubmitting, setRatingSubmitting] = useState<number | null>(null);
  const [snackbar, setSnackbar] = useState<{open: boolean, message: string, severity: 'success' | 'error'}>({open: false, message: '', severity: 'success'});
  const [pagination, setPagination] = useState<Pagination>({ page: 1, per_page: 20, total: 0 });

  const fetchMovies = (page = 1, per_page = 20) => {
    setLoading(true);
    api.get(`/movies?page=${page}&per_page=${per_page}`)
      .then(res => {
        setMovies(res.data.movies);
        setPagination(res.data.pagination);
        setError(null);
      })
      .catch(() => setError('Failed to load movies.'))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchMovies(1, pagination.per_page);
    // eslint-disable-next-line
  }, []);

  const handlePageChange = (newPage: number) => {
    fetchMovies(newPage, pagination.per_page);
  };

  const handleRate = async (movieId: number, value: number | null) => {
    if (!value) return;
    setRatingSubmitting(movieId);
    try {
      await api.post('/ratings', { movie_id: movieId, rating: value });
      setSnackbar({open: true, message: 'Rating submitted!', severity: 'success'});
    } catch {
      setSnackbar({open: true, message: 'Failed to submit rating.', severity: 'error'});
    } finally {
      setRatingSubmitting(null);
    }
  };

  const totalPages = Math.ceil(pagination.total / pagination.per_page);

  return (
    <Container maxWidth="lg" sx={{ mt: { xs: 2, sm: 4 }, mb: 4 }}>
      <Typography 
        variant="h4" 
        component="h1" 
        gutterBottom
        sx={{ 
          fontSize: { xs: '1.8rem', sm: '2.2rem', md: '2.5rem' },
          textAlign: { xs: 'center', sm: 'left' }
        }}
      >
        🎭 Movies
      </Typography>
      
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <CircularProgress />
        </Box>
      )}
      
      {error && (
        <Typography color="error" sx={{ textAlign: 'center', mt: 2 }}>
          {error}
        </Typography>
      )}
      
      {!loading && !error && movies.length === 0 && (
        <Typography sx={{ textAlign: 'center', mt: 4 }}>
          No movies found.
        </Typography>
      )}
      
      {!loading && !error && movies.length > 0 && (
        <>
          <Grid container spacing={{ xs: 1, sm: 2, md: 3 }} sx={{ mt: 2 }}>
            {movies.map(movie => (
              <Grid item xs={12} sm={6} md={4} lg={3} key={movie.id}>
                <Card 
                  sx={{ 
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
                    '&:hover': {
                      transform: 'translateY(-2px)',
                      boxShadow: 4
                    }
                  }}
                >
                  <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
                    <Typography 
                      variant="h6" 
                      sx={{ 
                        fontSize: { xs: '1rem', sm: '1.1rem', md: '1.2rem' },
                        mb: 1,
                        lineHeight: 1.2
                      }}
                    >
                      {movie.title} ({movie.year})
                    </Typography>
                    
                    <Typography 
                      variant="body2" 
                      color="text.secondary"
                      sx={{ mb: 1, fontSize: { xs: '0.8rem', sm: '0.9rem' } }}
                    >
                      Genre: {movie.genre}
                    </Typography>
                    
                    {movie.description && (
                      <Typography 
                        variant="body2" 
                        sx={{ 
                          mt: 1, 
                          mb: 2,
                          fontSize: { xs: '0.8rem', sm: '0.9rem' },
                          flexGrow: 1,
                          overflow: 'hidden',
                          display: '-webkit-box',
                          WebkitLineClamp: 3,
                          WebkitBoxOrient: 'vertical'
                        }}
                      >
                        {movie.description}
                      </Typography>
                    )}
                    
                    <Box sx={{ marginTop: 'auto' }}>
                      <Box sx={{ 
                        display: 'flex', 
                        alignItems: 'center', 
                        mb: 1,
                        flexDirection: { xs: 'column', sm: 'row' },
                        gap: { xs: 1, sm: 0 }
                      }}>
                        <Rating
                          name={`rating-${movie.id}`}
                          onChange={(_, value) => handleRate(movie.id, value)}
                          disabled={ratingSubmitting === movie.id}
                          size="small"
                        />
                        {ratingSubmitting === movie.id && (
                          <CircularProgress size={16} sx={{ ml: 1 }} />
                        )}
                      </Box>
                      
                      <Button 
                        href={`/movies/${movie.id}`} 
                        size="small"
                        variant="outlined"
                        sx={{ 
                          width: { xs: '100%', sm: 'auto' },
                          fontSize: { xs: '0.8rem', sm: '0.9rem' }
                        }}
                      >
                        View Details
                      </Button>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
          
          {/* Pagination Controls */}
          {totalPages > 1 && (
            <Stack 
              direction={{ xs: 'column', sm: 'row' }} 
              spacing={2} 
              justifyContent="center" 
              alignItems="center" 
              sx={{ mt: 4 }}
            >
              <Button
                variant="outlined"
                disabled={pagination.page === 1}
                onClick={() => handlePageChange(pagination.page - 1)}
                size="small"
              >
                Previous
              </Button>
              <Typography sx={{ fontSize: { xs: '0.9rem', sm: '1rem' } }}>
                Page {pagination.page} of {totalPages}
              </Typography>
              <Button
                variant="outlined"
                disabled={pagination.page === totalPages}
                onClick={() => handlePageChange(pagination.page + 1)}
                size="small"
              >
                Next
              </Button>
            </Stack>
          )}
        </>
      )}
      
      <Snackbar
        open={snackbar.open}
        autoHideDuration={3000}
        onClose={() => setSnackbar({...snackbar, open: false})}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={() => setSnackbar({...snackbar, open: false})} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default Movies; 