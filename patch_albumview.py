import re

with open('src/components/AlbumView.tsx', 'r') as f:
    content = f.read()

content = content.replace("onAddToPlaylist, isOfflineMode }: {", "onAddToPlaylist, onRemoveFromPlaylist, isOfflineMode }: {")
content = content.replace("onAddToPlaylist?: (song: Song) => void;", "onAddToPlaylist?: (song: Song) => void;\n  onRemoveFromPlaylist?: (song: Song) => void;")

# In contextMenu, add the remove button
context_search = """            <button 
              onClick={() => {
                onAddToPlaylist?.(contextMenu.song);
                closeContextMenu();
              }}
              className="w-full text-left px-4 py-2.5 text-[13px] font-semibold text-gray-700 hover:bg-gray-100/80 hover:text-gray-900 flex items-center gap-3 transition-colors"
            >
              <ListPlus size={16} /> Add to Playlist
            </button>"""

context_replace = """            {onRemoveFromPlaylist ? (
              <button 
                onClick={() => {
                  onRemoveFromPlaylist(contextMenu.song);
                  closeContextMenu();
                }}
                className="w-full text-left px-4 py-2.5 text-[13px] font-semibold text-[#fe5f64] hover:bg-gray-100/80 flex items-center gap-3 transition-colors"
              >
                <ListPlus size={16} /> Remove from Playlist
              </button>
            ) : (
              <button 
                onClick={() => {
                  onAddToPlaylist?.(contextMenu.song);
                  closeContextMenu();
                }}
                className="w-full text-left px-4 py-2.5 text-[13px] font-semibold text-gray-700 hover:bg-gray-100/80 hover:text-gray-900 flex items-center gap-3 transition-colors"
              >
                <ListPlus size={16} /> Add to Playlist
              </button>
            )}"""

content = content.replace(context_search, context_replace)

with open('src/components/AlbumView.tsx', 'w') as f:
    f.write(content)
