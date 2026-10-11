import React from 'react';
import { Play, Share2, Pause, SkipBack, SkipForward, Repeat, Shuffle, ListMusic, Minimize2, Maximize2, ChevronDown, Mic2, Volume2, VolumeX, Heart, Timer } from 'lucide-react';
import { Song } from '../types';
import { motion, AnimatePresence } from 'motion/react';
import { useEffect, useRef, useState } from 'react';
import { LyricsOverlay } from './LyricsOverlay';
import { Visualizer } from './Visualizer';
import { SongImage, getKnownArtwork } from './SongImage';

const FALLBACK_IMG = 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?w=400&q=80';

interface PlayerProps {
  song: Song | null;
  isPlaying: boolean;
  onTogglePlay: () => void;
  onToggleRightSidebar: () => void;
  onNext?: () => void;
  onPrev?: () => void;
  isShuffle?: boolean;
  repeatMode?: 'none' | 'all' | 'one';
  onToggleShuffle?: () => void;
  onToggleRepeat?: () => void;
  isLiked?: boolean;
  onToggleLike?: () => void;
  onShare?: (item: { type: 'song' | 'album' | 'artist', id: string, name: string }) => void;
  currentTime: number;
  duration: number;
  isBuffering: boolean;
  onSeek: (time: number) => void;
  isMini?: boolean;
  volume: number;
  onVolumeChange: (vol: number) => void;
  analyzerNode?: any;
  playbackRate?: number;
  onPlaybackRateChange?: (rate: number) => void;
  onFadeOut?: () => void;
  onSongContextMenu?: (e: React.MouseEvent, song: Song) => void;
}


const SoundLevelIndicator = ({ isPlaying, volume }: { isPlaying: boolean, volume: number }) => {
  return (
    <div className="flex items-end gap-[2px] h-4 w-6 overflow-hidden">
      {[1, 2, 3, 4].map((i) => (
        <motion.div
          key={i}
          className="w-[3px] bg-[#fe5f64] rounded-sm"
          animate={{
            height: isPlaying && volume > 0 ? [`${20 * volume}%`, `${100 * volume}%`, `${40 * volume}%`, `${80 * volume}%`, `${30 * volume}%`] : '10%'
          }}
          transition={{
            repeat: Infinity,
            duration: 0.4 + (i * 0.1),
            repeatType: 'mirror',
            ease: "easeInOut"
          }}
          style={{ originY: 1 }}
        />
      ))}
    </div>
  );
};

