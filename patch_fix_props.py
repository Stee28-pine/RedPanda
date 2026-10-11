import re

views = ['src/components/HomeView.tsx', 'src/components/AlbumView.tsx', 'src/components/ArtistView.tsx', 'src/components/SearchView.tsx']

for view in views:
    with open(view, 'r') as f:
        content = f.read()

    # The issue is `  onPlaySong?: (song: Song, context: { songs: Song[]   isOfflineMode?: boolean;\n  downloadedSongs?: Song[];\n}) => void;`
    content = content.replace("  isOfflineMode?: boolean;\n  downloadedSongs?: Song[];\n}) => void;", "}) => void;\n  isOfflineMode?: boolean;\n  downloadedSongs?: Song[];")
    
    # Another issue `  onShare: (item: { type: 'song' | 'album' | 'artist', id: string, name: string   isOfflineMode?: boolean;\n  downloadedSongs?: Song[];\n}) => void;`
    content = content.replace("  isOfflineMode?: boolean;\n  downloadedSongs?: Song[];\n}) => void;\n  onArtistClick", "}) => void;\n  isOfflineMode?: boolean;\n  downloadedSongs?: Song[];\n  onArtistClick")
    
    with open(view, 'w') as f:
        f.write(content)
