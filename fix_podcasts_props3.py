import re

with open('src/components/PodcastsView.tsx', 'r') as f:
    content = f.read()

content = re.sub(
    r'export function PodcastsView\(\{\s*searchQuery,\s*onSearchChange,\s*onPlaySong,\s*nowPlaying,\s*isPlaying,\s*likedSongs,\s*onToggleLike\s*\}:\s*\{',
    r'export function PodcastsView({ searchQuery, onSearchChange, onPlaySong, nowPlaying, isPlaying, likedSongs, onToggleLike, currentTime, bookmarks, onAddBookmark, onRemoveBookmark, onSeekToTime }: {',
    content
)

with open('src/components/PodcastsView.tsx', 'w') as f:
    f.write(content)
print("Patched successfully with regex")
