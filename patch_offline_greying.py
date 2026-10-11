import re

# HomeView
with open('src/components/HomeView.tsx', 'r') as f:
    home = f.read()

home_search = """              <motion.div 
                variants={{ hidden: { opacity: 0, y: 20 }, show: { opacity: 1, y: 0 } }}
                key={song.id}
                className="group flex flex-col gap-3 p-3 hover:bg-white rounded-2xl transition-all cursor-pointer border border-transparent hover:border-gray-100 hover:shadow-sm"
                onClick={(e) => { e.stopPropagation(); onPlaySong?.(song, { songs: recentlyPlayed }); }}
              >"""
home_replace = """              <motion.div 
                variants={{ hidden: { opacity: 0, y: 20 }, show: { opacity: 1, y: 0 } }}
                key={song.id}
                className={`group flex flex-col gap-3 p-3 hover:bg-white rounded-2xl transition-all cursor-pointer border border-transparent hover:border-gray-100 hover:shadow-sm ${isOfflineMode && !downloadedSongs?.some(d => d.id === song.id) ? "opacity-50 grayscale pointer-events-none" : ""}`}
                onClick={(e) => { e.stopPropagation(); onPlaySong?.(song, { songs: recentlyPlayed }); }}
              >"""
home = home.replace(home_search, home_replace)
with open('src/components/HomeView.tsx', 'w') as f:
    f.write(home)

# SearchView
with open('src/components/SearchView.tsx', 'r') as f:
    search_view = f.read()
search_view = search_view.replace("const isActive = nowPlaying?.id === song.id;", "const isActive = nowPlaying?.id === song.id;")
search_search = """                  key={song.id}
                  onClick={() => onPlaySong(song, { songs: searchResults })}
                  onContextMenu={(e) => handleContextMenu(e, song)}
                  className={`group relative flex items-center gap-3 p-2 rounded-xl transition-colors cursor-pointer border border-transparent ${isActive ? 'bg-[#fe5f64]/10 border-[#fe5f64]/20' : 'hover:bg-white hover:shadow-sm hover:border-gray-200'}`}
                >"""
search_replace = """                  key={song.id}
                  onClick={() => onPlaySong(song, { songs: searchResults })}
                  onContextMenu={(e) => handleContextMenu(e, song)}
                  className={`group relative flex items-center gap-3 p-2 rounded-xl transition-colors cursor-pointer border border-transparent ${isActive ? 'bg-[#fe5f64]/10 border-[#fe5f64]/20' : 'hover:bg-white hover:shadow-sm hover:border-gray-200'} ${isOfflineMode && !downloadedSongs?.some(d => d.id === song.id) ? "opacity-50 grayscale pointer-events-none" : ""}`}
                >"""
search_view = search_view.replace(search_search, search_replace)
with open('src/components/SearchView.tsx', 'w') as f:
    f.write(search_view)

