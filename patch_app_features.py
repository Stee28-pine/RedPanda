import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# 1. Add showCreatePlaylistModal state
state_old = "  const [playlistModalSong, setPlaylistModalSong] = useState<Song | null>(null);"
state_new = "  const [playlistModalSong, setPlaylistModalSong] = useState<Song | null>(null);\n  const [showCreatePlaylistModal, setShowCreatePlaylistModal] = useState(false);"
content = content.replace(state_old, state_new)

# 2. Add handleNavigatePlaylist
nav_old = """  const handleNavigateLikedSongs = () => {
    setActiveCollection({
      id: 'liked-songs',
      title: 'Liked Song',
      subtitle: '',
      type: 'playlist',
      coverUrl: 'https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=400&q=80',
      songs: likedSongs
    });
    setCurrentView('album');
    setSearchQuery('');
  };"""

nav_new = """  const handleNavigateLikedSongs = () => {
    setActiveCollection({
      id: 'liked-songs',
      title: 'Liked Song',
      subtitle: '',
      type: 'playlist',
      coverUrl: 'https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=400&q=80',
      songs: likedSongs
    });
    setCurrentView('album');
    setSearchQuery('');
  };

  const handleNavigatePlaylist = (playlist: Collection) => {
    setActiveCollection(playlist);
    setCurrentView('album');
    setSearchQuery('');
  };"""

content = content.replace(nav_old, nav_new)

# 3. Update Sidebar props
sidebar_old = """        <Sidebar 
          isCollapsed={isSidebarCollapsed}
          onToggleSidebar={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
          currentView={currentView} 
          onNavigateHome={() => setCurrentView('home')}
          onNavigateLikedSongs={handleNavigateLikedSongs}
          likedSongs={likedSongs}
          activeCollectionId={activeCollection?.id}
          nowPlaying={nowPlaying}
        />"""

sidebar_new = """        <Sidebar 
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

content = content.replace(sidebar_old, sidebar_new)

# 4. Update showCreatePlaylistModal UI
modal_ui = """      {showCreatePlaylistModal && (
        <div className="fixed inset-0 z-[100] bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-sm">
            <h3 className="text-lg font-bold mb-4">Create Playlist</h3>
            <div className="flex gap-2 mb-2">
              <input 
                type="text" 
                value={newPlaylistName}
                onChange={e => setNewPlaylistName(e.target.value)}
                placeholder="Playlist Name" 
                className="flex-1 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[#CA5A2C]"
              />
              <button 
                onClick={() => {
                  if(newPlaylistName.trim()) {
                    const p = createPlaylist(newPlaylistName.trim());
                    setNewPlaylistName('');
                    setShowCreatePlaylistModal(false);
                    showToast(`Created ${p.title}`);
                  }
                }}
                className="px-4 py-2 bg-[#CA5A2C] text-white font-bold rounded-lg hover:bg-[#A84A22] transition-colors"
              >
                Create
              </button>
            </div>
            <button 
              onClick={() => { setShowCreatePlaylistModal(false); setNewPlaylistName(''); }}
              className="w-full py-2 text-gray-500 font-medium mt-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              Cancel
            </button>
          </div>
        </div>
      )}"""

content = content.replace("      {playlistModalSong && (", modal_ui + "\n      {playlistModalSong && (")

# 5. Fix handleAddToQueue
queue_old = """  const handleAddToQueue = (song: Song) => {
    if (!nowPlaying) {
      setNowPlaying(song);
      setIsPlaying(true);
      setQueue([song]);
    } else {
      setQueue(prev => {
        if (prev.some(s => s.id === song.id)) return prev;
        return [...prev, song];
      });
    }
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

content = content.replace(queue_old, queue_new)

with open('src/App.tsx', 'w') as f:
    f.write(content)
