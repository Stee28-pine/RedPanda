import re

with open('src/components/Sidebar.tsx', 'r') as f:
    content = f.read()

old_destruct = """export function Sidebar({ 
  onNavigateHome, 
  currentView,
  onNavigateLikedSongs,
  likedSongs = [],
  activeCollectionId,
  isCollapsed = false,
  nowPlaying,
}: {"""

new_destruct = """export function Sidebar({ 
  onNavigateHome, 
  currentView,
  onNavigateLikedSongs,
  likedSongs = [],
  activeCollectionId,
  isCollapsed = false,
  nowPlaying,
  playlists,
  onNavigatePlaylist,
  onCreatePlaylist,
}: {"""

content = content.replace(old_destruct, new_destruct)

with open('src/components/Sidebar.tsx', 'w') as f:
    f.write(content)
