import re

# App.tsx
with open('src/App.tsx', 'r') as f:
    content = f.read()

sidebar_search = """        <Sidebar 
          onNavigateHome={handleNavigateHome} 
          onNavigateStats={() => setCurrentView('stats')}
          currentView={currentView} 
          onNavigateLikedSongs={handleNavigateLikedSongs}
          likedSongs={likedSongs}
          activeCollectionId={activeCollection?.id}
          isCollapsed={isSidebarCollapsed}
          nowPlaying={nowPlaying}
        />"""
sidebar_replace = """        <Sidebar 
          onNavigateHome={handleNavigateHome} 
          onNavigateStats={() => setCurrentView('stats')}
          currentView={currentView} 
          onNavigateLikedSongs={handleNavigateLikedSongs}
          likedSongs={likedSongs}
          activeCollectionId={activeCollection?.id}
          isCollapsed={isSidebarCollapsed}
          nowPlaying={nowPlaying}
          isOfflineMode={isOfflineMode}
          onToggleOfflineMode={() => setIsOfflineMode(!isOfflineMode)}
        />"""
content = content.replace(sidebar_search, sidebar_replace)
with open('src/App.tsx', 'w') as f:
    f.write(content)

# Sidebar.tsx
with open('src/components/Sidebar.tsx', 'r') as f:
    sidebar = f.read()

toggle_search = """            <div className={`w-8 h-4 rounded-full transition-colors relative ${isOfflineMode ? 'bg-[#fe5f64]' : 'bg-gray-300'}`}> 
               <div className={`absolute top-0.5 w-3 h-3 rounded-full bg-white transition-transform ${isOfflineMode ? 'translate-x-4.5 right-0.5' : 'translate-x-0.5 left-0'}`} />
            </div>"""
toggle_replace = """            <div className={`w-8 h-4 rounded-full transition-colors relative flex items-center ${isOfflineMode ? 'bg-[#fe5f64] justify-end pr-0.5' : 'bg-gray-300 justify-start pl-0.5'}`}> 
               <div className="w-3 h-3 rounded-full bg-white shadow-sm" />
            </div>"""

sidebar = sidebar.replace(toggle_search, toggle_replace)

# Ensure isOfflineMode toggle works
button_search = """          <button 
            onClick={() => onToggleOfflineMode?.()}
            className={`w-full flex items-center justify-between p-2 rounded-xl transition-colors ${isOfflineMode ? 'bg-[#fe5f64]/10' : 'hover:bg-gray-100'}`}
          >"""
button_replace = """          <button 
            onClick={(e) => { e.preventDefault(); e.stopPropagation(); onToggleOfflineMode?.(); }}
            className={`w-full flex items-center justify-between p-2 rounded-xl transition-colors ${isOfflineMode ? 'bg-[#fe5f64]/10' : 'hover:bg-gray-100'}`}
          >"""
sidebar = sidebar.replace(button_search, button_replace)

with open('src/components/Sidebar.tsx', 'w') as f:
    f.write(sidebar)
