import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

pattern = re.compile(r'(<HomeView[^>]*downloadedSongs=\{downloadedSongs\}\s*/>)', re.DOTALL)

new_str = """<HomeView 
                  onCollectionClick={handleNavigateToAlbum}
                  playlists={playlists}
                  onPlaySong={handlePlaySong}
                  onGenreClick={handleGenreClick}
                  downloadedSongs={downloadedSongs}
                  recentlyPlayedHistory={recentlyPlayed}
                  onDeletePlaylist={(id) => { deletePlaylist(id); setActiveCollection(null); }}
                  onMergePlaylist={(targetId, sourceId) => { mergePlaylists(targetId, sourceId); setActiveCollection(null); }}
                />"""

if pattern.search(content):
    content = pattern.sub(new_str, content)
    with open('src/App.tsx', 'w') as f:
        f.write(content)
    print("Patched successfully")
else:
    print("Could not find pattern in App.tsx")
