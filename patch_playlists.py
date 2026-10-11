with open('src/hooks/usePlaylists.ts', 'r') as f:
    content = f.read()

search = """  const removeSongFromPlaylist = (playlistId: string, songId: string) => {
    setPlaylists(prev => prev.map(p => {
      if (p.id === playlistId) {
        return { ...p, songs: p.songs.filter(s => s.id !== songId) };
      }
      return p;
    }));
  };

  return { playlists: computedPlaylists, createPlaylist, addSongToPlaylist, removeSongFromPlaylist };
}"""

replace = """  const removeSongFromPlaylist = (playlistId: string, songId: string) => {
    setPlaylists(prev => prev.map(p => {
      if (p.id === playlistId) {
        return { ...p, songs: p.songs.filter(s => s.id !== songId) };
      }
      return p;
    }));
  };

  const deletePlaylist = (playlistId: string) => {
    setPlaylists(prev => prev.filter(p => p.id !== playlistId));
  };

  const mergePlaylists = (targetId: string, sourceId: string) => {
    setPlaylists(prev => {
      const source = prev.find(p => p.id === sourceId);
      if (!source) return prev;
      
      return prev.map(p => {
        if (p.id === targetId) {
          const existingIds = new Set(p.songs.map(s => s.id));
          const newSongs = source.songs.filter(s => !existingIds.has(s.id));
          return { ...p, songs: [...p.songs, ...newSongs] };
        }
        return p;
      }).filter(p => p.id !== sourceId);
    });
  };

  return { playlists: computedPlaylists, createPlaylist, addSongToPlaylist, removeSongFromPlaylist, deletePlaylist, mergePlaylists };
}"""

content = content.replace(search, replace)

with open('src/hooks/usePlaylists.ts', 'w') as f:
    f.write(content)
