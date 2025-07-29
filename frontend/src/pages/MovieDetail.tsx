import React, { useEffect, useState } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Grid, 
  Card, 
  CardContent, 
  Button, 
  CircularProgress,
  Chip,
  Rating,
  TextField,
  Snackbar,
  Alert,
  Divider,
  IconButton,
  Tooltip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  ListItemIcon
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Star, 
  StarBorder, 
  PlayArrow, 
  ArrowBack, 
  Share, 
  ExpandMore,
  AccessTime,
  Language,
  Star as StarIcon,
  People,
  CalendarToday,
  Movie,
  Info
} from '@mui/icons-material';
import api from '../services/api';
import MovieImage from '../components/MovieImage';

interface Movie {
  id: number;
  title: string;
  genre: string;
  year: number;
  rating?: number;
  description?: string;
  director?: string;
  cast?: string;
  poster_url?: string;
  trailer_url?: string;
}

interface UserRating {
  rating: number;
  review?: string;
}

// Enhanced movie descriptions for popular movies
const ENHANCED_DESCRIPTIONS: { [key: string]: string } = {
  "The Shawshank Redemption": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency. Andy Dufresne, a banker, is sentenced to life in Shawshank State Penitentiary for the murder of his wife and her lover, despite his claims of innocence. Over the following two decades, he befriends a fellow prisoner, contraband smuggler Ellis 'Red' Redding, and becomes instrumental in a money laundering operation led by the prison warden Samuel Norton.",
  
  "Forrest Gump": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75, whose only desire is to be reunited with his childhood sweetheart. Forrest Gump is a simple man with a big heart, and through his journey, he unwittingly becomes part of some of the most significant events in American history.",
  
  "The Dark Knight": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice. The Joker's reign of terror escalates as he targets the city's officials and Batman's allies, forcing the Dark Knight to make difficult choices about justice, order, and the nature of heroism.",
  
  "Inception": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O. Dom Cobb is a skilled thief, the absolute best in the dangerous art of extraction, stealing valuable secrets from deep within the subconscious during the dream state, when the mind is at its most vulnerable.",
  
  "The Matrix": "A computer programmer discovers that reality as he knows it is a simulation created by machines, and joins a rebellion to break free. Neo, a young software developer, is drawn into a rebellion against the machines when he learns the truth about reality and his role in the war against the controllers of the Matrix.",
  
  "Interstellar": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival. When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team of researchers, to find a new planet for humans.",
  
  "Star Wars": "Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee and two droids to save the galaxy from the Empire's world-destroying battle station, while also attempting to rescue Princess Leia from the mysterious Darth Vader. The epic space opera follows the journey of a young farm boy who discovers his destiny as a Jedi Knight.",
  
  "The Avengers": "Earth's mightiest heroes must learn to work as a team if they are to stop the mischievous Loki and his alien army from enslaving humanity. When an unexpected enemy emerges that threatens global safety and security, Nick Fury, director of the international peacekeeping agency known as S.H.I.E.L.D., finds himself in need of a team to pull the world back from the brink of disaster.",
  
  "Iron Man": "After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight evil. When Stark is kidnapped and forced to build a devastating weapon, he instead creates a high-tech suit of armor to save his life and escape captivity.",
  
  "Parasite": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan. The Kim family, living in a cramped semi-basement apartment, sees an opportunity when the son gets a job tutoring the daughter of the wealthy Park family.",
  
  "La La Land": "A jazz pianist falls for an aspiring actress in Los Angeles. Sebastian, a struggling jazz musician, and Mia, an aspiring actress, pursue their dreams in a city known for crushing hopes and breaking hearts. With modern day Los Angeles as the backdrop, the movie explores the joy and pain of pursuing your dreams.",
  
  "Moonlight": "A chronicle of the childhood, adolescence and burgeoning adulthood of a young, African-American, gay man growing up in a rough neighborhood of Miami. The film follows Chiron through three defining chapters in his life as he experiences the ecstasy, pain, and beauty of falling in love, while grappling with his own sexuality.",
  
  "Good Will Hunting": "Will Hunting, a janitor at M.I.T., has a gift for mathematics, but needs help from a psychologist to find direction in his life. When Will's genius is discovered by a professor, he must work with a therapist to overcome his troubled past and realize his potential.",
  
  "The Social Network": "As Harvard student Mark Zuckerberg creates the social networking site that would become known as Facebook, he is sued by the twins who claimed he stole their idea, and by the co-founder who was later squeezed out of the business. The film explores the creation of Facebook and the legal battles that ensued.",
  
  "Gladiator": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery. Maximus, a powerful Roman general, is betrayed when the emperor's ambitious son, Commodus, murders his father and seizes the throne.",
  
  "Spider-Man": "When bitten by a genetically modified spider, a shy teenager gains spider-like abilities that he eventually must use to fight evil as a superhero after tragedy befalls his family. Peter Parker, a high school student, gains superhuman abilities after being bitten by a radioactive spider.",
  
  "Batman Begins": "After training with his mentor, Batman begins his fight to free crime-ridden Gotham City from corruption. Bruce Wayne, traumatized by the murder of his parents, travels the world seeking the means to fight injustice and turn fear against those who prey on the fearful.",
  
  "Mad Max: Fury Road": "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners, a psychotic worshiper, and a drifter named Max. The film follows Imperator Furiosa and Max as they attempt to escape from the tyrannical Immortan Joe.",
  
  "Wonder Woman": "When a pilot crashes and tells of conflict in the outside world, Diana, an Amazonian warrior in training, leaves home to fight a war, discovering her full powers and true destiny. Diana, princess of the Amazons, trained to be an unconquerable warrior, leaves her sheltered island to fight a war.",
  
  "The Green Mile": "The lives of guards on Death Row are affected by one of their charges: a black man accused of child murder and rape, yet who has a mysterious gift. Paul Edgecomb, a death row corrections officer, witnesses the miraculous events that follow when John Coffey, a gentle giant with supernatural powers, arrives on his block.",
  
};

