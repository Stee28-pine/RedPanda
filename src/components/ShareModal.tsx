import React from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { X, Copy, Twitter, Instagram, Link2 } from 'lucide-react';
import { Song, Collection } from '../types';

export function ShareModal({ 
  item, 
  onClose,
  onCopyLink
}: { 
  item: { type: 'song' | 'album' | 'artist', id: string, name: string, data?: any } | null;
  onClose: () => void;
  onCopyLink: (url: string) => void;
}) {
  if (!item) return null;

  const url = `https://music.applet.mock/${item.type}/${item.id}`;
  const text = `Listen to ${item.name} on the new Music App!`;
  
  // Try to extract coverUrl for deep links
  const coverUrl = item.data?.coverUrl || 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?w=800&q=80';

  const handleTwitterShare = () => {
    const twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`;
    window.open(twitterUrl, '_blank');
    onClose();
  };

  const handleInstagramShare = () => {
    // Instagram doesn't have a direct web deep-link for pre-filling a post exactly like Twitter,
    // but we can simulate the deep link generation or trigger a custom URI scheme if on mobile
    // For this mock, we'll just show an alert or open instagram web
    alert(`Generating Instagram Story deep-link with background image: ${coverUrl}\n\nURL: ${url}`);
    onClose();
  };

  return (
    <AnimatePresence>
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm"
        onClick={onClose}
      >
        <motion.div 
          initial={{ scale: 0.95, opacity: 0, y: 20 }}
          animate={{ scale: 1, opacity: 1, y: 0 }}
          exit={{ scale: 0.95, opacity: 0, y: 20 }}
          onClick={(e) => e.stopPropagation()}
          className="bg-white rounded-3xl w-full max-w-sm overflow-hidden shadow-2xl border border-gray-100"
        >
          <div className="p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold text-gray-900 tracking-tight">Share</h2>
              <button onClick={onClose} className="w-8 h-8 flex items-center justify-center bg-gray-100 text-gray-500 rounded-full hover:bg-gray-200 transition-colors">
                <X size={18} />
              </button>
            </div>
            
            <div className="flex flex-col items-center mb-8">
              <img src={coverUrl} className="w-32 h-32 rounded-2xl shadow-md object-cover mb-4" alt={item.name} />
              <div className="text-lg font-bold text-gray-900 text-center">{item.name}</div>
              <div className="text-sm text-gray-500 capitalize">{item.type}</div>
            </div>

            <div className="grid grid-cols-3 gap-3 mb-6">
              <button 
                onClick={handleTwitterShare}
                className="flex flex-col items-center justify-center gap-2 p-3 rounded-2xl hover:bg-gray-50 transition-colors group"
              >
                <div className="w-12 h-12 bg-black text-white rounded-full flex items-center justify-center group-hover:scale-105 transition-transform">
                  <Twitter size={20} fill="currentColor" />
                </div>
                <span className="text-[11px] font-semibold text-gray-600">Twitter</span>
              </button>
              
              <button 
                onClick={handleInstagramShare}
                className="flex flex-col items-center justify-center gap-2 p-3 rounded-2xl hover:bg-gray-50 transition-colors group"
              >
                <div className="w-12 h-12 bg-gradient-to-tr from-yellow-400 via-red-500 to-purple-500 text-white rounded-full flex items-center justify-center group-hover:scale-105 transition-transform">
                  <Instagram size={20} />
                </div>
                <span className="text-[11px] font-semibold text-gray-600">Instagram</span>
              </button>
              
              <button 
                onClick={() => { onCopyLink(url); onClose(); }}
                className="flex flex-col items-center justify-center gap-2 p-3 rounded-2xl hover:bg-gray-50 transition-colors group"
              >
                <div className="w-12 h-12 bg-gray-100 text-gray-700 rounded-full flex items-center justify-center group-hover:scale-105 transition-transform">
                  <Copy size={20} />
                </div>
                <span className="text-[11px] font-semibold text-gray-600">Copy Link</span>
              </button>
            </div>
            
            <div className="flex items-center gap-2 bg-gray-50 p-3 rounded-xl border border-gray-100">
              <Link2 size={16} className="text-gray-400 flex-shrink-0" />
              <div className="text-[12px] text-gray-500 truncate flex-1">{url}</div>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
