import { Song } from '../types';
import { motion, AnimatePresence, Reorder } from 'motion/react';
import { GripVertical } from 'lucide-react';
import React, { useEffect, useState, useRef } from 'react';
import { useLyricsScroll } from '../hooks/useLyricsScroll';
import { SongImage } from './SongImage';

const FALLBACK_IMG = 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?w=400&q=80';

export function RightSidebar({ nowPlaying, queue, onReorder, currentTime = 0, onSongContextMenu }: { nowPlaying: Song | null; queue?: Song[]; onReorder?: (newOrder: Song[]) => void; currentTime?: number; onSongContextMenu?: (e: React.MouseEvent, song: Song) => void }) {
  const currentIdx = queue && nowPlaying ? queue.findIndex(s => s.id === nowPlaying.id) : -1;
  const nextUp = currentIdx !== -1 && queue ? queue.slice(currentIdx + 1) : [];

  const [localNextUp, setLocalNextUp] = useState<Song[]>([]);
  const activeLyricRef = useRef<HTMLParagraphElement>(null);

  useEffect(() => {
    setLocalNextUp(nextUp);
  }, [nowPlaying, queue]);

  const handleReorder = (newOrder: Song[]) => {
    setLocalNextUp(newOrder);
    onReorder?.(newOrder);
  };

  const [fetchedLyrics, setFetchedLyrics] = useState<{ time: number; text: string }[] | null>(null);
  const [isLoadingLyrics, setIsLoadingLyrics] = useState(false);

  useEffect(() => {
    if (!nowPlaying) {
      setFetchedLyrics(null);
      return;
    }
    
    if (nowPlaying.lyrics && nowPlaying.lyrics.length > 0) {
      setFetchedLyrics(nowPlaying.lyrics);
      setIsLoadingLyrics(false);
      return;
    }

    setIsLoadingLyrics(true);
    setFetchedLyrics(null);
    
    fetch(`https://lrclib.net/api/get?artist_name=${encodeURIComponent(nowPlaying.artist)}&track_name=${encodeURIComponent(nowPlaying.title)}`)
      .then(res => res.json())
      .then(data => {
        if (data.syncedLyrics) {
          const lines = data.syncedLyrics.split('\n');
          const synced = lines.map((line: string) => {
            const match = line.match(/^\[(\d{2}):(\d{2}\.\d{2})\]\s*(.*)$/);
            if (match) {
              const minutes = parseInt(match[1]);
              const seconds = parseFloat(match[2]);
              return { time: minutes * 60 + seconds, text: match[3] || '...' };
            }
            return null;
          }).filter((l: any) => l !== null);
          setFetchedLyrics(synced);
        } else if (data.plainLyrics) {
          const lines = data.plainLyrics.split('\n').filter((l: string) => l.trim().length > 0);
          const timePerLine = (nowPlaying.durationSeconds || 180) / (lines.length || 1);
          const synced = lines.map((line: string, idx: number) => ({
            time: idx * timePerLine,
            text: line
          }));
          setFetchedLyrics(synced);
        } else {
          setFetchedLyrics([]);
        }
      })
      .catch(() => {
        setFetchedLyrics([]);
      })
      .finally(() => {
        setIsLoadingLyrics(false);
      });
  }, [nowPlaying]);

  const hasLyrics = fetchedLyrics && fetchedLyrics.length > 0;
  
  const activeLyricIdx = hasLyrics
    ? [...(fetchedLyrics || [])].reverse().findIndex(lyric => currentTime >= lyric.time)
    : -1;
    
  const currentLyricIdx = activeLyricIdx !== -1 && fetchedLyrics ? (fetchedLyrics.length - 1) - activeLyricIdx : -1;

  useEffect(() => {
    if (activeLyricRef.current) {
      activeLyricRef.current.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, [currentLyricIdx]);

  return (
    <aside className="w-full md:w-80 flex-shrink-0 flex flex-col h-full bg-[#f5f2ee] md:bg-transparent px-4 py-4 overflow-y-auto hide-scrollbar pb-32 absolute md:relative right-0 top-0 z-50 border-l border-white/20 shadow-xl md:shadow-none">
      <div className="mb-8">
        <h3 className="text-lg font-bold text-gray-900 mb-3 tracking-tight">Now Playing</h3>
        <AnimatePresence mode="popLayout">
          {nowPlaying ? (
            <motion.div 
              key={nowPlaying.id}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="bg-white/80 backdrop-blur-md p-3 rounded-2xl shadow-sm border border-white/50 flex items-center gap-3 cursor-pointer"
              onContextMenu={(e) => { if (nowPlaying) onSongContextMenu?.(e, nowPlaying); }}
              data-song-id={nowPlaying.id}
            >
               <SongImage song={nowPlaying} className="w-12 h-12 rounded-lg object-cover shadow-sm flex-shrink-0" alt={nowPlaying.title} />
               <div className="flex flex-col flex-1 overflow-hidden">
                  <span className="text-[14px] font-semibold text-gray-900 truncate leading-tight">{nowPlaying.title}</span>
                  <span className="text-[12px] text-gray-500 truncate mt-0.5 font-medium">{nowPlaying.artist}</span>
               </div>
               <span className="text-[12px] font-medium text-gray-400">{nowPlaying.duration}</span>
            </motion.div>
          ) : (
            <div className="bg-gray-200/50 p-4 rounded-2xl border border-gray-300 border-dashed text-center">
               <span className="text-sm font-medium text-gray-500">Not Playing</span>
            </div>
          )}
        </AnimatePresence>
      </div>

      {(hasLyrics || isLoadingLyrics) && (
        <div className="mb-8 flex-1 flex flex-col min-h-[250px]">
          <h3 className="text-lg font-bold text-gray-900 mb-3 tracking-tight">Lyrics</h3>
          <div className="bg-white/60 backdrop-blur-md rounded-2xl border border-white/50 p-4 flex-1 overflow-y-auto hide-scrollbar relative shadow-sm">
            {isLoadingLyrics ? (
              <div className="flex items-center justify-center h-full">
                 <div className="w-6 h-6 border-2 border-gray-200 border-t-[#fe5f64] rounded-full animate-spin"></div>
              </div>
            ) : (
            <div className="space-y-4 pb-[50%]">
              {fetchedLyrics!.map((lyric, idx) => {
                const isActive = idx === currentLyricIdx;
                const isPassed = idx < currentLyricIdx;
                return (
                  <motion.p
                    ref={isActive ? activeLyricRef : null}
                    key={idx}
                    animate={{
                      scale: isActive ? 1.05 : 1,
                      opacity: isActive ? 1 : isPassed ? 0.4 : 0.6,
                      color: isActive ? '#fe5f64' : '#111827',
                    }}
                    transition={{ duration: 0.3 }}
                    className={`text-[15px] font-medium leading-relaxed origin-left ${isActive ? 'font-bold' : ''}`}
                  >
                    {lyric.text}
                  </motion.p>
                );
              })}
            </div>
            )}
          </div>
        </div>
      )}

      {localNextUp.length > 0 && (
        <div className="mb-8">
          <h3 className="text-lg font-bold text-gray-900 mb-3 tracking-tight">Up Next</h3>
          
          <div 
            className="bg-white/80 backdrop-blur-md p-3 rounded-2xl shadow-sm border border-[#fe5f64]/40 flex items-center gap-3 mb-4 relative overflow-hidden cursor-pointer"
            onContextMenu={(e) => onSongContextMenu?.(e, localNextUp[0])}
            data-song-id={localNextUp[0].id}
          >
             <div className="absolute top-0 left-0 w-1 h-full bg-[#fe5f64]" />
             <SongImage song={localNextUp[0]} className="w-12 h-12 rounded-lg object-cover shadow-sm flex-shrink-0" alt={localNextUp[0].title} />
             <div className="flex flex-col flex-1 overflow-hidden">
                <span className="text-[14px] font-bold text-gray-900 truncate leading-tight">{localNextUp[0].title}</span>
                <span className="text-[12px] text-gray-500 truncate mt-0.5 font-medium">{localNextUp[0].artist}</span>
             </div>
             <div className="flex flex-col items-end">
                 <span className="text-[10px] uppercase font-bold tracking-wider text-[#fe5f64]">Next</span>
                 <span className="text-[12px] font-medium text-gray-400 mt-1">{localNextUp[0].duration}</span>
             </div>
          </div>

          {localNextUp.length > 1 && (
             <Reorder.Group axis="y" values={localNextUp.slice(1)} onReorder={(newSlice) => handleReorder([localNextUp[0], ...newSlice])} className="space-y-1">
               <AnimatePresence>
                 {localNextUp.slice(1).map((song) => (
                <Reorder.Item 
                  layout
                  key={song.id}
                  value={song}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, height: 0 }}
                  className="bg-transparent p-2 rounded-xl flex items-center gap-2 hover:bg-gray-300/50 transition-colors cursor-grab active:cursor-grabbing group relative"
                  onContextMenu={(e) => onSongContextMenu?.(e, song)}
                  data-song-id={song.id}
                >
                  <GripVertical size={16} className="text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                  <SongImage song={song} className="w-10 h-10 rounded-lg object-cover shadow-sm flex-shrink-0" alt={song.title} />
                  <div className="flex flex-col flex-1 overflow-hidden justify-center">
                      <span className="text-[14px] font-semibold text-gray-900 truncate leading-tight">{song.title}</span>
                      <span className="text-[12px] text-gray-500 truncate mt-0.5 font-medium">{song.artist}</span>
                  </div>
                  <span className="text-[12px] font-medium text-gray-400">{song.duration}</span>
                </Reorder.Item>
              ))}
            </AnimatePresence>
          </Reorder.Group>
          )}
        </div>
      )}
    </aside>
  );
}
