# Frontend - Mini RAG System

A modern React frontend for the Mini RAG System with internationalization support.

## Features

### 🌍 Internationalization
- **Multi-language Support**: English and Hebrew
- **RTL Layout**: Automatic right-to-left layout for Hebrew text
- **Language Switcher**: Easy toggle between languages
- **Auto-detection**: Detects browser language preference
- **Persistence**: Remembers language choice in localStorage

### 🎨 UI/UX
- **Modern Design**: Glassmorphism effects and gradient backgrounds
- **Responsive**: Works on all device sizes
- **Smooth Animations**: Hover effects and transitions
- **Real-time Status**: Live backend connection indicator

## Tech Stack

- **React 19**: Latest React with hooks
- **Create React App**: Development and build tooling
- **react-i18next**: Internationalization framework
- **CSS3**: Modern styling with flexbox and grid
- **Docker**: Containerization with Nginx

## Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/         # React components
│   │   ├── LanguageSwitcher.js
│   │   └── LanguageSwitcher.css
│   ├── locales/           # Translation files
│   │   ├── en.json        # English translations
│   │   └── he.json        # Hebrew translations
│   ├── App.js             # Main app component
│   ├── App.css            # Main app styles
│   ├── i18n.js            # i18n configuration
│   └── index.js           # App entry point
├── Dockerfile             # Docker configuration
├── nginx.conf             # Nginx configuration
└── package.json           # Dependencies and scripts
```

## Getting Started

### Prerequisites
- Node.js 18+ (for development)
- npm or yarn

### Installation

1. Install dependencies:
   ```sh
   npm install --legacy-peer-deps
   ```
   
   **Note**: Use `--legacy-peer-deps` to resolve TypeScript version conflicts.

2. Start development server:
   ```sh
   npm start
   ```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

### Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

## Internationalization

### Adding New Languages

1. Create a new translation file in `src/locales/`:
   ```json
   // fr.json
   {
     "header": {
       "title": "🎓 Mini RAG System",
       "subtitle": "Apprenez plus intelligemment avec l'assistance IA"
     }
   }
   ```

2. Update `src/i18n.js`:
   ```javascript
   import frTranslations from './locales/fr.json';
   
   const resources = {
     en: { translation: enTranslations },
     he: { translation: heTranslations },
     fr: { translation: frTranslations }  // Add new language
   };
   ```

3. Update `src/components/LanguageSwitcher.js`:
   ```javascript
   <button onClick={() => changeLanguage('fr')}>
     Français
   </button>
   ```

### Translation Keys

The app uses nested translation keys organized by feature:

- `header.*` - Header content
- `status.*` - System status indicators
- `features.*` - Feature card content
- `footer.*` - Footer content
- `language.*` - Language names

### RTL Support

Hebrew automatically activates RTL layout:
- Text direction switches to right-to-left
- Layout elements adjust accordingly
- CSS uses `[dir="rtl"]` selectors for RTL-specific styling

## Docker Deployment

### Build and Run
```sh
# Build the image
docker build -t mini-rag-frontend .

# Run the container
docker run -p 3000:3000 mini-rag-frontend
```

### Docker Compose
The frontend is configured to run with the backend using Docker Compose:
```sh
docker-compose up --build
```

### Nginx Configuration
The production build uses Nginx with:
- Static file serving
- API proxy to backend
- React Router support
- Asset caching

## Development

### Code Style
- Use functional components with hooks
- Follow React best practices
- Use CSS modules or styled-components for styling
- Implement proper error boundaries

### Testing
```sh
npm test
```

### Building for Production
```sh
npm run build
```

## Troubleshooting

### Common Issues

1. **TypeScript Version Conflicts**
   - Use `npm install --legacy-peer-deps`
   - Check package.json resolutions

2. **i18n Not Working**
   - Ensure `src/i18n.js` is imported in `index.js`
   - Check translation file syntax
   - Verify language codes match

3. **RTL Layout Issues**
   - Check `document.documentElement.dir` setting
   - Verify CSS RTL selectors
   - Test with Hebrew content

### Performance Tips

- Use React.memo for expensive components
- Implement lazy loading for routes
- Optimize translation bundle size
- Use production builds for testing

## Contributing

1. Follow the existing code structure
2. Add translations for new features
3. Test with both LTR and RTL layouts
4. Update documentation for new features

## License

MIT License - see main project README for details.
