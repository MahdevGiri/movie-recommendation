# 🎬 Movie Recommendation System - Frontend

A modern React TypeScript frontend for the movie recommendation system, built with Material-UI components and featuring a responsive design, JWT authentication, and advanced recommendation features.

## 🌟 Features

### 🎨 User Interface
- **Modern Design**: Material-UI components with dark theme
- **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile
- **Dark Theme**: Beautiful dark UI with consistent styling
- **Loading States**: Smooth loading indicators and transitions
- **Error Handling**: User-friendly error messages and notifications

### 🔐 Authentication
- **JWT Integration**: Secure token-based authentication
- **Login/Register**: Complete user authentication flow
- **Profile Management**: View and manage user preferences
- **Session Persistence**: Automatic login state management
- **Password Strength**: Visual password strength indicator
- **Role-Based Access**: Admin and user role management

### 🎬 Movie Features
- **Movie Browsing**: Browse all movies with pagination
- **Movie Details**: View comprehensive movie information
- **Rating System**: Rate movies on a 1-5 scale
- **Search & Filter**: Find movies by title, genre, or year
- **Movie Cards**: Beautiful movie presentation with ratings

### 💡 Smart Recommendations
- **Personalized Recommendations**: AI-powered movie suggestions
- **Genre-Focused Recommendations**: Top-rated movies in preferred genre
- **Algorithm Information**: Transparent recommendation explanations
- **Real-time Updates**: Instant recommendation updates after rating
- **Toggle Between Types**: Switch between recommendation algorithms

### 👤 User Experience
- **User Profiles**: View rating history and preferences
- **Navigation**: Intuitive navigation between pages
- **Responsive Design**: Optimized for all screen sizes
- **Accessibility**: Keyboard navigation and screen reader support
- **Performance**: Optimized rendering and data fetching
- **Admin Dashboard**: Full movie management interface for administrators

## 🏗️ Project Structure

```
frontend/
├── public/
│   ├── index.html              # Main HTML template
│   ├── manifest.json           # PWA manifest
│   └── favicon.ico             # App icon
├── src/
│   ├── components/             # Reusable UI components
│   │   ├── Navbar.tsx          # Navigation bar
│   │   ├── MovieCard.tsx       # Movie display card
│   │   ├── RatingStars.tsx     # Star rating component
│   │   └── LoadingSpinner.tsx  # Loading indicator
│   ├── pages/                  # Page components
│   │   ├── Home.tsx            # Home page
│   │   ├── Movies.tsx          # Movies browsing page
│   │   ├── Recommendations.tsx # Recommendations page
│   │   ├── Profile.tsx         # User profile page
│   │   ├── Login.tsx           # Login page
│   │   ├── Register.tsx        # Registration page
│   │   └── Admin.tsx           # Admin dashboard page
│   ├── services/               # API services
│   │   ├── api.ts              # API client configuration
│   │   ├── auth.ts             # Authentication services
│   │   ├── movies.ts           # Movie-related API calls
│   │   └── recommendations.ts  # Recommendation API calls
│   ├── contexts/               # React contexts
│   │   └── AuthContext.tsx     # Authentication context
│   ├── types/                  # TypeScript definitions
│   │   ├── auth.ts             # Authentication types
│   │   ├── movie.ts            # Movie-related types
│   │   └── api.ts              # API response types
│   ├── App.tsx                 # Main app component
│   ├── index.tsx               # App entry point
│   └── index.css               # Global styles
├── package.json                # Node.js dependencies
├── tsconfig.json               # TypeScript configuration
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Node.js 16+** and **npm**
2. **Git** (for cloning)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd movie-recommendation/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

The frontend will be available at: **http://localhost:3000**

## 🔧 Development

### Available Scripts

```bash
npm start                     # Start development server
npm build                     # Build for production
npm test                      # Run tests
npm run eject                 # Eject from Create React App
```

### Environment Variables

Create a `.env` file in the frontend directory:

```bash
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENVIRONMENT=development
```

### Development Server

The development server runs on `http://localhost:3000` and includes:
- Hot reloading for instant updates
- Source maps for debugging
- Error overlay for runtime errors
- ESLint integration for code quality

## 🎨 UI Components

### Material-UI Integration

The app uses Material-UI (MUI) for consistent, beautiful components:

