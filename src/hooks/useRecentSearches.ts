import { useState, useEffect } from 'react';

export function useRecentSearches() {
  const [recentSearches, setRecentSearches] = useState<string[]>(() => {
    if (typeof window === 'undefined') return [];
    try {
      const saved = localStorage.getItem('app_recent_searches');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  useEffect(() => {
    localStorage.setItem('app_recent_searches', JSON.stringify(recentSearches));
  }, [recentSearches]);

  const addSearch = (query: string) => {
    if (!query.trim()) return;
    setRecentSearches(prev => {
      const filtered = prev.filter(q => q.toLowerCase() !== query.toLowerCase());
      return [query, ...filtered].slice(0, 5); // keep top 10
    });
  };

  const removeSearch = (query: string) => {
    setRecentSearches(prev => prev.filter(q => q !== query));
  };

  const clearSearches = () => setRecentSearches([]);

  return { recentSearches, addSearch, removeSearch, clearSearches };
}
