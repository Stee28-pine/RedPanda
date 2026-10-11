import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

old_homeview_props = """                <HomeView 
                  onCollectionClick={handleNavigateToAlbum}
                  playlists={playlists}
                  onPlaySong={handlePlaySong}
                  onGenreClick={handleGenreClick}
                  downloadedSongs={downloadedSongs}
                  recentlyPlayedHistory={recentlyPlayed}
                  onDeletePlaylist={(id) => { deletePlaylist(id); setActiveCollection(null); }}
                  onMergePlaylist={(targetId, sourceId) => { mergePlaylists(targetId, sourceId); setActiveCollection(null); }}
                />"""

new_homeview_props = """                <HomeView 
                  onCollectionClick={handleNavigateToAlbum}
                  playlists={playlists}
                  onPlaySong={handlePlaySong}
                  onGenreClick={handleGenreClick}
                  downloadedSongs={downloadedSongs}
                  recentlyPlayedHistory={recentlyPlayed}
                  likedSongs={likedSongs}
                  onDeletePlaylist={(id) => { deletePlaylist(id); setActiveCollection(null); }}
                  onMergePlaylist={(targetId, sourceId) => { mergePlaylists(targetId, sourceId); setActiveCollection(null); }}
                />"""

content = content.replace(old_homeview_props, new_homeview_props)

with open('src/App.tsx', 'w') as f:
    f.write(content)

