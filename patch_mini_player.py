import re

with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

# Replace the inner content of the mini-player pill depending on `isMini`.
# Wait, let's find the pill content block.
# We will use AnimatePresence or just ternary to render the cleaner version.

pill_inner_old = """            <div className="flex items-center w-full gap-3">
              <motion.img layoutId="album-art" transition={{ type: "spring", bounce: 0.2, duration: 0.6 }} style={{ borderRadius: 4 }} src={song.coverUrl} onError={(e) => { e.currentTarget.src = FALLBACK_IMG }} className="w-10 h-10 rounded shadow-sm object-cover flex-shrink-0" alt={song.title} />
              <motion.div layoutId="song-info" transition={{ type: "spring", bounce: 0.2, duration: 0.6 }} className="flex flex-col flex-1 min-w-0 justify-center">
                <span className="text-[13px] font-semibold text-gray-900 truncate leading-tight">{song.title}</span>
                <span className="text-[11px] text-gray-500 truncate mt-0.5">{song.artist}</span>
              </motion.div>
              <motion.button initial={{opacity:0}} animate={{opacity:1}} transition={{delay:0.1}} 
                onClick={handleToggleLike}
                className={`transition-colors ${isLiked ? 'text-[#CA5A2C]' : 'text-gray-400 hover:text-gray-700'}`}
              >
                <Heart size={16} className={isLiked ? 'fill-[#CA5A2C]' : ''} />
              </motion.button>
              <motion.button initial={{opacity:0}} animate={{opacity:1}} transition={{delay:0.1}}
                onClick={() => onShare && onShare({ type: 'song', id: song.id, name: song.title })}
                className="mr-2 transition-colors text-gray-400 hover:text-gray-700"
              >
                <Share2 size={16} />
              </motion.button>
              <motion.div initial={{opacity:0}} animate={{opacity:1}} transition={{delay:0.1}} className="flex items-center gap-3 pr-1">
                <button onClick={handleTogglePlay} disabled={isBuffering} className="text-gray-900 hover:scale-105 transition-transform">
                  {isBuffering ? (
                    <div className="w-5 h-5 rounded-full border-2 border-gray-200 border-t-[#CA5A2C] animate-spin"></div>
                  ) : isPlaying ? <Pause size={18} fill="currentColor" /> : <Play size={18} fill="currentColor" />}
                </button>
                <button onClick={handleNextTrack} className="text-gray-700 hover:text-black transition-colors">
                  <SkipForward size={18} fill="currentColor" />
                </button>
                <button onClick={() => (!isMini && setIsCollapsed(false))} className="text-gray-400 hover:text-gray-700 ml-1">
                  <Maximize2 size={16} />
                </button>
              </motion.div>
            </div>"""

pill_inner_new = """            <div className="flex items-center w-full gap-3">
              <motion.img layoutId="album-art" transition={{ type: "spring", bounce: 0.2, duration: 0.6 }} style={{ borderRadius: 4 }} src={song.coverUrl} onError={(e) => { e.currentTarget.src = FALLBACK_IMG }} className="w-10 h-10 rounded shadow-sm object-cover flex-shrink-0" alt={song.title} />
              <motion.div layoutId="song-info" transition={{ type: "spring", bounce: 0.2, duration: 0.6 }} className="flex flex-col flex-1 min-w-0 justify-center">
                <span className="text-[13px] font-semibold text-gray-900 truncate leading-tight">{song.title}</span>
                {isMini ? (
                  <div className="w-full h-1 mt-1 bg-gray-200 rounded-full relative overflow-hidden">
                    <div className="absolute inset-y-0 left-0 bg-[#CA5A2C] rounded-full" style={{ width: `${progressPercent}%` }} />
                  </div>
                ) : (
                  <span className="text-[11px] text-gray-500 truncate mt-0.5">{song.artist}</span>
                )}
              </motion.div>
              
              {!isMini && (
                <>
                  <motion.button initial={{opacity:0}} animate={{opacity:1}} transition={{delay:0.1}} 
                    onClick={handleToggleLike}
                    className={`transition-colors ${isLiked ? 'text-[#CA5A2C]' : 'text-gray-400 hover:text-gray-700'}`}
                  >
                    <Heart size={16} className={isLiked ? 'fill-[#CA5A2C]' : ''} />
                  </motion.button>
                  <motion.button initial={{opacity:0}} animate={{opacity:1}} transition={{delay:0.1}}
                    onClick={() => onShare && onShare({ type: 'song', id: song.id, name: song.title })}
                    className="mr-2 transition-colors text-gray-400 hover:text-gray-700"
                  >
                    <Share2 size={16} />
                  </motion.button>
                </>
              )}
              
              <motion.div initial={{opacity:0}} animate={{opacity:1}} transition={{delay:0.1}} className={`flex items-center gap-3 ${isMini ? 'pr-2 pl-2' : 'pr-1'}`}>
                <button onClick={handleTogglePlay} disabled={isBuffering} className="text-gray-900 hover:scale-105 transition-transform p-1 -m-1">
                  {isBuffering ? (
                    <div className="w-5 h-5 rounded-full border-2 border-gray-200 border-t-[#CA5A2C] animate-spin"></div>
                  ) : isPlaying ? <Pause size={18} fill="currentColor" /> : <Play size={18} fill="currentColor" />}
                </button>
                {!isMini && (
                  <>
                    <button onClick={handleNextTrack} className="text-gray-700 hover:text-black transition-colors p-1 -m-1">
                      <SkipForward size={18} fill="currentColor" />
                    </button>
                    <button onClick={() => (!isMini && setIsCollapsed(false))} className="text-gray-400 hover:text-gray-700 ml-1 p-1 -m-1">
                      <Maximize2 size={16} />
                    </button>
                  </>
                )}
              </motion.div>
            </div>"""

content = content.replace(pill_inner_old, pill_inner_new)

with open('src/components/Player.tsx', 'w') as f:
    f.write(content)

print("Mini player patched")
