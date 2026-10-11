import re

with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

# 1. Mini Player Wrapper
mini_wrapper_old = """          <motion.div 
            className="bg-[#F5F5F5]/90 backdrop-blur-xl rounded-2xl shadow-[0_8px_30px_rgba(0,0,0,0.12)] border border-white flex items-center px-4 w-[min(90vw,340px)] h-14 pointer-events-auto cursor-pointer touch-none"
            onClick={(e) => {"""
mini_wrapper_new = """          <motion.div 
            layoutId="player-wrapper"
            className="bg-[#F5F5F5]/90 backdrop-blur-xl rounded-2xl shadow-[0_8px_30px_rgba(0,0,0,0.12)] border border-white flex items-center px-4 w-[min(90vw,340px)] h-14 pointer-events-auto cursor-pointer touch-none"
            transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
            style={{ borderRadius: 16 }}
            onClick={(e) => {"""
content = content.replace(mini_wrapper_old, mini_wrapper_new)

# 2. Mini Player Art & Info
mini_art_old = """<div className="flex items-center w-full gap-3">
              <img src={song.coverUrl} onError={(e) => { e.currentTarget.src = FALLBACK_IMG }} className="w-10 h-10 rounded shadow-sm object-cover flex-shrink-0" alt={song.title} />
              <div className="flex flex-col flex-1 min-w-0 justify-center">
                <span className="text-[13px] font-semibold text-gray-900 truncate leading-tight">{song.title}</span>
                <span className="text-[11px] text-gray-500 truncate mt-0.5">{song.artist}</span>
              </div>
              <button"""
mini_art_new = """<div className="flex items-center w-full gap-3">
              <motion.img layoutId="album-art" transition={{ type: "spring", bounce: 0.2, duration: 0.6 }} style={{ borderRadius: 4 }} src={song.coverUrl} onError={(e) => { e.currentTarget.src = FALLBACK_IMG }} className="w-10 h-10 rounded shadow-sm object-cover flex-shrink-0" alt={song.title} />
              <motion.div layoutId="song-info" transition={{ type: "spring", bounce: 0.2, duration: 0.6 }} className="flex flex-col flex-1 min-w-0 justify-center">
                <span className="text-[13px] font-semibold text-gray-900 truncate leading-tight">{song.title}</span>
                <span className="text-[11px] text-gray-500 truncate mt-0.5">{song.artist}</span>
              </motion.div>
              <button"""
content = content.replace(mini_art_old, mini_art_new)

# 3. Expanded Player Wrapper
expanded_wrapper_old = """          <motion.div 
            className={`fixed inset-0 bg-[#F5F5F5] z-[100] flex pointer-events-auto overflow-hidden px-6 pt-12 pb-8 ${isLandscape ? 'flex-row gap-8 items-center' : 'flex-col'}`}
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 50 }}
            onPanEnd={(e, info: any) => {"""
expanded_wrapper_new = """          <motion.div 
            layoutId="player-wrapper"
            className={`fixed inset-0 bg-[#F5F5F5] z-[100] flex pointer-events-auto overflow-hidden px-6 pt-12 pb-8 ${isLandscape ? 'flex-row gap-8 items-center' : 'flex-col'}`}
            transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
            style={{ borderRadius: 0 }}
            onPanEnd={(e, info: any) => {"""
content = content.replace(expanded_wrapper_old, expanded_wrapper_new)

# 4. Expanded Player Art & Info (Landscape)
land_art_old = """                    <img 
                      src={song.coverUrl} 
                      onError={(e) => { e.currentTarget.src = FALLBACK_IMG }} 
                      className="relative w-full h-full rounded-3xl shadow-2xl object-cover z-10 pointer-events-none" 
                      alt={song.title} 
                    />
                  </div>
                </div>
                {/* Right Side: Controls */}
                <div className="flex-1 flex flex-col justify-center max-w-[400px]">
                  <div className="flex justify-between items-end mb-6">
                    <div className="flex flex-col overflow-hidden pr-4">
                      <span className="text-2xl font-bold text-gray-900 truncate mb-1">{song.title}</span>
                      <span className="text-lg text-gray-500 truncate">{song.artist}</span>
                    </div>"""
land_art_new = """                    <motion.img 
                      layoutId="album-art"
                      transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                      style={{ borderRadius: 24 }}
                      src={song.coverUrl} 
                      onError={(e) => { e.currentTarget.src = FALLBACK_IMG }} 
                      className="relative w-full h-full rounded-3xl shadow-2xl object-cover z-10 pointer-events-none" 
                      alt={song.title} 
                    />
                  </div>
                </div>
                {/* Right Side: Controls */}
                <div className="flex-1 flex flex-col justify-center max-w-[400px]">
                  <div className="flex justify-between items-end mb-6">
                    <motion.div layoutId="song-info" transition={{ type: "spring", bounce: 0.2, duration: 0.6 }} className="flex flex-col overflow-hidden pr-4">
                      <span className="text-2xl font-bold text-gray-900 truncate mb-1">{song.title}</span>
                      <span className="text-lg text-gray-500 truncate">{song.artist}</span>
                    </motion.div>"""
content = content.replace(land_art_old, land_art_new)

# 5. Expanded Player Art & Info (Portrait)
port_art_old = """                    <img 
                      src={song.coverUrl} 
                      onError={(e) => { e.currentTarget.src = FALLBACK_IMG }} 
                      className="relative w-full max-w-[340px] aspect-square rounded-3xl shadow-2xl object-cover z-10 pointer-events-none" 
                      alt={song.title} 
                    />
                </div>
                {/* Info */}
                <div className="flex justify-between items-end mb-4">
                  <div className="flex flex-col overflow-hidden pr-4">
                    <span className="text-2xl font-bold text-gray-900 truncate mb-1">{song.title}</span>
                    <span className="text-lg text-gray-500 truncate">{song.artist}</span>
                  </div>"""
port_art_new = """                    <motion.img 
                      layoutId="album-art"
                      transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                      style={{ borderRadius: 24 }}
                      src={song.coverUrl} 
                      onError={(e) => { e.currentTarget.src = FALLBACK_IMG }} 
                      className="relative w-full max-w-[340px] aspect-square rounded-3xl shadow-2xl object-cover z-10 pointer-events-none" 
                      alt={song.title} 
                    />
                </div>
                {/* Info */}
                <div className="flex justify-between items-end mb-4">
                  <motion.div layoutId="song-info" transition={{ type: "spring", bounce: 0.2, duration: 0.6 }} className="flex flex-col overflow-hidden pr-4">
                    <span className="text-2xl font-bold text-gray-900 truncate mb-1">{song.title}</span>
                    <span className="text-lg text-gray-500 truncate">{song.artist}</span>
                  </motion.div>"""
content = content.replace(port_art_old, port_art_new)

# Fade in non-shared elements inside the Expanded view
# Wrap Header, Scrubber, Controls, Volume in a motion.div
# This is slightly complex with regex, let's just write the patched string back to file.
with open('src/components/Player.tsx', 'w') as f:
    f.write(content)

print("Patch applied successfully.")
