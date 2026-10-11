with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace("useState<'home' | 'album' | 'search' | 'artist'>('home')", "useState<'home' | 'album' | 'search' | 'artist' | 'stats'>('home')")

with open('src/App.tsx', 'w') as f:
    f.write(content)
