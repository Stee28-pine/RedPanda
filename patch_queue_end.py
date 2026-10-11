import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

queue_old = """  const handleAddToQueue = (song: Song) => {
    if (nowPlaying?.id === song.id) {
       showToast(`Already playing`);
       return;
    }
    if (!nowPlaying) {
      setNowPlaying(song);
      setIsPlaying(true);
      setQueue([song]);
    } else {
      setQueue(prev => {
        const filtered = prev.filter(s => s.id !== song.id);
        const currentIndex = filtered.findIndex(s => s.id === nowPlaying.id);
        
        // If not playing from the current queue, just append
        if (currentIndex === -1) {
           return [...filtered, song];
        }
        
        // Otherwise, insert it right after the current song for immediate feedback!
        const newQueue = [...filtered];
        newQueue.splice(currentIndex + 1, 0, song);
        return newQueue;
      });
    }
    setShowRightSidebar(true);
    showToast(`Added to queue`);
  };"""

queue_new = """  const handleAddToQueue = (song: Song) => {
    if (nowPlaying?.id === song.id) {
       showToast(`Already playing`);
       return;
    }
    if (!nowPlaying) {
      setNowPlaying(song);
      setIsPlaying(true);
      setQueue([song]);
    } else {
      setQueue(prev => {
        const filtered = prev.filter(s => s.id !== song.id);
        return [...filtered, song];
      });
    }
    setShowRightSidebar(true);
    showToast(`Added to queue`);
  };"""

content = content.replace(queue_old, queue_new)

with open('src/App.tsx', 'w') as f:
    f.write(content)
