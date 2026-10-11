import re

with open('src/components/AlbumView.tsx', 'r') as f:
    content = f.read()

search = """            <button 
              onClick={() => {
                onShare({ type: 'album', id: collection.id, name: collection.title });
                closeContextMenu();
              }}
              className="w-full text-left px-4 py-2.5 text-[13px] font-semibold text-gray-700 hover:bg-gray-100/80 hover:text-gray-900 flex items-center gap-3 transition-colors"
            >
              <Share2 size={16} /> Share Album
            </button>
          </div>
        </div>
      )}"""

replace = """            <button 
              onClick={() => {
                onShare({ type: 'album', id: collection.id, name: collection.title });
                closeContextMenu();
              }}
              className="w-full text-left px-4 py-2.5 text-[13px] font-semibold text-gray-700 hover:bg-gray-100/80 hover:text-gray-900 flex items-center gap-3 transition-colors"
            >
              <Share2 size={16} /> Share Album
            </button>
            
            {collection.type === 'playlist' && (
              <>
                {playlists && playlists.length > 1 && (
                  <button 
                    onClick={() => {
                      setMergeMenu({ x: albumContextMenu.x + 10, y: albumContextMenu.y + 10 });
                      setAlbumContextMenu(null);
                    }}
                    className="w-full text-left px-4 py-2.5 text-[13px] font-semibold text-gray-700 hover:bg-gray-100/80 hover:text-gray-900 flex items-center gap-3 transition-colors"
                  >
                    <Merge size={16} /> Merge Playlist...
                  </button>
                )}
                <button 
                  onClick={() => {
                    onDeletePlaylist?.(collection.id);
                    closeContextMenu();
                  }}
                  className="w-full text-left px-4 py-2.5 text-[13px] font-semibold text-[#fe5f64] hover:bg-red-50 hover:text-[#fe5f64] flex items-center gap-3 transition-colors"
                >
                  <Trash2 size={16} /> Delete Playlist
                </button>
              </>
            )}
          </div>
        </div>
      )}

      {mergeMenu && (
        <div 
          className="fixed z-[100] w-56 bg-white rounded-lg shadow-xl border border-gray-100 py-1"
          style={{ 
            top: Math.min(mergeMenu.y, typeof window !== 'undefined' ? window.innerHeight - 200 : mergeMenu.y), 
            left: Math.min(mergeMenu.x, typeof window !== 'undefined' ? window.innerWidth - 200 : mergeMenu.x) 
          }}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="px-4 py-2 text-xs font-semibold text-gray-500 uppercase border-b border-gray-100 mb-1">Merge with...</div>
          {playlists?.filter(p => p.id !== collection.id).map(p => (
            <button 
              key={p.id}
              className="w-full text-left px-4 py-2.5 text-[13px] font-semibold text-gray-700 hover:bg-gray-50 truncate"
              onClick={() => {
                onMergePlaylist?.(p.id, collection.id);
                closeContextMenu();
              }}
            >
              {p.title}
            </button>
          ))}
        </div>
      )}"""

content = content.replace(search, replace)

with open('src/components/AlbumView.tsx', 'w') as f:
    f.write(content)
