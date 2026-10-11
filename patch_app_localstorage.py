import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

search = """  // Local persistence
  useEffect(() => {
    if (typeof window !== 'undefined') {
      try {
        const liked = localStorage.getItem('ais_liked_songs');
        if (liked) setLikedSongs(JSON.parse(liked));
        
        const recent = localStorage.getItem('ais_recently_played');
        if (recent) setRecentlyPlayed(JSON.parse(recent));"""

replace = """  // Local persistence
  useEffect(() => {
    if (typeof window !== 'undefined') {
      try {
        const liked = localStorage.getItem('ais_liked_songs');
        if (liked) setLikedSongs(JSON.parse(liked));
        
        const downloaded = localStorage.getItem('ais_downloaded_songs');
        if (downloaded) setDownloadedSongs(JSON.parse(downloaded));
        
        const recent = localStorage.getItem('ais_recently_played');
        if (recent) setRecentlyPlayed(JSON.parse(recent));"""

content = content.replace(search, replace)
with open('src/App.tsx', 'w') as f:
    f.write(content)

