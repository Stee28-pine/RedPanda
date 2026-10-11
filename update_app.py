import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Add useRef to import
content = content.replace("import { useState, useEffect } from 'react';", "import { useState, useEffect, useRef } from 'react';")

# Inside App component
hooks_str = """
  const audioRef = useRef<HTMLAudioElement>(null);
  const [duration, setDuration] = useState(0);
  const [isBuffering, setIsBuffering] = useState(false);

  useEffect(() => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.play().catch(e => console.error("Playback error:", e));
      } else {
        audioRef.current.pause();
      }
    }
  }, [isPlaying]);

  useEffect(() => {
    if (audioRef.current && nowPlaying?.audioUrl) {
      audioRef.current.src = nowPlaying.audioUrl;
      setIsBuffering(true);
      audioRef.current.play().then(() => {
        setIsPlaying(true);
      }).catch(e => {
        console.error("Autoplay prevented:", e);
        setIsPlaying(false);
      });
    }
  }, [nowPlaying]);

  const handleTimeUpdate = () => {
    if (audioRef.current) {
      setCurrentPlaybackTime(audioRef.current.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    if (audioRef.current) {
      setDuration(audioRef.current.duration);
    }
  };
"""

content = re.sub(r'  const \[toast, setToast\] = useState<\{ message: string \} \| null>\(null\);\n', r'  const [toast, setToast] = useState<{ message: string } | null>(null);\n' + hooks_str, content)

# Change onTimeUpdate={setCurrentPlaybackTime} to the new props
# Find where <Player is rendered
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
            if (audioRef.current) {
               audioRef.current.currentTime = time;
            }
            setCurrentPlaybackTime(time);
          }}
        />
        <audio 
          ref={audioRef}
          onTimeUpdate={handleTimeUpdate}
          onLoadedMetadata={handleLoadedMetadata}
          onEnded={() => {
             if (repeatMode === 'one') {
                if (audioRef.current) audioRef.current.play();
             } else {
                handleNext();
             }
          }}
          onWaiting={() => setIsBuffering(true)}
          onPlaying={() => setIsBuffering(false)}
        />
"""

content = re.sub(r'<Player[\s\S]*?/>', player_render, content)

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("App.tsx updated")
