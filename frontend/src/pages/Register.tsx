import React from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  TextField, 
  Button, 
  Paper, 
  Grid,
  LinearProgress,
  InputAdornment,
  IconButton,
  Select,
  MenuItem,
  FormControl,
  InputLabel
} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

interface FormErrors {
  username?: string;
  password?: string;
  name?: string;
  email?: string;
  age?: string;
}

const Register: React.FC = () => {
  const { register, user } = useAuth();
  const navigate = useNavigate();

  // Redirect if already logged in
  React.useEffect(() => {
    if (user) {
      navigate('/');
    }
  }, [user, navigate]);

  const [formData, setFormData] = React.useState({
    username: '',
    password: '',
    name: '',
    email: '',
    age: '',
    preferred_genre: 'Drama'
  });

  const [errors, setErrors] = React.useState<FormErrors>({});
  const [loading, setLoading] = React.useState(false);
  const [showPassword, setShowPassword] = React.useState(false);
  const [passwordStrength, setPasswordStrength] = React.useState(0);

  // Password strength calculation
  const calculatePasswordStrength = (password: string): number => {
    let strength = 0;
    if (password.length >= 8) strength += 25;
    if (/[a-z]/.test(password)) strength += 25;
    if (/[A-Z]/.test(password)) strength += 25;
    if (/[0-9]/.test(password)) strength += 25;
    return strength;
  };

  // Form validation
  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    // Username validation
    if (!formData.username.trim()) {
      newErrors.username = 'Username is required';
    } else if (formData.username.length < 3) {
      newErrors.username = 'Username must be at least 3 characters';
    } else if (!/^[a-zA-Z0-9_]+$/.test(formData.username)) {
      newErrors.username = 'Username can only contain letters, numbers, and underscores';
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    } else if (passwordStrength < 75) {
      newErrors.password = 'Password is too weak';
    }

    // Name validation
    if (!formData.name.trim()) {
      newErrors.name = 'Full name is required';
    }

    // Email validation
    if (formData.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    // Age validation
    if (formData.age) {
      const age = parseInt(formData.age);
      if (isNaN(age) || age < 13 || age > 120) {
        newErrors.age = 'Age must be between 13 and 120';
      }
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
      await register({
        ...formData,
        age: formData.age ? parseInt(formData.age) : undefined
      });
      // Redirect to home page after successful registration
      navigate('/');
    } catch (error) {
      console.error('Registration failed:', error);
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

    // Update password strength
    if (name === 'password') {
      setPasswordStrength(calculatePasswordStrength(value));
    }

    // Clear error when user starts typing
    if (errors[name as keyof FormErrors]) {
      setErrors({
        ...errors,
        [name]: undefined
      });
    }
  };

  const handleSelectChange = (e: any) => {
    setFormData({
      ...formData,
      preferred_genre: e.target.value
    });
  };

  const getPasswordStrengthColor = () => {
    if (passwordStrength >= 75) return '#4caf50';
    if (passwordStrength >= 50) return '#ff9800';
    return '#f44336';
  };

  const getPasswordStrengthText = () => {
    if (passwordStrength >= 75) return 'Strong';
    if (passwordStrength >= 50) return 'Medium';
    return 'Weak';
  };

  const commonTextFieldStyles = {
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
  };

  return (
    <Container maxWidth="md" sx={{ mt: { xs: 2, sm: 4 }, mb: 4 }}>
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
            maxWidth: { xs: '100%', sm: '600px' },
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
            🎬 Join the Community
          </Typography>
          
          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  id="username"
                  label="Username"
                  name="username"
                  autoComplete="username"
                  value={formData.username}
                  onChange={handleChange}
                  error={!!errors.username}
                  helperText={errors.username}
                  disabled={loading}
                  sx={{ ...commonTextFieldStyles }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  id="name"
                  label="Full Name"
                  name="name"
                  autoComplete="name"
                  value={formData.name}
                  onChange={handleChange}
                  error={!!errors.name}
                  helperText={errors.name}
                  disabled={loading}
                  sx={{ ...commonTextFieldStyles }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  margin="normal"
                  fullWidth
                  id="email"
                  label="Email (Optional)"
                  name="email"
                  autoComplete="email"
                  value={formData.email}
                  onChange={handleChange}
                  error={!!errors.email}
                  helperText={errors.email}
                  disabled={loading}
                  sx={{ ...commonTextFieldStyles }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  margin="normal"
                  fullWidth
                  id="age"
                  label="Age (Optional)"
                  name="age"
                  type="number"
                  value={formData.age}
                  onChange={handleChange}
                  error={!!errors.age}
                  helperText={errors.age}
                  disabled={loading}
                  sx={{ ...commonTextFieldStyles }}
                />
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth margin="normal" disabled={loading}>
                  <InputLabel sx={{ color: 'rgba(255, 255, 255, 0.8)' }}>
                    Preferred Genre
                  </InputLabel>
                  <Select
                    value={formData.preferred_genre}
                    onChange={handleSelectChange}
                    sx={{
                      background: 'rgba(255, 255, 255, 0.1)',
                      backdropFilter: 'blur(10px)',
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: 2,
                      color: 'rgba(255, 255, 255, 0.9)',
                      '&:hover': {
                        border: '1px solid rgba(255, 255, 255, 0.4)',
                      },
                      '&.Mui-focused': {
                        border: '1px solid #2196F3',
                      },
                      '& .MuiSelect-icon': {
                        color: 'rgba(255, 255, 255, 0.7)',
                      }
                    }}
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
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  name="password"
                  label="Password"
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  autoComplete="new-password"
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
                  sx={{ ...commonTextFieldStyles }}
                />
                {formData.password && (
                  <Box sx={{ mt: 1 }}>
                    <LinearProgress 
                      variant="determinate" 
                      value={passwordStrength}
                      sx={{
                        height: 8,
                        borderRadius: 4,
                        background: 'rgba(255, 255, 255, 0.2)',
                        '& .MuiLinearProgress-bar': {
                          background: getPasswordStrengthColor(),
                          borderRadius: 4,
                        }
                      }}
                    />
                    <Typography 
                      variant="caption" 
                      sx={{ 
                        mt: 0.5, 
                        display: 'block',
                        color: getPasswordStrengthColor(),
                        textShadow: '0 1px 2px rgba(0,0,0,0.3)'
                      }}
                    >
                      Password strength: {getPasswordStrengthText()}
                    </Typography>
                  </Box>
                )}
              </Grid>
            </Grid>

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
                  Creating your account...
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
                mt: 3, 
                mb: 2,
                py: { xs: 1.5, sm: 2 },
                fontSize: { xs: '1rem', sm: '1.1rem' },
                background: 'linear-gradient(45deg, #FF6B35 30%, #F7931E 90%)',
                boxShadow: '0 8px 16px rgba(255, 107, 53, 0.3)',
                '&:hover': {
                  background: 'linear-gradient(45deg, #E64A19 30%, #F57C00 90%)',
                  transform: 'translateY(-2px)',
                  boxShadow: '0 12px 24px rgba(255, 107, 53, 0.4)',
                },
                '&:disabled': {
                  background: 'rgba(255, 255, 255, 0.2)',
                  color: 'rgba(255, 255, 255, 0.5)',
                }
              }}
            >
              {loading ? 'Creating Account...' : 'Create Account'}
            </Button>
            
            <Box sx={{ textAlign: 'center' }}>
              <Typography 
                variant="body2" 
                sx={{
                  color: 'rgba(255, 255, 255, 0.8)',
                  textShadow: '0 1px 2px rgba(0,0,0,0.3)'
                }}
              >
                Already have an account?{' '}
                <Button 
                  variant="text" 
                  onClick={() => navigate('/login')}
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
                  Sign in
                </Button>
              </Typography>
            </Box>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default Register; 