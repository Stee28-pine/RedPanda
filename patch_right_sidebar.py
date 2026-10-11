import re

with open('src/components/RightSidebar.tsx', 'r') as f:
    content = f.read()

# Replace old imports
content = content.replace("import { useEffect, useState, useRef } from 'react';", "import { useEffect, useState, useRef } from 'react';\nimport { useLyricsScroll } from '../hooks/useLyricsScroll';")

# Replace logic inside RightSidebar
old_logic = """  const [localNextUp, setLocalNextUp] = useState<Song[]>([]);
  const activeLyricRef = useRef<HTMLParagraphElement>(null);

  useEffect(() => {
    setLocalNextUp(nextUp);
  }, [nowPlaying, queue]);

  const handleReorder = (newOrder: Song[]) => {
    setLocalNextUp(newOrder);
    onReorder?.(newOrder);
  };

  const hasLyrics = nowPlaying?.lyrics && nowPlaying.lyrics.length > 0;
  
  // Find current lyric index
  const activeLyricIdx = hasLyrics
    ? [...(nowPlaying.lyrics || [])].reverse().findIndex(lyric => currentTime >= lyric.time)
    : -1;
    
  const currentLyricIdx = activeLyricIdx !== -1 ? (nowPlaying!.lyrics!.length - 1) - activeLyricIdx : -1;

  useEffect(() => {
    if (activeLyricRef.current) {
      activeLyricRef.current.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, [currentLyricIdx]);"""

new_logic = """  const [localNextUp, setLocalNextUp] = useState<Song[]>([]);
  const { activeLyricRef, currentLyricIdx, hasLyrics } = useLyricsScroll(nowPlaying, currentTime);

  useEffect(() => {
    setLocalNextUp(nextUp);
  }, [nowPlaying, queue]);

  const handleReorder = (newOrder: Song[]) => {
    setLocalNextUp(newOrder);
    onReorder?.(newOrder);
  };"""

content = content.replace(old_logic, new_logic)

with open('src/components/RightSidebar.tsx', 'w') as f:
    f.write(content)

print("RightSidebar patched")
