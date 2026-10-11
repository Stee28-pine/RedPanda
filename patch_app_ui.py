import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

sidebar_old = """        <Sidebar 
          isCollapsed={isSidebarCollapsed}
          onToggleSidebar={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
          currentView={currentView} 
          onNavigateHome={() => setCurrentView('home')}
          onNavigateLikedSongs={handleNavigateLikedSongs}
          likedSongs={likedSongs}
          activeCollectionId={activeCollection?.id}
          nowPlaying={nowPlaying}
          playlists={playlists}
          onNavigatePlaylist={handleNavigatePlaylist}
          onCreatePlaylist={() => setShowCreatePlaylistModal(true)}
        />"""

sidebar_new = """        <Sidebar 
          isCollapsed={isSidebarCollapsed}
          onToggleSidebar={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
          currentView={currentView} 
          onNavigateHome={() => setCurrentView('home')}
          onNavigateStats={() => setCurrentView('stats')}
          onNavigateLikedSongs={handleNavigateLikedSongs}
          likedSongs={likedSongs}
          activeCollectionId={activeCollection?.id}
          nowPlaying={nowPlaying}
          playlists={playlists}
          onNavigatePlaylist={handleNavigatePlaylist}
          onCreatePlaylist={() => setShowCreatePlaylistModal(true)}
          isOfflineMode={isOfflineMode}
          onToggleOfflineMode={() => setIsOfflineMode(!isOfflineMode)}
        />"""

content = content.replace(sidebar_old, sidebar_new)

# Add StatsView rendering block
view_old = """              </motion.div>
            )}
          </AnimatePresence>
        </main>"""

view_new = """              </motion.div>
            )}
            
            {currentView === 'stats' && (
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
            )}
          </AnimatePresence>
        </main>"""

content = content.replace(view_old, view_new)

with open('src/App.tsx', 'w') as f:
    f.write(content)
