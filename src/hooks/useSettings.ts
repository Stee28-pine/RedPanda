import { useState, useEffect } from 'react';

export function useSettings() {
  const [isOfflineMode, setIsOfflineMode] = useState(() => {
    if (typeof window === 'undefined') return false;
    return localStorage.getItem('app_offline_mode') === 'true';
  });

  useEffect(() => {
    localStorage.setItem('app_offline_mode', String(isOfflineMode));
  }, [isOfflineMode]);

  return { isOfflineMode, setIsOfflineMode };
}
