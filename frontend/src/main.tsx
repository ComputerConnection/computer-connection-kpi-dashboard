import React, { useEffect } from 'react';
import ReactDOM from 'react-dom/client';
import App from './pages/App';
import './styles/index.css';
import { useThemeStore } from './store/theme';

function Root() {
  const dark = useThemeStore((s) => s.dark);
  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark);
  }, [dark]);
  return <App />;
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Root />
  </React.StrictMode>
);
