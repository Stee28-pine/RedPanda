import re

with open('src/components/HistoryView.tsx', 'r') as f:
    content = f.read()

# 1. Imports
content = content.replace("import React, { useState, useRef } from 'react';", "import React, { useState } from 'react';")

# 2. State
content = content.replace("const [doubleClickedSongId, setDoubleClickedSongId] = useState<string | null>(null);", "const [contextMenuSongId, setContextMenuSongId] = useState<string | null>(null);")
content = content.replace("const clickTimeoutRef = useRef<NodeJS.Timeout | null>(null);", "")
content = content.replace("onClick={() => setDoubleClickedSongId(null)}", "onClick={() => setContextMenuSongId(null)}")

# 3. Click handlers
old_handlers = """                onClick={(e) => {
                  e.stopPropagation();
                  if (clickTimeoutRef.current) {
                    clearTimeout(clickTimeoutRef.current);
                    clickTimeoutRef.current = null;
                  }
                  if (doubleClickedSongId !== song.id) {
                    clickTimeoutRef.current = setTimeout(() => {
                      onPlaySong(song, { songs: recentlyPlayedHistory });
                    }, 250);
                  }
                }}
                onDoubleClick={(e) => {
                  e.stopPropagation();
                  if (clickTimeoutRef.current) {
                    clearTimeout(clickTimeoutRef.current);
                    clickTimeoutRef.current = null;
                  }
                  setDoubleClickedSongId(song.id);
                }}"""

new_handlers = """                onClick={(e) => {
                  e.stopPropagation();
                  if (contextMenuSongId !== song.id) {
                    onPlaySong(song, { songs: recentlyPlayedHistory });
                  } else {
                    setContextMenuSongId(null);
                  }
                }}
                onContextMenu={(e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  setContextMenuSongId(song.id);
                }}"""

content = content.replace(old_handlers, new_handlers)

# 4. Render condition
content = content.replace("doubleClickedSongId === song.id", "contextMenuSongId === song.id")
content = content.replace("setDoubleClickedSongId(null)", "setContextMenuSongId(null)")

with open('src/components/HistoryView.tsx', 'w') as f:
    f.write(content)
print("Patched for right-click")
