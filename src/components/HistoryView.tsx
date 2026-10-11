import React, { useState, useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { Song } from '../types';
import { motion, AnimatePresence } from 'motion/react';
import { Trash2, History, AlertTriangle } from 'lucide-react';
import { SongImage } from './SongImage';

export function HistoryView({ 
  recentlyPlayedHistory = [], 
  onPlaySong, 
  onRemoveFromHistory,
  onClearAll
}: { 
  recentlyPlayedHistory: Song[]; 
  onPlaySong: (song: Song, context: { songs: Song[] }) => void;
  onRemoveFromHistory: (song: Song) => void;
  onClearAll: () => void;
}) {
  const [localHistory, setLocalHistory] = useState<Song[]>(recentlyPlayedHistory);
  const [historyContextMenu, setHistoryContextMenu] = useState<{ x: number; y: number; song: Song } | null>(null);
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // Keep local state in sync when parent prop changes
  useEffect(() => {
    setLocalHistory(recentlyPlayedHistory);
  }, [recentlyPlayedHistory]);

  // Click outside and escape key handling
  useEffect(() => {
    if (!historyContextMenu) return;
    const handlePointerDown = (e: MouseEvent) => {
      if (menuRef.current && menuRef.current.contains(e.target as Node)) {
        return;
      }
      setHistoryContextMenu(null);
    };
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setHistoryContextMenu(null);
      }
    };
    window.addEventListener('mousedown', handlePointerDown);
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('mousedown', handlePointerDown);
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [historyContextMenu]);

  const handleDeleteSong = (song: Song) => {
    const isTarget = (s: Song) => 
      (Boolean(s.id) && Boolean(song.id) && String(s.id) === String(song.id)) ||
      (Boolean(s.title) && Boolean(song.title) && s.title.trim().toLowerCase() === song.title.trim().toLowerCase() &&
       Boolean(s.artist) && Boolean(song.artist) && s.artist.trim().toLowerCase() === song.artist.trim().toLowerCase());

    // 1. Immediately delete from local UI state (instant feedback)
    setLocalHistory(prev => prev.filter(s => !isTarget(s)));
    // 2. Dismiss menu immediately
    setHistoryContextMenu(null);
    // 3. Immediately persist to localStorage
    try {
      const saved = localStorage.getItem('ais_recently_played');
      if (saved) {
        const parsed: Song[] = JSON.parse(saved);
        const updated = parsed.filter(s => !isTarget(s));
        localStorage.setItem('ais_recently_played', JSON.stringify(updated));
      }
    } catch (e) {
      console.error(e);
    }
    // 4. Delegate to parent state handler
    onRemoveFromHistory(song);
  };

  const handleConfirmClear = () => {
    setLocalHistory([]);
    onClearAll();
    setShowConfirmModal(false);
  };

  return (
    <div className="px-6 md:px-10 py-8 pb-32 h-full overflow-y-auto" onClick={() => setHistoryContextMenu(null)}>
      <div className="flex flex-col md:flex-row items-start md:items-end justify-between mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 tracking-tight">History</h1>
          <p className="text-gray-500 mt-2">All the songs you have listened to</p>
        </div>
      </div>

      {localHistory.length > 0 ? (
        <div className="space-y-4">
          <div className="flex justify-between items-center mb-6">
            <span className="text-sm font-semibold text-gray-500">{localHistory.length} songs in history</span>
            <button 
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                setShowConfirmModal(true);
              }}
              className="text-[13px] font-bold text-[#fe5f64] hover:bg-[#fe5f64]/10 active:scale-95 px-4 py-2 rounded-lg transition-all cursor-pointer flex items-center gap-1.5"
            >
              <Trash2 size={15} />
              Clear All
            </button>
          </div>
          
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden relative">
            {localHistory.map((song, idx) => (
              <motion.div 
                key={`${song.id}-${idx}`}
                layout
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ delay: Math.min(idx * 0.03, 0.5) }}
                className="group flex items-center gap-4 p-3 hover:bg-gray-50 transition-colors border-b border-gray-50 last:border-0 cursor-pointer relative"
                onClick={() => {
                  onPlaySong(song, { songs: localHistory });
                }}
                onContextMenu={(e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  setHistoryContextMenu({
                    x: e.clientX,
                    y: e.clientY,
                    song,
                  });
                }}
              >
                <SongImage song={song} className="w-12 h-12 rounded-lg shadow-sm object-cover flex-shrink-0" alt={song.title} />
                <div className="flex-1 min-w-0">
                  <div className="text-[15px] font-semibold text-gray-900 truncate">{song.title}</div>
                  <div className="text-[13px] text-gray-500 truncate mt-0.5">{song.artist}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center h-[50vh] text-center px-4">
          <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mb-6">
            <History size={32} className="text-gray-400" />
          </div>
          <h2 className="text-xl font-bold text-gray-900 mb-2">No history yet</h2>
          <p className="text-gray-500 max-w-sm">
            Songs you listen to will appear here.
          </p>
        </div>
      )}

      {/* Confirmation Modal for Clear All */}
      <AnimatePresence>
        {showConfirmModal && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">
            <motion.div 
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              className="bg-white rounded-2xl shadow-xl border border-gray-100 max-w-md w-full p-6 text-center"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="w-12 h-12 rounded-full bg-red-50 flex items-center justify-center mb-4 text-[#fe5f64] mx-auto">
                <AlertTriangle size={24} />
              </div>

              <h3 className="text-lg font-bold text-gray-900 mb-2">Clear Listening History?</h3>
              <p className="text-sm text-gray-500 mb-6 leading-relaxed">
                This will remove all {localHistory.length} played track{localHistory.length === 1 ? '' : 's'} from your history. This action cannot be undone.
              </p>

              <div className="flex items-center gap-3 justify-end">
                <button
                  type="button"
                  onClick={() => setShowConfirmModal(false)}
                  className="px-4 py-2.5 rounded-xl text-sm font-semibold text-gray-600 hover:bg-gray-100 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={handleConfirmClear}
                  className="px-5 py-2.5 rounded-xl text-sm font-bold text-white shadow-md hover:shadow-lg active:scale-95 transition-all"
                  style={{ backgroundColor: '#fe5f64' }}
                >
                  Clear All
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      {/* Translucent context menu with single option "Delete From The History" */}
      {historyContextMenu && createPortal(
        <AnimatePresence>
          <motion.div
            ref={menuRef}
            initial={{ opacity: 0, scale: 0.94, y: 4 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.94 }}
            transition={{ duration: 0.12, ease: 'easeOut' }}
            style={{
              top: Math.max(10, Math.min(historyContextMenu.y, typeof window !== 'undefined' ? window.innerHeight - 70 : historyContextMenu.y)),
              left: Math.max(10, Math.min(historyContextMenu.x, typeof window !== 'undefined' ? window.innerWidth - 250 : historyContextMenu.x)),
            }}
            className="fixed z-[99999] min-w-[220px] bg-neutral-900/85 backdrop-blur-2xl border border-white/20 shadow-[0_20px_50px_rgba(0,0,0,0.6)] rounded-2xl p-1.5 text-white select-none overflow-hidden"
            onClick={(e) => e.stopPropagation()}
            onContextMenu={(e) => e.preventDefault()}
          >
            <button
              type="button"
              onPointerDown={(e) => {
                e.preventDefault();
                e.stopPropagation();
                handleDeleteSong(historyContextMenu.song);
              }}
              onMouseDown={(e) => {
                e.preventDefault();
                e.stopPropagation();
                handleDeleteSong(historyContextMenu.song);
              }}
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                handleDeleteSong(historyContextMenu.song);
              }}
              className="w-full text-left px-3.5 py-2.5 text-sm font-semibold text-white hover:bg-white/15 active:bg-white/25 rounded-xl flex items-center gap-2.5 transition-colors cursor-pointer select-none"
            >
              <Trash2 size={16} className="text-white shrink-0" />
              <span className="text-white">Delete From The History</span>
            </button>
          </motion.div>
        </AnimatePresence>,
        document.body
      )}
    </div>
  );
}
