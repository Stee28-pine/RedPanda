import re

with open('src/hooks/useSearch.ts', 'r') as f:
    content = f.read()

search = """        const itunesSongs: Song[] = data.results.map((track: any) => ({
          id: track.trackId.toString(),
          title: track.trackName,
          artist: track.artistName,
          album: track.collectionName,
          duration: formatDuration(track.trackTimeMillis),
          durationSeconds: Math.floor((track.trackTimeMillis || 0) / 1000),
          coverUrl: track.artworkUrl100?.replace('100x100bb', '400x400bb') || '',
        }));
                
        // Merge without duplicates
        const merged = [...localMatches];
        const existingIds = new Set(localMatches.map(s => s.id));
        
        for (const song of itunesSongs) {
           // Basic title+artist duplicate check since iTunes IDs won't match local IDs
           const isDuplicate = merged.some(s => s.title === song.title && s.artist === song.artist);
           if (!isDuplicate && !existingIds.has(song.id)) {
              merged.push(song);
              existingIds.add(song.id);
           }
        }
        
        setResults(merged);"""

replace = """        const itunesSongs: Song[] = data.results.map((track: any) => ({
          id: track.trackId?.toString() || Math.random().toString(),
          title: track.trackName,
          artist: track.artistName,
          album: track.collectionName || 'Single',
          duration: formatDuration(track.trackTimeMillis),
          durationSeconds: Math.floor((track.trackTimeMillis || 0) / 1000),
          coverUrl: track.artworkUrl100?.replace('100x100bb', '400x400bb') || '',
          audioUrl: track.previewUrl
        }));
        
        let ytSongs: Song[] = [];
        try {
           const ytRes = await fetch(`/api/search-tracks?q=${encodeURIComponent(query)}`);
           const ytData = await ytRes.json();
           if (ytData.results) {
              ytSongs = ytData.results;
           }
        } catch(e) {
           console.error("YT Search failed", e);
        }
                
        // Merge without duplicates
        const merged = [...localMatches];
        const existingIds = new Set(localMatches.map(s => s.id));
        
        for (const song of [...itunesSongs, ...ytSongs]) {
           // Basic title+artist duplicate check since iTunes IDs won't match local IDs
           const isDuplicate = merged.some(s => 
              s.title.toLowerCase() === song.title.toLowerCase() && 
              s.artist.toLowerCase() === song.artist.toLowerCase()
           );
           if (!isDuplicate && !existingIds.has(song.id)) {
              merged.push(song);
              existingIds.add(song.id);
           }
        }
        
        setResults(merged);"""

content = content.replace(search, replace)
# Also change the iTunes search limit from 30 to 50
content = content.replace('limit=30', 'limit=50')

with open('src/hooks/useSearch.ts', 'w') as f:
    f.write(content)
