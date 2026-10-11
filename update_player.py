import re

with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

# Remove react-player import
content = re.sub(r"import ReactPlayer from 'react-player';\n", "", content)

# Update PlayerProps
props_replacement = """interface PlayerProps {
  song: Song | null;
  isPlaying: boolean;
  onTogglePlay: () => void;
  onToggleRightSidebar: () => void;
  onNext?: () => void;
  onPrev?: () => void;
  isShuffle?: boolean;
  repeatMode?: 'none' | 'all' | 'one';
  onToggleShuffle?: () => void;
  onToggleRepeat?: () => void;
  isLiked?: boolean;
  onToggleLike?: () => void;
  onShare?: (item: { type: 'song' | 'album' | 'artist', id: string, name: string }) => void;
  currentTime: number;
  duration: number;
  isBuffering: boolean;
  onSeek: (time: number) => void;
}"""
content = re.sub(r'interface PlayerProps \{[\s\S]*?\}', props_replacement, content, count=1)

# Update component signature
sig_replacement = """export function Player({ 
  song, 
  isPlaying, 
  onTogglePlay, 
  onToggleRightSidebar, 
  onNext, 
  onPrev,
  isShuffle = false,
  repeatMode = 'none',
  onToggleShuffle,
  onToggleRepeat,
  isLiked = false,
  onToggleLike,
  onShare,
  currentTime,
  duration,
  isBuffering,
  onSeek
}: PlayerProps) {"""
content = re.sub(r'export function Player\(\{[\s\S]*?\}\: PlayerProps\) \{', sig_replacement, content, count=1)

# Remove internal state: playerRef, currentTime, duration, youtubeId, isLoadingYt
content = re.sub(r'  const playerRef = useRef<any>\(null\);\n', '', content)
content = re.sub(r'  const \[currentTime, setCurrentTime\] = useState\(0\);\n', '', content)
content = re.sub(r'  const \[duration, setDuration\] = useState\(song\?\.durationSeconds \|\| 0\);\n', '', content)
content = re.sub(r'  const \[youtubeId, setYoutubeId\] = useState<string \| null>\(song\?\.youtubeId \|\| null\);\n', '', content)
content = re.sub(r'  const \[isLoadingYt, setIsLoadingYt\] = useState\(false\);\n', '', content)

# Remove the two useEffects related to YT and resetting state
content = re.sub(r'  useEffect\(\(\) => \{\n    if \(\!song\) return;\n    // Reset state when song changes[\s\S]*?fetchYtId\(\);\n  \}, \[song\]\);\n', '', content)

# Change handleSeek
seek_replacement = """  const handleSeek = (e: React.MouseEvent<HTMLDivElement>) => {
    const bounds = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - bounds.left;
    const percent = Math.max(0, Math.min(1, x / bounds.width));
    const newTime = percent * duration;
    onSeek(newTime);
  };"""
content = re.sub(r'  const handleSeek = \(e: React\.MouseEvent<HTMLDivElement>\) => \{[\s\S]*?  \};\n', seek_replacement + '\n', content)

# Remove handleProgress and handleDuration
content = re.sub(r'  const handleProgress = \(state: \{ playedSeconds: number \}\) => \{[\s\S]*?  \};\n', '', content)
content = re.sub(r'  const handleDuration = \(duration: number\) => \{[\s\S]*?  \};\n', '', content)

# Remove ReactPlayer rendering
content = re.sub(r'      <div className="absolute opacity-\[0\.01\] pointer-events-none -z-10 w-\[200px\] h-\[200px\] overflow-hidden">[\s\S]*?      </div>\n', '', content)

# Replace isLoadingYt with isBuffering
content = content.replace('isLoadingYt', 'isBuffering')

with open('src/components/Player.tsx', 'w') as f:
    f.write(content)

print("Player.tsx updated")
