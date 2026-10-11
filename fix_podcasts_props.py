import re

with open('src/components/PodcastsView.tsx', 'r') as f:
    content = f.read()

old_props = """export function PodcastsView({ 
  searchQuery, 
  onSearchChange, 
  onPlaySong, 
  nowPlaying, 
  isPlaying, 
  likedSongs, 
  onToggleLike
}: {"""

new_props = """export function PodcastsView({ 
  searchQuery, 
  onSearchChange, 
  onPlaySong, 
  nowPlaying, 
  isPlaying, 
  likedSongs, 
  onToggleLike,
  currentTime,
  bookmarks,
  onAddBookmark,
  onRemoveBookmark,
  onSeekToTime
}: {"""

if old_props in content:
    content = content.replace(old_props, new_props)
    with open('src/components/PodcastsView.tsx', 'w') as f:
        f.write(content)
    print("Patched successfully")
else:
    print("Could not find old_props")
