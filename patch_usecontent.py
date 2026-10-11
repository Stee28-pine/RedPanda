import re

with open('src/hooks/useContent.ts', 'r') as f:
    content = f.read()

# Fix recently played state type
content = content.replace("const [recentlyPlayed, setRecentlyPlayed] = useState<Collection[]>(localRecentlyPlayed);", "const [recentlyPlayed, setRecentlyPlayed] = useState<Song[]>(localSongs.slice(0, 10));")

# Fix what we set it to
content = content.replace("setRecentlyPlayed(topAlbums.slice(10, 15));", "setRecentlyPlayed(topSongs.slice(15, 25));")

with open('src/hooks/useContent.ts', 'w') as f:
    f.write(content)
