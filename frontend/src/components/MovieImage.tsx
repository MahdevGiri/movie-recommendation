import React, { useState, useEffect } from 'react';
import { Box, Skeleton } from '@mui/material';
import { generateCanvasPlaceholder, getSimpleFallbackUrl } from '../utils/imageUtils';

interface MovieImageProps {
  posterUrl?: string;
  title: string;
  genre: string;
  year: number;
  width?: number | string;
  height?: number | string;
  sx?: any;
  alt?: string;
}

const MovieImage: React.FC<MovieImageProps> = ({
  posterUrl,
  title,
  genre,
  year,
  width = '100%',
  height = 200,
  sx = {},
  alt
}) => {
  const [imageUrl, setImageUrl] = useState<string>('');
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);
  const [fallbackGenerated, setFallbackGenerated] = useState(false);

  useEffect(() => {
    const loadImage = async () => {
      setIsLoading(true);
      setHasError(false);
      
      try {
        if (posterUrl) {
          // Try to load the original poster
          const img = new Image();
          img.onload = () => {
            setImageUrl(posterUrl);
            setIsLoading(false);
          };
          img.onerror = () => {
            // If original fails, generate fallback
            generateFallback();
          };
          img.src = posterUrl;
        } else {
          // No poster URL, generate fallback immediately
          generateFallback();
        }
      } catch (error) {
        generateFallback();
      }
    };

    const generateFallback = () => {
      try {
        // Try to generate canvas placeholder first
        const canvasUrl = generateCanvasPlaceholder(title, genre, year);
        setImageUrl(canvasUrl);
        setIsLoading(false);
        setFallbackGenerated(true);
      } catch (error) {
        // If canvas fails, use simple placeholder
        const simpleUrl = getSimpleFallbackUrl(title, genre);
        setImageUrl(simpleUrl);
        setIsLoading(false);
        setHasError(true);
        setFallbackGenerated(true);
      }
    };

    loadImage();
  }, [posterUrl, title, genre, year]);

  const handleImageError = () => {
    if (!fallbackGenerated) {
      try {
        const canvasUrl = generateCanvasPlaceholder(title, genre, year);
        setImageUrl(canvasUrl);
        setFallbackGenerated(true);
      } catch (error) {
        const simpleUrl = getSimpleFallbackUrl(title, genre);
        setImageUrl(simpleUrl);
        setHasError(true);
        setFallbackGenerated(true);
      }
    }
  };

  if (isLoading) {
    return (
      <Skeleton
        variant="rectangular"
        width={width}
        height={height}
        sx={{
          borderRadius: 2,
          background: 'rgba(255, 255, 255, 0.1)',
          '&::after': {
            background: 'linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent)',
          }
        }}
      />
    );
  }

  return (
    <Box
      component="img"
      src={imageUrl}
      alt={alt || `${title} (${year})`}
      onError={handleImageError}
      sx={{
        width,
        height,
        objectFit: 'cover',
        borderRadius: 2,
        transition: 'transform 0.3s ease',
        '&:hover': {
          transform: 'scale(1.05)',
        },
        ...sx
      }}
    />
  );
};

export default MovieImage; 