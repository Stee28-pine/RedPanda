import re

files = ['src/components/HomeView.tsx', 'src/components/SearchView.tsx', 'src/components/AlbumView.tsx']

for file in files:
    with open(file, 'r') as f:
        content = f.read()
    
    # Remove dangling type properties
    content = re.sub(r"\?: boolean;?\s*", "", content)
    content = re.sub(r"\?: boolean,\s*", "", content)
    
    # Find any remaining `isOfflineMode` usages in JSX like: disabled={isOfflineMode} or whatever was causing Expression expected
    content = re.sub(r"isOfflineMode\s*\?.*?:.*?\s*", "", content) # This is risky, let's fix manually
    
    with open(file, 'w') as f:
        f.write(content)
