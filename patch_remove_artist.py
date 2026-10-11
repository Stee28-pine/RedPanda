import re
import os

app_file = 'src/App.tsx'
with open(app_file, 'r') as f:
    content = f.read()

# 1. Remove imports
content = re.sub(r"import \{ ArtistView \} from '\./components/ArtistView';\n", "", content)
content = re.sub(r"import \{ AllArtistsView \} from '\./components/AllArtistsView';\n", "", content)

# 2. Update state type
content = content.replace("'artist' | 'stats' | 'artists'>", "'stats'>")

# 3. Remove activeArtist state
content = re.sub(r"  const \[activeArtist, setActiveArtist\] = useState<string \| null>\(null\);\n", "", content)

# 4. Remove handleNavigateArtist
handle_nav_artist_regex = r"  const handleNavigateArtist = \(artistName: string\) => \{[\s\S]*?\};\n"
content = re.sub(handle_nav_artist_regex, "", content)

# 5. Remove onArtistClick props
content = content.replace("onArtistClick={handleNavigateArtist}", "")
content = content.replace("onNavigateArtists={() => setCurrentView('artists')}", "")

# 6. Remove the artist views from the switch
artist_view_regex = r"            \) : currentView === 'artists' \? \([\s\S]*?            \) : currentView === 'artist' && activeArtist \? \([\s\S]*?                />\n              </motion\.div>\n"
content = re.sub(artist_view_regex, "", content)

with open(app_file, 'w') as f:
    f.write(content)

sidebar_file = 'src/components/Sidebar.tsx'
with open(sidebar_file, 'r') as f:
    sidebar = f.read()
sidebar = sidebar.replace("onNavigateArtists?: () => void,", "")
sidebar = sidebar.replace("onNavigateArtists,", "")
sidebar = re.sub(r"          <NavItem icon=\{<Mic2 size=\{18\} />\} label=\"Artists\".*?/>\n", "", sidebar)
with open(sidebar_file, 'w') as f:
    f.write(sidebar)

# We can also clean up the interfaces of HomeView, SearchView, AlbumView, and remove the "Go to Artist" context menu items.
