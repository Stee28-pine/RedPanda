import re

with open('src/components/HistoryView.tsx', 'r') as f:
    content = f.read()

# We need to add a ref to keep track of click timeouts
import_pattern = r'import React, \{ useState \} from \'react\';'
new_import = "import React, { useState, useRef } from 'react';"
content = content.replace(import_pattern, new_import)

# Add clickTimeoutRef to component
comp_start = """export function HistoryView({ 
  recentlyPlayedHistory, 
  onPlaySong, 
  onRemoveFromHistory,
  onClearAll
}: { 
  recentlyPlayedHistory: Song[]; 
  onPlaySong: (song: Song, context: { songs: Song[] }) => void;
  onRemoveFromHistory: (song: Song) => void;
  onClearAll: () => void;
}) {
  const [doubleClickedSongId, setDoubleClickedSongId] = useState<string | null>(null);"""

new_comp_start = """export function HistoryView({ 
  recentlyPlayedHistory, 
  onPlaySong, 
  onRemoveFromHistory,
  onClearAll
}: { 
  recentlyPlayedHistory: Song[]; 
  onPlaySong: (song: Song, context: { songs: Song[] }) => void;
  onRemoveFromHistory: (song: Song) => void;
  onClearAll: () => void;
}) {
  const [doubleClickedSongId, setDoubleClickedSongId] = useState<string | null>(null);
  const clickTimeoutRef = useRef<NodeJS.Timeout | null>(null);"""
content = content.replace(comp_start, new_comp_start)

# Replace the click handlers
old_click = """                onClick={(e) => {
                  e.stopPropagation();
                  if (doubleClickedSongId !== song.id) {
                    onPlaySong(song, { songs: recentlyPlayedHistory });
                  }
                }}
                onDoubleClick={(e) => {
                  e.stopPropagation();
                  setDoubleClickedSongId(song.id);
                }}"""

new_click = """                onClick={(e) => {
                  e.stopPropagation();
                  if (clickTimeoutRef.current) {
                    clearTimeout(clickTimeoutRef.current);
                    clickTimeoutRef.current = null;
                  }
                  if (doubleClickedSongId !== song.id) {
                    clickTimeoutRef.current = setTimeout(() => {
                      onPlaySong(song, { songs: recentlyPlayedHistory });
                    }, 250);
                  }
                }}
                onDoubleClick={(e) => {
                  e.stopPropagation();
                  if (clickTimeoutRef.current) {
                    clearTimeout(clickTimeoutRef.current);
                    clickTimeoutRef.current = null;
                  }
                  setDoubleClickedSongId(song.id);
                }}"""
content = content.replace(old_click, new_click)

with open('src/components/HistoryView.tsx', 'w') as f:
    f.write(content)

print("Patched click handlers with delay")
