import React from 'react';
import { Container, Typography, Box, Grid, Card, CardContent, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Home: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const features = [
    {
      title: '🎬 Movie Recommendations',
      description: 'Get personalized movie suggestions based on your preferences and rating history.',
      action: 'Get Recommendations',
      path: '/recommendations'
    },
    {
      title: '📚 Browse Movies',
      description: 'Explore our extensive collection of movies across different genres and years.',
      action: 'Browse Movies',
      path: '/movies'
    },
    {
      title: '⭐ Rate Movies',
      description: 'Rate movies you\'ve watched to help improve your recommendations.',
      action: 'Rate Movies',
      path: '/movies'
    }
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: { xs: 2, sm: 4 }, mb: 4 }}>
      {/* Hero Section */}
      <Box sx={{ textAlign: 'center', mb: { xs: 4, md: 6 } }}>
        <Typography 
          variant="h2" 
          component="h1" 
          gutterBottom
          sx={{ 
            fontSize: { xs: '2rem', sm: '3rem', md: '4rem' },
            fontWeight: 'bold',
            background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}
        >
          🎬 Movie Recommendations
        </Typography>
        <Typography 
          variant="h5" 
          color="text.secondary" 
          sx={{ 
            fontSize: { xs: '1.1rem', sm: '1.3rem', md: '1.5rem' },
            mb: 3
          }}
        >
          Discover your next favorite movie with AI-powered recommendations
        </Typography>
        {!user && (
          <Box sx={{ mt: 3 }}>
            <Button 
              variant="contained" 
              size="large" 
              onClick={() => navigate('/register')}
              sx={{ mr: 2, mb: { xs: 1, sm: 0 } }}
            >
              Get Started
            </Button>
            <Button 
              variant="outlined" 
              size="large" 
              onClick={() => navigate('/login')}
            >
              Sign In
            </Button>
          </Box>
        )}
      </Box>

      {/* Features Grid */}
      <Grid container spacing={{ xs: 2, md: 3 }} sx={{ mb: 4 }}>
        {features.map((feature, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card 
              sx={{ 
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                transition: 'transform 0.2s ease-in-out',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 4
                }
              }}
            >
              <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
                <Typography 
                  variant="h5" 
                  component="h2" 
                  gutterBottom
                  sx={{ fontSize: { xs: '1.2rem', sm: '1.4rem' } }}
                >
                  {feature.title}
                </Typography>
                <Typography 
                  variant="body1" 
                  color="text.secondary" 
                  sx={{ mb: 3, fontSize: { xs: '0.9rem', sm: '1rem' } }}
                >
                  {feature.description}
                </Typography>
                <Button 
                  variant="contained" 
                  onClick={() => navigate(feature.path)}
                  sx={{ 
                    width: { xs: '100%', sm: 'auto' },
                    minWidth: { sm: '120px' }
                  }}
                >
                  {feature.action}
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Welcome Message for Logged In Users */}
      {user && (
        <Box sx={{ textAlign: 'center', mt: 4 }}>
          <Typography 
            variant="h4" 
            gutterBottom
            sx={{ fontSize: { xs: '1.5rem', sm: '2rem', md: '2.5rem' } }}
          >
            Welcome back, {user.name}! 👋
          </Typography>
          <Typography 
            variant="body1" 
            color="text.secondary"
            sx={{ fontSize: { xs: '1rem', sm: '1.1rem' } }}
          >
            Ready to discover more great movies? Check out your personalized recommendations or browse our collection.
          </Typography>
        </Box>
      )}
    </Container>
  );
};

export default Home; 