import re
views = ['src/components/AlbumView.tsx', 'src/components/ArtistView.tsx', 'src/components/SearchView.tsx']

for view in views:
    with open(view, 'r') as f:
        content = f.read()

    style_search = "style={{ top: contextMenu.y, left: contextMenu.x }}"
    style_replace = "style={{ top: Math.min(contextMenu.y, typeof window !== 'undefined' ? window.innerHeight - 300 : contextMenu.y), left: Math.min(contextMenu.x, typeof window !== 'undefined' ? window.innerWidth - 200 : contextMenu.x) }}"
    
    content = content.replace(style_search, style_replace)

    with open(view, 'w') as f:
        f.write(content)
