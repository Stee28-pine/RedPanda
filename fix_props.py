import re

files = ['src/components/AlbumView.tsx', 'src/components/SearchView.tsx', 'src/components/HomeView.tsx']

for file in files:
    with open(file, 'r') as f:
        content = f.read()

    # Fix the trailing comma issue from props
    content = re.sub(r",\s*,?\s*isOfflineMode \}: \{", ", isOfflineMode }: {", content)
    content = re.sub(r",\s*isOfflineMode \}: \{", " isOfflineMode }: {", content)
    content = re.sub(r",\s*isOfflineMode,\s*downloadedSongs \}: \{", " isOfflineMode, downloadedSongs }: {", content)
    
    # Fix the interface property issue
    content = re.sub(r": \(artist: string\) => void;\n", "", content)

    with open(file, 'w') as f:
        f.write(content)
