import re

with open('src/components/SearchView.tsx', 'r') as f:
    content = f.read()

search = "  onShare, onAddToPlaylist, isOfflineMode }: {"
replace = "  onShare, onAddToPlaylist, isOfflineMode, onSearchSelect }: {"

content = content.replace(search, replace)

with open('src/components/SearchView.tsx', 'w') as f:
    f.write(content)
