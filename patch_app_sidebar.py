import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

pattern = re.compile(r'(<Sidebar.*?playlists=\{playlists\})', re.DOTALL)

new_str = r'\1\n          onDeletePlaylist={(id) => { deletePlaylist(id); if (activeCollection?.id === id) setActiveCollection(null); }}\n          onMergePlaylist={(targetId, sourceId) => { mergePlaylists(targetId, sourceId); if (activeCollection?.id === sourceId) setActiveCollection(null); }}'

if pattern.search(content):
    content = pattern.sub(new_str, content)
    with open('src/App.tsx', 'w') as f:
        f.write(content)
    print("Patched successfully")
else:
    print("Could not find pattern in App.tsx")
