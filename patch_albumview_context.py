import re

with open('src/components/AlbumView.tsx', 'r') as f:
    content = f.read()

# Add albumContextMenu state
state_search = "const [contextMenu, setContextMenu] = useState<{ x: number; y: number; song: Song } | null>(null);"
state_replace = """const [contextMenu, setContextMenu] = useState<{ x: number; y: number; song: Song } | null>(null);
  const [albumContextMenu, setAlbumContextMenu] = useState<{ x: number; y: number } | null>(null);"""
content = content.replace(state_search, state_replace)

# Update closeContextMenu
close_search = "const closeContextMenu = () => setContextMenu(null);"
close_replace = """const closeContextMenu = () => {
    setContextMenu(null);
    setAlbumContextMenu(null);
  };"""
content = content.replace(close_search, close_replace)

# Add onClick to album MoreHorizontal
button_search = """<button className="w-10 h-10 border border-gray-300 rounded-full flex items-center justify-center text-gray-700 hover:border-gray-500 transition-colors">
          <MoreHorizontal size={18} />
        </button>"""
button_replace = """<button 
          onClick={(e) => { e.stopPropagation(); setAlbumContextMenu({ x: e.clientX, y: e.clientY }); }}
          className="w-10 h-10 border border-gray-300 rounded-full flex items-center justify-center text-gray-700 hover:border-gray-500 transition-colors"
        >
          <MoreHorizontal size={18} />
        </button>"""
content = content.replace(button_search, button_replace)

# Add Album Context Menu UI
menu_ui = """      {albumContextMenu && (
        <div 
          className="fixed z-50 w-48 bg-white/80 backdrop-blur-md rounded-xl shadow-xl border border-gray-200/50 overflow-hidden py-1"
          style={{ 
             top: Math.min(albumContextMenu.y, typeof window !== 'undefined' ? window.innerHeight - 200 : albumContextMenu.y), 
             left: Math.min(albumContextMenu.x, typeof window !== 'undefined' ? window.innerWidth - 200 : albumContextMenu.x) 
          }}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="px-3 py-2 border-b border-gray-100">
            <div className="text-[13px] font-bold text-gray-900 truncate">{collection.title}</div>
            <div className="text-[11px] font-medium text-gray-500 truncate">Album Options</div>
          </div>
          <div className="p-1">
            <button 
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
      )}
"""
content = content.replace("{contextMenu && (", menu_ui + "\n      {contextMenu && (")

with open('src/components/AlbumView.tsx', 'w') as f:
    f.write(content)
