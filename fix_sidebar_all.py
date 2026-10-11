with open('src/components/Sidebar.tsx', 'r') as f:
    content = f.read()

# 1. Imports
import_react = "import React from 'react';"
new_import = "import React from 'react';\nimport { Bookmark } from '../types';\nimport { Trash2 as TrashIcon, Play } from 'lucide-react';"
content = content.replace(import_react, new_import)

# 2. Props
props_start = "onCreatePlaylist,\n}: {"
new_props_start = "onCreatePlaylist,\n  bookmarks,\n  onPlaySong,\n  onSeekToTime,\n  onRemoveBookmark,\n}: {"

if props_start in content:
    content = content.replace(props_start, new_props_start)
else:
    print("Props start not found")

props_end = "  onMergePlaylist?: (targetId: string, sourceId: string) => void,\n})"
new_props_end = "  onMergePlaylist?: (targetId: string, sourceId: string) => void,\n  bookmarks?: Bookmark[],\n  onPlaySong?: (song: any) => void,\n  onSeekToTime?: (time: number) => void,\n  onRemoveBookmark?: (id: string) => void,\n})"
content = content.replace(props_end, new_props_end)

# 3. Add formatTime
format_time = """  const handleContextMenu = (e: React.MouseEvent, playlistId: string) => {
    e.preventDefault();
    setContextMenu({ x: e.clientX, y: e.clientY, playlistId });
    setMergeMenu(null);
  };"""
new_format = format_time + """\n  const formatTime = (seconds: number) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    if (h > 0) return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    return `${m}:${s.toString().padStart(2, '0')}`;
  };"""
if format_time in content:
    content = content.replace(format_time, new_format)
else:
    print("Format time replace failed")

# 4. Add Bookmarks section
nav_end = "</nav>\n      </div>\n      <div className=\"mt-auto pt-4 pb-24 px-3 flex-shrink-0\">"
bookmarks_html = """</nav>
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

      <div className="mt-auto pt-4 pb-24 px-3 flex-shrink-0">"""

if nav_end in content:
    content = content.replace(nav_end, bookmarks_html)
else:
    print("Nav end not found")
    # try another way
    content = content.replace("      <div className=\"mt-auto pt-4 pb-24 px-3 flex-shrink-0\">", bookmarks_html.replace("</nav>\n      </div>\n", ""))

with open('src/components/Sidebar.tsx', 'w') as f:
    f.write(content)
print("done sidebar")
