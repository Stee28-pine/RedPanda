import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Update onSearchFocus in TopBar
search_topbar = r"onSearchFocus=\{\(\) => setCurrentView\('search'\)\}"
replace_topbar = r"onSearchFocus={() => { if (currentView !== 'podcasts') setCurrentView('search'); }}"
content = re.sub(search_topbar, replace_topbar, content)

# Pass searchQuery to PodcastsView
search_podcasts = r"(<PodcastsView \s*\n\s*onPlaySong=\{handlePlaySong\})"
replace_podcasts = r"<PodcastsView \n                  searchQuery={searchQuery}\n                  onSearchChange={handleSearchChange}\n                  onPlaySong={handlePlaySong}"
content = re.sub(search_podcasts, replace_podcasts, content)

with open('src/App.tsx', 'w') as f:
    f.write(content)
