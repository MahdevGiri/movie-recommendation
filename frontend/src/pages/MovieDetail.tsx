import React from 'react';
import { Container, Typography } from '@mui/material';

const MovieDetail: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        🎬 Movie Details
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Movie details coming soon...
      </Typography>
    </Container>
  );
};

export default MovieDetail; 