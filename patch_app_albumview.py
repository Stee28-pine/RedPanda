import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Add to AlbumView props
search = """                    onToggleDownload={toggleDownload}
                    onAddToQueue={handleAddToQueue}
                    onPlayNext={handlePlayNext}
                    onShare={(item) => console.log('Share', item)}"""
replace = """                    onToggleDownload={toggleDownload}
                    onAddToQueue={handleAddToQueue}
                    onPlayNext={handlePlayNext}
                    onShare={(item) => console.log('Share', item)}
                    playlists={playlists}
                    onDeletePlaylist={deletePlaylist}
                    onMergePlaylist={mergePlaylists}"""

content = content.replace(search, replace)

# Handle the case where they might have added onAddToPlaylist or something
# Let's just use regex
content = re.sub(
    r"(<AlbumView[\s\S]*?onShare=\{.*?\})",
    r"\1\n                    playlists={playlists}\n                    onDeletePlaylist={(id) => { deletePlaylist(id); setActiveCollection(null); }}\n                    onMergePlaylist={mergePlaylists}",
    content
)

with open('src/App.tsx', 'w') as f:
    f.write(content)
