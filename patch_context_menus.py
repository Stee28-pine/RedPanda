import re

components = ['src/components/AlbumView.tsx', 'src/components/ArtistView.tsx', 'src/components/SearchView.tsx']

for file in components:
    with open(file, 'r') as f:
        content = f.read()
    
    # Add prop
    content = content.replace("onShare: (item: { type: 'song' | 'album' | 'artist', id: string, name: string }) => void;", "onShare: (item: { type: 'song' | 'album' | 'artist', id: string, name: string }) => void;\n  onAddToPlaylist?: (song: Song) => void;")
    
    # Add destructured prop
    content = content.replace("onShare\n}:", "onShare,\n  onAddToPlaylist\n}:")
    # For some files that might be single line or differently formatted
    content = content.replace("onShare,", "onShare, onAddToPlaylist,")
    
    # Also if the destructuring is just onShare,
    if 'onAddToPlaylist' not in content:
        # fallback string replace
        content = content.replace("onShare:", "onAddToPlaylist?: (song: Song) => void; onShare:")
        content = content.replace("onShare }", "onShare, onAddToPlaylist }")
    
    # Add context menu button
    playlist_btn = """            <button 
              onClick={() => {
                onAddToPlaylist?.(contextMenu.song);
                closeContextMenu();
              }}
              className="w-full text-left px-4 py-2.5 text-[13px] font-semibold text-gray-700 hover:bg-gray-100/80 hover:text-gray-900 flex items-center gap-3 transition-colors"
            >
              <ListPlus size={16} /> Add to Playlist
            </button>"""
    
    content = content.replace("<Plus size={16} /> Add to Queue\n            </button>", "<Plus size={16} /> Add to Queue\n            </button>\n" + playlist_btn)
    
    with open(file, 'w') as f:
        f.write(content)

print("Context menus patched")
