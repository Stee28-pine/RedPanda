import { useState, useEffect } from 'react';
import { Song, Collection } from '../types';

export function usePlaylists() {
  const [playlists, setPlaylists] = useState<Collection[]>(() => {
    if (typeof window === 'undefined') return [];
    try {
      const saved = localStorage.getItem('app_playlists');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  useEffect(() => {
    localStorage.setItem('app_playlists', JSON.stringify(playlists));
  }, [playlists]);

  const createPlaylist = (name: string) => {
    const newPlaylist: Collection = {
      id: `playlist_${Date.now()}`,
      type: 'playlist',
      title: name,
      subtitle: 'My Playlist',
      coverUrl: 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?w=400&q=80',
      songs: []
    };
    setPlaylists(prev => [...prev, newPlaylist]);
    return newPlaylist;
  };

  const addSongToPlaylist = (playlistId: string, song: Song) => {
    setPlaylists(prev => prev.map(p => {
      if (p.id === playlistId) {
        if (p.songs.some(s => s.id === song.id)) return p;
        return { ...p, songs: [...p.songs, song] };
      }
      return p;
    }));
  };

  const computedPlaylists = playlists.map(p => {
    if (p.songs && p.songs.length > 0) {
      return { ...p, coverUrl: p.songs[0].coverUrl };
    }
    return p;
  });

  const removeSongFromPlaylist = (playlistId: string, songId: string) => {
    setPlaylists(prev => prev.map(p => {
      if (p.id === playlistId) {
        return { ...p, songs: p.songs.filter(s => s.id !== songId) };
      }
      return p;
    }));
  };

  const deletePlaylist = (playlistId: string) => {
    setPlaylists(prev => prev.filter(p => p.id !== playlistId));
  };

  const mergePlaylists = (targetId: string, sourceId: string) => {
    setPlaylists(prev => {
      const source = prev.find(p => p.id === sourceId);
      if (!source) return prev;
      
      return prev.map(p => {
        if (p.id === targetId) {
          const existingIds = new Set(p.songs.map(s => s.id));
          const newSongs = source.songs.filter(s => !existingIds.has(s.id));
          return { ...p, songs: [...p.songs, ...newSongs] };
        }
        return p;
      }).filter(p => p.id !== sourceId);
    });
  };

  return { playlists: computedPlaylists, createPlaylist, addSongToPlaylist, removeSongFromPlaylist, deletePlaylist, mergePlaylists };
}
