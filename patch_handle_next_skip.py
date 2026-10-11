import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

search = """        if (idx < queue.length - 1) {
          setNowPlaying(queue[idx + 1]);
          setIsPlaying(true);
          
          // Smart Queue logic: if 1 track left after this or it's the last track"""

replace = """        if (idx < queue.length - 1) {
          let nextIdx = idx + 1;
          if (isOfflineMode) {
             while(nextIdx < queue.length && !downloadedSongs.some(d => d.id === queue[nextIdx].id)) {
                nextIdx++;
             }
          }
          if (nextIdx < queue.length) {
            setNowPlaying(queue[nextIdx]);
            setIsPlaying(true);
          } else {
             // We reached the end due to offline skipping
             if (repeatMode === 'all') {
                const firstAvailable = queue.find(q => !isOfflineMode || downloadedSongs.some(d => d.id === q.id));
                if(firstAvailable) { setNowPlaying(firstAvailable); setIsPlaying(true); }
             } else {
                setNowPlaying(null);
                setIsPlaying(false);
             }
          }
          
          // Smart Queue logic: if 1 track left after this or it's the last track"""

content = content.replace(search, replace)
with open('src/App.tsx', 'w') as f:
    f.write(content)

