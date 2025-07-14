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
    <Box sx={{ width: 250 }}>
      <List>
        {navItems.map((item) => (
          <ListItem 
            key={item.text} 
            component={RouterLink} 
            to={item.path}
            onClick={handleDrawerToggle}
            sx={{ 
              color: 'inherit', 
              textDecoration: 'none',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.1)'
              }
            }}
          >
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
        {authItems.map((item) => (
          <ListItem 
            key={item.text} 
            component={isAuthItemWithPath(item) ? RouterLink : 'div'}
            to={isAuthItemWithPath(item) ? item.path : undefined}
            onClick={() => {
              if (isAuthItemWithAction(item)) item.action();
              handleDrawerToggle();
            }}
            sx={{ 
              color: 'inherit', 
              textDecoration: 'none',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.1)'
              }
            }}
          >
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <>
      <AppBar position="fixed">
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
                sx={{ mr: 1 }}
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
                textAlign: { xs: 'center', md: 'left' }
              }}
            >
              🎬 Movie Recommendations
            </Typography>
          </Box>
          
          {!isMobile && (
            <Box sx={{ display: 'flex', gap: { sm: 1, md: 2 } }}>
              <Button 
                color="inherit" 
                component={RouterLink} 
                to="/"
                sx={{ fontSize: { sm: '0.9rem', md: '1rem' } }}
              >
                Home
              </Button>
              <Button 
                color="inherit" 
                component={RouterLink} 
                to="/movies"
                sx={{ fontSize: { sm: '0.9rem', md: '1rem' } }}
              >
                Movies
              </Button>
              
              {user ? (
                <>
                  <Button 
                    color="inherit" 
                    component={RouterLink} 
                    to="/recommendations"
                    sx={{ fontSize: { sm: '0.9rem', md: '1rem' } }}
                  >
                    Recommendations
                  </Button>
                  <Button 
                    color="inherit" 
                    component={RouterLink} 
                    to="/profile"
                    sx={{ fontSize: { sm: '0.9rem', md: '1rem' } }}
                  >
                    Profile
                  </Button>
                  <Button 
                    color="inherit" 
                    onClick={logout}
                    sx={{ fontSize: { sm: '0.9rem', md: '1rem' } }}
                  >
                    Logout
                  </Button>
                </>
              ) : (
                <>
                  <Button 
                    color="inherit" 
                    component={RouterLink} 
                    to="/login"
                    sx={{ fontSize: { sm: '0.9rem', md: '1rem' } }}
                  >
                    Login
                  </Button>
                  <Button 
                    color="inherit" 
                    component={RouterLink} 
                    to="/register"
                    sx={{ fontSize: { sm: '0.9rem', md: '1rem' } }}
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
            backgroundColor: 'primary.main',
            color: 'white'
          },
        }}
      >
        {drawer}
      </Drawer>
    </>
  );
};

export default Navbar; 