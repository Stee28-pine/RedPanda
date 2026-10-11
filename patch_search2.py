import os

with open('src/hooks/useSearch.ts', 'r') as f:
    content = f.read()

new_content = """import { useState, useEffect } from 'react';
import { Song } from '../types';
import { SONGS } from '../data';

export function useSearch(query: string) {
  const [results, setResults] = useState<Song[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    if (!query || query.trim() === '') {
      setResults([]);
      return;
    }

    const timer = setTimeout(async () => {
      setIsLoading(true);
      try {
        const q = query.toLowerCase();
        
        // Local search first
        const localMatches = SONGS.filter(s => 
           s.title.toLowerCase().includes(q) || 
           s.artist.toLowerCase().includes(q)
        );
        
        let ytSongs: Song[] = [];
        try {
           const ytRes = await fetch(`/api/search-tracks?q=${encodeURIComponent(query)}`);
           const ytData = await ytRes.json();
           if (ytData.results) {
              ytSongs = ytData.results;
           }
        } catch(e) {
           console.error("YT Search failed", e);
        }

        let itunesSongs: Song[] = [];
        try {
          const res = await fetch(`https://itunes.apple.com/search?term=${encodeURIComponent(query)}&entity=song&limit=20`);
          const data = await res.json();
          itunesSongs = data.results.map((track: any) => ({
            id: track.trackId?.toString() || Math.random().toString(),
            title: track.trackName,
            artist: track.artistName,
            album: track.collectionName || 'Single',
            duration: formatDuration(track.trackTimeMillis),
            durationSeconds: Math.floor((track.trackTimeMillis || 0) / 1000),
            coverUrl: track.artworkUrl100?.replace('100x100bb', '400x400bb') || '',
            audioUrl: track.previewUrl
          }));
        } catch(e) {
          console.error("iTunes search failed", e);
        }
                
        // Merge without duplicates, prioritize YT songs since they have YouTube IDs
        const merged = [...localMatches];
        const existingIds = new Set(localMatches.map(s => s.id));
        
        for (const song of [...ytSongs, ...itunesSongs]) {
           const isDuplicate = merged.some(s => 
              s.title.toLowerCase() === song.title.toLowerCase() && 
              s.artist.toLowerCase() === song.artist.toLowerCase()
           );
           if (!isDuplicate && !existingIds.has(song.id)) {
              merged.push(song);
              existingIds.add(song.id);
           }
        }
        
        setResults(merged);
        setError(null);
      } catch (err: any) {
        setError(err);
      } finally {
        setIsLoading(false);
      }
    }, 500); // 500ms debounce

    return () => clearTimeout(timer);
  }, [query]);

  return { results, isLoading, error };
}

function formatDuration(millis: number) {
  if (!millis) return "0:00";
  const totalSeconds = Math.floor(millis / 1000);
  const m = Math.floor(totalSeconds / 60);
  const s = Math.floor(totalSeconds % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
}
"""

with open('src/hooks/useSearch.ts', 'w') as f:
    f.write(new_content)
