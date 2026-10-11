with open('src/App.tsx', 'r') as f:
    content = f.read()

search = """        if (idx < queue.length - 1) {
          let nextIdx = idx + 1;
          if (isOfflineMode) {
             while(nextIdx < queue.length && !downloadedSongs.some(d => d.id === queue[nextIdx].id)) {
                nextIdx++;
             }
          }
          if (nextIdx < queue.length) {"""

replace = """        if (idx < queue.length - 1) {
          let nextIdx = idx + 1;
          if (nextIdx < queue.length) {"""

content = content.replace(search, replace)

with open('src/App.tsx', 'w') as f:
    f.write(content)
