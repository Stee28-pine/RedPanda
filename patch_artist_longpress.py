import re

with open('src/components/ArtistView.tsx', 'r') as f:
    content = f.read()

content = content.replace('onClick={() => onPlaySong(song, { songs: artist.popularSongs })}\n                  onContextMenu={(e) => handleContextMenu(e, song)}', 
'''onClick={() => onPlaySong(song, { songs: artist.popularSongs })}
                  onContextMenu={(e) => handleContextMenu(e, song)}
                  onTouchStart={(e) => {
                    const timer = setTimeout(() => {
                      const touch = e.touches[0];
                      handleContextMenu({ 
                        preventDefault: () => {}, 
                        clientX: touch.clientX, 
                        clientY: touch.clientY 
                      } as any, song);
                    }, 500);
                    e.currentTarget.dataset.longPressTimer = timer.toString();
                  }}
                  onTouchEnd={(e) => {
                    const timer = e.currentTarget.dataset.longPressTimer;
                    if (timer) clearTimeout(parseInt(timer));
                  }}
                  onTouchCancel={(e) => {
                    const timer = e.currentTarget.dataset.longPressTimer;
                    if (timer) clearTimeout(parseInt(timer));
                  }}
                  onTouchMove={(e) => {
                    const timer = e.currentTarget.dataset.longPressTimer;
                    if (timer) clearTimeout(parseInt(timer));
                  }}''')

with open('src/components/ArtistView.tsx', 'w') as f:
    f.write(content)

with open('src/components/SearchView.tsx', 'r') as f:
    content = f.read()

content = content.replace('onClick={() => onPlaySong(song, { songs: results.songs })}\n                  onContextMenu={(e) => handleContextMenu(e, song)}', 
'''onClick={() => onPlaySong(song, { songs: results.songs })}
                  onContextMenu={(e) => handleContextMenu(e, song)}
                  onTouchStart={(e) => {
                    const timer = setTimeout(() => {
                      const touch = e.touches[0];
                      handleContextMenu({ 
                        preventDefault: () => {}, 
                        clientX: touch.clientX, 
                        clientY: touch.clientY 
                      } as any, song);
                    }, 500);
                    e.currentTarget.dataset.longPressTimer = timer.toString();
                  }}
                  onTouchEnd={(e) => {
                    const timer = e.currentTarget.dataset.longPressTimer;
                    if (timer) clearTimeout(parseInt(timer));
                  }}
                  onTouchCancel={(e) => {
                    const timer = e.currentTarget.dataset.longPressTimer;
                    if (timer) clearTimeout(parseInt(timer));
                  }}
                  onTouchMove={(e) => {
                    const timer = e.currentTarget.dataset.longPressTimer;
                    if (timer) clearTimeout(parseInt(timer));
                  }}''')

with open('src/components/SearchView.tsx', 'w') as f:
    f.write(content)

print("Artist/Search long press patched")
