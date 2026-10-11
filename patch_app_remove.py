import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace("const { playlists, createPlaylist, addSongToPlaylist } = usePlaylists();", "const { playlists, createPlaylist, addSongToPlaylist, removeSongFromPlaylist } = usePlaylists();")

album_search = """                  <AlbumView 
                    collection={activeCollection} 
                    onPlaySong={handlePlaySong} 
                    nowPlaying={nowPlaying} 
                    isPlaying={isPlaying} 
                    likedSongs={likedSongs}
                    downloadedSongs={downloadedSongs}
                    onToggleLike={toggleLike}
                    onToggleDownload={toggleDownload}
                    onAddToQueue={handleAddToQueue}
                  onPlayNext={handlePlayNext}
                  onAddToPlaylist={setPlaylistModalSong}  
                  onShare={handleShare}                  
                  isOfflineMode={isOfflineMode}
                  />"""

album_replace = """                  <AlbumView 
                    collection={activeCollection} 
                    onPlaySong={handlePlaySong} 
                    nowPlaying={nowPlaying} 
                    isPlaying={isPlaying} 
                    likedSongs={likedSongs}
                    downloadedSongs={downloadedSongs}
                    onToggleLike={toggleLike}
                    onToggleDownload={toggleDownload}
                    onAddToQueue={handleAddToQueue}
                  onPlayNext={handlePlayNext}
                  onAddToPlaylist={setPlaylistModalSong}
                  onRemoveFromPlaylist={
                    activeCollection && playlists.some(p => p.id === activeCollection.id) 
                      ? (song) => {
                          removeSongFromPlaylist(activeCollection.id, song.id);
                          // Also update activeCollection so the UI reflects it immediately
                          setActiveCollection(prev => prev ? { ...prev, songs: prev.songs.filter(s => s.id !== song.id) } : null);
                        }
                      : undefined
                  }
                  onShare={handleShare}                  
                  isOfflineMode={isOfflineMode}
                  />"""

content = content.replace(album_search, album_replace)

with open('src/App.tsx', 'w') as f:
    f.write(content)