export function Player({ 
  song, 
  isPlaying, 
  onTogglePlay, 
  onToggleRightSidebar, 
  onNext, 
  onPrev,
  isShuffle = false,
  repeatMode = 'none',
  onToggleShuffle,
  onToggleRepeat,
  isLiked = false,
  onToggleLike,
  onShare,
  currentTime,
  duration,
  isBuffering,
  onSeek,
  isMini = false,
  volume,
  onVolumeChange,
  playbackRate = 1,
  onPlaybackRateChange,
  onFadeOut,
  analyzerNode,
  onSongContextMenu
}: PlayerProps) {
  const [isMobile, setIsMobile] = useState(false);
  const [isLandscape, setIsLandscape] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [sleepTimerMinutes, setSleepTimerMinutes] = useState<number | null>(null);
  const [showTimerMenu, setShowTimerMenu] = useState(false);
  
  const [showLyrics, setShowLyrics] = useState(false);
  const [isMuted, setIsMuted] = useState(false);


  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < 768 || window.innerHeight < 500;
      setIsMobile(mobile);
      setIsLandscape(window.innerWidth > window.innerHeight);
      if (mobile) {
        setIsCollapsed(true);
      }
    };
    window.addEventListener('resize', handleResize);
    handleResize();
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useEffect(() => {
    if (sleepTimerMinutes === null) return;
    const timeout = setTimeout(() => {
      if (isPlaying) {
        onTogglePlay();
      }
      setSleepTimerMinutes(null);
    }, sleepTimerMinutes * 60 * 1000);
    return () => clearTimeout(timeout);
  }, [sleepTimerMinutes, isPlaying, onTogglePlay]);

  const formatTime = (time: number) => {
    if (isNaN(time)) return "0:00";
    const m = Math.floor(time / 60);
    const s = Math.floor(time % 60);
    return `${m}:${s.toString().padStart(2, '0')}`;
  };



  const handleSeek = (e: React.MouseEvent<HTMLDivElement>) => {
    const bounds = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - bounds.left;
    const percent = Math.max(0, Math.min(1, x / bounds.width));
    const newTime = percent * duration;
    onSeek(newTime);
  };

  const handleVolumeSeek = (e: React.MouseEvent<HTMLDivElement>) => {
    const bounds = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - bounds.left;
    const percent = Math.max(0, Math.min(1, x / bounds.width));
    onVolumeChange(percent);
    if (percent > 0) setIsMuted(false);
  };

  const progressPercent = duration > 0 ? (currentTime / duration) * 100 : 0;
  const volumePercent = volume * 100;


  if (!song) {
    return null;
  }


  // Haptic feedback wrappers
  const triggerHaptic = (pattern: number | number[] = 10) => {
    if (typeof navigator !== 'undefined' && navigator.vibrate) {
      try { navigator.vibrate(pattern); } catch(e) {}
    }
  };

  const handleTogglePlay = () => { triggerHaptic([15, 40, 15]); onTogglePlay(); };
  const handleNextTrack = () => { triggerHaptic(15); onNext?.(); };
  const handlePrevTrack = () => { triggerHaptic(15); onPrev?.(); };
  const handleToggleLike = () => { triggerHaptic(10); onToggleLike?.(); };
  const handleToggleShuffle = () => { triggerHaptic(10); onToggleShuffle?.(); };
  const handleToggleRepeat = () => { triggerHaptic(10); onToggleRepeat?.(); };
  
  return (
    <>
      <AnimatePresence>
        {showLyrics && song && (
          <LyricsOverlay 
            song={song} 
            currentTime={currentTime} 
            duration={duration} 
            onClose={() => setShowLyrics(false)} 
          />
        )}
      </AnimatePresence>

      <AnimatePresence>
        {song && (
        <motion.div 
          key="player"
          layout
          initial={{ y: 100, opacity: 0, scale: 0.9 }}
          animate={{ y: 0, opacity: 1, scale: 1 }}
          exit={{ y: 100, opacity: 0, scale: 0.9 }}
          transition={{ layout: { type: "spring", bounce: 0.2, duration: 0.6 }, type: "spring", stiffness: 300, damping: 25 }}
          className="fixed bottom-6 left-1/2 -translate-x-1/2 flex items-center justify-center gap-4 z-[55] w-full max-w-5xl px-4 pointer-events-none"
        >
          

        {(isCollapsed || (isMini && !isMobile)) ? (
          <motion.div 
            layoutId="player-wrapper"
            className="bg-[#F5F5F5]/90 backdrop-blur-xl rounded-2xl shadow-[0_8px_30px_rgba(0,0,0,0.12)] border border-white flex items-center px-4 w-[min(90vw,340px)] h-14 pointer-events-auto cursor-pointer touch-none"
            transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
            style={{ borderRadius: 16 }}
            onClick={(e) => {
              if ((e.target as HTMLElement).closest('button')) return;
              if (isMobile) setIsCollapsed(false);
            }}
            onPanEnd={(e, info: any) => {
               if (info.offset.x < -50) onNext?.();
               if (info.offset.x > 50) onPrev?.();
            }}
            onContextMenu={(e) => { if (song) onSongContextMenu?.(e, song); }}
            data-song-id={song.id}
          >
            <div className="flex items-center w-full gap-3">
              <div className="w-10 h-10 rounded shadow-sm overflow-hidden flex-shrink-0">
                <SongImage song={song} className="w-full h-full object-cover" alt={song.title} />
              </div>
              <motion.div layoutId="song-info" transition={{ type: "spring", bounce: 0.2, duration: 0.6 }} className="flex flex-col flex-1 min-w-0 justify-center">
                <span className="text-[13px] font-semibold text-gray-900 truncate leading-tight">{song.title}</span>
                {isMini ? (
                  <div className="w-full h-1 mt-1 bg-gray-200 rounded-full relative overflow-hidden">
                    <div className="absolute inset-y-0 left-0 bg-[#fe5f64] rounded-full" style={{ width: `${progressPercent}%` }} />
                  </div>
                ) : (
                  <span className="text-[11px] text-gray-500 truncate mt-0.5">{song.artist}</span>
                )}
              </motion.div>
              
              {!isMini && (
                <>
                  <motion.button 
                    initial={{opacity:0}} animate={{opacity:1}} 
                    whileTap={{ scale: 0.7 }}
                    transition={{ type: "spring", stiffness: 400, damping: 17 }}
                    onClick={handleToggleLike}
                    className={`transition-colors flex items-center justify-center ${isLiked ? 'text-[#fe5f64]' : 'text-gray-400 hover:text-gray-700'}`}
                  >
                    <Heart size={16} className={isLiked ? 'fill-[#fe5f64]' : ''} />
                  </motion.button>
                  <motion.button initial={{opacity:0}} animate={{opacity:1}} transition={{delay:0.1}}
                    onClick={() => onShare && onShare({ type: 'song', id: song.id, name: song.title })}
                    className="mr-2 transition-colors text-gray-400 hover:text-gray-700"
                  >
                    <Share2 size={16} />
                  </motion.button>
                </>
              )}
              
              <motion.div initial={{opacity:0}} animate={{opacity:1}} transition={{delay:0.1}} className={`flex items-center gap-3 ${isMini ? 'pr-2 pl-2' : 'pr-1'}`}>
                <button onClick={handleTogglePlay} disabled={isBuffering} className="text-gray-900 hover:scale-105 transition-transform p-1 -m-1">
                  {isBuffering ? (
                    <div className="w-5 h-5 rounded-full border-2 border-gray-200 border-t-[#fe5f64] animate-spin"></div>
                  ) : isPlaying ? <Pause size={18} fill="currentColor" /> : <Play size={18} fill="currentColor" />}
                </button>
                {!isMini && (
                  <>
                    <button onClick={handleNextTrack} className="text-gray-700 hover:text-black transition-colors p-1 -m-1">
                      <SkipForward size={18} fill="currentColor" />
                    </button>
                    <button onClick={() => (!isMini && setIsCollapsed(false))} className="text-gray-400 hover:text-gray-700 ml-1 p-1 -m-1">
                      <Maximize2 size={16} />
                    </button>
                  </>
                )}
              </motion.div>
            </div>
          </motion.div>
        ) : isMobile ? (
          <motion.div 
            layoutId="player-wrapper"
            className={`fixed inset-0 bg-[#F5F5F5] z-[100] flex pointer-events-auto overflow-hidden px-6 pt-12 pb-8 ${isLandscape ? 'flex-row gap-8 items-center' : 'flex-col'}`}
            transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
            style={{ borderRadius: 0 }}
            onPanEnd={(e, info: any) => {
              if (info.offset.y > 100 && !isLandscape) {
                setIsCollapsed(true);
              }
            }}
          >
            {isLandscape ? (
              // LANDSCAPE MOBILE/TABLET LAYOUT
              <>
                {/* Left Side: Art */}
                <div className="flex-1 flex justify-center items-center h-full relative">
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1, duration: 0.3 }} className="absolute top-0 left-0">
                    <button onClick={() => setIsCollapsed(true)} className="p-3 -m-3 min-w-[44px] min-h-[44px] flex items-center justify-center text-gray-500 hover:text-gray-900 transition-colors">
                      <ChevronDown size={32} />
                    </button>
                  </motion.div>
                  <div className="relative w-full max-w-[280px] aspect-square">
                    <div 
                      className={`absolute inset-0 rounded-3xl blur-3xl transition-opacity duration-700 ${isPlaying && !isBuffering ? 'opacity-70 animate-audio-pulse' : 'opacity-0'}`} 
                      style={{ backgroundImage: `url(${getKnownArtwork(song.title, song.artist) || song.coverUrl})`, backgroundSize: 'cover', backgroundPosition: 'center', transform: 'scale(0.95)' }} 
                    />
                    <div className="relative w-full h-full rounded-3xl shadow-2xl overflow-hidden z-10">
                      <SongImage 
                        song={song} 
                        className="w-full h-full object-cover pointer-events-none" 
                        alt={song.title} 
                      />
                    </div>
                  </div>
                </div>
                {/* Right Side: Controls */}
                <div className="flex-1 flex flex-col justify-center max-w-[400px]">
                  <div className="flex justify-between items-end mb-6">
                    <motion.div layoutId="song-info" transition={{ type: "spring", bounce: 0.2, duration: 0.6 }} className="flex flex-col overflow-hidden pr-4">
                      <span className="text-2xl font-bold text-gray-900 truncate mb-1">{song.title}</span>
                      <span className="text-lg text-gray-500 truncate">{song.artist}</span>
                    </motion.div>
                    <motion.button 
                      whileTap={{ scale: 0.7 }} 
                      transition={{ type: "spring", stiffness: 400, damping: 17 }}
                      onClick={handleToggleLike} 
                      className={`p-3 -m-3 min-w-[44px] min-h-[44px] flex items-center justify-center transition-colors mb-2 ${isLiked ? 'text-[#fe5f64]' : 'text-gray-400'}`}
                    >
                      <Heart size={28} className={isLiked ? 'fill-[#fe5f64]' : ''} />
                    </motion.button>
                  </div>
                  {/* Scrubber */}
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1, duration: 0.3 }} className="mb-6">
                    <div className="w-full h-8 flex items-center group cursor-pointer touch-none mb-1" onClick={handleSeek}>
                      <div className="w-full h-1.5 bg-gray-200 rounded-full relative pointer-events-none">
                        <div className="absolute inset-y-0 left-0 bg-[#fe5f64] rounded-full pointer-events-none" style={{ width: `${progressPercent}%` }}>
                           <div className="absolute right-0 top-1/2 -translate-y-1/2 w-4 h-4 bg-[#fe5f64] rounded-full shadow-md border-2 border-white translate-x-1/2 scale-100"></div>
                        </div>
                      </div>
                    </div>
                    <div className="flex justify-between text-[12px] font-semibold text-gray-400 tabular-nums">
                      <span>{formatTime(currentTime)}</span>
                      <span>{formatTime(duration)}</span>
                    </div>
                  </motion.div>
                  {/* Controls */}
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1, duration: 0.3 }} className="flex items-center justify-between mb-8 px-2">
                     <button onClick={handleToggleShuffle} className={`p-3 -m-3 min-w-[44px] min-h-[44px] flex items-center justify-center ${isShuffle ? 'text-[#fe5f64]' : 'text-gray-400'}`}><Shuffle size={24} /></button>
                     <button onClick={handlePrevTrack} className="p-3 -m-3 text-gray-800 min-w-[44px] min-h-[44px] flex items-center justify-center"><SkipBack size={36} fill="currentColor" /></button>
                     <button onClick={handleTogglePlay} disabled={isBuffering} className="w-16 h-16 flex items-center justify-center text-gray-900">
                        {isBuffering ? <div className="w-12 h-12 rounded-full border-4 border-gray-100 border-t-[#fe5f64] animate-spin"></div> : (isPlaying ? <Pause size={48} fill="currentColor" /> : <Play size={48} fill="currentColor" />)}
                     </button>
                     <button onClick={handleNextTrack} className="p-3 -m-3 text-gray-800 min-w-[44px] min-h-[44px] flex items-center justify-center"><SkipForward size={36} fill="currentColor" /></button>
                     <button onClick={handleToggleRepeat} className={`p-3 -m-3 min-w-[44px] min-h-[44px] flex items-center justify-center relative ${repeatMode !== 'none' ? 'text-[#fe5f64]' : 'text-gray-400'}`}>
                        <Repeat size={24} />
                        {repeatMode === 'one' && <span className="absolute top-1 right-1 text-[10px] font-bold bg-[#fe5f64] text-white rounded-full w-4 h-4 flex items-center justify-center">1</span>}
                     </button>
                  </motion.div>
                  {/* Volume & Advanced */}
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1, duration: 0.3 }} className="flex flex-col gap-4 px-2">
                    <div className="flex items-center gap-4">
                      <VolumeX size={20} className="text-gray-400" />
                      <input type="range" min="0" max="1" step="0.01" value={volume} onChange={(e) => onVolumeChange(parseFloat(e.target.value))} className="flex-1 h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-[#fe5f64]" />
                      <Volume2 size={20} className="text-gray-400" />
                      <SoundLevelIndicator isPlaying={isPlaying} volume={volume} />
                    </div>
                    <div className="flex items-center justify-between mt-1">
                      <button onClick={onFadeOut} className="text-[11px] font-bold px-3 py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full transition-colors uppercase tracking-wider">Fade Out</button>
                      <button onClick={() => {
                        const rates = [0.5, 1, 1.5, 2];
                        const nextRate = rates[(rates.indexOf(playbackRate) + 1) % rates.length];
                        onPlaybackRateChange?.(nextRate);
                      }} className="text-[11px] font-bold px-3 py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full transition-colors tracking-wider">{playbackRate}x Speed</button>
                    </div>
                  </motion.div>
                </div>
              </>
            ) : (
              // PORTRAIT MOBILE LAYOUT
              <>
                {/* Header */}
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1, duration: 0.3 }} className="flex justify-between items-center mb-6">
                   <button onClick={() => setIsCollapsed(true)} className="p-3 -m-3 min-w-[44px] min-h-[44px] flex items-center justify-center text-gray-500 hover:text-gray-900 transition-colors">
                     <ChevronDown size={32} />
                   </button>
                   <span className="text-[11px] font-bold tracking-widest text-gray-400 uppercase">Now Playing</span>
                   <button onClick={onToggleRightSidebar} className="p-3 -m-3 min-w-[44px] min-h-[44px] flex items-center justify-center text-gray-500 hover:text-gray-900 transition-colors">
                     <ListMusic size={24} />
                   </button>
                </motion.div>
                {/* Album Art with Glow */}
                <div 
                  className="relative flex-1 flex flex-col justify-center items-center mb-6 min-h-[250px] cursor-pointer"
                  onContextMenu={(e) => { if (song) onSongContextMenu?.(e, song); }}
                  data-song-id={song.id}
                >
                    <div 
                      className={`absolute inset-0 rounded-3xl blur-3xl transition-opacity duration-700 ${isPlaying && !isBuffering ? 'opacity-70 animate-audio-pulse' : 'opacity-0'}`} 
                      style={{ backgroundImage: `url(${getKnownArtwork(song.title, song.artist) || song.coverUrl})`, backgroundSize: 'cover', backgroundPosition: 'center', transform: 'scale(0.95)' }} 
                    />
                    <div className="relative w-full max-w-[340px] aspect-square rounded-3xl shadow-2xl overflow-hidden z-10">
                      <SongImage 
                        song={song} 
                        className="w-full h-full object-cover pointer-events-none" 
                        alt={song.title} 
                      />
                    </div>
                </div>
                {/* Info */}
                <div className="flex justify-between items-end mb-4">
                  <motion.div layoutId="song-info" transition={{ type: "spring", bounce: 0.2, duration: 0.6 }} className="flex flex-col overflow-hidden pr-4">
                    <span className="text-2xl font-bold text-gray-900 truncate mb-1">{song.title}</span>
                    <span className="text-lg text-gray-500 truncate">{song.artist}</span>
                  </motion.div>
                  <motion.button 
                    whileTap={{ scale: 0.7 }} 
                    transition={{ type: "spring", stiffness: 400, damping: 17 }}
                    onClick={handleToggleLike} 
                    className={`p-3 -m-3 min-w-[44px] min-h-[44px] flex items-center justify-center transition-colors mb-2 ${isLiked ? 'text-[#fe5f64]' : 'text-gray-400'}`}
                  >
                    <Heart size={28} className={isLiked ? 'fill-[#fe5f64]' : ''} />
                  </motion.button>
                </div>
                {/* Scrubber */}
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1, duration: 0.3 }} className="mb-6">
                  <div className="w-full h-8 flex items-center group cursor-pointer mb-1 touch-none" onClick={handleSeek}>
                    <div className="w-full h-1.5 bg-gray-200 rounded-full relative pointer-events-none">
                      <div className="absolute inset-y-0 left-0 bg-[#fe5f64] rounded-full pointer-events-none" style={{ width: `${progressPercent}%` }}>
                         <div className="absolute right-0 top-1/2 -translate-y-1/2 w-4 h-4 bg-[#fe5f64] rounded-full shadow-md border-2 border-white translate-x-1/2 scale-100"></div>
                      </div>
                    </div>
                  </div>
                  <div className="flex justify-between text-[12px] font-semibold text-gray-400 tabular-nums">
                    <span>{formatTime(currentTime)}</span>
                    <span>{formatTime(duration)}</span>
                  </div>
                </motion.div>
                {/* Controls */}
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1, duration: 0.3 }} className="flex items-center justify-between mb-8 px-2">
                   <button onClick={handleToggleShuffle} className={`p-3 -m-3 min-w-[44px] min-h-[44px] flex items-center justify-center ${isShuffle ? 'text-[#fe5f64]' : 'text-gray-400'}`}><Shuffle size={24} /></button>
                   <button onClick={handlePrevTrack} className="p-3 -m-3 text-gray-800 min-w-[44px] min-h-[44px] flex items-center justify-center"><SkipBack size={36} fill="currentColor" /></button>
                   <button onClick={handleTogglePlay} disabled={isBuffering} className="w-16 h-16 flex items-center justify-center text-gray-900">
                      {isBuffering ? <div className="w-12 h-12 rounded-full border-4 border-gray-100 border-t-[#fe5f64] animate-spin"></div> : (isPlaying ? <Pause size={48} fill="currentColor" /> : <Play size={48} fill="currentColor" />)}
                   </button>
                   <button onClick={handleNextTrack} className="p-3 -m-3 text-gray-800 min-w-[44px] min-h-[44px] flex items-center justify-center"><SkipForward size={36} fill="currentColor" /></button>
                   <button onClick={handleToggleRepeat} className={`p-3 -m-3 min-w-[44px] min-h-[44px] flex items-center justify-center relative ${repeatMode !== 'none' ? 'text-[#fe5f64]' : 'text-gray-400'}`}>
                      <Repeat size={24} />
                      {repeatMode === 'one' && <span className="absolute top-1 right-1 text-[10px] font-bold bg-[#fe5f64] text-white rounded-full w-4 h-4 flex items-center justify-center">1</span>}
                   </button>
                </motion.div>
                {/* Volume & Advanced */}
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1, duration: 0.3 }} className="flex flex-col gap-4 px-2 mt-4 mb-4">
                  <div className="flex items-center gap-4">
                    <VolumeX size={20} className="text-gray-400" />
                    <input type="range" min="0" max="1" step="0.01" value={volume} onChange={(e) => onVolumeChange(parseFloat(e.target.value))} className="flex-1 h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-[#fe5f64]" />
                    <Volume2 size={20} className="text-gray-400" />
                    <SoundLevelIndicator isPlaying={isPlaying} volume={volume} />
                  </div>
                  <div className="flex items-center justify-between mt-2">
                    <button onClick={onFadeOut} className="text-[11px] font-bold px-3 py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full transition-colors uppercase tracking-wider">Fade Out</button>
                    {song.genre === 'Podcast' && (
                      <button onClick={() => {
                        const rates = [1, 1.25, 1.5, 2];
                        const currentIndex = rates.indexOf(playbackRate);
                        const nextRate = rates[currentIndex !== -1 ? (currentIndex + 1) % rates.length : 1];
                        onPlaybackRateChange?.(nextRate);
                      }} className="text-[11px] font-bold px-3 py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full transition-colors tracking-wider flex items-center gap-1">
                        <Timer size={12} /> {playbackRate}x
                      </button>
                    )}
                  </div>
                </motion.div>
              </>
            )}
          </motion.div>
        ) : (
          <div className="flex items-center gap-3 md:gap-4 pointer-events-auto">
            {/* Pill 1: Controls */}
            <div className="bg-[#F9F9F9]/90 backdrop-blur-xl rounded-2xl shadow-lg border border-white/50 flex items-center justify-center px-5 h-14 gap-5">
              <button onClick={handlePrevTrack} className="text-gray-800 hover:text-black transition-colors">
                <SkipBack size={18} fill="currentColor" />
              </button>
              <div className="relative flex items-center justify-center w-6 h-6">
                {isBuffering && (
                  <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                     <div className="w-8 h-8 rounded-full border-2 border-gray-200 border-t-[#fe5f64] animate-spin absolute"></div>
                  </div>
                )}
                <button onClick={handleTogglePlay} disabled={isBuffering} className={`text-gray-900 hover:scale-105 transition-transform active:scale-95 ${isBuffering ? 'opacity-[0.01]' : 'opacity-100'}`}>
                  {isPlaying ? <Pause size={22} fill="currentColor" /> : <Play size={22} fill="currentColor" />}
                </button>
              </div>
              <button onClick={handleNextTrack} className="text-gray-800 hover:text-black transition-colors">
                <SkipForward size={18} fill="currentColor" />
              </button>
            </div>

            {/* Pill 2: Scrubber */}
            <div className="bg-[#F9F9F9]/90 backdrop-blur-xl rounded-2xl shadow-lg border border-white/50 flex items-center px-5 h-14 gap-3 md:w-[480px]">
              <span className="text-[11px] font-semibold text-gray-500 w-8 text-right tabular-nums">{formatTime(currentTime)}</span>
              <div 
                className="flex-1 h-1.5 bg-gray-300 rounded-full flex cursor-pointer shadow-inner relative group"
                onClick={handleSeek}
              >
                <div className="absolute inset-y-0 left-0 bg-[#fe5f64] rounded-full pointer-events-none transition-all duration-[250ms] ease-linear" style={{ width: `${progressPercent}%` }}>
                   <div className="absolute right-0 top-1/2 -translate-y-1/2 w-3 h-3 bg-[#fe5f64] rounded-full shadow border border-white translate-x-1/2 scale-0 group-hover:scale-100 transition-transform"></div>
                </div>
              </div>
              <span className="text-[11px] font-semibold text-gray-500 w-8 tabular-nums">{formatTime(duration)}</span>
            </div>

            {/* Pill 3: Options */}
            <div className="bg-[#F9F9F9]/90 backdrop-blur-xl rounded-2xl shadow-lg border border-white/50 flex items-center justify-center px-5 h-14 gap-5">
              <button 
                onClick={handleToggleRepeat}
                className={`transition-colors relative ${repeatMode !== 'none' ? 'text-[#fe5f64]' : 'text-gray-700 hover:text-black'}`}
                title="Repeat"
              >
                <Repeat size={16} />
                {repeatMode === 'one' && (
                  <span className="absolute -top-1 -right-1 text-[9px] font-bold bg-[#fe5f64] text-white rounded-full w-3 h-3 flex items-center justify-center">1</span>
                )}
              </button>
              <button 
                onClick={handleToggleShuffle}
                className={`transition-colors ${isShuffle ? 'text-[#fe5f64]' : 'text-gray-700 hover:text-black'}`}
                title="Shuffle"
              >
                <Shuffle size={16} />
              </button>
              <button onClick={onToggleRightSidebar} className="text-gray-700 hover:text-black transition-colors" title="Queue">
                <ListMusic size={16} />
              </button>
              {song.genre === 'Podcast' && (
                <button 
                  onClick={() => {
                    const rates = [1, 1.25, 1.5, 2];
                    const currentIndex = rates.indexOf(playbackRate);
                    const nextRate = rates[currentIndex !== -1 ? (currentIndex + 1) % rates.length : 1];
                    onPlaybackRateChange?.(nextRate);
                  }}
                  className="text-gray-700 hover:text-black transition-colors flex items-center justify-center font-bold text-[11px] leading-none tracking-tight h-4 w-6 rounded hover:bg-gray-200" 
                  title="Playback Speed"
                >
                  {playbackRate}x
                </button>
              )}
              
              <button onClick={() => setIsCollapsed(true)} className="text-gray-700 hover:text-black transition-colors ml-1 hidden md:block" title="Minimize">
                <Minimize2 size={16} />
              </button>
              
              <div className="relative">
                <button onClick={() => setShowTimerMenu(!showTimerMenu)} className={`transition-colors relative ${sleepTimerMinutes ? 'text-[#fe5f64]' : 'text-gray-700 hover:text-black'}`} title="Sleep Timer">
                  <Timer size={16} />
                  {sleepTimerMinutes && (
                    <span className="absolute -top-1.5 -right-2.5 text-[9px] font-bold bg-[#fe5f64] text-white rounded-full w-4 h-4 flex items-center justify-center">{sleepTimerMinutes}</span>
                  )}
                </button>
                <AnimatePresence>
                  {showTimerMenu && (
                    <motion.div
                      initial={{ opacity: 0, y: 10, scale: 0.95 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, y: 10, scale: 0.95 }}
                      className="absolute bottom-full mb-4 -right-2 bg-white/95 backdrop-blur-xl border border-gray-100 shadow-[0_8px_30px_rgba(0,0,0,0.12)] rounded-xl py-2 w-32 z-[60]"
                    >
                      <div className="px-3 py-1 text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">Sleep Timer</div>
                      {[15, 30, 60].map(mins => (
                        <button key={mins} onClick={() => { setSleepTimerMinutes(mins); setShowTimerMenu(false); }} className="w-full text-left px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50 hover:text-[#fe5f64] transition-colors flex items-center justify-between">
                          {mins} mins {sleepTimerMinutes === mins && <span className="w-1.5 h-1.5 rounded-full bg-[#fe5f64]"></span>}
                        </button>
                      ))}
                      <button onClick={() => { setSleepTimerMinutes(null); setShowTimerMenu(false); }} className="w-full text-left px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50 hover:text-[#fe5f64] transition-colors border-t border-gray-100 mt-1 flex items-center justify-between">
                        Off {sleepTimerMinutes === null && <span className="w-1.5 h-1.5 rounded-full bg-[#fe5f64]"></span>}
                      </button>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </div>
          </div>
        )}
        </motion.div>
        )}
    </AnimatePresence>
    </>
  );
}
