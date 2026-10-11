import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

old_album = """            ) : (
              <motion.div
                key="album"
                initial={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}"""

new_history_and_album = """            ) : currentView === 'history' ? (
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
              </motion.div>
            ) : (
              <motion.div
                key="album"
                initial={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}"""

if old_album in content:
    content = content.replace(old_album, new_history_and_album)
    with open('src/App.tsx', 'w') as f:
        f.write(content)
    print("Injected history view")
else:
    print("Could not find old_album block")
