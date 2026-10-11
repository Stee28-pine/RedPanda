with open('src/components/PodcastsView.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    "import { Play, ChevronLeft, Mic2, Pause, Clock } from 'lucide-react';",
    "import { Play, ChevronLeft, Mic2, Pause, Clock, BookmarkPlus, Bookmark as BookmarkIcon, Trash2 } from 'lucide-react';\nimport { Bookmark } from '../types';"
)

with open('src/components/PodcastsView.tsx', 'w') as f:
    f.write(content)
