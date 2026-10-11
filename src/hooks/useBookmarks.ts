import { useState, useEffect } from 'react';
import { Bookmark } from '../types';

export function useBookmarks() {
  const [bookmarks, setBookmarks] = useState<Bookmark[]>(() => {
    if (typeof window === 'undefined') return [];
    try {
      const saved = localStorage.getItem('app_bookmarks');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  useEffect(() => {
    localStorage.setItem('app_bookmarks', JSON.stringify(bookmarks));
  }, [bookmarks]);

  const addBookmark = (songId: string, timestamp: number, note: string) => {
    const newBookmark: Bookmark = {
      id: `bm_${Date.now()}`,
      songId,
      timestamp,
      note,
      createdAt: Date.now()
    };
    setBookmarks(prev => [...prev, newBookmark]);
    return newBookmark;
  };

  const removeBookmark = (id: string) => {
    setBookmarks(prev => prev.filter(b => b.id !== id));
  };

  return { bookmarks, addBookmark, removeBookmark };
}
