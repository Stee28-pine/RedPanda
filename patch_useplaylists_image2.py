import re

with open('src/hooks/usePlaylists.ts', 'r') as f:
    content = f.read()

search = """  const computedPlaylists = playlists;"""

replace = """  const computedPlaylists = playlists.map(p => {
    if (p.coverUrl === 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?w=400&q=80') {
        const idHash = p.id.split('_')[1] || '0';
        const idx = parseInt(idHash) % abstractImages.length;
        return { ...p, coverUrl: `https://images.unsplash.com/photo-${abstractImages[idx]}?w=400&q=80` };
    }
    return p;
  });"""

content = content.replace(search, replace)

with open('src/hooks/usePlaylists.ts', 'w') as f:
    f.write(content)
