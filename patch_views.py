import os

files = ['src/components/AlbumView.tsx', 'src/components/ArtistView.tsx', 'src/components/SearchView.tsx']

for file in files:
    with open(file, 'r') as f:
        content = f.read()
    
    # 1. Add to destructuring props
    content = content.replace('  onAddToQueue,', '  onAddToQueue,\n  onPlayNext,')
    
    # 2. Add to interface
    content = content.replace('  onAddToQueue: (song: Song) => void;', '  onAddToQueue: (song: Song) => void;\n  onPlayNext: (song: Song) => void;')
    
    # 3. Add Context Menu item
    menu_item = """            <button 
              onClick={() => {
                onPlayNext(contextMenu.song);
                closeContextMenu();
              }}
              className="w-full text-left px-4 py-2.5 text-[13px] font-semibold text-gray-700 hover:bg-gray-100/80 hover:text-gray-900 flex items-center gap-3 transition-colors"
            >
              <ListPlus size={16} /> Play Next
            </button>
            <button 
              onClick={() => {"""
    content = content.replace('            <button \n              onClick={() => {\n                onAddToQueue(contextMenu.song);', menu_item + '\n                onAddToQueue(contextMenu.song);')
    
    # Need to add ListPlus icon if not imported
    if 'ListPlus' not in content:
        content = content.replace('Plus, ', 'Plus, ListPlus, ')
        content = content.replace('{ Plus ', '{ Plus, ListPlus ')
    
    with open(file, 'w') as f:
        f.write(content)

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace('onAddToQueue={handleAddToQueue}', 'onAddToQueue={handleAddToQueue}\n                  onPlayNext={handlePlayNext}')

with open('src/App.tsx', 'w') as f:
    f.write(content)
print("Views patched")
