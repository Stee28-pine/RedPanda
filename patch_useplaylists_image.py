import re

with open('src/hooks/usePlaylists.ts', 'r') as f:
    content = f.read()

search = """  const createPlaylist = (name: string) => {
    const newPlaylist: Collection = {
      id: `playlist_${Date.now()}`,
      type: 'playlist',
      title: name,
      subtitle: 'My Playlist',
      coverUrl: 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?w=400&q=80',
      songs: []
    };"""

replace = """  const abstractImages = [
    '1614613535308-eb5fbd3d2c17',
    '1557672172-298e090bd0f1',
    '1550684848-fac1c5b4e853',
    '1493246507139-91e8fad9978e',
    '1579546929518-9e396f3cc809',
    '1618005182384-a83a8bd57fbe'
  ];

  const createPlaylist = (name: string) => {
    const randomImage = abstractImages[Math.floor(Math.random() * abstractImages.length)];
    const newPlaylist: Collection = {
      id: `playlist_${Date.now()}`,
      type: 'playlist',
      title: name,
      subtitle: 'My Playlist',
      coverUrl: `https://images.unsplash.com/photo-${randomImage}?w=400&q=80`,
      songs: []
    };"""

content = content.replace(search, replace)

# Update computedPlaylists so it doesn't override the coverUrl with the first song's coverUrl, 
# because that makes all playlists look like their first song which isn't "its own real image".
content = content.replace("const computedPlaylists = playlists.map(p => {\n     if (p.songs && p.songs.length > 0) {\n        return { ...p, coverUrl: p.songs[0].coverUrl };\n     }\n     return p;\n  });", "const computedPlaylists = playlists;")

with open('src/hooks/usePlaylists.ts', 'w') as f:
    f.write(content)
