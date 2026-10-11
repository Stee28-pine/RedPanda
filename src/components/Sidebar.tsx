import React from 'react';
import { Bookmark, Song } from '../types';
import { Trash2 as TrashIcon, Play } from 'lucide-react';
import { Home, Mic2, Disc, Music, Plus, Heart, Star, History, Download, MoreVertical, Trash2, Merge } from 'lucide-react';
import { SONGS } from '../data';
import { useState, useRef, useEffect } from 'react';
import { SongImage } from './SongImage';

const FALLBACK_IMG = 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?w=400&q=80';
const BACKUP_FALLBACK_SVG = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><rect width="100%" height="100%" fill="%23fe5f64"/><circle cx="50" cy="50" r="30" fill="%23ffffff" opacity="0.2"/><path d="M45 35v30a8 8 0 1 1-6-7.75V40h16v18a8 8 0 1 1-6-7.75V35H45z" fill="%23ffffff"/></svg>';

export function Sidebar({ 
  onDeletePlaylist,
  onMergePlaylist,
  onNavigateHome, 
  onNavigatePodcasts,
  onNavigateHistory,
  currentView,
  onNavigateLikedSongs,
  likedSongs = [],
  activeCollectionId,
  isCollapsed = false,
  nowPlaying,
  playlists,
  onNavigatePlaylist,
  onCreatePlaylist,
  bookmarks,
  onPlaySong,
  onSeekToTime,
  onRemoveBookmark,
}: { 
  onNavigateHome: () => void, 
  currentView: string,
  onNavigateLikedSongs?: () => void,
  likedSongs?: any[],
  activeCollectionId?: string,
  isCollapsed?: boolean,
  nowPlaying?: any,
  playlists?: any[],
  onNavigatePlaylist?: (p: any) => void,
  onCreatePlaylist?: () => void,
  onNavigatePodcasts?: () => void,
  onNavigateHistory?: () => void,
  onDeletePlaylist?: (id: string) => void,
  onMergePlaylist?: (targetId: string, sourceId: string) => void,
  bookmarks?: Bookmark[],
  onPlaySong?: (song: Song) => void,
  onSeekToTime?: (time: number) => void,
  onRemoveBookmark?: (id: string) => void,
}) {
  const [contextMenu, setContextMenu] = useState<{ x: number; y: number; playlistId: string } | null>(null);
  const [mergeMenu, setMergeMenu] = useState<{ x: number; y: number; sourcePlaylistId: string } | null>(null);

  useEffect(() => {
    const handleClick = () => {
      setContextMenu(null);
      setMergeMenu(null);
    };
    document.addEventListener('click', handleClick);
    return () => document.removeEventListener('click', handleClick);
  }, []);

  const handleContextMenu = (e: React.MouseEvent, playlistId: string) => {
    e.preventDefault();
    setContextMenu({ x: e.clientX, y: e.clientY, playlistId });
    setMergeMenu(null);
  };

  const formatTime = (seconds: number) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    if (h > 0) return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  return (
    <>
    <aside className={`w-64 min-w-[16rem] flex-shrink-0 flex flex-col h-full bg-[#f5f2ee] md:bg-transparent py-4 overflow-y-auto hide-scrollbar text-sm font-medium transition-all duration-300 z-40 relative`}>
      
      {/* Brand Logo */}
      <div className={`mb-8 px-4 flex items-center justify-start h-12`}>
        <img src="/698481-removebg-preview.png" alt="RedPanda Logo" className="h-full w-auto object-contain max-w-[180px]" onContextMenu={(e) => e.preventDefault()} />
      </div>

      <div className="mb-6 px-3">
        <h3 className={`text-[11px] font-bold text-gray-400 mb-2 px-3 tracking-widest uppercase ${isCollapsed ? 'block md:hidden' : 'block'}`}>MY MUSIC</h3>
        <nav className="space-y-0.5">
          <NavItem icon={<Home size={18} />} label="Home" active={currentView === 'home'} onClick={onNavigateHome} isCollapsed={isCollapsed} activeIconColor="text-[#fe5f64]" />
          <NavItem icon={<History size={18} />} label="History" active={currentView === 'history'} onClick={onNavigateHistory} isCollapsed={isCollapsed} activeIconColor="text-[#fe5f64]" />
          <NavItem icon={<Mic2 size={18} />} label="Podcasts" active={currentView === 'podcasts'} onClick={onNavigatePodcasts} isCollapsed={isCollapsed} activeIconColor="text-[#fe5f64]" />
        </nav>
      </div>

      <div className={`mb-8 px-3 ${isCollapsed ? 'block md:hidden' : 'block'}`}>
        <div className="flex items-center justify-between px-3 mb-2 text-gray-400">
          <h3 className="text-[11px] font-bold tracking-widest uppercase">PLAYLISTS</h3>
          <button onClick={onCreatePlaylist} className="hover:text-gray-900 transition-colors">
            <Plus size={14} />
          </button>
        </div>
        
        <nav className="space-y-0.5">
          <button onClick={onNavigateLikedSongs} className={`w-full flex items-center gap-3 px-3 py-1.5 rounded-lg transition-colors ${activeCollectionId === 'liked-songs' ? 'bg-gray-200/80 text-gray-900' : 'text-gray-700 hover:bg-gray-300/50'}`}>
            <div className="w-8 h-8 rounded bg-gray-200/80 flex items-center justify-center text-gray-500">
              <Star size={14} className="fill-[#fe5f64] text-[#fe5f64]" />
            </div>
            <div className="text-left flex-1 min-w-0">
              <div className="text-[13px] font-semibold truncate leading-tight">Liked Song</div>
            </div>
          </button>
          
          {playlists?.map(p => (
            <button 
              key={p.id} 
              onClick={() => onNavigatePlaylist?.(p)} 
              onContextMenu={(e) => handleContextMenu(e, p.id)}
              onDoubleClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                handleContextMenu(e, p.id);
              }}
              className={`w-full flex items-center gap-3 px-3 py-1.5 rounded-lg transition-colors ${activeCollectionId === p.id ? 'bg-gray-200/80 text-gray-900' : 'text-gray-700 hover:bg-gray-300/50'}`}
            >
              {p.songs && p.songs.length > 0 ? (
                 <img src={p.coverUrl} alt={p.title} className="w-8 h-8 rounded object-cover shadow-sm" />
              ) : (
                 <div className="w-8 h-8 rounded bg-gray-200/80 flex items-center justify-center text-gray-500">
                   <Music size={14} />
                 </div>
              )}
              <div className="text-left flex-1 min-w-0">
                <div className="text-[13px] font-semibold truncate leading-tight">{p.title}</div>
              </div>
            </button>
          ))}
        </nav>
      </div>


      {bookmarks && bookmarks.length > 0 && (
        <div className={`mb-8 px-3 ${isCollapsed ? 'hidden' : 'block'}`}>
          <h3 className="text-[11px] font-bold text-gray-400 mb-2 px-3 tracking-widest uppercase">BOOKMARKED MOMENTS</h3>
          <div className="space-y-1">
            {bookmarks.map(bm => {
              const song = SONGS.find(s => s.id === bm.songId);
              if (!song) return null;
              const isPlaying = nowPlaying?.id === song.id;
              
              return (
                <div key={bm.id} className="group relative w-full flex items-center gap-3 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-300/50 transition-colors">
                  <button 
                    className="flex-1 flex flex-col text-left min-w-0"
                    onClick={() => {
                      if (!isPlaying && onPlaySong) {
                        onPlaySong(song);
                        setTimeout(() => onSeekToTime?.(bm.timestamp), 300);
                      } else {
                        onSeekToTime?.(bm.timestamp);
                      }
                    }}
                  >
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-[#fe5f64] bg-[#fe5f64]/10 px-1.5 py-0.5 rounded">{formatTime(bm.timestamp)}</span>
                      <span className="text-[13px] font-semibold truncate text-gray-900">{bm.note}</span>
                    </div>
                    <span className="text-[11px] text-gray-500 truncate mt-0.5">{song.title}</span>
                  </button>
                  <button 
                    onClick={() => onRemoveBookmark?.(bm.id)}
                    className="opacity-0 group-hover:opacity-100 p-1.5 text-gray-400 hover:text-[#fe5f64] hover:bg-[#fe5f64]/10 rounded transition-all"
                  >
                    <TrashIcon size={14} />
                  </button>
                </div>
              );
            })}
          </div>
        </div>
      )}

      <div className="mt-auto pt-4 pb-24 px-3 flex-shrink-0">
        {nowPlaying && (
          <div className={`bg-[#F9F9F9] rounded-xl p-3 shadow-sm border border-gray-200 flex items-center gap-3 transition-all ${isCollapsed ? 'hidden md:flex flex-col text-center p-2' : 'flex'}`}>
            <SongImage 
              song={nowPlaying}
              alt={nowPlaying.title || 'Now Playing Track'} 
              className={`${isCollapsed ? 'w-10 h-10 min-w-[2.5rem] min-h-[2.5rem]' : 'w-12 h-12 min-w-[3rem] min-h-[3rem]'} rounded-lg object-cover shadow-sm flex-shrink-0 aspect-square block bg-gray-200 border border-black/5`} 
            />
            <div className={`flex-1 min-w-0 ${isCollapsed ? 'hidden' : 'block'}`}>
              <div className="text-sm font-bold text-gray-900 truncate">{nowPlaying.title}</div>
              <div className="text-[12px] text-gray-500 truncate">{nowPlaying.artist}</div>
            </div>
            <button className={`text-gray-400 hover:text-gray-900 transition-colors ${isCollapsed ? 'hidden' : 'block'}`}>
              <Heart size={16} />
            </button>
          </div>
        )}
      </div>

    </aside>

      {contextMenu && (
        <div 
          className="fixed z-[100] w-48 bg-white rounded-lg shadow-xl border border-gray-100 py-1"
          style={{ top: contextMenu.y, left: contextMenu.x }}
          onClick={(e) => e.stopPropagation()}
        >
          {playlists && playlists.length > 1 && (
            <button 
              className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2"
              onClick={() => {
                setMergeMenu({ x: contextMenu.x + 10, y: contextMenu.y + 10, sourcePlaylistId: contextMenu.playlistId });
                setContextMenu(null);
              }}
            >
              <Merge size={16} /> Merge Playlist...
            </button>
          )}
          <button 
            className="w-full text-left px-4 py-2 text-sm flex items-center gap-2 hover:bg-gray-50 text-[#fe5f64]"
            onClick={() => {
              onDeletePlaylist?.(contextMenu.playlistId);
              setContextMenu(null);
            }}
          >
            <Trash2 size={16} /> Delete Playlist
          </button>
        </div>
      )}

      {mergeMenu && (
        <div 
          className="fixed z-[100] w-56 bg-white rounded-lg shadow-xl border border-gray-100 py-1"
          style={{ top: mergeMenu.y, left: mergeMenu.x }}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="px-4 py-2 text-xs font-semibold text-gray-500 uppercase">Merge with...</div>
          {playlists?.filter(p => p.id !== mergeMenu.sourcePlaylistId).map(p => (
            <button 
              key={p.id}
              className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
              onClick={() => {
                onMergePlaylist?.(p.id, mergeMenu.sourcePlaylistId);
                setMergeMenu(null);
              }}
            >
              {p.title}
            </button>
          ))}
        </div>
      )}
    </>
  );
}

function NavItem({ icon, label, active, onClick, isCollapsed, activeIconColor = 'text-gray-900' }: { icon: React.ReactNode, label: string, active?: boolean, onClick?: () => void, isCollapsed?: boolean, activeIconColor?: string }) {
  return (
    <button 
      onClick={onClick}
      title={isCollapsed ? label : undefined}
      className={`w-full flex items-center ${isCollapsed ? 'justify-start px-3 md:justify-center md:px-0' : 'gap-3 px-3'} py-2.5 rounded-lg transition-colors ${active ? 'bg-gray-200/80 text-gray-900 shadow-sm' : 'text-gray-700 hover:bg-gray-300/50'}`}
    >
      <div className={`${active ? activeIconColor : 'text-gray-500'} ${isCollapsed ? 'mr-3 md:mr-0' : ''}`}>
        {icon}
      </div>
      <span className={`font-semibold text-[15px] tracking-tight ${isCollapsed ? 'block md:hidden' : 'block'} ${active ? 'text-[#fe5f64]' : ''}`}>{label}</span>
    </button>
  );
}
