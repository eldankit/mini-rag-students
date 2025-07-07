import React from 'react';
import { useTranslation } from 'react-i18next';
import './LanguageSwitcher.css';

const LanguageSwitcher = () => {
  const { i18n, t } = useTranslation();

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
  };

  return (
    <div className="language-switcher">
      <button
        className={`lang-btn ${i18n.language === 'en' ? 'active' : ''}`}
        onClick={() => changeLanguage('en')}
      >
        {t('language.en')}
      </button>
      <button
        className={`lang-btn ${i18n.language === 'he' ? 'active' : ''}`}
        onClick={() => changeLanguage('he')}
      >
        {t('language.he')}
      </button>
    </div>
  );
};

export default LanguageSwitcher; 