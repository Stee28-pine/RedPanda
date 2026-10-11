import React, { useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'motion/react';
import { Ban, Play, ListPlus, Plus, Heart, Share2, FolderPlus, Download, Trash2 } from 'lucide-react';
import { Song } from '../types';
import { SongImage } from './SongImage';

const FALLBACK_IMG = 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?w=400&q=80';

export interface SongContextMenuProps {
  isOpen: boolean;
  position: { x: number; y: number };
  song: Song | null;
  onClose: () => void;
  onDontRecommend: (song: Song) => void;
  onPlaySong?: (song: Song) => void;
  onPlayNext?: (song: Song) => void;
  onAddToQueue?: (song: Song) => void;
  onAddToPlaylist?: (song: Song) => void;
  onRemoveFromPlaylist?: (song: Song) => void;
  onToggleLike?: (song: Song) => void;
  isLiked?: boolean;
  onToggleDownload?: (song: Song) => void;
  isDownloaded?: boolean;
  onShare?: (song: Song) => void;
}

export function SongContextMenu({
  isOpen,
  position,
  song,
  onClose,
  onDontRecommend,
  onPlaySong,
  onPlayNext,
  onAddToQueue,
  onAddToPlaylist,
  onRemoveFromPlaylist,
  onToggleLike,
  isLiked = false,
  onToggleDownload,
  isDownloaded = false,
  onShare,
}: SongContextMenuProps) {
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isOpen) return;

    const handlePointerDown = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        onClose();
      }
    };

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    const handleScroll = () => {
      onClose();
    };

    window.addEventListener('mousedown', handlePointerDown);
    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('scroll', handleScroll, true);

    return () => {
      window.removeEventListener('mousedown', handlePointerDown);
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('scroll', handleScroll, true);
    };
  }, [isOpen, onClose]);

  if (!isOpen || !song || typeof document === 'undefined') return null;

  // Viewport boundaries clamp
  const menuWidth = 240;
  const menuHeight = 320;
  const clampedX = Math.max(10, Math.min(position.x, window.innerWidth - menuWidth - 12));
  const clampedY = Math.max(10, Math.min(position.y, window.innerHeight - menuHeight - 12));

  return createPortal(
    <AnimatePresence>
      <motion.div
        ref={menuRef}
        initial={{ opacity: 0, scale: 0.94, y: 6 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.94 }}
        transition={{ duration: 0.12, ease: 'easeOut' }}
        style={{ top: clampedY, left: clampedX }}
        className="fixed z-[99999] min-w-[230px] max-w-[260px] bg-neutral-900/85 backdrop-blur-2xl border border-white/20 shadow-[0_20px_50px_rgba(0,0,0,0.6)] rounded-2xl p-1.5 text-white select-none overflow-hidden"
        onClick={(e) => e.stopPropagation()}
        onContextMenu={(e) => e.preventDefault()}
      >
        {/* Song info header */}
        <div className="flex items-center gap-2.5 p-2 rounded-xl bg-white/10 mb-1">
          <SongImage
            song={song}
            alt={song.title}
            className="w-10 h-10 rounded-lg object-cover shadow-sm shrink-0"
          />
          <div className="min-w-0 flex-1">
            <div className="text-[13px] font-bold text-white truncate leading-tight">{song.title}</div>
            <div className="text-[11px] text-white/70 truncate mt-0.5">{song.artist}</div>
          </div>
        </div>

        {/* PRIMARY ACTION: Don't Recommend */}
        <button
          onClick={() => {
            onDontRecommend(song);
            onClose();
          }}
          className="w-full text-left px-3 py-2.5 text-[13px] font-semibold text-white bg-white/10 hover:bg-white/20 active:bg-white/25 rounded-xl flex items-center gap-3 transition-colors mb-1 cursor-pointer group"
        >
          <Ban size={16} className="text-white shrink-0 group-hover:scale-110 transition-transform" />
          <div className="flex-1">
            <span className="text-white">Don't Recommend</span>
            <span className="text-[10px] text-white/70 block font-normal leading-none mt-0.5">
              Never recommend this track again
            </span>
          </div>
        </button>

        <div className="h-px bg-white/10 my-1 mx-1" />

        {/* Secondary options with translucent background and white text */}
        {onPlaySong && (
          <button
            onClick={() => {
              onPlaySong(song);
              onClose();
            }}
            className="w-full text-left px-3 py-2 text-[13px] font-medium text-white hover:bg-white/15 active:bg-white/25 rounded-xl flex items-center gap-2.5 transition-colors cursor-pointer"
          >
            <Play size={15} className="text-white shrink-0 fill-current" />
            <span className="text-white">Play Now</span>
          </button>
        )}

        {onPlayNext && (
          <button
            onClick={() => {
              onPlayNext(song);
              onClose();
            }}
            className="w-full text-left px-3 py-2 text-[13px] font-medium text-white hover:bg-white/15 active:bg-white/25 rounded-xl flex items-center gap-2.5 transition-colors cursor-pointer"
          >
            <ListPlus size={15} className="text-white shrink-0" />
            <span className="text-white">Play Next</span>
          </button>
        )}

        {onAddToQueue && (
          <button
            onClick={() => {
              onAddToQueue(song);
              onClose();
            }}
            className="w-full text-left px-3 py-2 text-[13px] font-medium text-white hover:bg-white/15 active:bg-white/25 rounded-xl flex items-center gap-2.5 transition-colors cursor-pointer"
          >
            <Plus size={15} className="text-white shrink-0" />
            <span className="text-white">Add to Queue</span>
          </button>
        )}

        {onAddToPlaylist && (
          <button
            onClick={() => {
              onAddToPlaylist(song);
              onClose();
            }}
            className="w-full text-left px-3 py-2 text-[13px] font-medium text-white hover:bg-white/15 active:bg-white/25 rounded-xl flex items-center gap-2.5 transition-colors cursor-pointer"
          >
            <FolderPlus size={15} className="text-white shrink-0" />
            <span className="text-white">Add to Playlist</span>
          </button>
        )}

        {onRemoveFromPlaylist && (
          <button
            onClick={() => {
              onRemoveFromPlaylist(song);
              onClose();
            }}
            className="w-full text-left px-3 py-2 text-[13px] font-medium text-[#fe5f64] hover:bg-white/15 active:bg-white/25 rounded-xl flex items-center gap-2.5 transition-colors cursor-pointer"
          >
            <Trash2 size={15} className="text-[#fe5f64] shrink-0" />
            <span>Remove from Playlist</span>
          </button>
        )}

        {onToggleDownload && (
          <button
            onClick={() => {
              onToggleDownload(song);
              onClose();
            }}
            className="w-full text-left px-3 py-2 text-[13px] font-medium text-white hover:bg-white/15 active:bg-white/25 rounded-xl flex items-center gap-2.5 transition-colors cursor-pointer"
          >
            <Download size={15} className={`text-white shrink-0 ${isDownloaded ? 'text-[#fe5f64]' : ''}`} />
            <span className="text-white">{isDownloaded ? 'Remove Download' : 'Download'}</span>
          </button>
        )}

        {onToggleLike && (
          <button
            onClick={() => {
              onToggleLike(song);
              onClose();
            }}
            className="w-full text-left px-3 py-2 text-[13px] font-medium text-white hover:bg-white/15 active:bg-white/25 rounded-xl flex items-center gap-2.5 transition-colors cursor-pointer"
          >
            <Heart size={15} className={`text-white shrink-0 ${isLiked ? 'fill-white' : ''}`} />
            <span className="text-white">{isLiked ? 'Unlike' : 'Like'}</span>
          </button>
        )}

        {onShare && (
          <button
            onClick={() => {
              onShare(song);
              onClose();
            }}
            className="w-full text-left px-3 py-2 text-[13px] font-medium text-white hover:bg-white/15 active:bg-white/25 rounded-xl flex items-center gap-2.5 transition-colors cursor-pointer"
          >
            <Share2 size={15} className="text-white shrink-0" />
            <span className="text-white">Share</span>
          </button>
        )}
      </motion.div>
    </AnimatePresence>,
    document.body
  );
}
