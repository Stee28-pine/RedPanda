import re

with open('src/components/Sidebar.tsx', 'r') as f:
    content = f.read()

# 1. Add props for stats and offline mode
old_destruct = """export function Sidebar({ 
  onNavigateHome, 
  currentView,
  onNavigateLikedSongs,
  likedSongs = [],
  activeCollectionId,
  isCollapsed = false,
  nowPlaying,
  playlists,
  onNavigatePlaylist,
  onCreatePlaylist,
}: {"""

new_destruct = """import { BarChart3, Wifi, WifiOff } from 'lucide-react';

export function Sidebar({ 
  onNavigateHome, 
  onNavigateStats,
  currentView,
  onNavigateLikedSongs,
  likedSongs = [],
  activeCollectionId,
  isCollapsed = false,
  nowPlaying,
  playlists,
  onNavigatePlaylist,
  onCreatePlaylist,
  isOfflineMode = false,
  onToggleOfflineMode,
}: {"""

content = content.replace(old_destruct, new_destruct)

old_types = """  playlists?: any[],
  onNavigatePlaylist?: (p: any) => void,
  onCreatePlaylist?: () => void,
}) {"""

new_types = """  playlists?: any[],
  onNavigatePlaylist?: (p: any) => void,
  onCreatePlaylist?: () => void,
  onNavigateStats?: () => void,
  isOfflineMode?: boolean,
  onToggleOfflineMode?: () => void,
}) {"""

content = content.replace(old_types, new_types)

# 2. Add Stats NavItem
nav_old = """          <NavItem icon={<Mic2 size={18} />} label="Artists" isCollapsed={isCollapsed} />
        </nav>"""
nav_new = """          <NavItem icon={<Mic2 size={18} />} label="Artists" isCollapsed={isCollapsed} />
          <NavItem icon={<BarChart3 size={18} />} label="Stats" active={currentView === 'stats'} onClick={onNavigateStats} isCollapsed={isCollapsed} activeIconColor="text-[#CA5A2C]" />
        </nav>"""
content = content.replace(nav_old, nav_new)

# 3. Add Settings block
settings_block = """      <div className={`mb-8 px-3 ${isCollapsed ? 'block md:hidden' : 'block'}`}>
        <h3 className="text-[11px] font-bold text-gray-400 mb-2 px-3 tracking-widest uppercase">SETTINGS</h3>
        <nav className="space-y-0.5">
          <button 
            onClick={onToggleOfflineMode}
            className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg transition-colors text-gray-700 hover:bg-gray-300/50`}
          >
            <div className="flex items-center gap-3">
              <div className={`${isOfflineMode ? 'text-[#CA5A2C]' : 'text-gray-500'}`}>
                {isOfflineMode ? <WifiOff size={18} /> : <Wifi size={18} />}
              </div>
              <span className="font-semibold text-[15px] tracking-tight">Offline Mode</span>
            </div>
            <div className={`w-8 h-4 rounded-full transition-colors relative ${isOfflineMode ? 'bg-[#CA5A2C]' : 'bg-gray-300'}`}>
               <div className={`absolute top-0.5 w-3 h-3 rounded-full bg-white transition-transform ${isOfflineMode ? 'translate-x-4.5 right-0.5' : 'translate-x-0.5 left-0'}`} />
            </div>
          </button>
        </nav>
      </div>"""

content = content.replace('      <div className="mt-auto pt-4 pb-24 px-3 flex-shrink-0">', settings_block + '\n      <div className="mt-auto pt-4 pb-24 px-3 flex-shrink-0">')

with open('src/components/Sidebar.tsx', 'w') as f:
    f.write(content)
