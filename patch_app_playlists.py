import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

import_playlists = "import { usePlaylists } from './hooks/usePlaylists';\n"
content = content.replace("import { useSearch } from './hooks/useSearch';", "import { useSearch } from './hooks/useSearch';\n" + import_playlists)

state_injection = """  const { playlists, createPlaylist, addSongToPlaylist } = usePlaylists();
  const [playlistModalSong, setPlaylistModalSong] = useState<Song | null>(null);
  const [newPlaylistName, setNewPlaylistName] = useState('');
"""
content = content.replace("  const [currentView, setCurrentView] = useState<'home' | 'album' | 'search' | 'artist'>('home');", state_injection + "  const [currentView, setCurrentView] = useState<'home' | 'album' | 'search' | 'artist'>('home');")

# Inject the modal before <Player>
modal_ui = """      {playlistModalSong && (
        <div className="fixed inset-0 z-[100] bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-sm">
            <h3 className="text-lg font-bold mb-4">Add to Playlist</h3>
            
            <div className="flex gap-2 mb-6">
              <input 
                type="text" 
                value={newPlaylistName}
                onChange={e => setNewPlaylistName(e.target.value)}
                placeholder="New Playlist Name" 
                className="flex-1 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[#CA5A2C]"
              />
              <button 
                onClick={() => {
                  if(newPlaylistName.trim()) {
                    const p = createPlaylist(newPlaylistName.trim());
                    addSongToPlaylist(p.id, playlistModalSong);
                    setNewPlaylistName('');
                    setPlaylistModalSong(null);
                    setToast({ message: `Added to ${p.title}` });
                  }
                }}
                className="bg-[#CA5A2C] text-white px-4 py-2 rounded-lg text-sm font-bold"
              >
                Create
              </button>
            </div>
            
            <div className="space-y-2 max-h-60 overflow-y-auto hide-scrollbar mb-4">
              {playlists.map(p => (
                <button 
                  key={p.id}
                  onClick={() => {
                    addSongToPlaylist(p.id, playlistModalSong);
                    setPlaylistModalSong(null);
                    setToast({ message: `Added to ${p.title}` });
                  }}
                  className="w-full flex items-center gap-3 p-2 hover:bg-gray-100 rounded-lg transition-colors text-left"
                >
                  <img src={p.coverUrl} className="w-10 h-10 rounded object-cover" />
                  <span className="font-semibold text-sm truncate">{p.title}</span>
                </button>
              ))}
              {playlists.length === 0 && <p className="text-sm text-gray-500 text-center py-4">No playlists yet</p>}
            </div>
            
            <button 
              onClick={() => { setPlaylistModalSong(null); setNewPlaylistName(''); }}
              className="w-full py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded-lg text-sm font-bold transition-colors"
            >
              Cancel
            </button>
          </div>
        </div>
      )}"""

content = content.replace("      <Player", modal_ui + "\n      <Player")

# Pass onAddToPlaylist to AlbumView, SearchView, ArtistView
content = content.replace("onPlayNext={handlePlayNext}", "onPlayNext={handlePlayNext}\n                  onAddToPlaylist={setPlaylistModalSong}")

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("App patched with playlists")
