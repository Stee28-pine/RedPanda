import re

with open('src/App.tsx', 'r') as f:
    app = f.read()

sidebar_search = """        <Sidebar 
          onNavigateHome={handleNavigateHome} 
          onNavigateStats={() => setCurrentView('stats')}          
          onNavigateDownloads={() => setCurrentView('downloads')}
          currentView={currentView} 
          onNavigateLikedSongs={handleNavigateLikedSongs}
          likedSongs={likedSongs}
          activeCollectionId={activeCollection?.id}
          isCollapsed={isSidebarCollapsed}
          nowPlaying={nowPlaying}
          isOfflineMode={isOfflineMode}
          onToggleOfflineMode={() => setIsOfflineMode(!isOfflineMode)}
        />"""

sidebar_replace = """        <Sidebar 
          onNavigateHome={handleNavigateHome} 
          onNavigateStats={() => setCurrentView('stats')}          
          onNavigateDownloads={() => setCurrentView('downloads')}
          currentView={currentView} 
          onNavigateLikedSongs={handleNavigateLikedSongs}
          likedSongs={likedSongs}
          activeCollectionId={activeCollection?.id}
          isCollapsed={isSidebarCollapsed}
          nowPlaying={nowPlaying}
          isOfflineMode={isOfflineMode}
          onToggleOfflineMode={() => setIsOfflineMode(!isOfflineMode)}
          playlists={playlists}
          onNavigatePlaylist={(p) => {
             setActiveCollection(p);
             setCurrentView('album');
          }}
          onCreatePlaylist={() => setShowCreatePlaylistModal(true)}
        />"""

app = app.replace(sidebar_search, sidebar_replace)

with open('src/App.tsx', 'w') as f:
    f.write(app)
