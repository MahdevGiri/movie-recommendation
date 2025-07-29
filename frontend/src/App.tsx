import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box, ThemeProvider } from '@mui/material';
import { theme } from './theme';
import { AuthProvider } from './contexts/AuthContext';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Movies from './pages/Movies';
import Recommendations from './pages/Recommendations';
import Profile from './pages/Profile';
import MovieDetail from './pages/MovieDetail';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <AuthProvider>
        <Box 
          sx={{ 
            minHeight: '100vh',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)',
            backgroundSize: '400% 400%',
            animation: 'gradientShift 15s ease infinite',
            position: 'relative',
            '&::before': {
              content: '""',
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: 'url("data:image/svg+xml,%3Csvg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"%3E%3Cg fill="none" fill-rule="evenodd"%3E%3Cg fill="%23ffffff" fill-opacity="0.05"%3E%3Ccircle cx="30" cy="30" r="2"/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")',
              pointerEvents: 'none',
            }
          }}
        >
          <Navbar />
          <Box 
            component="main" 
            sx={{ 
              pt: 8,
              position: 'relative',
              zIndex: 1,
            }}
          >
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/movies" element={<Movies />} />
              <Route path="/movies/:id" element={<MovieDetail />} />
              <Route 
                path="/recommendations" 
                element={
                  <ProtectedRoute>
                    <Recommendations />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/profile" 
                element={
                  <ProtectedRoute>
                    <Profile />
                  </ProtectedRoute>
                } 
              />
            </Routes>
          </Box>
        </Box>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App; 