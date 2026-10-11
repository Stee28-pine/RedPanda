import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

view_search = """            ) : currentView === 'artist' && activeArtist ? (
              <motion.div
                key="artist\""""
view_replace = """            ) : currentView === 'artists' ? (
              <motion.div
                key="artists"
                initial={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}
                animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
                exit={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}
                transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                className="h-full"
              >
                <AllArtistsView
                  songs={SONGS}
                  albums={ALBUMS}
                  onArtistClick={handleNavigateArtist}
                />
              </motion.div>
            ) : currentView === 'stats' ? (
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
            ) : currentView === 'artist' && activeArtist ? (
              <motion.div
                key="artist\""""
content = content.replace(view_search, view_replace)

with open('src/App.tsx', 'w') as f:
    f.write(content)

