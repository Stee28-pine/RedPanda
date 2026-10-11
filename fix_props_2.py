import re

files = ['src/components/AlbumView.tsx', 'src/components/SearchView.tsx', 'src/components/HomeView.tsx']

for file in files:
    with open(file, 'r') as f:
        content = f.read()

    content = content.replace("onAddToPlaylist isOfflineMode", "onAddToPlaylist, isOfflineMode")
    content = content.replace("onAddToPlaylist  isOfflineMode", "onAddToPlaylist, isOfflineMode")
    content = content.replace("onAddToPlaylist downloadedSongs", "onAddToPlaylist, downloadedSongs")
    content = content.replace("onShare downloadedSongs", "onShare, downloadedSongs")
    content = content.replace("onShare  downloadedSongs", "onShare, downloadedSongs")
    content = content.replace("onShare isOfflineMode", "onShare, isOfflineMode")

    with open(file, 'w') as f:
        f.write(content)
