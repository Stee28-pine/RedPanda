import re

with open('src/components/SearchView.tsx', 'r') as f:
    content = f.read()

# Add Mic2
if 'Mic2' not in content:
    content = content.replace("import { Play, Share2, Heart, Plus, ListPlus, Download, MoreHorizontal, Check } from 'lucide-react';", "import { Play, Share2, Heart, Plus, ListPlus, Download, MoreHorizontal, Check, Mic2 } from 'lucide-react';")

go_to_artist = """            <button 
              onClick={() => {
                onToggleDownload(contextMenu.song);
                closeContextMenu();
              }}
              className="w-full text-left px-4 py-2.5 text-[13px] font-semibold text-gray-700 hover:bg-gray-100/80 hover:text-gray-900 flex items-center gap-3 transition-colors"
            >
              <Download size={16} className={downloadedSongs.some(s => s.id === contextMenu.song.id) ? 'text-[#fe5f64]' : ''} /> 
              {downloadedSongs.some(s => s.id === contextMenu.song.id) ? 'Remove Download' : 'Download'}
            </button>
            <div className="h-px bg-gray-200/60 my-1 mx-2" />
            <button 
              onClick={() => {
                onArtistClick(contextMenu.song.artist);
                closeContextMenu();
              }}
              className="w-full text-left px-4 py-2.5 text-[13px] font-semibold text-gray-700 hover:bg-gray-100/80 hover:text-gray-900 flex items-center gap-3 transition-colors"
            >
              <Mic2 size={16} /> Go to Artist
            </button>"""

search = """            <button 
              onClick={() => {
                onToggleDownload(contextMenu.song);
                closeContextMenu();
              }}
              className="w-full text-left px-4 py-2.5 text-[13px] font-semibold text-gray-700 hover:bg-gray-100/80 hover:text-gray-900 flex items-center gap-3 transition-colors"
            >
              <Download size={16} className={downloadedSongs.some(s => s.id === contextMenu.song.id) ? 'text-[#fe5f64]' : ''} /> 
              {downloadedSongs.some(s => s.id === contextMenu.song.id) ? 'Remove Download' : 'Download'}
            </button>
            <div className="h-px bg-gray-200/60 my-1 mx-2" />"""

content = content.replace(search, go_to_artist)

with open('src/components/SearchView.tsx', 'w') as f:
    f.write(content)

