import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

search = """                  <SearchView 
                    query={searchQuery} 
                    results={searchResults} 
                    isLoading={isSearchLoading} 
                    onPlaySong={handlePlaySong}
                    nowPlaying={nowPlaying}
                    isPlaying={isPlaying}
                    likedSongs={likedSongs}
                    downloadedSongs={downloadedSongs}
                    onToggleLike={toggleLike}
                    onToggleDownload={toggleDownload}
                    onAddToQueue={handleAddToQueue}
                    onPlayNext={handlePlayNext}
                    onShare={handleShare}
                    onAddToPlaylist={setPlaylistModalSong}
                    isOfflineMode={isOfflineMode}
                  />"""

replace = """                  <SearchView 
                    query={searchQuery} 
                    results={searchResults} 
                    isLoading={isSearchLoading} 
                    onPlaySong={handlePlaySong}
                    nowPlaying={nowPlaying}
                    isPlaying={isPlaying}
                    likedSongs={likedSongs}
                    downloadedSongs={downloadedSongs}
                    onToggleLike={toggleLike}
                    onToggleDownload={toggleDownload}
                    onAddToQueue={handleAddToQueue}
                    onPlayNext={handlePlayNext}
                    onShare={handleShare}
                    onAddToPlaylist={setPlaylistModalSong}
                    isOfflineMode={isOfflineMode}
                    onSearchSelect={(q) => setSearchQuery(q)}
                  />"""

content = content.replace(search, replace)

with open('src/App.tsx', 'w') as f:
    f.write(content)
