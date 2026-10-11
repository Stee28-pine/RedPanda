import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Add initial state for recentlyPlayed
old_rp = '  const [recentlyPlayed, setRecentlyPlayed] = useState<Song[]>([]);'
new_rp = '''  const [recentlyPlayed, setRecentlyPlayed] = useState<Song[]>(() => {
    try {
      const saved = localStorage.getItem('ais_recently_played');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  useEffect(() => {
    localStorage.setItem('ais_recently_played', JSON.stringify(recentlyPlayed));
  }, [recentlyPlayed]);'''

content = content.replace(old_rp, new_rp)

# Add recentlyPlayed to HomeView props
old_homeview = '''                <HomeView 
                  onCollectionClick={handleNavigateToAlbum}
                  
                  playlists={playlists}
                  onPlaySong={handlePlaySong}
                  onGenreClick={handleGenreClick}
                  
                  downloadedSongs={downloadedSongs}
                />'''
new_homeview = '''                <HomeView 
                  onCollectionClick={handleNavigateToAlbum}
                  playlists={playlists}
                  onPlaySong={handlePlaySong}
                  onGenreClick={handleGenreClick}
                  downloadedSongs={downloadedSongs}
                  recentlyPlayedHistory={recentlyPlayed}
                />'''

content = content.replace(old_homeview, new_homeview)

with open('src/App.tsx', 'w') as f:
    f.write(content)
