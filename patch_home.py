import re

with open('src/components/HomeView.tsx', 'r') as f:
    content = f.read()

# Imports
content = re.sub(
    r"import { Play, Download } from 'lucide-react';",
    "import { Play, Download, MoreVertical, Merge, Trash2 } from 'lucide-react';\nimport { useState, useEffect } from 'react';",
    content
)

# Props definition
content = re.sub(
    r"downloadedSongs\?: Song\[\];\n  onGenreClick\?: \(genre: string\) => void;\n\}\)",
    r"downloadedSongs?: Song[];\n  onGenreClick?: (genre: string) => void;\n  onDeletePlaylist?: (id: string) => void;\n  onMergePlaylist?: (targetId: string, sourceId: string) => void;\n})",
    content
)

# Destructuring props
content = re.sub(
    r"downloadedSongs \}: \{",
    r"downloadedSongs, onDeletePlaylist, onMergePlaylist }: {",
    content
)

# Component body start
content = re.sub(
    r"  const { deferredPrompt, installPWA } = usePWAInstall\(\);",
    r"""  const { deferredPrompt, installPWA } = usePWAInstall();

  const [contextMenu, setContextMenu] = useState<{ x: number; y: number; playlistId: string } | null>(null);
  const [mergeMenu, setMergeMenu] = useState<{ x: number; y: number; sourcePlaylistId: string } | null>(null);

  useEffect(() => {
    const handleClick = () => {
      setContextMenu(null);
      setMergeMenu(null);
    };
    document.addEventListener('click', handleClick);
    return () => document.removeEventListener('click', handleClick);
  }, []);

  const handleContextMenu = (e: React.MouseEvent, playlistId: string) => {
    e.preventDefault();
    setContextMenu({ x: e.clientX, y: e.clientY, playlistId });
    setMergeMenu(null);
  };""",
    content
)

# Playlist click
content = re.sub(
    r"              onClick=\{\(\) => onCollectionClick\(playlist\)\}\n              className=\"cursor-pointer group\"",
    r"              onClick={() => onCollectionClick(playlist)}\n              onContextMenu={(e) => handleContextMenu(e, playlist.id)}\n              className=\"cursor-pointer group relative\"",
    content
)

# Component end
content = re.sub(
    r"    </div>\n  \);\n\}",
    r"""    </div>

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
  );
}""",
    content
)

with open('src/components/HomeView.tsx', 'w') as f:
    f.write(content)
