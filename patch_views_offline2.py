import glob
import re

views = ['src/components/AlbumView.tsx', 'src/components/ArtistView.tsx', 'src/components/SearchView.tsx']

for view in views:
    with open(view, 'r') as f:
        content = f.read()
    
    # We want to find:
    # key={song.id}
    # ...
    # className="something"
    # Or className={`something`}
    
    def repl(m):
        prefix = m.group(1)
        classname = m.group(2)
        suffix = m.group(3)
        if classname.startswith('"') and classname.endswith('"'):
            classes = classname[1:-1]
        elif classname.startswith('{`') and classname.endswith('`}'):
            classes = classname[2:-2]
        else:
            return m.group(0) # don't touch if weird
            
        return f'{prefix}className={{`{classes} ${{isOfflineMode && !downloadedSongs?.some(d => d.id === song.id) ? "opacity-50 grayscale pointer-events-none" : ""}}`}}{suffix}'
    
    content = re.sub(r'(key=\{song\.id\}[\s\S]*?)className=(\"[^\"]+\"|\{`[^`]+`\})([\s\S]*?\>)', repl, content)

    with open(view, 'w') as f:
        f.write(content)
