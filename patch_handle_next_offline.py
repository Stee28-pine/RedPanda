import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

search = """          if (idx + 1 >= queue.length - 1) {
             const similar = SONGS.filter(s => s.genre === queue[idx + 1].genre && !queue.some(q => q.id === s.id)).slice(0, 5);"""

replace = """          if (idx + 1 >= queue.length - 1) {
             const similar = SONGS.filter(s => s.genre === queue[idx + 1].genre && !queue.some(q => q.id === s.id) && (!isOfflineMode || downloadedSongs.some(d => d.id === s.id))).slice(0, 5);"""

content = content.replace(search, replace)

search_2 = """          const similar = SONGS.filter(s => s.genre === nowPlaying.genre && !queue.some(q => q.id === s.id)).slice(0, 5);"""
replace_2 = """          const similar = SONGS.filter(s => s.genre === nowPlaying.genre && !queue.some(q => q.id === s.id) && (!isOfflineMode || downloadedSongs.some(d => d.id === s.id))).slice(0, 5);"""
content = content.replace(search_2, replace_2)

with open('src/App.tsx', 'w') as f:
    f.write(content)
