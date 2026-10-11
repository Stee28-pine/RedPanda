import re

with open('src/components/HomeView.tsx', 'r') as f:
    content = f.read()

old_signature = """export function HomeView({ 
  onCollectionClick, 
  playlists = [],
  onPlaySong,
  onGenreClick,
  downloadedSongs,
  onDeletePlaylist, 
  onMergePlaylist,
  recentlyPlayedHistory = []
}: {"""

new_signature = """export function HomeView({ 
  onCollectionClick, 
  playlists = [],
  onPlaySong,
  onGenreClick,
  downloadedSongs,
  onDeletePlaylist, 
  onMergePlaylist,
  recentlyPlayedHistory = [],
  likedSongs = []
}: {"""

content = content.replace(old_signature, new_signature)

with open('src/components/HomeView.tsx', 'w') as f:
    f.write(content)

