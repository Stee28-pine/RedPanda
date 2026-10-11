import { useState, useEffect } from 'react';
import { Song } from '../types';

export interface ListeningStats {
  totalTimeSeconds: number;
  songPlays: Record<string, number>;
  artistPlays: Record<string, number>;
  genrePlays: Record<string, number>;
  dailyActivity: Record<string, number>; // YYYY-MM-DD -> total seconds
}

export function useListeningStats() {
  const [stats, setStats] = useState<ListeningStats>(() => {
    if (typeof window === 'undefined') return { totalTimeSeconds: 0, songPlays: {}, artistPlays: {}, genrePlays: {}, dailyActivity: {} };
    try {
      const saved = localStorage.getItem('app_listening_stats');
      return saved ? JSON.parse(saved) : { totalTimeSeconds: 0, songPlays: {}, artistPlays: {}, genrePlays: {}, dailyActivity: {} };
    } catch {
      return { totalTimeSeconds: 0, songPlays: {}, artistPlays: {}, genrePlays: {}, dailyActivity: {} };
    }
  });

  useEffect(() => {
    localStorage.setItem('app_listening_stats', JSON.stringify(stats));
  }, [stats]);

  const recordPlay = (song: Song) => {
    setStats(prev => {
      const newStats = { ...prev };
      
      const playDuration = 180; // Estimated 3 mins per play
      newStats.totalTimeSeconds = (newStats.totalTimeSeconds || 0) + playDuration;
      
      newStats.songPlays = { ...newStats.songPlays };
      newStats.songPlays[song.title] = (newStats.songPlays[song.title] || 0) + 1;
      
      newStats.artistPlays = { ...newStats.artistPlays };
      newStats.artistPlays[song.artist] = (newStats.artistPlays[song.artist] || 0) + 1;
      
      if (song.genre) {
        newStats.genrePlays = { ...newStats.genrePlays };
        newStats.genrePlays[song.genre] = (newStats.genrePlays[song.genre] || 0) + 1;
      }

      newStats.dailyActivity = { ...(newStats.dailyActivity || {}) };
      const today = new Date().toISOString().split('T')[0];
      newStats.dailyActivity[today] = (newStats.dailyActivity[today] || 0) + playDuration;
      
      return newStats;
    });
  };

  return { stats, recordPlay };
}
