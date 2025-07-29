export interface User {
  id: number;
  username: string;
  name: string;
  email?: string;
  age?: number;
  preferred_genre?: string;
  role: string;
}

export interface Movie {
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

export interface Rating {
  id?: number;
  user_id?: number;
  movie_id: number;
  rating: number;
  review?: string;
  created_at?: string;
  movie?: Movie;
  // For user ratings API response:
  title?: string;
  year?: number;
  genre?: string;
}

export interface Recommendation {
  movie_id: number;
  title: string;
  genre: string;
  year: number;
  predicted_rating?: number;
  similarity_score?: number;
  hybrid_score?: number;
  poster_url?: string;
  trailer_url?: string;
  description?: string;
}

export interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (username: string, password: string) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

export interface RegisterData {
  username: string;
  password: string;
  name: string;
  email?: string;
  age?: number;
  preferred_genre?: string;
}

export interface LoginData {
  username: string;
  password: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
} 