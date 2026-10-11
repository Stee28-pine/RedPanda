import re

with open('src/components/PodcastsView.tsx', 'r') as f:
    content = f.read()

# Add imports
content = content.replace("import { Play, Pause, ChevronLeft, Mic2, Clock } from 'lucide-react';", "import { Play, Pause, ChevronLeft, Mic2, Clock, BookmarkPlus, Bookmark as BookmarkIcon, Trash2 } from 'lucide-react';\nimport { Bookmark } from '../types';\nimport { useState } from 'react';")

# Add props
props_start = """export function PodcastsView({ 
  searchQuery, 
  onSearchChange, 
  onPlaySong, 
  nowPlaying, 
  isPlaying, 
  likedSongs, 
  onToggleLike
}: {"""
new_props_start = """export function PodcastsView({ 
  searchQuery, 
  onSearchChange, 
  onPlaySong, 
  nowPlaying, 
  isPlaying, 
  likedSongs, 
  onToggleLike,
  currentTime,
  bookmarks,
  onAddBookmark,
  onRemoveBookmark,
  onSeekToTime
}: {"""
content = content.replace(props_start, new_props_start)

props_type = """  likedSongs: Song[];
  onToggleLike: (song: Song) => void;
}) {"""
new_props_type = """  likedSongs: Song[];
  onToggleLike: (song: Song) => void;
  currentTime?: number;
  bookmarks?: Bookmark[];
  onAddBookmark?: (songId: string, timestamp: number, note: string) => void;
  onRemoveBookmark?: (id: string) => void;
  onSeekToTime?: (time: number) => void;
}) {
  const [noteText, setNoteText] = useState('');
  
  const formatTime = (seconds: number) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    if (h > 0) return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    return `${m}:${s.toString().padStart(2, '0')}`;
  };
"""
content = content.replace(props_type, new_props_type)

# Add bookmark section
episode_row = """                    <div className="flex-shrink-0 flex items-center gap-2">
                      <div className="hidden md:flex items-center text-xs font-bold text-gray-400 bg-gray-100 px-3 py-1.5 rounded-lg">
                        <Clock size={12} className="mr-1.5" />
                        {podcast.duration}
                      </div>
                    </div>
                  </div>
                );"""

new_episode_row = """                    <div className="flex-shrink-0 flex items-center gap-2">
                      <div className="hidden md:flex items-center text-xs font-bold text-gray-400 bg-gray-100 px-3 py-1.5 rounded-lg">
                        <Clock size={12} className="mr-1.5" />
                        {podcast.duration}
                      </div>
                    </div>
                  </div>
                  
                  {isCurrent && (
                    <div className="pl-[5.5rem] pr-4 pb-4 animate-in fade-in slide-in-from-top-2 duration-300">
                      <div className="bg-gray-50 border border-gray-100 rounded-xl p-4">
                        <h4 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-2">
                          <BookmarkIcon size={14} /> Bookmarks & Notes
                        </h4>
                        
                        <div className="flex items-center gap-2 mb-4">
                          <div className="text-sm font-bold text-[#fe5f64] bg-[#fe5f64]/10 px-2 py-1.5 rounded-md min-w-[3.5rem] text-center">
                            {formatTime(currentTime || 0)}
                          </div>
                          <input 
                            type="text"
                            placeholder="Add a note at this timestamp..."
                            className="flex-1 bg-white border border-gray-200 rounded-lg px-3 py-1.5 text-sm outline-none focus:border-[#fe5f64] focus:ring-1 focus:ring-[#fe5f64] transition-all"
                            value={noteText}
                            onChange={(e) => setNoteText(e.target.value)}
                            onKeyDown={(e) => {
                              if (e.key === 'Enter' && noteText.trim()) {
                                onAddBookmark?.(podcast.id, currentTime || 0, noteText.trim());
                                setNoteText('');
                              }
                            }}
                          />
                          <button 
                            className="bg-[#fe5f64] text-white p-1.5 rounded-lg hover:bg-red-500 transition-colors disabled:opacity-50"
                            disabled={!noteText.trim()}
                            onClick={() => {
                              if (noteText.trim()) {
                                onAddBookmark?.(podcast.id, currentTime || 0, noteText.trim());
                                setNoteText('');
                              }
                            }}
                          >
                            <BookmarkPlus size={18} />
                          </button>
                        </div>

                        {bookmarks?.filter(b => b.songId === podcast.id).length > 0 && (
                          <div className="space-y-2 mt-4 max-h-[200px] overflow-y-auto pr-2 hide-scrollbar">
                            {bookmarks.filter(b => b.songId === podcast.id).sort((a, b) => a.timestamp - b.timestamp).map(bm => (
                              <div key={bm.id} className="group flex items-start gap-3 bg-white p-2.5 rounded-lg border border-gray-100 hover:border-gray-200 transition-colors">
                                <button 
                                  onClick={() => onSeekToTime?.(bm.timestamp)}
                                  className="text-xs font-bold text-[#fe5f64] bg-[#fe5f64]/10 hover:bg-[#fe5f64]/20 px-2 py-1 rounded transition-colors"
                                >
                                  {formatTime(bm.timestamp)}
                                </button>
                                <p className="text-sm text-gray-700 flex-1 leading-tight">{bm.note}</p>
                                <button 
                                  onClick={() => onRemoveBookmark?.(bm.id)}
                                  className="opacity-0 group-hover:opacity-100 p-1 text-gray-400 hover:text-[#fe5f64] hover:bg-[#fe5f64]/10 rounded transition-all"
                                >
                                  <Trash2 size={14} />
                                </button>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
                );"""
content = content.replace(episode_row, new_episode_row)

# Fix map element return div wrap
content = content.replace("onClick={() => onPlaySong(podcast)}\n                  >", "onClick={() => onPlaySong(podcast)}\n                  >")
# Wait, I need to wrap the whole row and the expansion in a single parent div!
# Inside the map: return ( <div key={podcast.id}> ... </div> );

row_start = """                  <div 
                    key={podcast.id}
                    className={`flex items-center gap-4 p-3 rounded-2xl transition-all group cursor-pointer border"""

new_row_start = """                  <div key={podcast.id} className="flex flex-col">
                  <div 
                    className={`flex items-center gap-4 p-3 rounded-2xl transition-all group cursor-pointer border"""
content = content.replace(row_start, new_row_start)

with open('src/components/PodcastsView.tsx', 'w') as f:
    f.write(content)
print("Patched PodcastsView.tsx")

