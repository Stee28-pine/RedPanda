import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

play_old = """  const handlePlaySong = (song: Song, context?: { songs: Song[] } | Collection) => {
    setNowPlaying(song);"""
    
play_new = """  const handlePlaySong = (song: Song, context?: { songs: Song[] } | Collection) => {
    if (isOfflineMode && !downloadedSongs.some(d => d.id === song.id)) {
       showToast('Song not available offline');
       return;
    }
    setNowPlaying(song);"""
    
content = content.replace(play_old, play_new)

with open('src/App.tsx', 'w') as f:
    f.write(content)
