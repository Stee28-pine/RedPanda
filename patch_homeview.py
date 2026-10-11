import re

with open('src/components/HomeView.tsx', 'r') as f:
    content = f.read()

# Update props interface
old_props = """  onDeletePlaylist?: (id: string) => void;
  onMergePlaylist?: (targetId: string, sourceId: string) => void;
  recentlyPlayedHistory?: Song[];
}) {"""
new_props = """  onDeletePlaylist?: (id: string) => void;
  onMergePlaylist?: (targetId: string, sourceId: string) => void;
  recentlyPlayedHistory?: Song[];
  likedSongs?: Song[];
}) {"""
content = content.replace(old_props, new_props)

# Update logic
old_logic = """  const { mixes, albums, songs, isLoading } = useContent();
  
  // Threshold for personalizing recommendations
  const HISTORY_THRESHOLD = 4;
  const hasEnoughHistory = recentlyPlayedHistory && recentlyPlayedHistory.length >= HISTORY_THRESHOLD;
  
  const betterMixes = (() => {
    if (!hasEnoughHistory || !songs.length) return mixes; // fallback
    
    // Advanced Weighting Algorithm: count frequencies of genres and artists,
    // weighting more recently played items higher.
    const genreCounts: Record<string, number> = {};
    const artistCounts: Record<string, number> = {};
    
    recentlyPlayedHistory.forEach((s, idx) => {
      // More recent items (lower index) get higher weights.
      // e.g. index 0 gets 1.0, index 1 gets 0.9, etc.
      const weight = Math.max(0.2, 1 - (idx * 0.1)); 
      
      if (s.genre) {
        genreCounts[s.genre] = (genreCounts[s.genre] || 0) + weight;
      }
      if (s.artist) {
        artistCounts[s.artist] = (artistCounts[s.artist] || 0) + weight;
      }
    });

    const sortedGenres = Object.entries(genreCounts)
      .sort((a, b) => b[1] - a[1])
      .map(entry => entry[0]);
      
    const sortedArtists = Object.entries(artistCounts)
      .sort((a, b) => b[1] - a[1])
      .map(entry => entry[0]);
    
    const customMixes: Collection[] = [];
    
    // 1. Top Artist Mix
    if (sortedArtists.length > 0) {
      const topArtist = sortedArtists[0];
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

    // 2. Second Top Artist Mix (if applicable)
    if (sortedArtists.length > 1) {
      const secondArtist = sortedArtists[1];
      const secondArtistSongs = songs.filter(s => s.artist.includes(secondArtist) || secondArtist.includes(s.artist));
      if (secondArtistSongs.length >= 3) {
        customMixes.push({
          id: 'custom-m2',
          type: 'mix',
          title: `${secondArtist} Essentials`,
          subtitle: 'Based on your history',
          coverUrl: secondArtistSongs[0].coverUrl,
          songs: secondArtistSongs.length >= 5 ? secondArtistSongs : [...secondArtistSongs, ...songs.slice(10, 20)]
        });
      }
    }
    
    // 3. Top Genre Mixes
    sortedGenres.slice(0, 3).forEach((genre, i) => {
      if (!genre) return;
      const genreSongs = songs.filter(s => s.genre && s.genre.includes(genre));
      if (genreSongs.length > 0) {
        customMixes.push({
          id: `custom-g${i}`,
          type: 'mix',
          title: `${genre} Mix`,
          subtitle: 'Because you listened to ' + genre,
          coverUrl: genreSongs[0].coverUrl,
          songs: genreSongs.length >= 5 ? genreSongs : [...genreSongs, ...songs.slice(20, 30)]
        });
      }
    });
    
    // Fill the rest with general mixes if needed to maintain layout
    const combined = [...customMixes, ...mixes];
    
    // Ensure unique IDs and exact 5 limit for grid
    const finalMixes = [];
    const seenIds = new Set();
    for (const mix of combined) {
      if (!seenIds.has(mix.id) && finalMixes.length < 5) {
        finalMixes.push(mix);
        seenIds.add(mix.id);
      }
    }
    
    return finalMixes;
  })();"""

new_logic = """  const { mixes, albums, songs, isLoading } = useContent();
  
  // Use both history and liked songs for personalization
  const userSignals = [...(recentlyPlayedHistory || []), ...(likedSongs || [])];
  const hasEnoughHistory = userSignals.length > 0;
  
  const recommendedSongs = (() => {
    if (!hasEnoughHistory || !songs.length) return songs.slice(0, 5); // Fallback to trending
    
    const genreCounts: Record<string, number> = {};
    const artistCounts: Record<string, number> = {};
    
    userSignals.forEach((s, idx) => {
      const weight = Math.max(0.5, 1 - (idx * 0.05)); 
      if (s.genre) genreCounts[s.genre] = (genreCounts[s.genre] || 0) + weight;
      if (s.artist) artistCounts[s.artist] = (artistCounts[s.artist] || 0) + weight;
    });

    const topGenres = Object.entries(genreCounts).sort((a, b) => b[1] - a[1]).map(e => e[0]);
    const topArtists = Object.entries(artistCounts).sort((a, b) => b[1] - a[1]).map(e => e[0]);
    
    const recommendations = new Set<Song>();
    
    // 1. Add songs by top artists
    topArtists.slice(0, 3).forEach(artist => {
      songs.filter(s => s.artist.includes(artist)).forEach(s => recommendations.add(s));
    });
    
    // 2. Add songs from top genres
    topGenres.slice(0, 2).forEach(genre => {
      songs.filter(s => s.genre?.includes(genre)).forEach(s => recommendations.add(s));
    });
    
    // Convert to array and filter out songs already played a lot, or just show them
    let recArray = Array.from(recommendations);
    
    // Shuffle the recommendations slightly to keep it fresh
    recArray = recArray.sort(() => 0.5 - Math.random());
    
    // Pad with other popular non-English / diverse songs if we don't have enough
    if (recArray.length < 5) {
      const unused = songs.filter(s => !recommendations.has(s)).sort(() => 0.5 - Math.random());
      recArray = [...recArray, ...unused];
    }
    
    return recArray.slice(0, 5);
  })();"""

content = content.replace(old_logic, new_logic)

# Replace the markup rendering 'betterMixes' with 'recommendedSongs'
old_markup = """      {hasEnoughHistory ? (
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
                className="cursor-pointer group relative"
                onClick={() => onCollectionClick(mix)}
              >
                <div className="aspect-square rounded-2xl overflow-hidden mb-3 shadow-[0_8px_20px_rgb(0,0,0,0.12)] bg-gray-100 flex items-center justify-center relative">
                  <img 
                    src={mix.coverUrl} 
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" 
                    alt={mix.title} 
                  />
                </div>
                <h3 className="font-semibold text-gray-900 truncate leading-tight tracking-tight">{mix.title}</h3>
                <p className="text-[13px] font-medium text-gray-500 truncate mt-0.5">{mix.subtitle}</p>
              </motion.div>
            ))}
          </div>
        </motion.section>
      ) : ("""

new_markup = """      {hasEnoughHistory ? (
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
                className="cursor-pointer group"
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
      ) : ("""

content = content.replace(old_markup, new_markup)

with open('src/components/HomeView.tsx', 'w') as f:
    f.write(content)

