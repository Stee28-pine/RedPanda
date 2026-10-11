import re

with open('src/components/HomeView.tsx', 'r') as f:
    content = f.read()

old_props1 = '''export function HomeView({ 
  onCollectionClick, 
  playlists = [],
  onPlaySong,
  onGenreClick,downloadedSongs, onDeletePlaylist, onMergePlaylist }: { 
  onCollectionClick: (c: Collection) => void;
  playlists?: Collection[];
  onPlaySong?: (song: Song, context: { songs: Song[] }) => void;downloadedSongs?: Song[];
  onGenreClick?: (genre: string) => void;
  onDeletePlaylist?: (id: string) => void;
  onMergePlaylist?: (targetId: string, sourceId: string) => void;
}) {'''

new_props1 = '''export function HomeView({ 
  onCollectionClick, 
  playlists = [],
  onPlaySong,
  onGenreClick,
  downloadedSongs,
  onDeletePlaylist, 
  onMergePlaylist,
  recentlyPlayedHistory = []
}: { 
  onCollectionClick: (c: Collection) => void;
  playlists?: Collection[];
  onPlaySong?: (song: Song, context: { songs: Song[] }) => void;
  downloadedSongs?: Song[];
  onGenreClick?: (genre: string) => void;
  onDeletePlaylist?: (id: string) => void;
  onMergePlaylist?: (targetId: string, sourceId: string) => void;
  recentlyPlayedHistory?: Song[];
}) {'''

content = content.replace(old_props1, new_props1)

with open('src/components/HomeView.tsx', 'w') as f:
    f.write(content)
