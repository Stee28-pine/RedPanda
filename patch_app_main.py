import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# 1. Imports
if 'ShareModal' not in content:
    content = content.replace("import { StatsView } from './components/StatsView';", "import { StatsView } from './components/StatsView';\nimport { ShareModal } from './components/ShareModal';\nimport { DownloadsView } from './components/DownloadsView';\nimport { saveAudioOffline, deleteAudioOffline, clearAllOfflineAudio } from './lib/offlineStorage';")

# 2. Add shareItem state
if 'shareItem' not in content:
    state_search = "  const [toast, setToast] = useState<{ message: string } | null>(null);"
    state_replace = "  const [toast, setToast] = useState<{ message: string } | null>(null);\n  const [shareItem, setShareItem] = useState<{ type: 'song' | 'album' | 'artist', id: string, name: string, data?: any } | null>(null);"
    content = content.replace(state_search, state_replace)

# 3. Update currentView type
content = content.replace("<'home' | 'album' | 'search' | 'stats'>", "<'home' | 'album' | 'search' | 'stats' | 'downloads'>")

# 4. Update handleShare
old_handleShare = """  const handleShare = (item: { type: 'song' | 'album' | 'artist', id: string, name: string }) => {
    const url = `https://music.applet.mock/${item.type}/${item.id}`;
    if (typeof navigator !== 'undefined' && navigator.share) {
      navigator.share({ title: item.name, url }).catch(err => {
         // fallback
         if (navigator.clipboard) {
             navigator.clipboard.writeText(url).catch(() => {});
         }
      });
    } else if (typeof navigator !== 'undefined' && navigator.clipboard) {
      navigator.clipboard.writeText(url).catch(() => {});
    }
    showToast(`Link to ${item.name} copied`);
  };"""

new_handleShare = """  const handleShare = (item: { type: 'song' | 'album' | 'artist', id: string, name: string, data?: any }) => {
    setShareItem(item);
  };
  const handleCopyLink = (url: string) => {
    if (typeof navigator !== 'undefined' && navigator.clipboard) {
      navigator.clipboard.writeText(url).catch(() => {});
    }
    showToast(`Link copied to clipboard`);
  };"""

content = content.replace(old_handleShare, new_handleShare)

# 5. Update toggleDownload
old_toggleDownload = """  const toggleDownload = (song: Song) => {
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

new_toggleDownload = """  const toggleDownload = (song: Song) => {
    setDownloadedSongs(prev => {
      const exists = prev.some(s => s.id === song.id);
      if (exists) {
        deleteAudioOffline(song.id);
        showToast("Removed from downloads");
        return prev.filter(s => s.id !== song.id);
      }
      
      saveAudioOffline(song);
      showToast("Download started...");
      return [...prev, song];
    });
  };"""

content = content.replace(old_toggleDownload, new_toggleDownload)

# 6. Add ShareModal to the end of return
share_modal_markup = """      {showCreatePlaylistModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">"""
new_share_modal = """      <ShareModal item={shareItem} onClose={() => setShareItem(null)} onCopyLink={handleCopyLink} />
      {showCreatePlaylistModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">"""
content = content.replace(share_modal_markup, new_share_modal)

# 7. Add onNavigateDownloads to Sidebar
sidebar_search = """          onNavigateStats={() => setCurrentView('stats')}
          currentView={currentView}"""
sidebar_replace = """          onNavigateStats={() => setCurrentView('stats')}
          onNavigateDownloads={() => setCurrentView('downloads')}
          currentView={currentView}"""
content = content.replace(sidebar_search, sidebar_replace)

# 8. Add DownloadsView to routing
views_search = """            ) : currentView === 'stats' ? (
              <motion.div
                key="stats"
                initial={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}
                animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
                exit={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}
                transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                className="h-full"
              >
                <StatsView stats={stats} />
              </motion.div>
            ) : ("""

views_replace = """            ) : currentView === 'stats' ? (
              <motion.div
                key="stats"
                initial={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}
                animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
                exit={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}
                transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                className="h-full"
              >
                <StatsView stats={stats} />
              </motion.div>
            ) : currentView === 'downloads' ? (
              <motion.div
                key="downloads"
                initial={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}
                animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
                exit={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}
                transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                className="h-full"
              >
                <DownloadsView 
                  downloadedSongs={downloadedSongs} 
                  onPlaySong={handlePlaySong} 
                  onRemoveDownload={toggleDownload}
                  onClearAll={() => setDownloadedSongs([])}
                />
              </motion.div>
            ) : ("""

content = content.replace(views_search, views_replace)

with open('src/App.tsx', 'w') as f:
    f.write(content)
