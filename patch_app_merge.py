import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

search = """                    onDeletePlaylist={(id) => { deletePlaylist(id); setActiveCollection(null); }}
                    onMergePlaylist={mergePlaylists}"""

replace = """                    onDeletePlaylist={(id) => { deletePlaylist(id); setActiveCollection(null); }}
                    onMergePlaylist={(targetId, sourceId) => { mergePlaylists(targetId, sourceId); setActiveCollection(null); }}"""

content = content.replace(search, replace)

with open('src/App.tsx', 'w') as f:
    f.write(content)
