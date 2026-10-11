import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# 1. Remove useSettings import and hook
content = re.sub(r"import \{ useSettings \} from '\.\/hooks\/useSettings';\n?", "", content)
content = re.sub(r"  const \{ isOfflineMode, setIsOfflineMode \} = useSettings\(\);\n?", "", content)

# 2. Remove isOfflineMode logic from handlePlaySong
search_play = """    if (isOfflineMode && !downloadedSongs.some(d => d.id === song.id)) {
       showToast('Song not available offline');
       return;
    }"""
content = content.replace(search_play, "")

# 3. Clean up handleNext
search_next1 = "const firstAvailable = queue.find(q => !isOfflineMode || downloadedSongs.some(d => d.id === q.id));"
replace_next1 = "const firstAvailable = queue[0];"
content = content.replace(search_next1, replace_next1)

search_next2 = "const similar = SONGS.filter(s => s.genre === queue[idx + 1].genre && !queue.some(q => q.id === s.id) && (!isOfflineMode || downloadedSongs.some(d => d.id === s.id))).slice(0, 5);"
replace_next2 = "const similar = SONGS.filter(s => s.genre === queue[idx + 1].genre && !queue.some(q => q.id === s.id)).slice(0, 5);"
content = content.replace(search_next2, replace_next2)

search_next3 = "const similar = SONGS.filter(s => s.genre === nowPlaying.genre && !queue.some(q => q.id === s.id) && (!isOfflineMode || downloadedSongs.some(d => d.id === s.id))).slice(0, 5);"
replace_next3 = "const similar = SONGS.filter(s => s.genre === nowPlaying.genre && !queue.some(q => q.id === s.id)).slice(0, 5);"
content = content.replace(search_next3, replace_next3)

# 4. Remove prop passing in App.tsx
content = re.sub(r"isOfflineMode=\{isOfflineMode\}\s*", "", content)
content = re.sub(r"onToggleOfflineMode=\{.*?\}\s*", "", content)

with open('src/App.tsx', 'w') as f:
    f.write(content)
