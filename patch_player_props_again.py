with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace("<Player \n          song={nowPlaying}\n          isPlaying={isPlaying}", "<Player \n          song={nowPlaying}\n          analyzerNode={analyzerNode}\n          isPlaying={isPlaying}")

with open('src/App.tsx', 'w') as f:
    f.write(content)
