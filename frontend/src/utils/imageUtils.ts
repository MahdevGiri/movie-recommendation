/**
 * Image utility functions for handling movie posters and fallbacks
 */

// Generate a placeholder image URL based on movie title and genre
export const generatePlaceholderImage = (title: string, genre: string, year: number): string => {
  // Use a service like Picsum for placeholder images
  const width = 300;
  const height = 450;
  
  // Generate a consistent color based on genre
  const genreColors: { [key: string]: string } = {
    'Drama': '6c5ce7',
    'Action': 'e17055',
    'Comedy': 'fdcb6e',
    'Thriller': '2d3436',
    'Romance': 'fd79a8',
    'Sci-Fi': '74b9ff',
    'Horror': 'd63031',
    'Documentary': '00b894',
    'Biography': 'a29bfe',
    'Musical': 'fd79a8',
    'Adventure': 'fdcb6e',
    'Crime': '2d3436',
    'Fantasy': '6c5ce7',
    'Animation': 'fd79a8',
    'Family': '00b894',
    'War': 'e17055',
    'Mystery': '2d3436',
    'Western': 'fdcb6e',
    'Sport': '00b894',
    'History': 'a29bfe'
  };
  
  const color = genreColors[genre] || '6c5ce7';
  
  // Use a placeholder service that generates images with text
  return `https://via.placeholder.com/${width}x${height}/${color}/ffffff?text=${encodeURIComponent(title.substring(0, 20))}`;
};

// Try to get movie poster from multiple sources
export const getMoviePosterFromMultipleSources = async (title: string, year: number): Promise<string> => {
  // Try different image search APIs
  const sources = [
    `https://source.unsplash.com/300x450/?movie,poster,${encodeURIComponent(title)}`,
    `https://picsum.photos/300/450?random=${title.length}`,
    `https://via.placeholder.com/300x450/6c5ce7/ffffff?text=${encodeURIComponent(title.substring(0, 20))}`,
  ];
  
  for (const source of sources) {
    try {
      const response = await fetch(source, { method: 'HEAD' });
      if (response.ok) {
        return source;
      }
    } catch (error) {
      continue;
    }
  }
  
  // Fallback to generated placeholder
  return generateCanvasPlaceholder(title, 'Drama', year);
};

// Generate a more sophisticated placeholder using Canvas API
export const generateCanvasPlaceholder = (title: string, genre: string, year: number): string => {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  
  if (!ctx) {
    return generatePlaceholderImage(title, genre, year);
  }
  
  const width = 300;
  const height = 450;
  canvas.width = width;
  canvas.height = height;
  
  // Generate gradient background based on genre
  const genreGradients: { [key: string]: [string, string] } = {
    'Drama': ['#6c5ce7', '#a29bfe'],
    'Action': ['#e17055', '#fd79a8'],
    'Comedy': ['#fdcb6e', '#fd79a8'],
    'Thriller': ['#2d3436', '#636e72'],
    'Romance': ['#fd79a8', '#fdcb6e'],
    'Sci-Fi': ['#74b9ff', '#0984e3'],
    'Horror': ['#d63031', '#e17055'],
    'Documentary': ['#00b894', '#00cec9'],
    'Biography': ['#a29bfe', '#6c5ce7'],
    'Musical': ['#fd79a8', '#fdcb6e'],
    'Adventure': ['#fdcb6e', '#e17055'],
    'Crime': ['#2d3436', '#636e72'],
    'Fantasy': ['#6c5ce7', '#a29bfe'],
    'Animation': ['#fd79a8', '#fdcb6e'],
    'Family': ['#00b894', '#00cec9'],
    'War': ['#e17055', '#d63031'],
    'Mystery': ['#2d3436', '#636e72'],
    'Western': ['#fdcb6e', '#e17055'],
    'Sport': ['#00b894', '#00cec9'],
    'History': ['#a29bfe', '#6c5ce7']
  };
  
  const gradient = genreGradients[genre] || ['#6c5ce7', '#a29bfe'];
  const gradientObj = ctx.createLinearGradient(0, 0, width, height);
  gradientObj.addColorStop(0, gradient[0]);
  gradientObj.addColorStop(1, gradient[1]);
  
  // Fill background
  ctx.fillStyle = gradientObj;
  ctx.fillRect(0, 0, width, height);
  
  // Add some geometric shapes for visual interest
  ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
  ctx.beginPath();
  ctx.arc(width * 0.8, height * 0.2, 50, 0, Math.PI * 2);
  ctx.fill();
  
  ctx.beginPath();
  ctx.rect(width * 0.1, height * 0.7, 80, 40);
  ctx.fill();
  
  // Add movie title
  ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
  ctx.font = 'bold 16px Arial';
  ctx.textAlign = 'center';
  
  // Split title into lines if too long
  const words = title.split(' ');
  const lines: string[] = [];
  let currentLine = '';
  
  for (const word of words) {
    const testLine = currentLine ? `${currentLine} ${word}` : word;
    if (ctx.measureText(testLine).width > width - 40) {
      if (currentLine) lines.push(currentLine);
      currentLine = word;
    } else {
      currentLine = testLine;
    }
  }
  if (currentLine) lines.push(currentLine);
  
  // Draw title lines
  lines.forEach((line, index) => {
    ctx.fillText(line, width / 2, height * 0.5 + (index - lines.length / 2) * 20);
  });
  
  // Add genre and year
  ctx.font = '14px Arial';
  ctx.fillText(`${genre} • ${year}`, width / 2, height * 0.7);
  
  // Add film icon
  ctx.font = '24px Arial';
  ctx.fillText('🎬', width / 2, height * 0.85);
  
  return canvas.toDataURL();
};

// Check if an image URL is valid and accessible
export const checkImageUrl = async (url: string): Promise<boolean> => {
  try {
    const response = await fetch(url, { method: 'HEAD' });
    return response.ok;
  } catch {
    return false;
  }
};

// Get the best available image URL for a movie with multiple fallbacks
export const getMovieImageUrl = async (posterUrl: string | null, title: string, genre: string, year: number): Promise<string> => {
  if (!posterUrl) {
    return await getMoviePosterFromMultipleSources(title, year);
  }
  
  // Check if the poster URL is accessible
  const isAccessible = await checkImageUrl(posterUrl);
  if (!isAccessible) {
    return await getMoviePosterFromMultipleSources(title, year);
  }
  
  return posterUrl;
};

// Generate a simple fallback image URL (for cases where Canvas API might not work)
export const getSimpleFallbackUrl = (title: string, genre: string): string => {
  const genreColors: { [key: string]: string } = {
    'Drama': '6c5ce7',
    'Action': 'e17055',
    'Comedy': 'fdcb6e',
    'Thriller': '2d3436',
    'Romance': 'fd79a8',
    'Sci-Fi': '74b9ff',
    'Horror': 'd63031',
    'Documentary': '00b894',
    'Biography': 'a29bfe',
    'Musical': 'fd79a8',
    'Adventure': 'fdcb6e',
    'Crime': '2d3436',
    'Fantasy': '6c5ce7',
    'Animation': 'fd79a8',
    'Family': '00b894',
    'War': 'e17055',
    'Mystery': '2d3436',
    'Western': 'fdcb6e',
    'Sport': '00b894',
    'History': 'a29bfe'
  };
  
  const color = genreColors[genre] || '6c5ce7';
  const shortTitle = title.substring(0, 20).replace(/[^a-zA-Z0-9]/g, '');
  
  return `https://via.placeholder.com/300x450/${color}/ffffff?text=${encodeURIComponent(shortTitle)}`;
}; 