import re

with open('src/components/HomeView.tsx', 'r') as f:
    content = f.read()

search = """              className="cursor-pointer group"
              onClick={() => onCollectionClick(playlist)}"""

replace = """              className="cursor-pointer group relative"
              onClick={() => onCollectionClick(playlist)}
              onContextMenu={(e) => handleContextMenu(e, playlist.id)}
              onDoubleClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                handleContextMenu(e, playlist.id);
              }}"""

content = content.replace(search, replace)

with open('src/components/HomeView.tsx', 'w') as f:
    f.write(content)

with open('src/components/Sidebar.tsx', 'r') as f:
    content = f.read()

search_sidebar = """            <button key={p.id} onClick={() => onNavigatePlaylist?.(p)} className={`w-full flex items-center gap-3 px-3 py-1.5 rounded-lg transition-colors ${activeCollectionId === p.id ? 'bg-gray-200/80 text-gray-900' : 'text-gray-700 hover:bg-gray-300/50'}`}>"""

replace_sidebar = """            <button 
              key={p.id} 
              onClick={() => onNavigatePlaylist?.(p)} 
              onContextMenu={(e) => handleContextMenu(e, p.id)}
              onDoubleClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                handleContextMenu(e, p.id);
              }}
              className={`w-full flex items-center gap-3 px-3 py-1.5 rounded-lg transition-colors ${activeCollectionId === p.id ? 'bg-gray-200/80 text-gray-900' : 'text-gray-700 hover:bg-gray-300/50'}`}
            >"""

content = content.replace(search_sidebar, replace_sidebar)

with open('src/components/Sidebar.tsx', 'w') as f:
    f.write(content)
