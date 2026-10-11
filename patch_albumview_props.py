import re

with open('src/components/AlbumView.tsx', 'r') as f:
    content = f.read()

# Add imports for Merge and Trash2 if not there
content = re.sub(
    r"import \{ Play, Share2, Pause, Heart, MoreHorizontal, Clock, Shuffle, Plus, ListPlus, Download, Check, Mic2 \} from 'lucide-react';",
    "import { Play, Share2, Pause, Heart, MoreHorizontal, Clock, Shuffle, Plus, ListPlus, Download, Check, Mic2, Merge, Trash2 } from 'lucide-react';",
    content
)

# Props destructuring
content = re.sub(
    r"onAddToPlaylist, onRemoveFromPlaylist,\}: \{",
    r"onAddToPlaylist, onRemoveFromPlaylist,\n  playlists = [], onDeletePlaylist, onMergePlaylist\n}: {",
    content
)

# Props types
content = re.sub(
    r"onRemoveFromPlaylist\?: \(song: Song\) => void;\n\}\)",
    r"onRemoveFromPlaylist?: (song: Song) => void;\n  playlists?: Collection[];\n  onDeletePlaylist?: (id: string) => void;\n  onMergePlaylist?: (targetId: string, sourceId: string) => void;\n})",
    content
)

# Also add a state for mergeMenu in AlbumView
content = re.sub(
    r"  const \[albumContextMenu, setAlbumContextMenu\] = useState<\{ x: number; y: number \} \| null>\(null\);",
    r"  const [albumContextMenu, setAlbumContextMenu] = useState<{ x: number; y: number } | null>(null);\n  const [mergeMenu, setMergeMenu] = useState<{ x: number; y: number } | null>(null);",
    content
)

content = re.sub(
    r"    setAlbumContextMenu\(null\);\n  \};",
    r"    setAlbumContextMenu(null);\n    setMergeMenu(null);\n  };",
    content
)

with open('src/components/AlbumView.tsx', 'w') as f:
    f.write(content)
