import re

with open('src/components/HomeView.tsx', 'r') as f:
    content = f.read()

# Replace the useContent destructuring
old_use_content = '  const { mixes, recentlyPlayed, albums, isLoading } = useContent();'
new_use_content = '''  const { mixes, albums, songs, isLoading } = useContent();
  
  // Calculate dynamic "Made For You" based on recentlyPlayedHistory
  const hasEnoughHistory = recentlyPlayedHistory && recentlyPlayedHistory.length >= 3;
  
  const betterMixes = (() => {
    if (!hasEnoughHistory || !songs.length) return mixes; // fallback
    
    // Find top genres and artists from history
    const genres = recentlyPlayedHistory.map(s => s.genre).filter(Boolean);
    const artists = recentlyPlayedHistory.map(s => s.artist).filter(Boolean);
    
    const uniqueGenres = Array.from(new Set(genres));
    const uniqueArtists = Array.from(new Set(artists));
    
    const customMixes: Collection[] = [];
    
    // Create an artist mix
    if (uniqueArtists.length > 0) {
      const topArtist = uniqueArtists[0];
      const artistSongs = songs.filter(s => s.artist.includes(topArtist) || topArtist.includes(s.artist));
      if (artistSongs.length > 0) {
        customMixes.push({
          id: 'custom-m1',
          type: 'mix',
          title: `${topArtist} Mix`,
          subtitle: 'Made for you',
          coverUrl: artistSongs[0].coverUrl,
          songs: artistSongs.length >= 5 ? artistSongs : [...artistSongs, ...songs.slice(0, 10)]
        });
      }
    }
    
    // Create genre mixes based on user's recent history
    uniqueGenres.slice(0, 3).forEach((genre, i) => {
      if (!genre) return;
      const genreSongs = songs.filter(s => s.genre && s.genre.includes(genre));
      if (genreSongs.length > 0) {
        customMixes.push({
          id: `custom-g${i}`,
          type: 'mix',
          title: `${genre} Mix`,
          subtitle: 'Because you listened to ' + genre,
          coverUrl: genreSongs[0].coverUrl,
          songs: genreSongs.length >= 5 ? genreSongs : [...genreSongs, ...songs.slice(10, 20)]
        });
      }
    });
    
    // Fill the rest with general mixes if needed
    const combined = [...customMixes, ...mixes];
    
    // Ensure unique IDs
    const finalMixes = [];
    const seenIds = new Set();
    for (const mix of combined) {
      if (!seenIds.has(mix.id) && finalMixes.length < 5) {
        finalMixes.push(mix);
        seenIds.add(mix.id);
      }
    }
    
    return finalMixes;
  })();
'''

content = content.replace(old_use_content, new_use_content)

# Now, conditionally render Made For You and Recently Played
old_made_for_you = '''      <motion.section 
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
          {mixes.map((mix, i) => (
            <motion.div 
              key={mix.id}
              variants={{
                hidden: { opacity: 0, y: 15, scale: 0.95 },
                show: { opacity: 1, y: 0, scale: 1, transition: { type: "spring", stiffness: 200, damping: 20 } }
              }}
              whileHover={{ y: -6, scale: 1.03, transition: { duration: 0.2 } }}
              className="cursor-pointer group"
              onClick={() => onCollectionClick(albums[0] || albums[0])} // Routing everything to the one album we have data for
            >
              <div className="aspect-square rounded-2xl overflow-hidden mb-3 shadow-[0_8px_20px_rgb(0,0,0,0.12)]">
                <img 
                  src={mix.coverUrl} 
                  onError={(e) => { e.currentTarget.src = FALLBACK_IMG }}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" 
                  alt={mix.title} 
                />
              </div>
              <h3 className="font-bold text-gray-900 truncate mb-1">{mix.title}</h3>
              <p className="text-sm text-gray-500 truncate">{mix.subtitle}</p>
            </motion.div>
          ))}
        </div>
      </motion.section>'''

new_made_for_you = '''      {hasEnoughHistory && (
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
          {betterMixes.map((mix, i) => (
            <motion.div 
              key={mix.id}
              variants={{
                hidden: { opacity: 0, y: 15, scale: 0.95 },
                show: { opacity: 1, y: 0, scale: 1, transition: { type: "spring", stiffness: 200, damping: 20 } }
              }}
              whileHover={{ y: -6, scale: 1.03, transition: { duration: 0.2 } }}
              className="cursor-pointer group"
              onClick={() => onCollectionClick(mix)} 
            >
              <div className="aspect-square rounded-2xl overflow-hidden mb-3 shadow-[0_8px_20px_rgb(0,0,0,0.12)]">
                <img 
                  src={mix.coverUrl} 
                  onError={(e) => { e.currentTarget.src = FALLBACK_IMG }}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" 
                  alt={mix.title} 
                />
              </div>
              <h3 className="font-bold text-gray-900 truncate mb-1">{mix.title}</h3>
              <p className="text-sm text-gray-500 truncate">{mix.subtitle}</p>
            </motion.div>
          ))}
        </div>
      </motion.section>
      )}'''
