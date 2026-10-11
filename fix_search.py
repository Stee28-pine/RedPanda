with open('src/components/SearchView.tsx', 'r') as f:
    content = f.read()

content = content.replace("  onArtistClick, isOfflineMode, downloadedSongs }: { ", "  onArtistClick, isOfflineMode }: { ")

with open('src/components/SearchView.tsx', 'w') as f:
    f.write(content)