- **Theme**: Custom dark theme with primary/secondary colors
- **Typography**: Consistent text styling across the app
- **Grid System**: Responsive layout with Material-UI Grid
- **Components**: Buttons, cards, forms, navigation, and more

### Responsive Design

The app is fully responsive and optimized for:

- **Desktop**: Full-featured experience with all controls
- **Tablet**: Optimized layout for medium screens
- **Mobile**: Touch-friendly interface for small screens

### Key Components

#### Navbar
- Responsive navigation with hamburger menu on mobile
- User authentication status display
- Smooth transitions and animations

#### MovieCard
- Beautiful movie presentation with poster placeholders
- Rating display with star icons
- Hover effects and interactions
- Responsive grid layout

#### RatingStars
- Interactive star rating component
- Visual feedback for user interactions
- Accessible keyboard navigation

## 🔐 Authentication Flow

### Login Process
1. User enters credentials
2. Form validation ensures data quality
3. API call to backend authentication endpoint
4. JWT token stored in localStorage
5. User redirected to home page
6. Authentication context updated

### Registration Process
1. User fills out registration form
2. Password strength validation
3. Form submission with user data
4. Automatic login after successful registration
5. User redirected to home page

### Session Management
- JWT tokens automatically included in API requests
- Automatic token refresh handling
- Secure logout with token removal
- Session persistence across browser sessions

## 🎬 Movie Features

### Movie Browsing
- **Pagination**: Efficient browsing of large movie collections
- **Search**: Find movies by title or description
- **Filtering**: Filter by genre, year, or rating
- **Sorting**: Sort by title, year, rating, or popularity

### Movie Details
- **Comprehensive Information**: Title, genre, year, description
- **Rating Display**: Average rating and number of ratings
- **User Rating**: Rate movies with interactive star component
- **Responsive Layout**: Optimized for all screen sizes

### Rating System
- **Interactive Stars**: Click to rate movies 1-5 stars
- **Real-time Updates**: Instant feedback on rating submission
- **Rating History**: View all user ratings in profile
- **Validation**: Prevent duplicate ratings

## 💡 Recommendation System

### Personalized Recommendations
- **Smart Algorithm**: AI-powered collaborative filtering
- **User Similarity**: Based on similar users' preferences
- **Genre Boosting**: Enhanced recommendations for preferred genres
- **Real-time Updates**: Recommendations update after rating

### Genre-Focused Recommendations
- **Preferred Genre**: Top-rated movies in user's preferred genre
- **Discovery**: Find new movies in favorite genres
- **Quality Filter**: Only highly-rated movies included
- **Complementary**: Works alongside personalized recommendations

### Algorithm Transparency
- **Algorithm Info**: Display which algorithm is being used
- **Preferred Genre**: Show user's preferred genre
- **Toggle Options**: Switch between recommendation types
- **Explanation**: Help users understand recommendations

## 👤 User Profile

### Profile Information
- **User Details**: Username, email, age, preferred genre
- **Account Management**: View and update preferences
- **Security**: Password change functionality

### Rating History
- **All Ratings**: Complete list of user's movie ratings
- **Rating Details**: Movie information with rating values
- **Chronological Order**: Sorted by rating date
- **Quick Actions**: Easy access to rate or re-rate movies

## 👑 Admin Dashboard

### Admin Access
- **Role-Based Navigation**: Admin link only visible to admin users
- **Protected Routes**: Server-side verification of admin privileges
- **Access Control**: Automatic redirect for unauthorized users

### Movie Management
- **Add Movies**: Create new movies with full details
- **Edit Movies**: Update existing movie information
- **Delete Movies**: Remove movies with confirmation
- **Search & Filter**: Find movies by title or genre
- **Pagination**: Navigate through large collections

### Admin Interface
- **Movie Grid**: Visual display of all movies
- **Action Buttons**: Edit and delete buttons on each movie card
- **Add Movie Dialog**: Comprehensive form for new movies
- **Real-time Updates**: Changes reflect immediately
- **Responsive Design**: Works on all device sizes

### Admin Features
- **Movie Creation**: Add movies with title, genre, year, description, director, cast, poster URL, trailer URL
- **Movie Editing**: Update any movie information
- **Movie Deletion**: Remove movies and their associated ratings
- **Search Functionality**: Find specific movies by title
- **Genre Filtering**: View movies by specific genre
- **Bulk Management**: Handle large collections efficiently

