import re

with open('src/hooks/usePlaylists.ts', 'r') as f:
    content = f.read()

content = content.replace("return { playlists: computedPlaylists, createPlaylist, addSongToPlaylist };", "const removeSongFromPlaylist = (playlistId: string, songId: string) => {\n    setPlaylists(prev => prev.map(p => {\n      if (p.id === playlistId) {\n        return { ...p, songs: p.songs.filter(s => s.id !== songId) };\n      }\n      return p;\n    }));\n  };\n\n  return { playlists: computedPlaylists, createPlaylist, addSongToPlaylist, removeSongFromPlaylist };")

with open('src/hooks/usePlaylists.ts', 'w') as f:
    f.write(content)
