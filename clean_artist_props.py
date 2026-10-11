import re
import os

files = ['src/components/AlbumView.tsx', 'src/components/SearchView.tsx', 'src/components/HomeView.tsx']

for file in files:
    with open(file, 'r') as f:
        content = f.read()

    # Remove the prop declaration and type
    content = re.sub(r"  onArtistClick,?", "", content)
    content = re.sub(r"  onArtistClick\??: \(artist: string\) => void;\n", "", content)
    
    # Remove the context menu "Go to Artist"
    context_menu_item = r"""            <div className="h-px bg-gray-200/60 my-1 mx-2" />
            <button 
              onClick=\(\(\) => \{
                onArtistClick\(contextMenu\.song\.artist\);
                closeContextMenu\(\);
              \}\)
              className="w-full text-left px-4 py-2\.5 text-\[13px\] font-semibold text-gray-700 hover:bg-gray-100/80 hover:text-gray-900 flex items-center gap-3 transition-colors"
            >
              <Mic2 size=\{16\} /> Go to Artist
            </button>"""
    content = re.sub(context_menu_item, "", content)
    
    # Remove the inline click handlers (hover:underline cursor-pointer etc.)
    # In AlbumView, the subtitle:
    content = re.sub(r"""onClick=\{\(\) => collection\.subtitle && onArtistClick\(collection\.subtitle\)\}""", "", content)
    content = content.replace('className="text-gray-900 font-bold hover:underline cursor-pointer"', 'className="text-gray-900 font-bold"')
    
    # In AlbumView song item:
    content = re.sub(r"""onClick=\{\(e\) => \{ e\.stopPropagation\(\); onArtistClick\(song\.artist\); \}\}""", "", content)
    content = content.replace('className="text-[12px] text-gray-500 truncate mt-0.5 hover:underline cursor-pointer flex items-center gap-1"', 'className="text-[12px] text-gray-500 truncate mt-0.5 flex items-center gap-1"')

    # In SearchView song item:
    content = re.sub(r"""onClick=\{\(e\) => \{ e\.stopPropagation\(\); onArtistClick\(song\.artist\); \}\}""", "", content)
    content = content.replace('className="text-[13px] font-medium text-gray-500 truncate mt-0.5 hover:underline"', 'className="text-[13px] font-medium text-gray-500 truncate mt-0.5"')

    # In HomeView song item:
    content = re.sub(r"""onClick=\{\(e\) => \{ e\.stopPropagation\(\); onArtistClick\?\.([\s\S]*?)\}\}""", "", content)
    content = content.replace('className="text-[13px] font-medium text-gray-500 truncate mt-0.5 hover:underline"', 'className="text-[13px] font-medium text-gray-500 truncate mt-0.5"')

    with open(file, 'w') as f:
        f.write(content)

