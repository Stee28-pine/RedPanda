import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Mic } from 'lucide-react';

interface VoiceOverlayProps {
  isListening: boolean;
  transcript: string;
  onClose: () => void;
}

export function VoiceOverlay({ isListening, transcript, onClose }: VoiceOverlayProps) {
  useEffect(() => {
    if (isListening) {
      const timer = setTimeout(() => {
        // Auto close after 10s of no action just in case to prevent hanging
        onClose();
      }, 10000);
      return () => clearTimeout(timer);
    }
  }, [isListening, transcript, onClose]);

  return (
    <AnimatePresence>
      {isListening && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-[120] flex items-center justify-center bg-black/60 backdrop-blur-md"
        >
          <div className="flex flex-col items-center justify-center gap-6 p-12 bg-[#1C1C1E]/80 backdrop-blur-3xl border border-white/10 rounded-[32px] shadow-2xl">
            <motion.div 
              animate={{ 
                scale: [1, 1.2, 1],
                opacity: [0.5, 1, 0.5]
              }}
              transition={{ 
                duration: 1.5, 
                repeat: Infinity,
                ease: "easeInOut"
              }}
              className="w-24 h-24 rounded-full bg-blue-500/20 flex items-center justify-center mb-4"
            >
              <div className="w-16 h-16 rounded-full bg-blue-500 flex items-center justify-center text-white shadow-[0_0_40px_rgba(59,130,246,0.5)]">
                <Mic className="w-8 h-8" />
              </div>
            </motion.div>
            
            <h3 className="text-2xl font-semibold text-white tracking-tight">Listening...</h3>
            <p className="text-white/60 text-lg max-w-md text-center line-clamp-2 h-14">
              {transcript || "Speak to search for movies, shows, or genres"}
            </p>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
