import re

with open('src/components/Sidebar.tsx', 'r') as f:
    content = f.read()

old_playlist_item = """          {playlists?.map(p => (
            <button key={p.id} onClick={() => onNavigatePlaylist?.(p)} className={`w-full flex items-center gap-3 px-3 py-1.5 rounded-lg transition-colors ${activeCollectionId === p.id ? 'bg-gray-200/80 text-gray-900' : 'text-gray-700 hover:bg-gray-300/50'}`}>
              <div className="w-8 h-8 rounded bg-gray-200/80 flex items-center justify-center text-gray-500">
                <Music size={14} />
              </div>
              <div className="text-left flex-1 min-w-0">
                <div className="text-[13px] font-semibold truncate leading-tight">{p.title}</div>
              </div>
            </button>
          ))}"""

new_playlist_item = """          {playlists?.map(p => (
            <button key={p.id} onClick={() => onNavigatePlaylist?.(p)} className={`w-full flex items-center gap-3 px-3 py-1.5 rounded-lg transition-colors ${activeCollectionId === p.id ? 'bg-gray-200/80 text-gray-900' : 'text-gray-700 hover:bg-gray-300/50'}`}>
              {p.songs && p.songs.length > 0 ? (
                 <img src={p.coverUrl} alt={p.title} className="w-8 h-8 rounded object-cover shadow-sm" />
              ) : (
                 <div className="w-8 h-8 rounded bg-gray-200/80 flex items-center justify-center text-gray-500">
                   <Music size={14} />
                 </div>
              )}
              <div className="text-left flex-1 min-w-0">
                <div className="text-[13px] font-semibold truncate leading-tight">{p.title}</div>
              </div>
            </button>
          ))}"""

content = content.replace(old_playlist_item, new_playlist_item)

with open('src/components/Sidebar.tsx', 'w') as f:
    f.write(content)
