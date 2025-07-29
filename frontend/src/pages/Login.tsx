import React from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  TextField, 
  Button, 
  Paper,
  LinearProgress,
  InputAdornment,
  IconButton
} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

interface FormErrors {
  username?: string;
  password?: string;
}

const Login: React.FC = () => {
  const { login, user } = useAuth();
  const navigate = useNavigate();

  // Redirect if already logged in
  React.useEffect(() => {
    if (user) {
      navigate('/');
    }
  }, [user, navigate]);

  const [formData, setFormData] = React.useState({
    username: '',
    password: ''
  });

  const [errors, setErrors] = React.useState<FormErrors>({});
  const [loading, setLoading] = React.useState(false);
  const [showPassword, setShowPassword] = React.useState(false);

  // Form validation
  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    if (!formData.username.trim()) {
      newErrors.username = 'Username is required';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setLoading(true);
    try {
      await login(formData.username, formData.password);
      // Redirect to home page after successful login
      navigate('/');
    } catch (error) {
      console.error('Login failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });

    // Clear error when user starts typing
    if (errors[name as keyof FormErrors]) {
      setErrors({
        ...errors,
        [name]: undefined
      });
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: { xs: 2, sm: 4 }, mb: 4 }}>
      <Box sx={{ 
        display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center',
        minHeight: { xs: '60vh', sm: '70vh' },
        justifyContent: 'center',
        animation: 'fadeInUp 0.8s ease-out'
      }}>
        <Paper 
          elevation={0}
          sx={{ 
            p: { xs: 3, sm: 4, md: 5 }, 
            width: '100%',
            maxWidth: { xs: '100%', sm: '450px' },
            background: 'rgba(255, 255, 255, 0.1)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            borderRadius: 3,
            boxShadow: '0 20px 40px rgba(0, 0, 0, 0.1)',
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'translateY(-5px)',
              boxShadow: '0 25px 50px rgba(0, 0, 0, 0.15)',
            }
          }}
        >
          <Typography 
            variant="h4" 
            component="h1" 
            gutterBottom
            sx={{ 
              textAlign: 'center',
              fontSize: { xs: '1.8rem', sm: '2.2rem', md: '2.5rem' },
              mb: 3,
              color: 'rgba(255, 255, 255, 0.95)',
              fontWeight: 600,
              textShadow: '0 2px 4px rgba(0,0,0,0.3)'
            }}
          >
            🔐 Welcome Back
          </Typography>
          
          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              autoComplete="username"
              autoFocus
              value={formData.username}
              onChange={handleChange}
              error={!!errors.username}
              helperText={errors.username}
              disabled={loading}
              sx={{ 
                mb: 2,
                '& .MuiOutlinedInput-root': {
                  background: 'rgba(255, 255, 255, 0.1)',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                  borderRadius: 2,
                  '&:hover': {
                    border: '1px solid rgba(255, 255, 255, 0.4)',
                  },
                  '&.Mui-focused': {
                    border: '1px solid #2196F3',
                  }
                },
                '& .MuiInputLabel-root': {
                  color: 'rgba(255, 255, 255, 0.8)',
                  '&.Mui-focused': {
                    color: '#2196F3',
                  }
                },
                '& .MuiInputBase-input': {
                  color: 'rgba(255, 255, 255, 0.9)',
                },
                '& .MuiFormHelperText-root': {
                  color: '#ff6b6b',
                }
              }}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type={showPassword ? 'text' : 'password'}
              id="password"
              autoComplete="current-password"
              value={formData.password}
              onChange={handleChange}
              error={!!errors.password}
              helperText={errors.password}
              disabled={loading}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="toggle password visibility"
                      onClick={() => setShowPassword(!showPassword)}
                      edge="end"
                      sx={{
                        color: 'rgba(255, 255, 255, 0.7)',
                        '&:hover': {
                          color: 'rgba(255, 255, 255, 0.9)',
                        }
                      }}
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
              sx={{ 
                mb: 3,
                '& .MuiOutlinedInput-root': {
                  background: 'rgba(255, 255, 255, 0.1)',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                  borderRadius: 2,
                  '&:hover': {
                    border: '1px solid rgba(255, 255, 255, 0.4)',
                  },
                  '&.Mui-focused': {
                    border: '1px solid #2196F3',
                  }
                },
                '& .MuiInputLabel-root': {
                  color: 'rgba(255, 255, 255, 0.8)',
                  '&.Mui-focused': {
                    color: '#2196F3',
                  }
                },
                '& .MuiInputBase-input': {
                  color: 'rgba(255, 255, 255, 0.9)',
                },
                '& .MuiFormHelperText-root': {
                  color: '#ff6b6b',
                }
              }}
            />

            {loading && (
              <Box sx={{ mt: 2, mb: 2 }}>
                <LinearProgress 
                  sx={{
                    background: 'rgba(255, 255, 255, 0.2)',
                    '& .MuiLinearProgress-bar': {
                      background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
                    }
                  }}
                />
                <Typography 
                  variant="body2" 
                  sx={{ 
                    mt: 1, 
                    textAlign: 'center',
                    color: 'rgba(255, 255, 255, 0.8)',
                    textShadow: '0 1px 2px rgba(0,0,0,0.3)'
                  }}
                >
                  Signing you in...
                </Typography>
              </Box>
            )}

            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={loading}
              sx={{ 
                mt: 2, 
                mb: 2,
                py: { xs: 1.5, sm: 2 },
                fontSize: { xs: '1rem', sm: '1.1rem' },
                background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
                boxShadow: '0 8px 16px rgba(33, 150, 243, 0.3)',
                '&:hover': {
                  background: 'linear-gradient(45deg, #1976D2 30%, #1E88E5 90%)',
                  transform: 'translateY(-2px)',
                  boxShadow: '0 12px 24px rgba(33, 150, 243, 0.4)',
                },
                '&:disabled': {
                  background: 'rgba(255, 255, 255, 0.2)',
                  color: 'rgba(255, 255, 255, 0.5)',
                }
              }}
            >
              {loading ? 'Signing In...' : 'Sign In'}
            </Button>
            
            <Box sx={{ textAlign: 'center' }}>
              <Typography 
                variant="body2" 
                sx={{
                  color: 'rgba(255, 255, 255, 0.8)',
                  textShadow: '0 1px 2px rgba(0,0,0,0.3)'
                }}
              >
                Don't have an account?{' '}
                <Button 
                  variant="text" 
                  onClick={() => navigate('/register')}
                  disabled={loading}
                  sx={{ 
                    fontSize: { xs: '0.9rem', sm: '1rem' },
                    p: 0,
                    minWidth: 'auto',
                    color: '#2196F3',
                    textShadow: 'none',
                    '&:hover': {
                      background: 'rgba(33, 150, 243, 0.1)',
                      transform: 'translateY(-1px)',
                    }
                  }}
                >
                  Sign up
                </Button>
              </Typography>
            </Box>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default Login; 