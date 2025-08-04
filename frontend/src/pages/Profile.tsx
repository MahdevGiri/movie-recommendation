import React, { useEffect, useState } from 'react';
import { Container, Typography, Card, CardContent, Box, CircularProgress, Rating, Stack, Grid, Avatar, Chip, Divider, Paper } from '@mui/material';
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

  const isAdmin = user?.role === 'admin';

  return (
    <Container maxWidth="lg" sx={{ mt: { xs: 2, sm: 4 }, mb: 4 }}>
      <Typography 
        variant="h4" 
        component="h1" 
        gutterBottom
        sx={{ 
          fontSize: { xs: '1.8rem', sm: '2.2rem', md: '2.5rem' },
          textAlign: { xs: 'center', sm: 'left' },
          color: 'rgba(255, 255, 255, 0.95)',
          fontWeight: 600,
          textShadow: '0 2px 4px rgba(0,0,0,0.3)',
          animation: 'fadeInUp 0.6s ease-out'
        }}
      >
        {isAdmin ? '👑 Admin Profile' : '👤 Profile'}
      </Typography>
      
      {user && (
        <Card 
          sx={{ 
            mb: { xs: 3, md: 4 }, 
            p: { xs: 2, sm: 3 },
            background: isAdmin 
              ? 'linear-gradient(135deg, rgba(255, 215, 0, 0.1) 0%, rgba(255, 140, 0, 0.1) 100%)'
              : 'rgba(255, 255, 255, 0.1)',
            backdropFilter: 'blur(10px)',
            border: isAdmin 
              ? '2px solid rgba(255, 215, 0, 0.3)'
              : '1px solid rgba(255, 255, 255, 0.2)',
            borderRadius: 3,
            boxShadow: isAdmin 
              ? '0 8px 32px rgba(255, 215, 0, 0.2)'
              : '0 4px 16px rgba(0, 0, 0, 0.1)',
            animation: 'fadeInUp 0.8s ease-out'
          }}
        >
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
              <Avatar 
                sx={{ 
                  width: 80, 
                  height: 80, 
                  mr: 3,
                  background: isAdmin 
                    ? 'linear-gradient(135deg, #FFD700 0%, #FFA500 100%)'
                    : 'linear-gradient(135deg, #2196F3 0%, #21CBF3 100%)',
                  fontSize: '2rem',
                  fontWeight: 'bold',
                  boxShadow: '0 4px 12px rgba(0,0,0,0.2)'
                }}
              >
                {isAdmin ? '👑' : user.name.charAt(0).toUpperCase()}
              </Avatar>
              <Box>
                <Typography 
                  variant="h5" 
                  sx={{ 
                    fontSize: { xs: '1.3rem', sm: '1.5rem', md: '1.8rem' },
                    fontWeight: 700,
                    color: 'rgba(255, 255, 255, 0.95)',
                    textShadow: '0 2px 4px rgba(0,0,0,0.3)'
                  }}
                >
                  {user.name}
                </Typography>
                <Typography 
                  variant="body1" 
                  sx={{ 
                    color: 'rgba(255, 255, 255, 0.8)',
                    fontSize: { xs: '0.9rem', sm: '1rem' }
                  }}
                >
                  @{user.username}
                </Typography>
                {isAdmin && (
                  <Chip 
                    label="ADMINISTRATOR" 
                    sx={{ 
                      mt: 1,
                      background: 'linear-gradient(135deg, #FFD700 0%, #FFA500 100%)',
                      color: '#000',
                      fontWeight: 'bold',
                      fontSize: '0.8rem',
                      boxShadow: '0 2px 8px rgba(255, 215, 0, 0.3)'
                    }}
                  />
                )}
              </Box>
            </Box>

            <Divider sx={{ mb: 3, borderColor: 'rgba(255, 255, 255, 0.2)' }} />

            <Grid container spacing={{ xs: 2, md: 3 }}>
              <Grid item xs={12} sm={6} md={3}>
                <Paper 
                  sx={{ 
                    p: 2, 
                    background: 'rgba(255, 255, 255, 0.05)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: 2
                  }}
                >
                  <Typography 
                    variant="body2" 
                    sx={{ 
                      color: 'rgba(255, 255, 255, 0.7)',
                      fontSize: '0.8rem',
                      textTransform: 'uppercase',
                      letterSpacing: '0.5px'
                    }}
                  >
                    Email
                  </Typography>
                  <Typography 
                    variant="body1" 
                    sx={{ 
                      color: 'rgba(255, 255, 255, 0.95)',
                      fontWeight: 500
                    }}
                  >
                    {user.email || 'N/A'}
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Paper 
                  sx={{ 
                    p: 2, 
                    background: 'rgba(255, 255, 255, 0.05)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: 2
                  }}
                >
                  <Typography 
                    variant="body2" 
                    sx={{ 
                      color: 'rgba(255, 255, 255, 0.7)',
                      fontSize: '0.8rem',
                      textTransform: 'uppercase',
                      letterSpacing: '0.5px'
                    }}
                  >
                    Age
                  </Typography>
                  <Typography 
                    variant="body1" 
                    sx={{ 
                      color: 'rgba(255, 255, 255, 0.95)',
                      fontWeight: 500
                    }}
                  >
                    {user.age || 'N/A'}
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Paper 
                  sx={{ 
                    p: 2, 
                    background: 'rgba(255, 255, 255, 0.05)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: 2
                  }}
                >
                  <Typography 
                    variant="body2" 
                    sx={{ 
                      color: 'rgba(255, 255, 255, 0.7)',
                      fontSize: '0.8rem',
                      textTransform: 'uppercase',
                      letterSpacing: '0.5px'
                    }}
                  >
                    Role
                  </Typography>
                  <Typography 
                    variant="body1" 
                    sx={{ 
                      color: 'rgba(255, 255, 255, 0.95)',
                      fontWeight: 500,
                      textTransform: 'capitalize'
                    }}
                  >
                    {user.role}
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Paper 
                  sx={{ 
                    p: 2, 
                    background: 'rgba(255, 255, 255, 0.05)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: 2
                  }}
                >
                  <Typography 
                    variant="body2" 
                    sx={{ 
                      color: 'rgba(255, 255, 255, 0.7)',
                      fontSize: '0.8rem',
                      textTransform: 'uppercase',
                      letterSpacing: '0.5px'
                    }}
                  >
                    Preferred Genre
                  </Typography>
                  <Typography 
                    variant="body1" 
                    sx={{ 
                      color: 'rgba(255, 255, 255, 0.95)',
                      fontWeight: 500
                    }}
                  >
                    {user.preferred_genre || 'N/A'}
                  </Typography>
                </Paper>
              </Grid>
            </Grid>

            {isAdmin && (
              <Box sx={{ mt: 4, p: 3, background: 'rgba(255, 215, 0, 0.05)', borderRadius: 2, border: '1px solid rgba(255, 215, 0, 0.2)' }}>
                <Typography 
                  variant="h6" 
                  sx={{ 
                    color: 'rgba(255, 215, 0, 0.9)',
                    fontWeight: 600,
                    mb: 2,
                    display: 'flex',
                    alignItems: 'center',
                    gap: 1
                  }}
                >
                  🛡️ Admin Privileges
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <Box sx={{ width: 8, height: 8, borderRadius: '50%', bgcolor: '#4CAF50', mr: 2 }} />
                      <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.9)' }}>
                        Full system access and management
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <Box sx={{ width: 8, height: 8, borderRadius: '50%', bgcolor: '#4CAF50', mr: 2 }} />
                      <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.9)' }}>
                        Movie collection management
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <Box sx={{ width: 8, height: 8, borderRadius: '50%', bgcolor: '#4CAF50', mr: 2 }} />
                      <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.9)' }}>
                        User data oversight
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <Box sx={{ width: 8, height: 8, borderRadius: '50%', bgcolor: '#4CAF50', mr: 2 }} />
                      <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.9)' }}>
                        System configuration access
                      </Typography>
                    </Box>
                  </Grid>
                </Grid>
              </Box>
            )}
          </CardContent>
        </Card>
      )}
      
      {!isAdmin && (
        <>
          <Typography 
            variant="h5" 
            gutterBottom
            sx={{ 
              fontSize: { xs: '1.4rem', sm: '1.6rem', md: '1.8rem' },
              textAlign: { xs: 'center', sm: 'left' },
              color: 'rgba(255, 255, 255, 0.95)',
              fontWeight: 600,
              textShadow: '0 2px 4px rgba(0,0,0,0.3)',
              animation: 'fadeInUp 0.6s ease-out 0.2s both'
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
        </>
      )}
    </Container>
  );
};

export default Profile; 