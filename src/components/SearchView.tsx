import React from 'react';
import { Play, Share2, Heart, Plus, ListPlus, Download, MoreHorizontal, Check, Mic2, Clock, X, Ban } from 'lucide-react';
import { useRecentSearches } from '../hooks/useRecentSearches';
import { Song } from '../types';
import { motion, AnimatePresence } from 'motion/react';
import { useState } from 'react';
import { createPortal } from 'react-dom';
import { SongImage } from './SongImage';

const FALLBACK_IMG = 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?w=400&q=80';

export function SearchView({ 
  query, 
  results, 
  isLoading, 
  onPlaySong,
  nowPlaying,
  isPlaying,
  likedSongs,
  downloadedSongs,
  onToggleLike,
  onToggleDownload,
  onAddToQueue,
  onPlayNext,
  onShare, onAddToPlaylist,onSearchSelect,
  onDontRecommend,
  onSongContextMenu
}: { 
  query: string;
  results: Song[];
  isLoading: boolean;
  onPlaySong: (s: Song, context?: { songs: Song[] }) => void;nowPlaying: Song | null;
  isPlaying: boolean;
  likedSongs: Song[];
  downloadedSongs: Song[];
  onToggleLike: (s: Song) => void;
  onToggleDownload: (song: Song) => void;
  onAddToQueue: (s: Song) => void;
  onPlayNext: (s: Song) => void;
  onShare: (item: { type: 'song' | 'album' | 'artist', id: string, name: string }) => void;
  onAddToPlaylist?: (song: Song) => void;
  onSearchSelect?: (query: string) => void;
  onDontRecommend?: (song: Song) => void;
  onSongContextMenu?: (e: React.MouseEvent, song: Song) => void;
}) {
  const { recentSearches, addSearch, removeSearch, clearSearches } = useRecentSearches();
  const [filterByArtist, setFilterByArtist] = useState(false);
  const displayResults = filterByArtist && query ? results.filter(s => s.artist.toLowerCase().includes(query.toLowerCase())) : results;
  const [contextMenu, setContextMenu] = useState<{ x: number; y: number; song: Song } | null>(null);

  const handleContextMenu = (e: React.MouseEvent, song: Song) => {
    e.preventDefault();
    if (onSongContextMenu) {
      onSongContextMenu(e, song);
      return;
    }
    setContextMenu({
      x: e.clientX,
      y: e.clientY,
      song
    });
  };

  const closeContextMenu = () => setContextMenu(null);

  return (
    <div className="px-6 md:px-10 py-8 min-h-full pb-32" onClick={closeContextMenu}>
      {isLoading ? (
        <div className="flex flex-col items-center justify-center pt-20">
          <div className="w-8 h-8 rounded-full border-2 border-gray-200 border-t-[#fe5f64] animate-spin"></div>
          <span className="mt-4 text-sm font-medium text-gray-500">Searching...</span>
        </div>
      ) : query && results.length === 0 ? (
        <div className="flex flex-col items-center justify-center pt-20 text-center">
          <div className="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mb-4">
            <span className="text-2xl">🔍</span>
          </div>
          <h3 className="text-lg font-bold text-gray-900 mb-1">No results found</h3>
          <p className="text-sm text-gray-500">Please make sure your words are spelled correctly or use less or different keywords.</p>
        </div>
      ) : query && results.length > 0 ? (
        <>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-900 tracking-tight">Top Results</h2>
            <button 
              onClick={(e) => { e.stopPropagation(); setFilterByArtist(!filterByArtist); }}
              className={`text-[13px] font-medium px-4 py-1.5 rounded-full transition-colors border ${filterByArtist ? 'bg-[#fe5f64] text-white border-[#fe5f64]' : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'}`}
            >
              Filter by Artist
            </button>
          </div>
          {displayResults.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {displayResults.map((song) => {
              const isActive = nowPlaying?.id === song.id;
              const isLiked = likedSongs.some(s => s.id === song.id);
              const isDownloaded = downloadedSongs.some(s => s.id === song.id);

              return (
                <div 
                  key={song.id}
                  onClick={() => { if (query) addSearch(query); onPlaySong(song, { songs: results }); }}
                  onContextMenu={(e) => handleContextMenu(e, song)}
                  data-song-id={song.id}
                  className={`group relative flex items-center gap-3 p-2 rounded-xl transition-colors cursor-pointer border border-transparent ${isActive ? 'bg-[#fe5f64]/10 border-[#fe5f64]/20' : 'hover:bg-white hover:shadow-sm hover:border-gray-200'} `}
                >
                  <div className="relative w-12 h-12 rounded-lg overflow-hidden shadow-sm flex-shrink-0">
                    <SongImage song={song} className="w-full h-full object-cover" alt={song.title} />
                    <div className={`absolute inset-0 bg-black/40 flex items-center justify-center transition-opacity ${isActive && isPlaying ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'}`}>
                      {isActive && isPlaying ? (
                        <div className="flex gap-[3px] items-end h-3">
                          <motion.div animate={{ height: [4, 10, 4] }} transition={{ repeat: Infinity, duration: 0.8 }} className="w-[3px] bg-white rounded-full"></motion.div>
                          <motion.div animate={{ height: [8, 10, 8] }} transition={{ repeat: Infinity, duration: 1.2, delay: 0.2 }} className="w-[3px] bg-white rounded-full"></motion.div>
                          <motion.div animate={{ height: [6, 10, 6] }} transition={{ repeat: Infinity, duration: 1, delay: 0.4 }} className="w-[3px] bg-white rounded-full"></motion.div>
                        </div>
                      ) : (
                        <Play size={20} className="fill-white text-white ml-0.5" />
                      )}
                    </div>
                  </div>
                  
                  <div className="flex flex-col flex-1 min-w-0 justify-center">
                    <span className={`text-[14px] font-semibold truncate leading-tight ${isActive ? 'text-[#fe5f64]' : 'text-gray-900'}`}>{song.title}</span>
                    <span 
                      className="text-[12px] text-gray-500 truncate mt-0.5 flex items-center gap-1"
                      
                    >
                      {isDownloaded && <Check size={12} className="text-[#fe5f64]" />}
                      {song.artist}
                    </span>
                  </div>

                  <div className="flex items-center gap-2 pr-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button 
                      onClick={(e) => { e.stopPropagation(); onToggleLike(song); }}
                      className={`transition-colors ${isLiked ? 'text-[#fe5f64]' : 'text-gray-400 hover:text-gray-700'}`}
                    >
                      <Heart size={18} className={isLiked ? 'fill-[#fe5f64]' : ''} />
                    </button>
                    <button 
                      onClick={(e) => { e.stopPropagation(); handleContextMenu(e, song); }}
                      className="text-gray-400 hover:text-gray-700"
                    >
                      <MoreHorizontal size={18} />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <p className="text-gray-500 text-sm">No results match this artist filter.</p>
            </div>
          )}
        </>
      ) : (
        <div className="pt-8">
          {!query && recentSearches.length > 0 && (
            <div className="mb-12">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-gray-900 tracking-tight">Recent Searches</h2>
                <button onClick={clearSearches} className="text-sm font-semibold text-gray-500 hover:text-gray-900">Clear</button>
              </div>
              <div className="flex flex-wrap gap-2">
                {recentSearches.map(q => (
                  <div key={q} className="flex items-center bg-white border border-gray-200 rounded-full pl-4 pr-1 py-1.5 shadow-sm hover:border-gray-300 transition-colors group cursor-pointer" onClick={() => onSearchSelect?.(q)}>
                    <Clock size={14} className="text-gray-400 mr-2" />
                    <span className="text-[13px] font-medium text-gray-700 mr-2">{q}</span>
                    <button onClick={(e) => { e.stopPropagation(); removeSearch(q); }} className="w-6 h-6 rounded-full flex items-center justify-center text-gray-400 hover:bg-gray-100 hover:text-gray-900 transition-colors">
                      <X size={14} />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
          <h2 className="text-xl font-bold text-gray-900 mb-6 tracking-tight">Browse All</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {['Pop', 'Hip-Hop', 'Rock', 'Electronic', 'R&B', 'Classical', 'Jazz', 'Indie'].map((genre, i) => (
              <div 
                key={genre} 
                className="aspect-[4/3] rounded-xl overflow-hidden relative group cursor-pointer"
                style={{ backgroundColor: `hsl(${i * 45}, 70%, 60%)` }}
              >
                <div className="absolute inset-0 bg-black/10 group-hover:bg-black/0 transition-colors" />
                <span className="absolute top-4 left-4 font-bold text-white text-lg tracking-tight shadow-sm drop-shadow-md">{genre}</span>
                <div className="absolute -bottom-4 -right-4 w-24 h-24 bg-black/20 rounded-full blur-2xl" />
              </div>
            ))}
          </div>
        </div>
      )}

      {typeof document !== 'undefined' && createPortal(
        <AnimatePresence>
        {contextMenu && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.1 }}
            style={{ top: Math.min(contextMenu.y, typeof window !== 'undefined' ? window.innerHeight - 300 : contextMenu.y), left: Math.min(contextMenu.x, typeof window !== 'undefined' ? window.innerWidth - 200 : contextMenu.x) }}
            className="fixed bg-neutral-900/85 backdrop-blur-2xl rounded-2xl shadow-[0_20px_50px_rgba(0,0,0,0.6)] border border-white/20 p-1.5 min-w-[220px] text-white z-[99999] overflow-hidden"
            onClick={(e) => e.stopPropagation()}
          >
            {onDontRecommend && (
              <button 
                onClick={() => {
                  onDontRecommend(contextMenu.song);
                  closeContextMenu();
                }}
                className="w-full text-left px-3 py-2.5 text-[13px] font-semibold text-white bg-white/10 hover:bg-white/20 active:bg-white/25 rounded-xl flex items-center gap-2.5 transition-colors mb-1 cursor-pointer"
              >
                <Ban size={16} className="text-white shrink-0" />
                <span className="text-white">Don't Recommend</span>
              </button>
            )}
            <button 
              onClick={() => {
                onPlayNext(contextMenu.song);
                closeContextMenu();
              }}
              className="w-full text-left px-3 py-2 text-[13px] font-medium text-white hover:bg-white/15 active:bg-white/25 rounded-xl flex items-center gap-2.5 transition-colors"
            >
              <ListPlus size={15} className="text-white shrink-0" /> <span className="text-white">Play Next</span>
            </button>
            <button 
              onClick={() => {
                onAddToQueue(contextMenu.song);
                closeContextMenu();
              }}
              className="w-full text-left px-3 py-2 text-[13px] font-medium text-white hover:bg-white/15 active:bg-white/25 rounded-xl flex items-center gap-2.5 transition-colors"
            >
              <Plus size={15} className="text-white shrink-0" /> <span className="text-white">Add to Queue</span>
            </button>
            <button 
              onClick={() => {
                onAddToPlaylist?.(contextMenu.song);
                closeContextMenu();
              }}
              className="w-full text-left px-3 py-2 text-[13px] font-medium text-white hover:bg-white/15 active:bg-white/25 rounded-xl flex items-center gap-2.5 transition-colors"
            >
              <ListPlus size={15} className="text-white shrink-0" /> <span className="text-white">Add to Playlist</span>
            </button>
            <button 
              onClick={() => {
                onToggleLike(contextMenu.song);
                closeContextMenu();
              }}
              className="w-full text-left px-3 py-2 text-[13px] font-medium text-white hover:bg-white/15 active:bg-white/25 rounded-xl flex items-center gap-2.5 transition-colors"
            >
              <Heart size={15} className={likedSongs.some(s => s.id === contextMenu.song.id) ? 'fill-white text-white' : 'text-white'} /> 
              <span className="text-white">{likedSongs.some(s => s.id === contextMenu.song.id) ? 'Unlike' : 'Like'}</span>
            </button>
            <button 
              onClick={() => {
                onToggleDownload(contextMenu.song);
                closeContextMenu();
              }}
              className="w-full text-left px-3 py-2 text-[13px] font-medium text-white hover:bg-white/15 active:bg-white/25 rounded-xl flex items-center gap-2.5 transition-colors"
            >
              <Download size={15} className={downloadedSongs.some(s => s.id === contextMenu.song.id) ? 'text-[#fe5f64]' : 'text-white'} /> 
              <span className="text-white">{downloadedSongs.some(s => s.id === contextMenu.song.id) ? 'Remove Download' : 'Download'}</span>
            </button>
            <div className="h-px bg-white/10 my-1 mx-1" />
            <button 
              onClick={() => {
                onShare({ type: 'song', id: contextMenu.song.id, name: contextMenu.song.title });
                closeContextMenu();
              }}
              className="w-full text-left px-3 py-2 text-[13px] font-medium text-white hover:bg-white/15 active:bg-white/25 rounded-xl flex items-center gap-2.5 transition-colors"
            >
              <Share2 size={15} className="text-white shrink-0" /> <span className="text-white">Share</span>
            </button>
          </motion.div>
        )}
      </AnimatePresence>, document.body)}
    </div>
  );
}
