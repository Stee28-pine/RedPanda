import { useEffect, useRef } from 'react';
import { Song } from '../types';

export function useLyricsScroll(nowPlaying: Song | null, currentTime: number) {
  const activeLyricRef = useRef<HTMLParagraphElement>(null);

  const hasLyrics = nowPlaying?.lyrics && nowPlaying.lyrics.length > 0;
  
  const activeLyricIdx = hasLyrics
    ? [...(nowPlaying!.lyrics || [])].reverse().findIndex(lyric => currentTime >= lyric.time)
    : -1;
    
  const currentLyricIdx = activeLyricIdx !== -1 ? (nowPlaying!.lyrics!.length - 1) - activeLyricIdx : -1;

  useEffect(() => {
    if (activeLyricRef.current) {
      activeLyricRef.current.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, [currentLyricIdx]);

  return { activeLyricRef, currentLyricIdx, hasLyrics };
}
