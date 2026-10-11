import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Replace Imports
content = content.replace("import { DownloadsView } from './components/DownloadsView';", "import { HistoryView } from './components/HistoryView';")

# Replace currentView state
content = content.replace("'home' | 'album' | 'search' | 'podcasts' | 'downloads'", "'home' | 'album' | 'search' | 'podcasts' | 'history'")

# Replace Sidebar props
content = content.replace("onNavigateDownloads={() => setCurrentView('downloads')}", "onNavigateHistory={() => setCurrentView('history')}")

# Add remove from history handler
# Wait, I'll just find the DownloadsView render and replace it.

old_render = """            ) : currentView === 'downloads' ? (
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
                  onRemoveDownload={handleToggleDownload}
                  onClearAll={() => setDownloadedSongs([])}
                />
              </motion.div>"""

new_render = """            ) : currentView === 'history' ? (
              <motion.div
                key="history"
                initial={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}
                animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
                exit={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}
                transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                className="h-full"
              >
                <HistoryView 
                  recentlyPlayedHistory={recentlyPlayed}
                  onPlaySong={handlePlaySong}
                  onRemoveFromHistory={(song) => {
                    setRecentlyPlayed(prev => prev.filter(s => s.id !== song.id));
                  }}
                  onClearAll={() => setRecentlyPlayed([])}
                />
              </motion.div>"""

if old_render in content:
    content = content.replace(old_render, new_render)
    print("Render patched")
else:
    print("Render block NOT FOUND")

with open('src/App.tsx', 'w') as f:
    f.write(content)
