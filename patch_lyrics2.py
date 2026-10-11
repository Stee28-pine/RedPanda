import re

with open('src/components/LyricsOverlay.tsx', 'r') as f:
    content = f.read()

search_internals = """export function LyricsOverlay({ song, currentTime, duration, onClose }: LyricsOverlayProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  
  // Calculate active line based on current time
  const lyrics = song.lyrics || MOCK_LYRICS;
  
  let activeIndex = 0;
  if (song.lyrics) {
    activeIndex = lyrics.findIndex(l => l.time > currentTime) - 1;
    if (activeIndex < 0) activeIndex = 0;
  } else if (duration > 0) {
    // If the song is short, just map the mock lyrics linearly to the duration
    const progress = currentTime / duration;
    activeIndex = Math.min(
      Math.floor(progress * lyrics.length),
      lyrics.length - 1
    );
  }

  useEffect(() => {
    // Scroll active line into view smoothly
    if (scrollRef.current) {
      const activeElement = scrollRef.current.children[activeIndex] as HTMLElement;
      if (activeElement) {
        activeElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  }, [activeIndex]);"""

replace_internals = """export function LyricsOverlay({ song, currentTime, duration, onClose }: LyricsOverlayProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const scrollTimeoutRef = useRef<any>(null);
  const isUserScrollingRef = useRef(false);
  
  // Calculate active line based on current time in ms
  const currentMs = currentTime * 1000;
  const lyrics = song.lyrics || MOCK_LYRICS;
  
  let activeIndex = 0;
  if (song.lyrics) {
    const nextIdx = lyrics.findIndex(l => l.time > currentMs);
    if (nextIdx === -1) {
      activeIndex = lyrics.length - 1;
    } else {
      activeIndex = Math.max(0, nextIdx - 1);
    }
  } else if (duration > 0) {
    // Map the mock lyrics linearly to the duration
    const progress = currentTime / duration;
    activeIndex = Math.min(
      Math.floor(progress * lyrics.length),
      lyrics.length - 1
    );
  }

  const snapToActive = () => {
    if (scrollRef.current) {
      const activeElement = scrollRef.current.children[activeIndex] as HTMLElement;
      if (activeElement) {
        activeElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  };

  useEffect(() => {
    if (!isUserScrollingRef.current) {
      snapToActive();
    }
  }, [activeIndex]);

  const handleScroll = () => {
    isUserScrollingRef.current = true;
    if (scrollTimeoutRef.current) clearTimeout(scrollTimeoutRef.current);
    
    scrollTimeoutRef.current = setTimeout(() => {
      isUserScrollingRef.current = false;
      snapToActive();
    }, 1500); // Snap back after 1.5s of no scrolling
  };

  useEffect(() => {
    return () => {
      if (scrollTimeoutRef.current) clearTimeout(scrollTimeoutRef.current);
    };
  }, []);"""

# Add onScroll={handleScroll} to the div
search_div = """        <div 
          ref={scrollRef}
          className="flex-1 overflow-y-auto hide-scrollbar py-[40vh] px-8 md:px-16"
        >"""

replace_div = """        <div 
          ref={scrollRef}
          onScroll={handleScroll}
          className="flex-1 overflow-y-auto hide-scrollbar py-[40vh] px-8 md:px-16"
        >"""

content = content.replace(search_internals, replace_internals)
content = content.replace(search_div, replace_div)

with open('src/components/LyricsOverlay.tsx', 'w') as f:
    f.write(content)
