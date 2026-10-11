import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Fix usePlaylists destructuring
content = re.sub(
    r"const \{ playlists, createPlaylist, addSongToPlaylist, removeSongFromPlaylist \} = usePlaylists\(\);",
    r"const { playlists, createPlaylist, addSongToPlaylist, removeSongFromPlaylist, deletePlaylist, mergePlaylists } = usePlaylists();",
    content
)

# Add to Sidebar props
content = re.sub(
    r"          playlists=\{playlists\}\n          onNavigatePlaylist=\{handleNavigatePlaylist\}\n          onCreatePlaylist=\{handleCreatePlaylist\}",
    r"          playlists={playlists}\n          onNavigatePlaylist={handleNavigatePlaylist}\n          onCreatePlaylist={handleCreatePlaylist}\n          onDeletePlaylist={deletePlaylist}\n          onMergePlaylist={mergePlaylists}",
    content
)

# Add to HomeView props
content = re.sub(
    r"                  playlists=\{playlists\}\n                  downloadedSongs=\{downloadedSongs\}\n                  onGenreClick=\{handleGenreClick\}\n                />",
    r"                  playlists={playlists}\n                  downloadedSongs={downloadedSongs}\n                  onGenreClick={handleGenreClick}\n                  onDeletePlaylist={deletePlaylist}\n                  onMergePlaylist={mergePlaylists}\n                />",
    content
)

with open('src/App.tsx', 'w') as f:
    f.write(content)