## 🔧 Technical Implementation

### State Management
- **React Context**: Authentication state management
- **Local State**: Component-level state for UI interactions
- **API State**: Loading, error, and success states
- **Form State**: Controlled components for user input

### API Integration
- **Axios**: HTTP client for API communication
- **Interceptors**: Automatic token inclusion and error handling
- **Error Handling**: Comprehensive error management
- **Loading States**: User feedback during API calls

### TypeScript Integration
- **Type Safety**: Full TypeScript implementation
- **Interface Definitions**: Comprehensive type definitions
- **API Types**: Strongly typed API responses
- **Component Props**: Type-safe component interfaces

## 📱 Responsive Design

### Breakpoints
- **xs**: 0px - 599px (Mobile)
- **sm**: 600px - 959px (Tablet)
- **md**: 960px - 1279px (Small Desktop)
- **lg**: 1280px - 1919px (Desktop)
- **xl**: 1920px+ (Large Desktop)

### Mobile Optimization
- **Touch Targets**: Adequate size for touch interaction
- **Navigation**: Collapsible hamburger menu
- **Layout**: Single-column layout on small screens
- **Performance**: Optimized for mobile devices

### Tablet Optimization
- **Grid Layout**: Multi-column grid for medium screens
- **Navigation**: Horizontal navigation bar
- **Content**: Balanced content density
- **Interaction**: Touch and mouse-friendly controls

## 🚀 Performance Optimization

### Code Splitting
- **Route-based Splitting**: Lazy loading of page components
- **Component Splitting**: Separate bundles for large components
- **Dynamic Imports**: On-demand loading of features

### Bundle Optimization
- **Tree Shaking**: Remove unused code
- **Minification**: Compressed production builds
- **Caching**: Optimized caching strategies
- **CDN**: Static asset delivery optimization

### Runtime Performance
- **Memoization**: React.memo for expensive components
- **Virtual Scrolling**: Efficient list rendering
- **Debouncing**: Optimized search and filter inputs
- **Image Optimization**: Lazy loading and compression

## 🧪 Testing

### Testing Strategy
- **Unit Tests**: Component and utility function testing
- **Integration Tests**: API integration testing
- **E2E Tests**: End-to-end user flow testing
- **Accessibility Tests**: Screen reader and keyboard navigation

### Available Test Commands
```bash
npm test                      # Run all tests
npm test -- --coverage        # Run tests with coverage
npm test -- --watch           # Run tests in watch mode
```

## 🚀 Deployment

### Production Build
```bash
npm run build
```

This creates an optimized production build in the `build` folder.

### Deployment Options
- **Netlify**: Drag and drop deployment
- **Vercel**: Git-based deployment
- **AWS S3**: Static website hosting
- **GitHub Pages**: Free hosting for public repositories

### Environment Configuration
- **Production API**: Update API endpoint for production
- **Environment Variables**: Configure for production environment
- **Build Optimization**: Enable production optimizations
- **CDN Setup**: Configure content delivery network

## 🔧 Customization

### Theme Customization
Edit the theme configuration in `src/App.tsx`:
```typescript
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#your-primary-color',
    },
    secondary: {
      main: '#your-secondary-color',
    },
  },
});
```

### Component Styling
- **Material-UI Styling**: Use `sx` prop for component styling
- **CSS Modules**: Component-specific stylesheets
- **Styled Components**: CSS-in-JS styling approach
- **Global Styles**: App-wide styling in `index.css`

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Ensure backend server is running
   - Check API URL configuration
   - Verify CORS settings

2. **Authentication Issues**
   - Clear browser localStorage
   - Check JWT token expiration
   - Verify backend authentication endpoints

3. **Build Errors**
   - Clear node_modules and reinstall
   - Check TypeScript configuration
   - Verify all dependencies are installed

4. **Performance Issues**
   - Enable production build optimizations
   - Check bundle size with webpack analyzer
   - Optimize image assets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Material-UI** for the beautiful UI components
- **React** for the modern frontend framework
- **TypeScript** for type safety
- **Axios** for HTTP client functionality

---

**Happy Coding! 🚀✨** 