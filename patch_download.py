import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

dl_old = """  const toggleDownload = (song: Song) => {
    setDownloadedSongs(prev => {
      const exists = prev.some(s => s.id === song.id);
      if (exists) return prev.filter(s => s.id !== song.id);
      return [...prev, song];
    });
  };"""

dl_new = """  const toggleDownload = (song: Song) => {
    setDownloadedSongs(prev => {
      const exists = prev.some(s => s.id === song.id);
      if (exists) {
        showToast("Removed from downloads");
        return prev.filter(s => s.id !== song.id);
      }
      
      // Simulate real download
      if (typeof document !== 'undefined') {
        const link = document.createElement('a');
        link.href = song.audioUrl || '#';
        link.download = `${song.title} - ${song.artist}.mp3`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
      
      showToast("Download started");
      return [...prev, song];
    });
  };"""

content = content.replace(dl_old, dl_new)

with open('src/App.tsx', 'w') as f:
    f.write(content)
