import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import LanguageSwitcher from './components/LanguageSwitcher';
import './App.css';

function App() {
  const { t, i18n } = useTranslation();
  const [backendStatus, setBackendStatus] = useState('checking');
  const [isConnected, setIsConnected] = useState(false);

  // Use localhost for browser requests (Docker exposes backend on localhost:8000)
  const backendUrl = 'http://localhost:8000';

  useEffect(() => {
    // Check backend connection
    fetch(`${backendUrl}/api/ping`)
      .then(response => response.json())
      .then(data => {
        setBackendStatus('connected');
        setIsConnected(true);
      })
      .catch(error => {
        setBackendStatus('disconnected');
        setIsConnected(false);
      });
  }, [backendUrl]);

  // Set document direction based on language
  useEffect(() => {
    document.documentElement.dir = i18n.language === 'he' ? 'rtl' : 'ltr';
  }, [i18n.language]);

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <div className="header-text">
            <h1>{t('header.title')}</h1>
            <p>{t('header.subtitle')}</p>
          </div>
          <LanguageSwitcher />
        </div>
      </header>
      
      <main className="App-main">
        <div className="status-card">
          <h2>{t('status.title')}</h2>
          <div className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
            <span className="status-dot"></span>
            <span className="status-text">Backend: {t(`status.${backendStatus}`)}</span>
          </div>
        </div>

        <div className="feature-cards">
          <div className="feature-card">
            <h3>{t('features.upload.title')}</h3>
            <p>{t('features.upload.description')}</p>
            <button className="btn-primary">{t('features.upload.button')}</button>
          </div>

          <div className="feature-card">
            <h3>{t('features.chat.title')}</h3>
            <p>{t('features.chat.description')}</p>
            <button className="btn-primary">{t('features.chat.button')}</button>
          </div>

          <div className="feature-card">
            <h3>{t('features.analytics.title')}</h3>
            <p>{t('features.analytics.description')}</p>
            <button className="btn-primary">{t('features.analytics.button')}</button>
          </div>
        </div>
      </main>

      <footer className="App-footer">
        <p>{t('footer.text')}</p>
      </footer>
    </div>
  );
}

export default App;
