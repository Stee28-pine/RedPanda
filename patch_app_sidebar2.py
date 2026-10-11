import re

with open('src/App.tsx', 'r') as f:
    app = f.read()

app = re.sub(
    r"<Sidebar[\s\S]*?nowPlaying=\{nowPlaying\}\s*/>",
    """<Sidebar 
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
        />""",
    app
)

with open('src/App.tsx', 'w') as f:
    f.write(app)
