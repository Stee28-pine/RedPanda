import re

with open('src/components/HistoryView.tsx', 'r') as f:
    content = f.read()

old_click = """                onClick={(e) => {
                  if (doubleClickedSongId !== song.id) {
                    onPlaySong(song, { songs: recentlyPlayedHistory });
                  }
                }}
                onDoubleClick={(e) => {
                  e.stopPropagation();
                  setDoubleClickedSongId(song.id);
                }}"""

new_click = """                onClick={(e) => {
                  e.stopPropagation();
                  if (doubleClickedSongId !== song.id) {
                    onPlaySong(song, { songs: recentlyPlayedHistory });
                  }
                }}
                onDoubleClick={(e) => {
                  e.stopPropagation();
                  setDoubleClickedSongId(song.id);
                }}"""

if old_click in content:
    content = content.replace(old_click, new_click)
    with open('src/components/HistoryView.tsx', 'w') as f:
        f.write(content)
    print("Patched click handlers")
else:
    print("Could not find click handlers")
