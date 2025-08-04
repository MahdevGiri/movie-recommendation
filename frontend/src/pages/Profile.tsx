import React, { useEffect, useState } from 'react';
import { Container, Typography, Card, CardContent, Box, CircularProgress, Rating, Stack, Grid } from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import { getUserRatings } from '../services/api';
import { Rating as RatingType } from '../types';

const Profile: React.FC = () => {
  const { user } = useAuth();
  const [ratings, setRatings] = useState<RatingType[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchRatings = async () => {
      setLoading(true);
      setError(null);
      try {
        console.log('Fetching ratings for user:', user?.id);
        const data = await getUserRatings();
        console.log('Ratings API response:', data);
        setRatings(data.ratings || []);
      } catch (error: any) {
        console.error('Error fetching ratings:', error);
        console.error('Error details:', error.response?.data || error.message);
        setError(error.response?.data?.error || error.message || 'Failed to fetch ratings');
        setRatings([]);
      } finally {
        setLoading(false);
      }
    };
    
    if (user) {
      fetchRatings();
    } else {
      setLoading(false);
    }
  }, [user]);

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
        👤 Profile
      </Typography>
      
      {user && (
        <Card sx={{ mb: { xs: 3, md: 4 }, p: { xs: 2, sm: 3 } }}>
          <CardContent>
            <Grid container spacing={{ xs: 2, md: 3 }}>
              <Grid item xs={12} sm={6} md={3}>
                <Typography 
                  variant="h6" 
                  sx={{ fontSize: { xs: '1.1rem', sm: '1.3rem' } }}
                >
                  {user.name} ({user.username})
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Typography variant="body1">
                  Email: {user.email || 'N/A'}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Typography variant="body1">
                  Age: {user.age || 'N/A'}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Typography variant="body1">
                  Role: {user.role}
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="body1">
                  Preferred Genre: {user.preferred_genre || 'N/A'}
                </Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}
      
      <Typography 
        variant="h5" 
        gutterBottom
        sx={{ 
          fontSize: { xs: '1.4rem', sm: '1.6rem', md: '1.8rem' },
          textAlign: { xs: 'center', sm: 'left' }
        }}
      >
        ⭐ Your Ratings ({ratings.length})
      </Typography>
      
      {error && (
        <Typography 
          color="error" 
          sx={{ 
            textAlign: 'center', 
            mt: 2,
            fontSize: { xs: '0.9rem', sm: '1rem' }
          }}
        >
          Error: {error}
        </Typography>
      )}
      
      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <CircularProgress />
        </Box>
      ) : ratings.length === 0 ? (
        <Typography 
          color="text.secondary" 
          sx={{ 
            textAlign: 'center', 
            mt: 4,
            fontSize: { xs: '1rem', sm: '1.1rem' }
          }}
        >
          You haven't rated any movies yet.
        </Typography>
      ) : (
        <Grid container spacing={{ xs: 1, sm: 2, md: 3 }} sx={{ mt: 2 }}>
          {ratings.map((r, idx) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={r.movie_id + '-' + idx}>
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
                    variant="subtitle1" 
                    sx={{ 
                      fontSize: { xs: '1rem', sm: '1.1rem' },
                      mb: 1,
                      lineHeight: 1.2
                    }}
                  >
                    {r.title} ({r.year})
                  </Typography>
                  
                  <Typography 
                    variant="body2" 
                    color="text.secondary"
                    sx={{ 
                      mb: 2,
                      fontSize: { xs: '0.8rem', sm: '0.9rem' }
                    }}
                  >
                    Genre: {r.genre}
                  </Typography>
                  
                  <Box sx={{ marginTop: 'auto' }}>
                    <Box sx={{ 
                      display: 'flex', 
                      alignItems: 'center',
                      flexDirection: { xs: 'column', sm: 'row' },
                      gap: { xs: 1, sm: 0 }
                    }}>
                      <Rating 
                        value={r.rating} 
                        readOnly 
                        precision={0.5}
                        size="small"
                      />
                      <Typography 
                        sx={{ 
                          ml: { sm: 1 },
                          fontSize: { xs: '0.9rem', sm: '1rem' }
                        }}
                      >
                        {r.rating}/5
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  );
};

export default Profile; 