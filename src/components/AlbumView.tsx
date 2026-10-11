import React from 'react';
import { Collection, Song } from '../types';
import { Play, Share2, Pause, Heart, MoreHorizontal, Clock, Shuffle, Plus, ListPlus, Download, Check, Mic2, Merge, Trash2, Ban } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { useState } from 'react';
import { createPortal } from 'react-dom';
import { SongImage } from './SongImage';

const FALLBACK_IMG = 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?w=400&q=80';

export function AlbumView({ 
  collection, 
  onPlaySong, 
  nowPlaying, 
  isPlaying, 
  likedSongs,
  downloadedSongs,
  onToggleLike,
  onToggleDownload,
  onAddToQueue,
  onPlayNext,
  onShare, onAddToPlaylist, onRemoveFromPlaylist,
  playlists = [], onDeletePlaylist, onMergePlaylist,
  onDontRecommend,
  onSongContextMenu
}: { 
  collection: Collection; 
  onPlaySong: (song: Song, context: Collection) => void; 
  nowPlaying: Song | null; 
  isPlaying: boolean;
  likedSongs: Song[];
  downloadedSongs: Song[];
  onToggleLike: (song: Song) => void;
  onToggleDownload: (song: Song) => void;
  onAddToQueue: (song: Song) => void;
  onPlayNext: (song: Song) => void;
  onShare: (item: { type: 'song' | 'album' | 'artist', id: string, name: string }) => void;onAddToPlaylist?: (song: Song) => void;
  onRemoveFromPlaylist?: (song: Song) => void;
  playlists?: Collection[];
  onDeletePlaylist?: (id: string) => void;
  onMergePlaylist?: (targetId: string, sourceId: string) => void;
  onDontRecommend?: (song: Song) => void;
  onSongContextMenu?: (e: React.MouseEvent, song: Song, options?: { onRemoveFromPlaylist?: (s: Song) => void }) => void;
}) {
  const [contextMenu, setContextMenu] = useState<{ x: number; y: number; song: Song } | null>(null);
  const [albumContextMenu, setAlbumContextMenu] = useState<{ x: number; y: number } | null>(null);
  const [mergeMenu, setMergeMenu] = useState<{ x: number; y: number } | null>(null);

  const handleContextMenu = (e: React.MouseEvent, song: Song) => {
    e.preventDefault();
    if (onSongContextMenu) {
      onSongContextMenu(e, song, {
        onRemoveFromPlaylist: onRemoveFromPlaylist ? () => onRemoveFromPlaylist(song) : undefined
      });
      return;
    }
    setContextMenu({
      x: e.clientX,
      y: e.clientY,
      song
    });
  };

  const closeContextMenu = () => {
    setContextMenu(null);
    setAlbumContextMenu(null);
    setMergeMenu(null);
  };

  return (
    <div className="relative min-h-full pb-32" onClick={closeContextMenu}>
      {/* Header */}
      <div className="flex flex-col md:flex-row items-end gap-6 md:gap-8 px-6 md:px-10 pt-16 pb-8 relative overflow-hidden bg-gradient-to-b from-gray-200/50 to-transparent">
        <motion.div 
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="w-48 h-48 md:w-60 md:h-60 rounded-2xl overflow-hidden shadow-2xl flex-shrink-0 z-10"
        >
          <img src={collection.coverUrl} className="w-full h-full object-cover" alt={collection.title} />
        </motion.div>
        
        <motion.div 
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.1 }}
          className="z-10 flex-1 w-full"
        >
          <span className="text-[11px] font-bold tracking-widest uppercase text-gray-500 mb-2 block">{collection.type}</span>
          <h1 className="text-4xl md:text-6xl font-black text-gray-900 tracking-tight leading-none mb-4">{collection.title}</h1>
          <div className="flex items-center gap-3 text-sm text-gray-600 font-medium">
            <img src={collection.coverUrl} className="w-6 h-6 rounded-full object-cover shadow-sm" alt="Author" />
            <span className="text-gray-900 font-bold" >{collection.subtitle || 'RedPanda'}</span>
            <span className="w-1 h-1 rounded-full bg-gray-400"></span>
            <span>{collection.songs.length} songs</span>
            <span className="w-1 h-1 rounded-full bg-gray-400"></span>
            <span>2024</span>
          </div>
        </motion.div>
      </div>

      {/* Controls */}
      <div className="px-6 md:px-10 py-4 flex items-center gap-4 z-20 relative">
        <button 
          onClick={() => collection.songs.length > 0 && onPlaySong(collection.songs[0], collection)}
          className="w-14 h-14 bg-[#fe5f64] hover:bg-[#A84A24] rounded-full flex items-center justify-center text-white shadow-lg hover:scale-105 transition-transform"
        >
          <Play fill="currentColor" size={24} className="ml-1" />
        </button>
        <button className="w-10 h-10 border border-gray-300 rounded-full flex items-center justify-center text-gray-700 hover:border-gray-500 transition-colors">
          <Shuffle size={18} />
        </button>
        <motion.button 
          whileTap={{ scale: 0.9 }}
          onClick={() => onShare({ type: 'album', id: collection.id, name: collection.title })}
          className="w-10 h-10 border border-gray-300 rounded-full flex items-center justify-center text-gray-700 hover:border-gray-500 transition-colors"
        >
          <Share2 size={18} />
        </motion.button>
        <button 
          onClick={(e) => { e.stopPropagation(); setAlbumContextMenu({ x: e.clientX, y: e.clientY }); }}
          className="w-10 h-10 border border-gray-300 rounded-full flex items-center justify-center text-gray-700 hover:border-gray-500 transition-colors"
        >
          <MoreHorizontal size={18} />
        </button>
      </div>

      {/* Song List */}
      <div className="px-2 md:px-10 mt-6">
        <div className="flex items-center text-[12px] font-semibold text-gray-400 border-b border-gray-200 pb-2 mb-4 px-2 tracking-widest uppercase">
          <div className="w-8 text-center">#</div>
          <div className="flex-1">Title</div>
          <div className="w-32 hidden md:block">Plays</div>
          <div className="w-12 text-right"><Clock size={16} className="inline-block" /></div>
        </div>
        
        <div className="space-y-1">
          {collection.songs.map((song, idx) => {
            const isActive = nowPlaying?.id === song.id;
            const isLiked = likedSongs.some(s => s.id === song.id);
            const isDownloaded = downloadedSongs.some(s => s.id === song.id);
            
            return (
              <div 
                key={song.id}
                onClick={() => onPlaySong(song, collection)}
                onContextMenu={(e) => handleContextMenu(e, song)}
                onTouchStart={(e) => {
                  const timer = setTimeout(() => {
                    const touch = e.touches[0];
                    handleContextMenu({ 
                      preventDefault: () => {}, 
                      clientX: touch.clientX, 
                      clientY: touch.clientY 
                    } as any, song);
                  }, 500);
                  e.currentTarget.dataset.longPressTimer = timer.toString();
                }}
                onTouchEnd={(e) => {
                  const timer = e.currentTarget.dataset.longPressTimer;
                  if (timer) clearTimeout(parseInt(timer));
                }}
                onTouchCancel={(e) => {
                  const timer = e.currentTarget.dataset.longPressTimer;
                  if (timer) clearTimeout(parseInt(timer));
                }}
                onTouchMove={(e) => {
                  const timer = e.currentTarget.dataset.longPressTimer;
                  if (timer) clearTimeout(parseInt(timer));
                }}
                data-song-id={song.id}
                className={`group flex items-center p-2 rounded-xl transition-colors cursor-pointer ${isActive ? 'bg-gray-200/50' : 'hover:bg-gray-100'} `}
              >
                <div className="w-8 text-center text-[13px] font-medium text-gray-400 group-hover:text-gray-900 flex items-center justify-center">
                  {isActive && isPlaying ? (
                    <div className="flex gap-[3px] items-end h-3">
                      <motion.div animate={{ height: [4, 12, 4] }} transition={{ repeat: Infinity, duration: 0.8 }} className="w-1 bg-[#fe5f64] rounded-full"></motion.div>
                      <motion.div animate={{ height: [8, 12, 8] }} transition={{ repeat: Infinity, duration: 1.2, delay: 0.2 }} className="w-1 bg-[#fe5f64] rounded-full"></motion.div>
                      <motion.div animate={{ height: [6, 12, 6] }} transition={{ repeat: Infinity, duration: 1, delay: 0.4 }} className="w-1 bg-[#fe5f64] rounded-full"></motion.div>
                    </div>
                  ) : isActive ? (
                    <span className="text-[#fe5f64]">{(idx + 1).toString().padStart(2, '0')}</span>
                  ) : (
                    <span className="group-hover:hidden">{(idx + 1).toString().padStart(2, '0')}</span>
                  )}
                  {!isActive && <Play size={14} className="hidden group-hover:block fill-current" />}
                </div>
                
                <div className="flex-1 min-w-0 flex items-center gap-3 ml-2">
                  <SongImage song={song} className="w-10 h-10 rounded shadow-sm object-cover flex-shrink-0" alt={song.title} />
                  <div className="flex flex-col min-w-0">
                    <span className={`text-[14px] font-semibold truncate leading-tight ${isActive ? 'text-[#fe5f64]' : 'text-gray-900'}`}>{song.title}</span>
                    <span 
                      className="text-[12px] text-gray-500 truncate mt-0.5 flex items-center gap-1"
                      
                    >
                      {isDownloaded && <Check size={12} className="text-[#fe5f64]" />}
                      {song.artist}
                    </span>
                  </div>
                </div>
                
                <div className="w-32 hidden md:block text-[13px] text-gray-500 font-medium truncate pr-4">
                  {song.plays ? song.plays.toLocaleString() : '—'}
                </div>

                <div className="flex items-center gap-3 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button 
                    onClick={(e) => { e.stopPropagation(); onToggleLike(song); }}
                    className={`transition-colors ${isLiked ? 'text-[#fe5f64]' : 'text-gray-400 hover:text-gray-700'}`}
                  >
                    <motion.div animate={isLiked ? { scale: [1, 1.4, 1] } : { scale: 1 }} transition={{ duration: 0.3 }}>
                       <Heart size={18} className={isLiked ? 'fill-[#fe5f64]' : ''} />
                    </motion.div>
                  </button>
                  <button 
                    onClick={(e) => { e.stopPropagation(); handleContextMenu(e, song); }}
                    className="text-gray-400 hover:text-gray-700"
                  >
                    <MoreHorizontal size={18} />
                  </button>
                </div>
                
                <div className="w-12 text-right text-[13px] font-medium text-gray-400 ml-2">
                  {song.duration}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {typeof document !== 'undefined' && createPortal(
        <AnimatePresence>
              {albumContextMenu && (
        <div 
          className="fixed z-50 w-48 bg-white/80 backdrop-blur-md rounded-xl shadow-xl border border-gray-200/50 overflow-hidden py-1"
          style={{ 
             top: Math.min(albumContextMenu.y, typeof window !== 'undefined' ? window.innerHeight - 200 : albumContextMenu.y), 
             left: Math.min(albumContextMenu.x, typeof window !== 'undefined' ? window.innerWidth - 200 : albumContextMenu.x) 
          }}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="px-3 py-2 border-b border-gray-100">
            <div className="text-[13px] font-bold text-gray-900 truncate">{collection.title}</div>
            <div className="text-[11px] font-medium text-gray-500 truncate">Album Options</div>
          </div>
          <div className="p-1">
            <button 
              onClick={() => {
                onShare({ type: 'album', id: collection.id, name: collection.title });
                closeContextMenu();
              }}
              className="w-full text-left px-4 py-2.5 text-[13px] font-semibold text-gray-700 hover:bg-gray-100/80 hover:text-gray-900 flex items-center gap-3 transition-colors"
            >
              <Share2 size={16} /> Share Album
            </button>
            
            {collection.type === 'playlist' && (
              <>
                {playlists && playlists.length > 1 && (
                  <button 
                    onClick={() => {
                      setMergeMenu({ x: albumContextMenu.x + 10, y: albumContextMenu.y + 10 });
                      setAlbumContextMenu(null);
                    }}
                    className="w-full text-left px-4 py-2.5 text-[13px] font-semibold text-gray-700 hover:bg-gray-100/80 hover:text-gray-900 flex items-center gap-3 transition-colors"
                  >
                    <Merge size={16} /> Merge Playlist...
                  </button>
                )}
                <button 
                  onClick={() => {
                    onDeletePlaylist?.(collection.id);
                    closeContextMenu();
                  }}
                  className="w-full text-left px-4 py-2.5 text-[13px] font-semibold text-[#fe5f64] hover:bg-red-50 hover:text-[#fe5f64] flex items-center gap-3 transition-colors"
                >
                  <Trash2 size={16} /> Delete Playlist
                </button>
              </>
            )}
          </div>
        </div>
      )}

      {mergeMenu && (
        <div 
          className="fixed z-[100] w-56 bg-white rounded-lg shadow-xl border border-gray-100 py-1"
          style={{ 
            top: Math.min(mergeMenu.y, typeof window !== 'undefined' ? window.innerHeight - 200 : mergeMenu.y), 
            left: Math.min(mergeMenu.x, typeof window !== 'undefined' ? window.innerWidth - 200 : mergeMenu.x) 
          }}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="px-4 py-2 text-xs font-semibold text-gray-500 uppercase border-b border-gray-100 mb-1">Merge with...</div>
          {playlists?.filter(p => p.id !== collection.id).map(p => (
            <button 
              key={p.id}
              className="w-full text-left px-4 py-2.5 text-[13px] font-semibold text-gray-700 hover:bg-gray-50 truncate"
              onClick={() => {
                onMergePlaylist?.(p.id, collection.id);
                closeContextMenu();
              }}
            >
              {p.title}
            </button>
          ))}
        </div>
      )}

      {contextMenu && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.1 }}
            style={{ top: Math.min(contextMenu.y, typeof window !== 'undefined' ? window.innerHeight - 300 : contextMenu.y), left: Math.min(contextMenu.x, typeof window !== 'undefined' ? window.innerWidth - 200 : contextMenu.x) }}
            className="fixed bg-neutral-900/85 backdrop-blur-2xl rounded-2xl shadow-[0_20px_50px_rgba(0,0,0,0.6)] border border-white/20 p-1.5 min-w-[220px] z-[99999] overflow-hidden text-white"
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
            {onRemoveFromPlaylist ? (
              <button 
                onClick={() => {
                  onRemoveFromPlaylist(contextMenu.song);
                  closeContextMenu();
                }}
                className="w-full text-left px-3 py-2 text-[13px] font-medium text-[#fe5f64] hover:bg-white/15 active:bg-white/25 rounded-xl flex items-center gap-2.5 transition-colors"
              >
                <Trash2 size={15} className="text-[#fe5f64] shrink-0" /> <span>Remove from Playlist</span>
              </button>
            ) : (
              <button 
                onClick={() => {
                  onAddToPlaylist?.(contextMenu.song);
                  closeContextMenu();
                }}
                className="w-full text-left px-3 py-2 text-[13px] font-medium text-white hover:bg-white/15 active:bg-white/25 rounded-xl flex items-center gap-2.5 transition-colors"
              >
                <ListPlus size={15} className="text-white shrink-0" /> <span className="text-white">Add to Playlist</span>
              </button>
            )}
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