content = content.replace(old_made_for_you, new_made_for_you)


old_recently_played = '''      <motion.section 
        className="mb-12"
        initial="hidden"
        animate="show"
        variants={{
          hidden: { opacity: 0 },
          show: { opacity: 1, transition: { staggerChildren: 0.08, delayChildren: 0.2 } }
        }}
      >
        <h2 className="text-[22px] font-bold text-gray-900 mb-5 tracking-tight">Recently Played</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
          {recentlyPlayed.length > 0 ? recentlyPlayed.map((song) => (
            <motion.div 
              key={song.id}
              variants={{
                hidden: { opacity: 0, y: 15, scale: 0.95 },
                show: { opacity: 1, y: 0, scale: 1, transition: { type: "spring", stiffness: 200, damping: 20 } }
              }}
              whileHover={{ y: -6, scale: 1.03, transition: { duration: 0.2 } }}
              className="cursor-pointer group"
              onClick={() => onPlaySong?.(song, { songs: recentlyPlayed })}
            >
              <div className="aspect-square rounded-2xl overflow-hidden mb-3 shadow-[0_8px_20px_rgb(0,0,0,0.12)] relative">
                <img 
                  src={song.coverUrl} 
                  onError={(e) => { e.currentTarget.src = FALLBACK_IMG }}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" 
                  alt={song.title} 
                />
                <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                  <div className="w-12 h-12 bg-[#fe5f64] rounded-full flex items-center justify-center shadow-lg transform scale-75 group-hover:scale-100 transition-transform">
                    <Play fill="white" className="w-6 h-6 text-white ml-1" />
                  </div>
                </div>
              </div>
              <h3 className="font-bold text-gray-900 truncate mb-1">{song.title}</h3>
              <p className="text-sm text-gray-500 truncate">{song.artist}</p>
            </motion.div>
          )) : recentlyPlayed.map((item, i) => (
            <div key={i} className="animate-pulse">
              <div className="aspect-square bg-gray-200 rounded-2xl mb-3"></div>
              <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div className="h-3 bg-gray-200 rounded w-1/2"></div>
            </div>
          ))}
        </div>
      </motion.section>'''

new_recently_played = '''      {hasEnoughHistory && (
      <motion.section 
        className="mb-12"
        initial="hidden"
        animate="show"
        variants={{
          hidden: { opacity: 0 },
          show: { opacity: 1, transition: { staggerChildren: 0.08, delayChildren: 0.2 } }
        }}
      >
        <h2 className="text-[22px] font-bold text-gray-900 mb-5 tracking-tight">Recently Played</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
          {recentlyPlayedHistory.map((song, idx) => (
            <motion.div 
              key={`${song.id}-${idx}`}
              variants={{
                hidden: { opacity: 0, y: 15, scale: 0.95 },
                show: { opacity: 1, y: 0, scale: 1, transition: { type: "spring", stiffness: 200, damping: 20 } }
              }}
              whileHover={{ y: -6, scale: 1.03, transition: { duration: 0.2 } }}
              className="cursor-pointer group"
              onClick={() => onPlaySong?.(song, { songs: recentlyPlayedHistory })}
            >
              <div className="aspect-square rounded-2xl overflow-hidden mb-3 shadow-[0_8px_20px_rgb(0,0,0,0.12)] relative">
                <img 
                  src={song.coverUrl} 
                  onError={(e) => { e.currentTarget.src = FALLBACK_IMG }}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" 
                  alt={song.title} 
                />
                <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                  <div className="w-12 h-12 bg-[#fe5f64] rounded-full flex items-center justify-center shadow-lg transform scale-75 group-hover:scale-100 transition-transform">
                    <Play fill="white" className="w-6 h-6 text-white ml-1" />
                  </div>
                </div>
              </div>
              <h3 className="font-bold text-gray-900 truncate mb-1">{song.title}</h3>
              <p className="text-sm text-gray-500 truncate">{song.artist}</p>
            </motion.div>
          ))}
        </div>
      </motion.section>
      )}'''

content = content.replace(old_recently_played, new_recently_played)

with open('src/components/HomeView.tsx', 'w') as f:
    f.write(content)
