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
          textAlign: { xs: 'center', sm: 'left' }
        }}
      >
        🎯 Personalized Recommendations
      </Typography>
      
      <Typography 
        variant="body1" 
        color="text.secondary" 
        sx={{ 
          mb: 3,
          fontSize: { xs: '1rem', sm: '1.1rem' },
          textAlign: { xs: 'center', sm: 'left' }
        }}
      >
        Choose your preferred recommendation style:
      </Typography>

      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'center', 
        mb: 4,
        flexDirection: { xs: 'column', sm: 'row' },
        gap: 2
      }}>
        <ToggleButtonGroup
          value={recommendationType}
          exclusive
          onChange={handleRecommendationTypeChange}
          aria-label="recommendation type"
          size="large"
        >
          <ToggleButton value="collaborative" aria-label="collaborative">
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                Smart Recommendations
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Based on similar users + your genre preference
              </Typography>
            </Box>
          </ToggleButton>
          <ToggleButton value="genre-focused" aria-label="genre-focused">
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                Genre Focused
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Top rated movies in your preferred genre
              </Typography>
            </Box>
          </ToggleButton>
        </ToggleButtonGroup>
      </Box>

      {recommendationInfo && (
        <Alert 
          severity="info" 
          sx={{ 
            mb: 3,
            '& .MuiAlert-message': {
              width: '100%'
            }
          }}
        >
          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, gap: 1, alignItems: { xs: 'flex-start', sm: 'center' } }}>
            <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
              {recommendationInfo.algorithm_info}
            </Typography>
            {recommendationInfo.user_preferred_genre && (
              <Chip 
                label={`Preferred: ${recommendationInfo.user_preferred_genre}`} 
                color="primary" 
                size="small"
              />
            )}
          </Box>
        </Alert>
      )}

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

      {!loading && !error && recommendations.length === 0 && (
        <Box sx={{ textAlign: 'center', mt: 4 }}>
          <Typography variant="h6" gutterBottom>
            No recommendations found
          </Typography>
          <Typography color="text.secondary" sx={{ mb: 3 }}>
            Rate more movies to get personalized recommendations!
          </Typography>
          <Button 
            variant="contained" 
            href="/movies"
            sx={{ 
              fontSize: { xs: '0.9rem', sm: '1rem' }
            }}
          >
            Browse Movies
          </Button>
        </Box>
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
                  transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
                  '&:hover': {
                    transform: 'translateY(-2px)',
                    boxShadow: 4
                  }
                }}
              >
                <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
                  <Box sx={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    mb: 1,
                    flexDirection: { xs: 'column', sm: 'row' },
                    gap: { xs: 0.5, sm: 1 }
                  }}>
                    <Typography 
                      variant="h6" 
                      sx={{ 
                        fontSize: { xs: '1rem', sm: '1.1rem', md: '1.2rem' },
                        lineHeight: 1.2,
                        textAlign: { xs: 'center', sm: 'left' }
                      }}
                    >
                      #{index + 1}
                    </Typography>
                    {rec.reason && (
                      <Chip 
                        label={rec.reason} 
                        size="small" 
                        color="secondary"
                        sx={{ fontSize: '0.7rem' }}
                      />
                    )}
                  </Box>
                  
                  <Typography 
                    variant="h6" 
                    sx={{ 
                      fontSize: { xs: '1rem', sm: '1.1rem', md: '1.2rem' },
                      mb: 1,
                      lineHeight: 1.2
                    }}
                  >
                    {rec.title} ({rec.year})
                  </Typography>
                  
                  <Typography 
                    variant="body2" 
                    color="text.secondary"
                    sx={{ 
                      mb: 1,
                      fontSize: { xs: '0.8rem', sm: '0.9rem' }
                    }}
                  >
                    Genre: {rec.genre}
                  </Typography>
                  
                  {rec.predicted_rating && (
                    <Typography 
                      variant="body2" 
                      color="primary"
                      sx={{ 
                        mb: 2,
                        fontSize: { xs: '0.9rem', sm: '1rem' },
                        fontWeight: 'bold'
                      }}
                    >
                      Predicted Rating: {rec.predicted_rating.toFixed(1)}/5
                    </Typography>
                  )}

                  {rec.rating && (
                    <Typography 
                      variant="body2" 
                      color="primary"
                      sx={{ 
                        mb: 2,
                        fontSize: { xs: '0.9rem', sm: '1rem' },
                        fontWeight: 'bold'
                      }}
                    >
                      Average Rating: {rec.rating.toFixed(1)}/5
                    </Typography>
                  )}
                  
                  <Box sx={{ marginTop: 'auto' }}>
                    <Button 
                      href={`/movies/${rec.movie_id}`} 
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
      )}
    </Container>
  );
};

export default Recommendations; 