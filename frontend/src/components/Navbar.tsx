import React, { useState } from 'react';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Button, 
  Box, 
  IconButton, 
  Drawer, 
  List, 
  ListItem, 
  ListItemText,
  useTheme,
  useMediaQuery
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { Link as RouterLink } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

type NavItem = {
  text: string;
  path: string;
};

type AuthItemWithPath = {
  text: string;
  path: string;
};

type AuthItemWithAction = {
  text: string;
  action: () => void;
};

type AuthItem = AuthItemWithPath | AuthItemWithAction;

const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const navItems: NavItem[] = [
    { text: 'Home', path: '/' },
    { text: 'Movies', path: '/movies' },
    ...(user ? [
      { text: 'Recommendations', path: '/recommendations' },
      { text: 'Profile', path: '/profile' }
    ] : [])
  ];

  const authItems: AuthItem[] = user ? [
    { text: 'Logout', action: logout }
  ] : [
    { text: 'Login', path: '/login' },
    { text: 'Register', path: '/register' }
  ];

  const isAuthItemWithPath = (item: AuthItem): item is AuthItemWithPath => {
    return 'path' in item;
  };

  const isAuthItemWithAction = (item: AuthItem): item is AuthItemWithAction => {
    return 'action' in item;
  };

  const drawer = (
    <Box sx={{ 
      width: 250,
      background: 'rgba(255, 255, 255, 0.1)',
      backdropFilter: 'blur(20px)',
      height: '100%'
    }}>
      <List>
        {navItems.map((item, index) => (
          <ListItem 
            key={item.text} 
            component={RouterLink} 
            to={item.path}
            onClick={handleDrawerToggle}
            sx={{ 
              color: 'rgba(255, 255, 255, 0.9)', 
              textDecoration: 'none',
              animation: `fadeInUp 0.6s ease-out ${index * 0.1}s both`,
              transition: 'all 0.3s ease',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                transform: 'translateX(5px)',
              }
            }}
          >
            <ListItemText 
              primary={item.text} 
              sx={{
                '& .MuiTypography-root': {
                  fontWeight: 500,
                  fontSize: '1.1rem'
                }
              }}
            />
          </ListItem>
        ))}
        {authItems.map((item, index) => (
          <ListItem 
            key={item.text} 
            component={isAuthItemWithPath(item) ? RouterLink : 'div'}
            to={isAuthItemWithPath(item) ? item.path : undefined}
            onClick={() => {
              if (isAuthItemWithAction(item)) item.action();
              handleDrawerToggle();
            }}
            sx={{ 
              color: 'rgba(255, 255, 255, 0.9)', 
              textDecoration: 'none',
              animation: `fadeInUp 0.6s ease-out ${(navItems.length + index) * 0.1}s both`,
              transition: 'all 0.3s ease',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                transform: 'translateX(5px)',
              }
            }}
          >
            <ListItemText 
              primary={item.text} 
              sx={{
                '& .MuiTypography-root': {
                  fontWeight: 500,
                  fontSize: '1.1rem'
                }
              }}
            />
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <>
      <AppBar 
        position="fixed" 
        elevation={0}
        sx={{
          background: 'rgba(255, 255, 255, 0.1)',
          backdropFilter: 'blur(20px)',
          borderBottom: '1px solid rgba(255, 255, 255, 0.2)',
          transition: 'all 0.3s ease',
          animation: 'fadeInUp 0.6s ease-out'
        }}
      >
        <Toolbar sx={{ 
          justifyContent: 'space-between',
          px: { xs: 1, sm: 2, md: 3 }
        }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            {isMobile && (
              <IconButton
                color="inherit"
                aria-label="open drawer"
                edge="start"
                onClick={handleDrawerToggle}
                sx={{ 
                  mr: 1,
                  color: 'rgba(255, 255, 255, 0.9)',
                  '&:hover': {
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    transform: 'scale(1.1)',
                  },
                  transition: 'all 0.3s ease'
                }}
              >
                <MenuIcon />
              </IconButton>
            )}
            
            <Typography 
              variant="h6" 
              component="div" 
              sx={{ 
                flexGrow: { xs: 1, md: 0 },
                fontSize: { xs: '1.1rem', sm: '1.3rem', md: '1.5rem' },
                textAlign: { xs: 'center', md: 'left' },
                color: 'rgba(255, 255, 255, 0.95)',
                fontWeight: 600,
                textShadow: '0 2px 4px rgba(0,0,0,0.3)',
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'scale(1.05)',
                }
              }}
            >
              🎬 Movie Recommendations
            </Typography>
          </Box>
          
          {!isMobile && (
            <Box sx={{ display: 'flex', gap: { sm: 1, md: 2 } }}>
              <Button 
                component={RouterLink} 
                to="/"
                sx={{ 
                  fontSize: { sm: '0.9rem', md: '1rem' },
                  color: 'rgba(255, 255, 255, 0.9)',
                  fontWeight: 500,
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    transform: 'translateY(-2px)',
                    color: 'rgba(255, 255, 255, 1)',
                  }
                }}
              >
                Home
              </Button>
              <Button 
                component={RouterLink} 
                to="/movies"
                sx={{ 
                  fontSize: { sm: '0.9rem', md: '1rem' },
                  color: 'rgba(255, 255, 255, 0.9)',
                  fontWeight: 500,
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    transform: 'translateY(-2px)',
                    color: 'rgba(255, 255, 255, 1)',
                  }
                }}
              >
                Movies
              </Button>
              
              {user ? (
                <>
                  <Button 
                    component={RouterLink} 
                    to="/recommendations"
                    sx={{ 
                      fontSize: { sm: '0.9rem', md: '1rem' },
                      color: 'rgba(255, 255, 255, 0.9)',
                      fontWeight: 500,
                      transition: 'all 0.3s ease',
                      '&:hover': {
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        transform: 'translateY(-2px)',
                        color: 'rgba(255, 255, 255, 1)',
                      }
                    }}
                  >
                    Recommendations
                  </Button>
                  <Button 
                    component={RouterLink} 
                    to="/profile"
                    sx={{ 
                      fontSize: { sm: '0.9rem', md: '1rem' },
                      color: 'rgba(255, 255, 255, 0.9)',
                      fontWeight: 500,
                      transition: 'all 0.3s ease',
                      '&:hover': {
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        transform: 'translateY(-2px)',
                        color: 'rgba(255, 255, 255, 1)',
                      }
                    }}
                  >
                    Profile
                  </Button>
                  <Button 
                    onClick={logout}
                    sx={{ 
                      fontSize: { sm: '0.9rem', md: '1rem' },
                      color: 'rgba(255, 255, 255, 0.9)',
                      fontWeight: 500,
                      transition: 'all 0.3s ease',
                      '&:hover': {
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        transform: 'translateY(-2px)',
                        color: 'rgba(255, 255, 255, 1)',
                      }
                    }}
                  >
                    Logout
                  </Button>
                </>
              ) : (
                <>
                  <Button 
                    component={RouterLink} 
                    to="/login"
                    sx={{ 
                      fontSize: { sm: '0.9rem', md: '1rem' },
                      color: 'rgba(255, 255, 255, 0.9)',
                      fontWeight: 500,
                      transition: 'all 0.3s ease',
                      '&:hover': {
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        transform: 'translateY(-2px)',
                        color: 'rgba(255, 255, 255, 1)',
                      }
                    }}
                  >
                    Login
                  </Button>
                  <Button 
                    component={RouterLink} 
                    to="/register"
                    sx={{ 
                      fontSize: { sm: '0.9rem', md: '1rem' },
                      color: 'rgba(255, 255, 255, 0.9)',
                      fontWeight: 500,
                      transition: 'all 0.3s ease',
                      '&:hover': {
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        transform: 'translateY(-2px)',
                        color: 'rgba(255, 255, 255, 1)',
                      }
                    }}
                  >
                    Register
                  </Button>
                </>
              )}
            </Box>
          )}
        </Toolbar>
      </AppBar>
      
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true, // Better open performance on mobile.
        }}
        sx={{
          display: { xs: 'block', md: 'none' },
          '& .MuiDrawer-paper': { 
            boxSizing: 'border-box', 
            width: 250,
            background: 'rgba(255, 255, 255, 0.1)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            boxShadow: '0 20px 40px rgba(0, 0, 0, 0.1)',
          },
        }}
      >
        {drawer}
      </Drawer>
    </>
  );
};

export default Navbar; 