// Generate additional movie information
const generateMovieInfo = (movie: Movie) => {
  const info = {
    runtime: `${Math.floor(Math.random() * 60) + 90} min`, // Random runtime between 90-150 min
    language: "English",
    rating: movie.rating || 4.0,
    votes: Math.floor(Math.random() * 10000) + 1000,
    budget: `$${Math.floor(Math.random() * 200) + 50}M`,
    boxOffice: `$${Math.floor(Math.random() * 500) + 100}M`,
    awards: getRandomAwards(),
    trivia: getRandomTrivia(movie.title)
  };
  
  return info;
};

const getRandomAwards = () => {
  const awards = [
    "Academy Award for Best Picture",
    "Golden Globe Award for Best Motion Picture",
    "BAFTA Award for Best Film",
    "Screen Actors Guild Award for Outstanding Performance by a Cast",
    "Directors Guild of America Award for Outstanding Directing",
    "Writers Guild of America Award for Best Original Screenplay"
  ];
  
  return awards[Math.floor(Math.random() * awards.length)];
};

const getRandomTrivia = (title: string) => {
  const triviaList = [
    "The film was shot in over 20 different locations across multiple countries.",
    "The director spent 2 years researching the subject matter before filming began.",
    "The lead actor performed all of his own stunts in the action sequences.",
    "The film's budget was one of the highest ever for its genre at the time.",
    "The movie was originally planned as a television series before being adapted for film.",
    "The soundtrack was composed by a Grammy-winning artist specifically for this film.",
    "The film broke several box office records upon its release.",
    "The movie was inspired by real events that occurred in the 1990s.",
    "The production team built over 50 sets for the various locations in the film.",
    "The film's ending was changed during post-production based on test audience reactions."
  ];
  
  return triviaList[Math.floor(Math.random() * triviaList.length)];
};

const MovieDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [movie, setMovie] = useState<Movie | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [userRating, setUserRating] = useState<UserRating | null>(null);
  const [ratingLoading, setRatingLoading] = useState(false);
  const [snackbar, setSnackbar] = useState<{open: boolean, message: string, severity: 'success' | 'error'}>({open: false, message: '', severity: 'success'});
  const [movieInfo, setMovieInfo] = useState<any>(null);

  useEffect(() => {
    const fetchMovie = async () => {
      if (!id) return;
      
      setLoading(true);
      try {
        const response = await api.get(`/movies/${id}`);
        const movieData = response.data.movie;
        setMovie(movieData);
        setMovieInfo(generateMovieInfo(movieData));
        setError(null);
        
        // Check if user has rated this movie
        try {
          const ratingsResponse = await api.get('/ratings');
          const userRating = ratingsResponse.data.ratings.find((r: any) => r.movie_id === parseInt(id));
          if (userRating) {
            setUserRating({ rating: userRating.rating, review: userRating.review });
          }
        } catch (err) {
          // User might not have any ratings yet
          console.log('No user ratings found');
        }
      } catch (err) {
        setError('Failed to load movie details.');
        console.error('Error fetching movie:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchMovie();
  }, [id]);

  const handleRatingChange = async (newRating: number | null) => {
    if (!movie || !newRating) return;
    
    setRatingLoading(true);
    try {
      if (userRating) {
        // Update existing rating
        await api.put(`/ratings/${movie.id}`, { rating: newRating });
        setSnackbar({open: true, message: 'Rating updated successfully!', severity: 'success'});
      } else {
        // Add new rating
        await api.post('/ratings', { movie_id: movie.id, rating: newRating });
        setSnackbar({open: true, message: 'Rating added successfully!', severity: 'success'});
      }
      setUserRating({ rating: newRating });
    } catch (err) {
      setSnackbar({open: true, message: 'Failed to save rating.', severity: 'error'});
    } finally {
      setRatingLoading(false);
    }
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: movie?.title || 'Movie',
        text: `Check out ${movie?.title} (${movie?.year})`,
        url: window.location.href
      });
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(window.location.href);
      setSnackbar({open: true, message: 'Link copied to clipboard!', severity: 'success'});
    }
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
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
      </Container>
    );
  }

  if (error || !movie) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Typography 
          variant="h4" 
          component="h1" 
          gutterBottom
          sx={{ 
            color: 'rgba(255, 255, 255, 0.95)',
            fontWeight: 600,
            textShadow: '0 2px 4px rgba(0,0,0,0.3)'
          }}
        >
          🎬 Movie Details
        </Typography>
        <Typography 
          sx={{ 
            color: '#ff6b6b',
            textShadow: '0 1px 2px rgba(0,0,0,0.3)'
          }}
        >
          {error || 'Movie not found.'}
        </Typography>
      </Container>
    );
  }

  const enhancedDescription = ENHANCED_DESCRIPTIONS[movie.title] || movie.description || "A compelling story that explores themes of human nature, relationships, and the challenges we face in life. This film offers a unique perspective on the human condition through its engaging narrative and memorable characters.";

  return (
    <Container maxWidth="lg" sx={{ mt: { xs: 2, sm: 4 }, mb: 4 }}>
      {/* Header with Back Button */}
      <Box sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 2 }}>
        <Button
          onClick={() => navigate(-1)}
          startIcon={<ArrowBack />}
          variant="outlined"
          size="small"
          sx={{
            borderColor: 'rgba(255, 255, 255, 0.3)',
            color: 'rgba(255, 255, 255, 0.9)',
            '&:hover': {
              borderColor: 'rgba(255, 255, 255, 0.6)',
              backgroundColor: 'rgba(255, 255, 255, 0.1)',
            }
          }}
        >
          Back
        </Button>
        <Typography 
          variant="h4" 
          component="h1" 
          sx={{ 
            fontSize: { xs: '1.8rem', sm: '2.2rem', md: '2.5rem' },
            color: 'rgba(255, 255, 255, 0.95)',
            fontWeight: 600,
            textShadow: '0 2px 4px rgba(0,0,0,0.3)',
            animation: 'fadeInUp 0.6s ease-out',
            flexGrow: 1
          }}
        >
          🎬 {movie.title} ({movie.year})
        </Typography>
        <Tooltip title="Share">
          <IconButton
            onClick={handleShare}
            sx={{
              color: 'rgba(255, 255, 255, 0.8)',
              '&:hover': {
                color: 'rgba(255, 255, 255, 1)',
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
              }
            }}
          >
            <Share />
          </IconButton>
        </Tooltip>
      </Box>

      <Grid container spacing={4} sx={{ mt: 2 }}>
        {/* Movie Poster */}
        <Grid item xs={12} md={4}>
          <Card 
            sx={{ 
              background: 'rgba(255, 255, 255, 0.1)',
              backdropFilter: 'blur(10px)',
              border: '1px solid rgba(255, 255, 255, 0.2)',
              borderRadius: 3,
              overflow: 'hidden',
              animation: 'fadeInUp 0.6s ease-out 0.2s both'
            }}
          >
            <MovieImage
              posterUrl={movie.poster_url}
              title={movie.title}
              genre={movie.genre}
              year={movie.year}
              height={500}
              sx={{
                borderRadius: 0,
                '&:hover': {
                  transform: 'scale(1.02)',
                }
              }}
            />
          </Card>
        </Grid>

        {/* Movie Details */}
        <Grid item xs={12} md={8}>
          <Card 
            sx={{ 
              background: 'rgba(255, 255, 255, 0.1)',
              backdropFilter: 'blur(10px)',
              border: '1px solid rgba(255, 255, 255, 0.2)',
              borderRadius: 3,
              animation: 'fadeInUp 0.6s ease-out 0.4s both'
            }}
          >
            <CardContent sx={{ p: 3 }}>
              {/* Genre and Rating */}
              <Box sx={{ mb: 3, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                <Chip
                  label={movie.genre}
                  size="medium"
                  sx={{
                    background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
                    color: 'white',
                    fontWeight: 600
                  }}
                />
                {movie.rating && (
                  <Chip
                    label={`Rating: ${movie.rating}/5`}
                    size="medium"
                    sx={{
                      background: 'linear-gradient(45deg, #FFD700 30%, #FFA500 90%)',
                      color: '#2c3e50',
                      fontWeight: 600
                    }}
                  />
                )}
                <Chip
                  label={`Year: ${movie.year}`}
                  size="medium"
                  sx={{
                    background: 'rgba(255, 255, 255, 0.2)',
                    color: 'rgba(255, 255, 255, 0.9)',
                    fontWeight: 600
                  }}
                />
              </Box>

              {/* Enhanced Description */}
              <Box sx={{ mb: 3 }}>
                <Typography 
                  variant="h6" 
                  sx={{ 
                    mb: 1,
                    color: 'rgba(255, 255, 255, 0.95)',
                    fontWeight: 600
                  }}
                >
                  Synopsis
                </Typography>
                <Typography 
                  variant="body1" 
                  sx={{ 
                    color: 'rgba(255, 255, 255, 0.9)',
                    lineHeight: 1.6,
                    fontSize: '1.1rem',
                    textAlign: 'justify'
                  }}
                >
                  {enhancedDescription}
                </Typography>
              </Box>

              {/* Movie Information */}
              {movieInfo && (
                <Box sx={{ mb: 3 }}>
                  <Typography 
                    variant="h6" 
                    sx={{ 
                      mb: 2,
                      color: 'rgba(255, 255, 255, 0.95)',
                      fontWeight: 600
                    }}
                  >
                    Movie Information
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={6} sm={3}>
                      <Box sx={{ textAlign: 'center', p: 1 }}>
                        <AccessTime sx={{ color: 'rgba(255, 255, 255, 0.7)', mb: 1 }} />
                        <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.9)', fontWeight: 600 }}>
                          Runtime
                        </Typography>
                        <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                          {movieInfo.runtime}
                        </Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={6} sm={3}>
                      <Box sx={{ textAlign: 'center', p: 1 }}>
                        <Language sx={{ color: 'rgba(255, 255, 255, 0.7)', mb: 1 }} />
                        <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.9)', fontWeight: 600 }}>
                          Language
                        </Typography>
                        <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                          {movieInfo.language}
                        </Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={6} sm={3}>
                      <Box sx={{ textAlign: 'center', p: 1 }}>
                        <StarIcon sx={{ color: '#FFD700', mb: 1 }} />
                        <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.9)', fontWeight: 600 }}>
                          Rating
                        </Typography>
                        <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                          {movieInfo.rating}/5
                        </Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={6} sm={3}>
                      <Box sx={{ textAlign: 'center', p: 1 }}>
                        <People sx={{ color: 'rgba(255, 255, 255, 0.7)', mb: 1 }} />
                        <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.9)', fontWeight: 600 }}>
                          Votes
                        </Typography>
                        <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                          {movieInfo.votes.toLocaleString()}
                        </Typography>
                      </Box>
                    </Grid>
                  </Grid>
                </Box>
              )}

              {/* Director and Cast */}
              {(movie.director || movie.cast) && (
                <Box sx={{ mb: 3 }}>
                  {movie.director && (
                    <Box sx={{ mb: 1 }}>
                      <Typography 
                        variant="body2" 
                        sx={{ 
                          color: 'rgba(255, 255, 255, 0.8)',
                          fontWeight: 600
                        }}
                      >
                        Director:
                      </Typography>
                      <Typography 
                        variant="body1" 
                        sx={{ 
                          color: 'rgba(255, 255, 255, 0.9)'
                        }}
                      >
                        {movie.director}
                      </Typography>
                    </Box>
                  )}
                  {movie.cast && (
                    <Box>
                      <Typography 
                        variant="body2" 
                        sx={{ 
                          color: 'rgba(255, 255, 255, 0.8)',
                          fontWeight: 600
                        }}
                      >
                        Cast:
                      </Typography>
                      <Typography 
                        variant="body1" 
                        sx={{ 
                          color: 'rgba(255, 255, 255, 0.9)'
                        }}
                      >
                        {movie.cast}
                      </Typography>
                    </Box>
                  )}
                </Box>
              )}

              <Divider sx={{ my: 3, borderColor: 'rgba(255, 255, 255, 0.2)' }} />

              {/* User Rating Section */}
              <Box sx={{ mb: 3 }}>
                <Typography 
                  variant="h6" 
                  sx={{ 
                    mb: 2,
                    color: 'rgba(255, 255, 255, 0.95)',
                    fontWeight: 600
                  }}
                >
                  Rate This Movie
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                  <Rating
                    value={userRating?.rating || 0}
                    onChange={(_, value) => handleRatingChange(value)}
                    disabled={ratingLoading}
                    size="large"
                    sx={{
                      '& .MuiRating-iconFilled': {
                        color: '#FFD700',
                      },
                      '& .MuiRating-iconHover': {
                        color: '#FFD700',
                      },
                    }}
                  />
                  {ratingLoading && (
                    <CircularProgress size={24} sx={{ color: '#2196F3' }} />
                  )}
                </Box>
                {userRating && (
                  <Typography 
                    variant="body2" 
                    sx={{ 
                      color: 'rgba(255, 255, 255, 0.7)',
                      fontStyle: 'italic'
                    }}
                  >
                    You rated this movie {userRating.rating}/5 stars
                  </Typography>
                )}
              </Box>

              {/* Action Buttons */}
              <Box sx={{ 
                display: 'flex', 
                gap: 2, 
                flexDirection: { xs: 'column', sm: 'row' }
              }}>
                {movie.trailer_url && (
                  <Button 
                    href={movie.trailer_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    variant="contained"
                    size="large"
                    startIcon={<PlayArrow />}
                    sx={{ 
                      background: 'linear-gradient(45deg, #FF6B35 30%, #F7931E 90%)',
                      boxShadow: '0 8px 16px rgba(255, 107, 53, 0.3)',
                      '&:hover': {
                        background: 'linear-gradient(45deg, #E64A19 30%, #F57C00 90%)',
                        transform: 'translateY(-2px)',
                        boxShadow: '0 12px 24px rgba(255, 107, 53, 0.4)',
                      }
                    }}
                  >
                    Watch Trailer
                  </Button>
                )}
                <Button 
                  variant="outlined"
                  size="large"
                  sx={{
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                    color: 'rgba(255, 255, 255, 0.9)',
                    '&:hover': {
                      borderColor: 'rgba(255, 255, 255, 0.6)',
                      backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    }
                  }}
                >
                  Add to Watchlist
                </Button>
                <Button 
                  href="/movies"
                  variant="outlined"
                  size="large"
                  sx={{
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                    color: 'rgba(255, 255, 255, 0.9)',
                    '&:hover': {
                      borderColor: 'rgba(255, 255, 255, 0.6)',
                      backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    }
                  }}
                >
                  Browse More Movies
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Additional Information Accordion */}
      {movieInfo && (
        <Box sx={{ mt: 4, animation: 'fadeInUp 0.6s ease-out 0.6s both' }}>
          <Accordion 
            sx={{ 
              background: 'rgba(255, 255, 255, 0.1)',
              backdropFilter: 'blur(10px)',
              border: '1px solid rgba(255, 255, 255, 0.2)',
              '&:before': { display: 'none' }
            }}
          >
            <AccordionSummary 
              expandIcon={<ExpandMore sx={{ color: 'rgba(255, 255, 255, 0.8)' }} />}
              sx={{ color: 'rgba(255, 255, 255, 0.9)' }}
            >
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Additional Information
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <List>
                    <ListItem>
                      <ListItemIcon>
                        <CalendarToday sx={{ color: 'rgba(255, 255, 255, 0.7)' }} />
                      </ListItemIcon>
                      <ListItemText 
                        primary="Release Year" 
                        secondary={movie.year}
                        sx={{
                          '& .MuiListItemText-primary': { color: 'rgba(255, 255, 255, 0.9)', fontWeight: 600 },
                          '& .MuiListItemText-secondary': { color: 'rgba(255, 255, 255, 0.7)' }
                        }}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon>
                        <AccessTime sx={{ color: 'rgba(255, 255, 255, 0.7)' }} />
                      </ListItemIcon>
                      <ListItemText 
                        primary="Runtime" 
                        secondary={movieInfo.runtime}
                        sx={{
                          '& .MuiListItemText-primary': { color: 'rgba(255, 255, 255, 0.9)', fontWeight: 600 },
                          '& .MuiListItemText-secondary': { color: 'rgba(255, 255, 255, 0.7)' }
                        }}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon>
                        <Movie sx={{ color: 'rgba(255, 255, 255, 0.7)' }} />
                      </ListItemIcon>
                      <ListItemText 
                        primary="Budget" 
                        secondary={movieInfo.budget}
                        sx={{
                          '& .MuiListItemText-primary': { color: 'rgba(255, 255, 255, 0.9)', fontWeight: 600 },
                          '& .MuiListItemText-secondary': { color: 'rgba(255, 255, 255, 0.7)' }
                        }}
                      />
                    </ListItem>
                  </List>
                </Grid>
                <Grid item xs={12} md={6}>
                  <List>
                    <ListItem>
                      <ListItemIcon>
                        <StarIcon sx={{ color: '#FFD700' }} />
                      </ListItemIcon>
                      <ListItemText 
                        primary="Box Office" 
                        secondary={movieInfo.boxOffice}
                        sx={{
                          '& .MuiListItemText-primary': { color: 'rgba(255, 255, 255, 0.9)', fontWeight: 600 },
                          '& .MuiListItemText-secondary': { color: 'rgba(255, 255, 255, 0.7)' }
                        }}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon>
                        <Info sx={{ color: 'rgba(255, 255, 255, 0.7)' }} />
                      </ListItemIcon>
                      <ListItemText 
                        primary="Awards" 
                        secondary={movieInfo.awards}
                        sx={{
                          '& .MuiListItemText-primary': { color: 'rgba(255, 255, 255, 0.9)', fontWeight: 600 },
                          '& .MuiListItemText-secondary': { color: 'rgba(255, 255, 255, 0.7)' }
                        }}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon>
                        <Movie sx={{ color: 'rgba(255, 255, 255, 0.7)' }} />
                      </ListItemIcon>
                      <ListItemText 
                        primary="Trivia" 
                        secondary={movieInfo.trivia}
                        sx={{
                          '& .MuiListItemText-primary': { color: 'rgba(255, 255, 255, 0.9)', fontWeight: 600 },
                          '& .MuiListItemText-secondary': { color: 'rgba(255, 255, 255, 0.7)' }
                        }}
                      />
                    </ListItem>
                  </List>
                </Grid>
              </Grid>
            </AccordionDetails>
          </Accordion>
        </Box>
      )}

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={3000}
        onClose={() => setSnackbar({...snackbar, open: false})}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert 
          onClose={() => setSnackbar({...snackbar, open: false})} 
          severity={snackbar.severity} 
          sx={{ 
            width: '100%',
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
          }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default MovieDetail; 