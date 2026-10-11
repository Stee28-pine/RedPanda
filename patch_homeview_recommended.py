import re

with open('src/components/HomeView.tsx', 'r') as f:
    content = f.read()

old_logic = """    return recArray.slice(0, 5);
  })();"""

new_logic = """    return recArray.slice(0, 5);
  })();

  const recommendedForYou = (() => {
    if (!hasEnoughHistory || !songs.length) return [];
    
    const userGenres = new Set(userSignals.map(s => s.genre).filter(Boolean));
    const playedIds = new Set(recentlyPlayedHistory?.map(s => s.id) || []);
    
    const genreMatches = songs.filter(s => s.genre && userGenres.has(s.genre));
    
    const unheard = genreMatches.filter(s => !playedIds.has(s.id)).sort(() => 0.5 - Math.random());
    const heard = genreMatches.filter(s => playedIds.has(s.id)).sort(() => 0.5 - Math.random());
    
    let combined = [...unheard, ...heard];
    
    if (combined.length < 5) {
      const otherUnheard = songs.filter(s => !playedIds.has(s.id) && !combined.includes(s)).sort(() => 0.5 - Math.random());
      combined = [...combined, ...otherUnheard];
    }
    
    return combined.slice(0, 5);
  })();"""

content = content.replace(old_logic, new_logic)

old_markup = """        </motion.section>
      ) : ("""

new_markup = """        </motion.section>
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

      {false ? ("""

content = content.replace(old_markup, new_markup)

# Now fix the ending syntax of the false condition
old_end = """        </motion.section>
      )}
      {playlists.length > 0 && ("""

new_end = """      ) : null}
      {playlists.length > 0 && ("""

content = content.replace(old_end, new_end)

with open('src/components/HomeView.tsx', 'w') as f:
    f.write(content)

