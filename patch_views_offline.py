import re
import os

files = ['src/components/HomeView.tsx', 'src/components/SearchView.tsx', 'src/components/AlbumView.tsx']

for file in files:
    if os.path.exists(file):
        with open(file, 'r') as f:
            content = f.read()
        
        # Remove isOfflineMode from the destructured props
        content = re.sub(r"\s*isOfflineMode(?: \?: boolean)?(?: = false)?,?\s*", "", content)
        
        # We also need to remove any places where it was used, usually to hide a song or check if it can be played.
        # But looking at previous code, `isOfflineMode` wasn't heavily used in the views except to pass to child components or show badges.
        # Let's just do a regex replace for the prop definition.
        # Note: the above regex might break if it matches randomly, but it's specific enough.
        # Wait, a safer way is to just let TS complain if we missed something and fix it.
        
        with open(file, 'w') as f:
            f.write(content)
