import re

with open('src/components/HomeView.tsx', 'r') as f:
    content = f.read()

old_logic = """  // Calculate dynamic "Made For You" based on recentlyPlayedHistory
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
  })();"""

new_logic = """  // Threshold for personalizing recommendations
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

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open('src/components/HomeView.tsx', 'w') as f:
        f.write(content)
    print("Replaced successfully!")
else:
    print("Could not find the exact old_logic. Writing diff check.")

