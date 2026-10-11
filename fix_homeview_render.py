import re

with open('src/components/HomeView.tsx', 'r') as f:
    content = f.read()

# I will find everything from `<div className="px-4 md:px-8 pb-32 pt-6">` up to `      <AnimatePresence>`

start_marker = '<div className="px-4 md:px-8 pb-32 pt-6">'
end_marker = '<AnimatePresence>'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_render = """<div className="px-4 md:px-8 pb-32 pt-6">
      {hasEnoughHistory ? (
        <motion.section 
          className="mb-12"
          initial="hidden"
          animate="show"
          variants={{
            hidden: { opacity: 0 },
            show: { opacity: 1, transition: { staggerChildren: 0.08 } }
          }}
        >
          <h2 className="text-[22px] font-bold text-gray-900 mb-5 tracking-tight">Made for You</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
            {recommendedSongs.map((song) => (
              <motion.div 
                key={song.id}
                variants={{
                  hidden: { opacity: 0, y: 15, scale: 0.95 },
                  show: { opacity: 1, y: 0, scale: 1, transition: { type: "spring", stiffness: 200, damping: 20 } }
                }}
                whileHover={{ y: -6, scale: 1.03, transition: { duration: 0.2 } }}
                className="cursor-pointer group relative"
                onClick={() => onPlaySong?.(song, { songs: recommendedSongs })}
              >
                <div className="aspect-square rounded-2xl overflow-hidden mb-3 shadow-[0_8px_20px_rgb(0,0,0,0.12)] relative">
                  <img 
                    src={song.coverUrl} 
                    onError={(e) => { e.currentTarget.src = FALLBACK_IMG }}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" 
                    alt={song.title} 
                  />
                  <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <div className="w-10 h-10 rounded-full bg-white/90 backdrop-blur shadow-sm flex items-center justify-center pl-1 text-gray-900">
                      <Play size={20} fill="currentColor" />
                    </div>
                  </div>
                </div>
                <h3 className="font-semibold text-gray-900 truncate leading-tight tracking-tight">{song.title}</h3>
                <p className="text-[13px] font-medium text-gray-500 truncate mt-0.5">{song.artist}</p>
              </motion.div>
            ))}
          </div>
        </motion.section>
      ) : (
        <motion.section 
          className="mb-12"
          initial="hidden"
          animate="show"
          variants={{
            hidden: { opacity: 0 },
            show: { opacity: 1, transition: { staggerChildren: 0.08 } }
          }}
        >
          <h2 className="text-[22px] font-bold text-gray-900 mb-5 tracking-tight">Trending Now</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
            {songs.slice(0, 5).map((song) => (
              <motion.div 
                key={song.id}
                variants={{
                  hidden: { opacity: 0, y: 15, scale: 0.95 },
                  show: { opacity: 1, y: 0, scale: 1, transition: { type: "spring", stiffness: 200, damping: 20 } }
                }}
                whileHover={{ y: -6, scale: 1.03, transition: { duration: 0.2 } }}
                className="cursor-pointer group"
                onClick={() => onPlaySong?.(song, { songs })}
              >
                <div className="aspect-square rounded-2xl overflow-hidden mb-3 shadow-[0_8px_20px_rgb(0,0,0,0.12)] relative">
                  <img 
                    src={song.coverUrl} 
                    onError={(e) => { e.currentTarget.src = FALLBACK_IMG }}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" 
                    alt={song.title} 
                  />
                  <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <div className="w-10 h-10 rounded-full bg-white/90 backdrop-blur shadow-sm flex items-center justify-center pl-1 text-gray-900">
                      <Play size={20} fill="currentColor" />
                    </div>
                  </div>
                </div>
                <h3 className="font-semibold text-gray-900 truncate leading-tight tracking-tight">{song.title}</h3>
                <p className="text-[13px] font-medium text-gray-500 truncate mt-0.5">{song.artist}</p>
              </motion.div>
            ))}
          </div>
        </motion.section>
      )}

      {hasEnoughHistory && recommendedForYou.length > 0 && (
        <motion.section 
          className="mb-12"
          initial="hidden"
          animate="show"
          variants={{
            hidden: { opacity: 0 },
            show: { opacity: 1, transition: { staggerChildren: 0.08 } }
          }}
        >
          <h2 className="text-[22px] font-bold text-gray-900 mb-5 tracking-tight">Recommended for You</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
            {recommendedForYou.map((song) => (
              <motion.div 
                key={song.id}
                variants={{
                  hidden: { opacity: 0, y: 15, scale: 0.95 },
                  show: { opacity: 1, y: 0, scale: 1, transition: { type: "spring", stiffness: 200, damping: 20 } }
                }}
                whileHover={{ y: -6, scale: 1.03, transition: { duration: 0.2 } }}
                className="cursor-pointer group relative"
                onClick={() => onPlaySong?.(song, { songs: recommendedForYou })}
              >
                <div className="aspect-square rounded-2xl overflow-hidden mb-3 shadow-[0_8px_20px_rgb(0,0,0,0.12)] relative">
                  <img 
                    src={song.coverUrl} 
                    onError={(e) => { e.currentTarget.src = FALLBACK_IMG }}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" 
                    alt={song.title} 
                  />
                  <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <div className="w-10 h-10 rounded-full bg-white/90 backdrop-blur shadow-sm flex items-center justify-center pl-1 text-gray-900">
                      <Play size={20} fill="currentColor" />
                    </div>
                  </div>
                </div>
                <h3 className="font-semibold text-gray-900 truncate leading-tight tracking-tight">{song.title}</h3>
                <p className="text-[13px] font-medium text-gray-500 truncate mt-0.5">{song.artist}</p>
              </motion.div>
            ))}
          </div>
        </motion.section>
      )}

      {playlists.length > 0 && (
      <motion.section 
        className="mb-12"
        initial="hidden"
        animate="show"
        variants={{
          hidden: { opacity: 0 },
          show: { opacity: 1, transition: { staggerChildren: 0.08, delayChildren: 0.1 } }
        }}
      >
        <h2 className="text-[22px] font-bold text-gray-900 mb-5 tracking-tight">Your Playlists</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
          {playlists.map((playlist) => (
            <motion.div 
              key={playlist.id}
              variants={{
                hidden: { opacity: 0, y: 15, scale: 0.95 },
                show: { opacity: 1, y: 0, scale: 1, transition: { type: "spring", stiffness: 200, damping: 20 } }
              }}
              whileHover={{ y: -6, scale: 1.03, transition: { duration: 0.2 } }}
              className="cursor-pointer group relative"
              onClick={() => onCollectionClick(playlist)}
              onContextMenu={(e) => handleContextMenu(e, playlist.id)}
              onDoubleClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                handleContextMenu(e, playlist.id);
              }}
            >
              <div className="aspect-square rounded-2xl overflow-hidden mb-3 shadow-[0_8px_20px_rgb(0,0,0,0.12)] bg-gray-100 flex items-center justify-center relative">
                {playlist.songs.length > 0 ? (
                   <img src={playlist.songs[0].coverUrl} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" alt={playlist.title} />
                ) : (
                   <div className="w-full h-full bg-gradient-to-br from-gray-200 to-gray-300" />
                )}
                <div className="absolute bottom-2 right-2 bg-black/60 backdrop-blur-sm text-white text-[10px] font-bold px-2 py-1 rounded-md">
                   {playlist.songs.length}
                </div>
              </div>
              <h3 className="font-semibold text-gray-900 truncate leading-tight tracking-tight">{playlist.title}</h3>
              <p className="text-[13px] font-medium text-gray-500 truncate mt-0.5">Playlist</p>
            </motion.div>
          ))}
        </div>
      </motion.section>
      )}

      """
    
    content = content[:start_idx] + new_render + content[end_idx:]

with open('src/components/HomeView.tsx', 'w') as f:
    f.write(content)

