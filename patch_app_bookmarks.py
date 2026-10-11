import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Add useBookmarks import
import_pattern = "import { useSearch } from './hooks/useSearch';"
new_import = "import { useBookmarks } from './hooks/useBookmarks';\nimport { useSearch } from './hooks/useSearch';"
content = content.replace(import_pattern, new_import)

# Add useBookmarks call
hook_pattern = "const { stats, recordPlay } = useListeningStats();"
new_hook = "const { stats, recordPlay } = useListeningStats();\n  const { bookmarks, addBookmark, removeBookmark } = useBookmarks();"
content = content.replace(hook_pattern, new_hook)

# Add handleSeekToTime
seek_pattern = "const handlePlaySong = (song: Song, context?: { songs: Song[] } | Collection) => {"
new_seek = """  const handleSeekToTime = (time: number) => {
    if (playerRef.current) {
      playerRef.current.seekTo(time, 'seconds');
    }
    setCurrentPlaybackTime(time);
  };

  const handlePlaySong = (song: Song, context?: { songs: Song[] } | Collection) => {"""
content = content.replace(seek_pattern, new_seek)

# Update PodcastsView props
podcasts_view = """                <PodcastsView 
                  searchQuery={searchQuery}
                  onSearchChange={handleSearchChange}
                  onPlaySong={handlePlaySong} 
                  nowPlaying={nowPlaying} 
                  isPlaying={isPlaying} 
                  likedSongs={likedSongs}
                  onToggleLike={toggleLike}
                />"""

new_podcasts_view = """                <PodcastsView 
                  searchQuery={searchQuery}
                  onSearchChange={handleSearchChange}
                  onPlaySong={handlePlaySong} 
                  nowPlaying={nowPlaying} 
                  isPlaying={isPlaying} 
                  likedSongs={likedSongs}
                  onToggleLike={toggleLike}
                  currentTime={currentPlaybackTime}
                  bookmarks={bookmarks}
                  onAddBookmark={addBookmark}
                  onRemoveBookmark={removeBookmark}
                  onSeekToTime={handleSeekToTime}
                />"""
content = content.replace(podcasts_view, new_podcasts_view)

# Update Sidebar props
sidebar = """          onNavigateLikedSongs={handleNavigateLikedSongs}
          likedSongs={likedSongs}
          activeCollectionId={activeCollection?.id}
          isCollapsed={isSidebarCollapsed}
          nowPlaying={nowPlaying}
          playlists={playlists}
          onDeletePlaylist={(id) => { deletePlaylist(id); if (activeCollection?.id === id) setActiveCollection(null); }}
          onMergePlaylist={(targetId, sourceId) => { mergePlaylists(targetId, sourceId); if (activeCollection?.id === sourceId) setActiveCollection(null); }}
        />"""

new_sidebar = """          onNavigateLikedSongs={handleNavigateLikedSongs}
          likedSongs={likedSongs}
          activeCollectionId={activeCollection?.id}
          isCollapsed={isSidebarCollapsed}
          nowPlaying={nowPlaying}
          playlists={playlists}
          bookmarks={bookmarks}
          onPlaySong={handlePlaySong}
          onSeekToTime={handleSeekToTime}
          onRemoveBookmark={removeBookmark}
          onDeletePlaylist={(id) => { deletePlaylist(id); if (activeCollection?.id === id) setActiveCollection(null); }}
          onMergePlaylist={(targetId, sourceId) => { mergePlaylists(targetId, sourceId); if (activeCollection?.id === sourceId) setActiveCollection(null); }}
        />"""
content = content.replace(sidebar, new_sidebar)


with open('src/App.tsx', 'w') as f:
    f.write(content)
print("Patched App.tsx")

