with open('src/components/HomeView.tsx', 'r') as f:
    content = f.read()

# Replace the last `    </div>\n  );\n}` with the menus
# Let's find the last occurrence of `    </div>`
idx = content.rfind('    </div>')
if idx != -1:
    content = content[:idx] + """    </div>

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
              className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 truncate"
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
}"""

content = content.replace("  return (\n    <div className", "  return (\n    <>\n    <div className")

with open('src/components/HomeView.tsx', 'w') as f:
    f.write(content)
