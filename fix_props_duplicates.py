import re
views = ['src/components/AlbumView.tsx', 'src/components/ArtistView.tsx', 'src/components/SearchView.tsx']

for view in views:
    with open(view, 'r') as f:
        content = f.read()

    content = content.replace('  downloadedSongs?: Song[];\n', '')

    with open(view, 'w') as f:
        f.write(content)
