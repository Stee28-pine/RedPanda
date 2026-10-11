import re
import glob

views = ['src/components/HomeView.tsx', 'src/components/AlbumView.tsx', 'src/components/ArtistView.tsx', 'src/components/SearchView.tsx']

for view in views:
    with open(view, 'r') as f:
        content = f.read()
    
    # Just add to the prop destructuring and interface
    if 'isOfflineMode' not in content:
        # Destructuring
        content = re.sub(r'(export function \w+\(.*?)(\}: \{)', r'\1, isOfflineMode, downloadedSongs \2', content, flags=re.DOTALL)
        
        # Interface
        content = re.sub(r'(\}: \{.*?)(?=\})', r'\1  isOfflineMode?: boolean;\n  downloadedSongs?: Song[];\n', content, flags=re.DOTALL)
        
        with open(view, 'w') as f:
            f.write(content)
