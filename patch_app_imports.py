with open('src/App.tsx', 'r') as f:
    content = f.read()

import re
old_imports = "import { usePlaylists } from './hooks/usePlaylists';"
new_imports = "import { usePlaylists } from './hooks/usePlaylists';\nimport { useSettings } from './hooks/useSettings';\nimport { useListeningStats } from './hooks/useListeningStats';\nimport { StatsView } from './components/StatsView';"

content = content.replace(old_imports, new_imports)

# Add state hook usage
hook_old = "  const { playlists, createPlaylist, addSongToPlaylist } = usePlaylists();"
hook_new = "  const { playlists, createPlaylist, addSongToPlaylist } = usePlaylists();\n  const { isOfflineMode, setIsOfflineMode } = useSettings();\n  const { stats, recordPlay } = useListeningStats();"

content = content.replace(hook_old, hook_new)

with open('src/App.tsx', 'w') as f:
    f.write(content)
