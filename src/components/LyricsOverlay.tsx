import { Song } from '../types';
import { motion, AnimatePresence } from 'motion/react';
import { ChevronDown } from 'lucide-react';
import { useEffect, useRef } from 'react';
import { SongImage } from './SongImage';

interface LyricsOverlayProps {
  song: Song;
  currentTime: number;
  duration: number;
  onClose: () => void;
}

const FALLBACK_IMG = 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?w=400&q=80';

// A mock set of lyrics to show synchronization
const MOCK_LYRICS = [
  { time: 0, text: "(Instrumental Intro)" },
  { time: 5000, text: "I've been running through the jungle" },
  { time: 9000, text: "I've been running with the wolves" },
  { time: 13000, text: "To get to you, to get to you" },
  { time: 18000, text: "I've been down the darkest alleys" },
  { time: 22000, text: "Saw the dark side of the moon" },
  { time: 26000, text: "To get to you, to get to you" },
  { time: 31000, text: "I've looked for love in every stranger" },
  { time: 35000, text: "Took too much to ease the anger" },
  { time: 39000, text: "All for you, yeah, all for you" },
  { time: 44000, text: "Let it play, let it play, let it play" },
  { time: 49000, text: "(Chorus)" },
  { time: 55000, text: "Oh, it's just a placeholder lyric" },
  { time: 60000, text: "Since we don't have the real ones" },
  { time: 65000, text: "But it looks amazing" },
  { time: 70000, text: "Doesn't it?" },
];

export function LyricsOverlay({ song, currentTime, duration, onClose }: LyricsOverlayProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const scrollTimeoutRef = useRef<any>(null);
  const isUserScrollingRef = useRef(false);
  
  // Calculate active line based on current time in ms
  const currentMs = currentTime * 1000;
  const lyrics = song.lyrics || MOCK_LYRICS;
  
  let activeIndex = 0;
  if (song.lyrics) {
    const nextIdx = lyrics.findIndex(l => l.time > currentMs);
    if (nextIdx === -1) {
      activeIndex = lyrics.length - 1;
    } else {
      activeIndex = Math.max(0, nextIdx - 1);
    }
  } else if (duration > 0) {
    // Map the mock lyrics linearly to the duration
    const progress = currentTime / duration;
    activeIndex = Math.min(
      Math.floor(progress * lyrics.length),
      lyrics.length - 1
    );
  }

  const targetScrollY = useRef<number | null>(null);
  const currentScrollY = useRef<number | null>(null);

  useEffect(() => {
    if (scrollRef.current) {
      const container = scrollRef.current;
      const activeElement = container.children[activeIndex] as HTMLElement;
      if (activeElement) {
        const elementTop = activeElement.offsetTop;
        const elementHeight = activeElement.offsetHeight;
        const containerHeight = container.clientHeight;
        
        targetScrollY.current = elementTop - (containerHeight / 2) + (elementHeight / 2);
      }
    }
  }, [activeIndex, duration]);

  useEffect(() => {
    let rafId: number;

    const loop = () => {
      const container = scrollRef.current;
      if (container && targetScrollY.current !== null) {
        if (!isUserScrollingRef.current) {
          if (currentScrollY.current === null) {
             currentScrollY.current = container.scrollTop;
          }
          
          const diff = targetScrollY.current - currentScrollY.current;
          
          if (Math.abs(diff) > 0.5) {
             currentScrollY.current += diff * 0.08; // Smooth easing factor
             container.scrollTop = currentScrollY.current;
          } else {
             currentScrollY.current = targetScrollY.current;
             container.scrollTop = currentScrollY.current;
          }
        } else {
           // Sync internal state to actual scroll position during user interaction
           currentScrollY.current = container.scrollTop;
        }
      }
      rafId = requestAnimationFrame(loop);
    };

    rafId = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(rafId);
  }, []);

  const handleUserInteraction = () => {
    isUserScrollingRef.current = true;
    if (scrollTimeoutRef.current) clearTimeout(scrollTimeoutRef.current);
    
    scrollTimeoutRef.current = setTimeout(() => {
      isUserScrollingRef.current = false;
    }, 1500); // Snap back after 1.5s of no interaction
  };

  useEffect(() => {
    return () => {
      if (scrollTimeoutRef.current) clearTimeout(scrollTimeoutRef.current);
    };
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0, y: 50, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: 50, scale: 0.95 }}
      transition={{ type: 'spring', stiffness: 250, damping: 25 }}
      className="fixed inset-0 z-[60] flex flex-col md:flex-row overflow-hidden bg-black text-white"
    >
      {/* Blurred background */}
      <div className="absolute inset-0 z-0">
        <SongImage 
          song={song} 
          className="w-full h-full object-cover blur-[80px] opacity-40 transform scale-110" 
          alt="" 
        />
        <div className="absolute inset-0 bg-gradient-to-b from-black/20 to-black/60" />
      </div>

      {/* Close button */}
      <button 
        onClick={onClose}
        className="absolute top-8 right-8 z-[70] w-10 h-10 bg-white/10 hover:bg-white/20 backdrop-blur rounded-full flex items-center justify-center transition-colors"
      >
        <ChevronDown size={24} />
      </button>

      {/* Album Art Side (Desktop) */}
      <div className="relative z-10 flex-1 flex flex-col items-center justify-center p-8 lg:p-20">
        <motion.div 
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.2, type: 'spring' }}
          className="w-full max-w-md aspect-square rounded-2xl shadow-2xl overflow-hidden mb-8"
        >
          <SongImage 
            song={song} 
            className="w-full h-full object-cover" 
            alt={song.title} 
          />
        </motion.div>
        <div className="text-center">
          <h2 className="text-2xl md:text-3xl font-bold tracking-tight mb-2">{song.title}</h2>
          <p className="text-lg text-white/60 font-medium">{song.artist}</p>
        </div>
      </div>

      {/* Lyrics Side */}
      <div className="relative z-10 flex-1 h-full flex flex-col mask-fade-y">
        <div 
          ref={scrollRef}
          onWheel={handleUserInteraction}
          onTouchStart={handleUserInteraction}
          onTouchMove={handleUserInteraction}
          onPointerDown={handleUserInteraction}
          className="relative flex-1 overflow-y-auto hide-scrollbar py-[40vh] px-8 md:px-16"
        >
          {lyrics.map((lyric, idx) => {
            const isActive = idx === activeIndex;
            const isPassed = idx < activeIndex;
            
            return (
              <motion.div 
                key={idx}
                animate={{
                  scale: isActive ? 1.05 : 1,
                  opacity: isActive ? 1 : isPassed ? 0.3 : 0.4,
                  originX: 0
                }}
                transition={{ duration: 0.4 }}
                className="mb-8"
              >
                <p className={`text-3xl md:text-5xl font-bold tracking-tight leading-tight transition-colors duration-500 ${isActive ? 'text-white' : 'text-white/80'}`}>
                  {lyric.text}
                </p>
              </motion.div>
            );
          })}
        </div>
      </div>
    </motion.div>
  );
}
