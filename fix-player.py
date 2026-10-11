import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Add ReactPlayer import
content = content.replace("import { motion, AnimatePresence } from 'motion/react';", "import { motion, AnimatePresence } from 'motion/react';\nimport ReactPlayer from 'react-player';")

# Replace audioRef and hooks
hooks_str = """
  const playerRef = useRef<any>(null);
  const [duration, setDuration] = useState(0);
  const [isBuffering, setIsBuffering] = useState(false);
  const [youtubeId, setYoutubeId] = useState<string | null>(null);

  useEffect(() => {
    if (!nowPlaying) return;
    
    // Attempt to use existing youtubeId or fetch a new one
    if (nowPlaying.youtubeId) {
      setYoutubeId(nowPlaying.youtubeId);
      setIsBuffering(false);
      return;
    }

    const fetchYtId = async () => {
      setIsBuffering(true);
      try {
        const res = await fetch(`/api/youtube-search?q=${encodeURIComponent(nowPlaying.title + ' ' + nowPlaying.artist)}`);
        const data = await res.json();
        if (data.videoId) {
          setYoutubeId(data.videoId);
          nowPlaying.youtubeId = data.videoId;
        }
      } catch (err) {
        console.error("Failed to fetch YT ID", err);
      } finally {
        setIsBuffering(false);
      }
    };
    fetchYtId();
  }, [nowPlaying]);

  const handleProgress = (state: { playedSeconds: number }) => {
    setCurrentPlaybackTime(state.playedSeconds);
  };
"""

content = re.sub(
    r'  const audioRef = useRef<HTMLAudioElement>\(null\);\n  const \[duration, setDuration\] = useState\(0\);\n  const \[isBuffering, setIsBuffering\] = useState\(false\);\n[\s\S]*?  const handleLoadedMetadata = \(\) => \{\n    if \(audioRef\.current\) \{\n      setDuration\(audioRef\.current\.duration\);\n    \}\n  \};\n',
    hooks_str,
    content
)

# Replace <audio> with <ReactPlayer> inside the hidden div
player_render = """<Player 
          song={nowPlaying} 
          isPlaying={isPlaying} 
          onTogglePlay={() => setIsPlaying(!isPlaying)} 
          onToggleRightSidebar={() => setShowRightSidebar(!showRightSidebar)}
          onNext={handleNext}
          onPrev={handlePrev}
          isShuffle={isShuffle}
          repeatMode={repeatMode}
          onToggleShuffle={() => setIsShuffle(!isShuffle)}
          onToggleRepeat={() => {
            if (repeatMode === 'none') setRepeatMode('all');
            else if (repeatMode === 'all') setRepeatMode('one');
            else setRepeatMode('none');
          }}
          isLiked={nowPlaying ? likedSongs.some(s => s.id === nowPlaying.id) : false}
          onToggleLike={() => nowPlaying && toggleLike(nowPlaying)}
          onShare={handleShare}
          currentTime={currentPlaybackTime}
          duration={duration}
          isBuffering={isBuffering}
          onSeek={(time) => {
            if (playerRef.current) {
               playerRef.current.seekTo(time, 'seconds');
            }
            setCurrentPlaybackTime(time);
          }}
        />
        <div className="absolute opacity-[0.01] pointer-events-none -z-10 w-[200px] h-[200px] overflow-hidden">
          <ReactPlayer
            ref={playerRef}
            url={youtubeId ? `https://www.youtube.com/watch?v=${youtubeId}` : ""}
            playing={isPlaying && !isBuffering}
            width="200px"
            height="200px"
            controls={false}
            onProgress={handleProgress}
            onDuration={(d) => setDuration(d)}
            onBuffer={() => setIsBuffering(true)}
            onBufferEnd={() => setIsBuffering(false)}
            onEnded={() => {
               if (repeatMode === 'one') {
                  if (playerRef.current) {
                    playerRef.current.seekTo(0);
                  }
               } else {
                  handleNext();
               }
            }}
          />
        </div>
"""

content = re.sub(r'<Player[\s\S]*?/>\n        <audio[\s\S]*?/>', player_render, content)

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("Updated App.tsx")
