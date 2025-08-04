import React from 'react';
import { Container, Typography, Box, Grid, Card, CardContent, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Home: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const allFeatures = [
    {
      title: '🎬 Movie Recommendations',
      description: 'Get personalized movie suggestions based on your preferences and rating history.',
      action: 'Get Recommendations',
      path: '/recommendations',
      icon: '🎬',
      color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    },
    {
      title: '📚 Browse Movies',
      description: 'Explore our extensive collection of movies across different genres and years.',
      action: 'Browse Movies',
      path: '/movies',
      icon: '📚',
      color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
    },
    {
      title: '⭐ Rate Movies',
      description: 'Rate movies you\'ve watched to help improve your recommendations.',
      action: 'Rate Movies',
      path: '/movies',
      icon: '⭐',
      color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
    }
  ];

  // Filter features based on user role
  const features = user?.role === 'admin' 
    ? allFeatures.filter(feature => feature.title === '📚 Browse Movies')
    : allFeatures;

  return (
    <Container maxWidth="lg" sx={{ mt: { xs: 2, sm: 4 }, mb: 4 }}>
      {/* Hero Section */}
      <Box 
        sx={{ 
          textAlign: 'center', 
          mb: { xs: 4, md: 6 },
          animation: 'fadeInUp 0.8s ease-out'
        }}
      >
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
            WebkitTextFillColor: 'transparent',
            textShadow: '0 4px 8px rgba(0,0,0,0.1)',
            animation: 'pulse 3s ease-in-out infinite'
          }}
        >
          🎬 Movie Recommendations
        </Typography>
        <Typography 
          variant="h5" 
          color="text.secondary" 
          sx={{ 
            fontSize: { xs: '1.1rem', sm: '1.3rem', md: '1.5rem' },
            mb: 3,
            color: 'rgba(255, 255, 255, 0.9)',
            textShadow: '0 2px 4px rgba(0,0,0,0.3)'
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
              sx={{ 
                mr: 2, 
                mb: { xs: 1, sm: 0 },
                background: 'linear-gradient(45deg, #FF6B35 30%, #F7931E 90%)',
                boxShadow: '0 8px 16px rgba(255, 107, 53, 0.3)',
                '&:hover': {
                  background: 'linear-gradient(45deg, #E64A19 30%, #F57C00 90%)',
                  transform: 'translateY(-3px)',
                  boxShadow: '0 12px 24px rgba(255, 107, 53, 0.4)',
                }
              }}
            >
              Get Started
            </Button>
            <Button 
              variant="outlined" 
              size="large" 
              onClick={() => navigate('/login')}
              sx={{
                borderColor: 'rgba(255, 255, 255, 0.5)',
                color: 'rgba(255, 255, 255, 0.9)',
                '&:hover': {
                  borderColor: 'rgba(255, 255, 255, 0.8)',
                  backgroundColor: 'rgba(255, 255, 255, 0.1)',
                }
              }}
            >
              Sign In
            </Button>
          </Box>
        )}
      </Box>

      {/* Features Grid */}
      <Grid 
        container 
        spacing={{ xs: 2, md: 3 }} 
        sx={{ 
          mb: 4,
          justifyContent: user?.role === 'admin' ? 'center' : 'flex-start'
        }}
      >
        {features.map((feature, index) => (
          <Grid 
            item 
            xs={12} 
            sm={user?.role === 'admin' ? 6 : 6} 
            md={user?.role === 'admin' ? 4 : 4} 
            key={index}
          >
            <Card 
              sx={{ 
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                background: 'rgba(255, 255, 255, 0.1)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                animation: `fadeInUp 0.6s ease-out ${index * 0.2}s both`,
                '&:hover': {
                  transform: 'translateY(-12px) scale(1.02)',
                  boxShadow: '0 20px 40px rgba(0, 0, 0, 0.2)',
                  border: '1px solid rgba(255, 255, 255, 0.4)',
                }
              }}
            >
              <CardContent sx={{ flexGrow: 1, textAlign: 'center', p: 3 }}>
                <Box
                  sx={{
                    width: 80,
                    height: 80,
                    borderRadius: '50%',
                    background: feature.color,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '2rem',
                    margin: '0 auto 1rem',
                    boxShadow: '0 8px 16px rgba(0,0,0,0.2)',
                    animation: 'pulse 2s ease-in-out infinite'
                  }}
                >
                  {feature.icon}
                </Box>
                <Typography 
                  variant="h5" 
                  component="h2" 
                  gutterBottom
                  sx={{ 
                    fontSize: { xs: '1.2rem', sm: '1.4rem' },
                    color: 'rgba(255, 255, 255, 0.95)',
                    fontWeight: 600
                  }}
                >
                  {feature.title}
                </Typography>
                <Typography 
                  variant="body1" 
                  sx={{ 
                    mb: 3, 
                    fontSize: { xs: '0.9rem', sm: '1rem' },
                    color: 'rgba(255, 255, 255, 0.8)',
                    lineHeight: 1.6
                  }}
                >
                  {feature.description}
                </Typography>
                <Button 
                  variant="contained" 
                  onClick={() => navigate(feature.path)}
                  sx={{ 
                    width: { xs: '100%', sm: 'auto' },
                    minWidth: { sm: '120px' },
                    background: feature.color,
                    '&:hover': {
                      background: feature.color,
                      transform: 'translateY(-2px)',
                      boxShadow: '0 8px 16px rgba(0,0,0,0.3)',
                    }
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
        <Box 
          sx={{ 
            textAlign: 'center', 
            mt: 4,
            animation: 'fadeInUp 0.8s ease-out 0.6s both'
          }}
        >
          <Typography 
            variant="h4" 
            gutterBottom
            sx={{ 
              fontSize: { xs: '1.5rem', sm: '2rem', md: '2.5rem' },
              color: 'rgba(255, 255, 255, 0.95)',
              fontWeight: 600,
              textShadow: '0 2px 4px rgba(0,0,0,0.3)'
            }}
          >
            Welcome back, {user.name}! 👋
          </Typography>
          <Typography 
            variant="body1" 
            sx={{ 
              fontSize: { xs: '1rem', sm: '1.1rem' },
              color: 'rgba(255, 255, 255, 0.8)',
              textShadow: '0 1px 2px rgba(0,0,0,0.3)'
            }}
          >
            {user.role === 'admin' 
              ? 'As an admin, you can browse and manage the movie collection.'
              : 'Ready to discover more great movies? Check out your personalized recommendations or browse our collection.'
            }
          </Typography>
        </Box>
      )}
    </Container>
  );
};

export default Home; 