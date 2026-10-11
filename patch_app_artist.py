import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

search = """                  artistName={activeArtist}
                  popularSongs={SONGS.filter(s => s.artist === activeArtist)}
                  topAlbums={ALBUMS.filter(a => a.subtitle === activeArtist || a.songs.some(s => s.artist === activeArtist))}"""

replace = """                  artistName={activeArtist}
                  popularSongs={SONGS.filter(s => s.artist.includes(activeArtist))}
                  topAlbums={ALBUMS.filter(a => (a.subtitle && a.subtitle.includes(activeArtist)) || a.songs.some(s => s.artist.includes(activeArtist)))}"""

content = content.replace(search, replace)

with open('src/App.tsx', 'w') as f:
    f.write(content)
