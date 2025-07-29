import React, { useEffect, useState } from 'react';
import { 
  Container, 
  Typography, 
  CircularProgress, 
  Card, 
  CardContent, 
  Box, 
  Button, 
  Grid,
  ToggleButton,
  ToggleButtonGroup,
  Chip,
  Alert
} from '@mui/material';
import api from '../services/api';
import MovieImage from '../components/MovieImage';

interface Recommendation {
  movie_id: number;
  title: string;
  genre: string;
  year: number;
  predicted_rating?: number;
  similarity_score?: number;
  hybrid_score?: number;
  rating?: number;
  reason?: string;
  poster_url?: string;
  trailer_url?: string;
  description?: string;
}

interface RecommendationResponse {
  recommendations: Recommendation[];
  type: string;
  user_preferred_genre?: string;
  algorithm_info?: string;
  count: number;
}

const Recommendations: React.FC = () => {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [recommendationType, setRecommendationType] = useState<'collaborative' | 'genre-focused'>('collaborative');
  const [recommendationInfo, setRecommendationInfo] = useState<RecommendationResponse | null>(null);

  const fetchRecommendations = async (type: 'collaborative' | 'genre-focused') => {
    setLoading(true);
    try {
      const endpoint = type === 'collaborative' 
        ? '/recommendations/personalized?limit=12'
        : '/recommendations/genre-focused?limit=12';
      
      const response = await api.get(endpoint);
      setRecommendations(response.data.recommendations);
      setRecommendationInfo(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load recommendations.');
      console.error('Error fetching recommendations:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations(recommendationType);
  }, [recommendationType]);

  const handleRecommendationTypeChange = (
    event: React.MouseEvent<HTMLElement>,
    newType: 'collaborative' | 'genre-focused' | null,
  ) => {
    if (newType !== null) {
      setRecommendationType(newType);
    }
  };

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
        🎯 Personalized Recommendations
      </Typography>
      
      <Typography 
        variant="body1" 
        sx={{ 
          mb: 3,
          fontSize: { xs: '1rem', sm: '1.1rem' },
          textAlign: { xs: 'center', sm: 'left' },
          color: 'rgba(255, 255, 255, 0.8)',
          textShadow: '0 1px 2px rgba(0,0,0,0.3)'
        }}
      >
        Discover movies tailored to your taste using our advanced recommendation algorithms.
      </Typography>

      {/* Recommendation Type Toggle */}
      <Box sx={{ mb: 3, textAlign: 'center' }}>
        <ToggleButtonGroup
          value={recommendationType}
          exclusive
          onChange={handleRecommendationTypeChange}
          sx={{
            background: 'rgba(255, 255, 255, 0.1)',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            borderRadius: 2,
            '& .MuiToggleButton-root': {
              color: 'rgba(255, 255, 255, 0.8)',
              border: 'none',
              '&.Mui-selected': {
                background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
                color: 'white',
                '&:hover': {
                  background: 'linear-gradient(45deg, #1976D2 30%, #1E88E5 90%)',
                }
              },
              '&:hover': {
                background: 'rgba(255, 255, 255, 0.1)',
              }
            }
          }}
        >
          <ToggleButton value="collaborative">
            🤝 Collaborative
          </ToggleButton>
          <ToggleButton value="genre-focused">
            🎭 Genre-Focused
          </ToggleButton>
        </ToggleButtonGroup>
      </Box>

      {/* Algorithm Info */}
      {recommendationInfo && (
        <Box sx={{ mb: 3, animation: 'fadeInUp 0.6s ease-out 0.2s both' }}>
          <Alert 
            severity="info" 
            sx={{ 
              background: 'rgba(255, 255, 255, 0.1)',
              backdropFilter: 'blur(10px)',
              border: '1px solid rgba(255, 255, 255, 0.2)',
              color: 'rgba(255, 255, 255, 0.9)',
              '& .MuiAlert-icon': {
                color: '#2196F3'
              }
            }}
          >
            <Typography variant="body2">
              <strong>Algorithm:</strong> {recommendationInfo.algorithm_info}
              {recommendationInfo.user_preferred_genre && (
                <span> • <strong>Preferred Genre:</strong> {recommendationInfo.user_preferred_genre}</span>
              )}
            </Typography>
          </Alert>
        </Box>
      )}
      
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <CircularProgress 
            size={60}
            sx={{
              color: '#2196F3',
              '& .MuiCircularProgress-circle': {
                strokeLinecap: 'round',
              }
            }}
          />
        </Box>
      )}
      
      {error && (
        <Typography 
          sx={{ 
            textAlign: 'center', 
            mt: 2,
            color: '#ff6b6b',
            textShadow: '0 1px 2px rgba(0,0,0,0.3)'
          }}
        >
          {error}
        </Typography>
      )}
      
      {!loading && !error && recommendations.length === 0 && (
        <Typography 
          sx={{ 
            textAlign: 'center', 
            mt: 4,
            color: 'rgba(255, 255, 255, 0.8)',
            textShadow: '0 1px 2px rgba(0,0,0,0.3)'
          }}
        >
          No recommendations available. Try rating some movies first!
        </Typography>
      )}
      
      {!loading && !error && recommendations.length > 0 && (
        <Grid container spacing={{ xs: 1, sm: 2, md: 3 }} sx={{ mt: 2 }}>
          {recommendations.map((rec, index) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={rec.movie_id}>
              <Card 
                sx={{ 
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  background: 'rgba(255, 255, 255, 0.1)',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                  transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                  animation: `fadeInUp 0.6s ease-out ${index * 0.1}s both`,
                  '&:hover': {
                    transform: 'translateY(-8px) scale(1.02)',
                    boxShadow: '0 20px 40px rgba(0, 0, 0, 0.2)',
                    border: '1px solid rgba(255, 255, 255, 0.4)',
                  }
                }}
              >
                <MovieImage
                  posterUrl={rec.poster_url}
                  title={rec.title}
                  genre={rec.genre}
                  year={rec.year}
                  height={200}
                  sx={{
                    borderTopLeftRadius: 12,
                    borderTopRightRadius: 12,
                  }}
                />
                <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', p: 2 }}>
                  <Typography 
                    variant="h6" 
                    sx={{ 
                      fontSize: { xs: '1rem', sm: '1.1rem', md: '1.2rem' },
                      mb: 1,
                      lineHeight: 1.2,
                      color: 'rgba(255, 255, 255, 0.95)',
                      fontWeight: 600
                    }}
                  >
                    {rec.title} ({rec.year})
                  </Typography>
                  
                  <Typography 
                    variant="body2" 
                    sx={{ 
                      mb: 1, 
                      fontSize: { xs: '0.8rem', sm: '0.9rem' },
                      color: 'rgba(255, 255, 255, 0.8)'
                    }}
                  >
                    Genre: {rec.genre}
                  </Typography>
                  
                  {rec.description && (
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
                        WebkitBoxOrient: 'vertical',
                        color: 'rgba(255, 255, 255, 0.7)',
                        lineHeight: 1.4
                      }}
                    >
                      {rec.description}
                    </Typography>
                  )}
                  
                  {/* Prediction Score */}
                  {(rec.predicted_rating || rec.rating) && (
                    <Box sx={{ mb: 2 }}>
                      <Chip
                        label={`${recommendationType === 'collaborative' ? 'Predicted' : 'Rating'}: ${rec.predicted_rating || rec.rating}/5`}
                        size="small"
                        sx={{
                          background: 'linear-gradient(45deg, #FFD700 30%, #FFA500 90%)',
                          color: '#2c3e50',
                          fontWeight: 600,
                          fontSize: '0.75rem'
                        }}
                      />
                    </Box>
                  )}
                  
                  <Box sx={{ marginTop: 'auto' }}>
                    <Box sx={{ 
                      display: 'flex', 
                      gap: 1, 
                      flexDirection: { xs: 'column', sm: 'row' },
                      width: '100%'
                    }}>
                      <Button 
                        href={`/movies/${rec.movie_id}`} 
                        size="small"
                        variant="outlined"
                        sx={{ 
                          flex: 1,
                          fontSize: { xs: '0.8rem', sm: '0.9rem' },
                          borderColor: 'rgba(255, 255, 255, 0.3)',
                          color: 'rgba(255, 255, 255, 0.9)',
                          '&:hover': {
                            borderColor: 'rgba(255, 255, 255, 0.6)',
                            backgroundColor: 'rgba(255, 255, 255, 0.1)',
                          }
                        }}
                      >
                        View Details
                      </Button>
                      {rec.trailer_url && (
                        <Button 
                          href={rec.trailer_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          size="small"
                          variant="contained"
                          sx={{ 
                            flex: 1,
                            fontSize: { xs: '0.8rem', sm: '0.9rem' },
                            background: 'linear-gradient(45deg, #FF6B35 30%, #F7931E 90%)',
                            '&:hover': {
                              background: 'linear-gradient(45deg, #E64A19 30%, #F57C00 90%)',
                              transform: 'translateY(-2px)',
                            }
                          }}
                        >
                          🎬 Trailer
                        </Button>
                      )}
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

export default Recommendations; 