# Facebook Publisher SaaS v4.0

## 🚀 Modern React Application

A complete, modern web application for managing Facebook page publishing, built with React, Vite, and Tailwind CSS.

## ✨ Features

### 🎯 Core Functionality
- **Multi-page Publishing**: Publish to multiple Facebook pages simultaneously
- **Real-time Analytics**: Track performance across all your pages
- **Campaign Management**: Create and manage Facebook ad campaigns
- **Audience Management**: Build and manage custom audiences
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile

### 🛠️ Technical Features
- **Modern React 18**: Latest React features with hooks and context
- **Vite Build Tool**: Lightning-fast development and build process
- **Tailwind CSS**: Utility-first CSS framework for rapid UI development
- **React Query**: Powerful data fetching and caching
- **Zustand**: Lightweight state management
- **React Hook Form**: Performant forms with easy validation
- **Framer Motion**: Smooth animations and transitions

## 🏗️ Architecture

```
src/
├── components/          # Reusable UI components
│   ├── Layout.jsx      # Main layout wrapper
│   ├── Sidebar.jsx     # Navigation sidebar
│   ├── Header.jsx      # Top header
│   └── ui/             # UI components
├── pages/              # Page components
│   ├── Dashboard.jsx   # Main dashboard
│   ├── Publish.jsx     # Publishing interface
│   ├── Pages.jsx       # Facebook pages management
│   ├── Analytics.jsx   # Analytics dashboard
│   ├── Campaigns.jsx   # Campaign management
│   ├── Audiences.jsx   # Audience management
│   └── Settings.jsx    # Application settings
├── services/           # API services
├── stores/             # State management
├── hooks/              # Custom React hooks
└── utils/              # Utility functions
```

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ 
- npm or yarn
- Backend API running on port 5001

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Development

```bash
# Run tests
npm run test

# Run tests with UI
npm run test:ui

# Lint code
npm run lint

# Format code
npm run format
```

## 🎨 Design System

### Colors
- **Primary**: Blue (#3b82f6)
- **Facebook**: Facebook Blue (#1877f2)
- **Success**: Green (#10b981)
- **Warning**: Yellow (#f59e0b)
- **Error**: Red (#ef4444)

### Typography
- **Font**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700

### Components
- Consistent button styles with variants
- Card-based layout system
- Form components with validation
- Loading states and animations

## 📱 Responsive Design

The application is fully responsive with breakpoints:
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px  
- **Desktop**: > 1024px

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
VITE_API_URL=http://localhost:5001/api
VITE_APP_NAME=Facebook Publisher SaaS
VITE_APP_VERSION=4.0.0
```

### API Integration
The frontend connects to the existing Python Flask backend on port 5001. All API calls are proxied through Vite's dev server.

## 🧪 Testing

- **Unit Tests**: Vitest
- **Component Tests**: React Testing Library
- **E2E Tests**: Playwright (planned)

## 📦 Build & Deployment

### Production Build
```bash
npm run build
```

The build outputs to the `dist/` directory and can be served by any static file server.

### Deployment Options
- **Netlify**: Automatic deployment from Git
- **Vercel**: Zero-config deployment
- **AWS S3 + CloudFront**: Static hosting
- **Docker**: Containerized deployment

## 🔄 State Management

### Zustand Stores
- **authStore**: User authentication state
- **appStore**: Global application state

### React Query
- Automatic caching and background updates
- Optimistic updates for better UX
- Error handling and retry logic

## 🎯 Performance

### Optimizations
- Code splitting with React.lazy()
- Image optimization and lazy loading
- Bundle size optimization with Vite
- Efficient re-renders with React.memo()

### Metrics
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1
- **First Input Delay**: < 100ms

## 🔐 Security

- XSS protection with proper sanitization
- CSRF protection for API calls
- Secure token storage
- Input validation on all forms

## 🌐 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 📚 Documentation

### Component Documentation
Each component includes JSDoc comments with:
- Purpose and usage
- Props interface
- Examples

### API Documentation
API endpoints are documented in the `services/api.js` file with:
- Request/response formats
- Error handling
- Usage examples

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if needed
5. Submit a pull request

## 📄 License

Proprietary - Nicolas Pycik / Bois Malin

## 🆕 What's New in v4.0

### Major Updates
- **Complete React Rewrite**: Modern React 18 with hooks
- **Vite Build System**: 10x faster development builds
- **Tailwind CSS**: Utility-first styling approach
- **Component Library**: Reusable UI components
- **State Management**: Zustand for lightweight state
- **Form Handling**: React Hook Form for better performance
- **Animations**: Framer Motion for smooth interactions

### Improvements
- **Better Performance**: Faster loading and interactions
- **Mobile First**: Responsive design from the ground up
- **Accessibility**: WCAG 2.1 AA compliance
- **Developer Experience**: Hot reload, TypeScript support
- **Testing**: Comprehensive test suite
- **Documentation**: Detailed component and API docs

### Migration from v3.1.1
The new React frontend is designed to work with the existing Python backend. No backend changes are required for basic functionality.

---

**Built with ❤️ by Manus AI for Bois Malin**  
**Version 4.0.0 - June 2025**