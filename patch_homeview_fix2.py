import re

with open('src/components/HomeView.tsx', 'r') as f:
    content = f.read()

# Make the personalization more aggressive and skip English fallback if they have history
old_logic = """    // Convert to array and filter out songs already played a lot, or just show them
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

new_logic = """    let recArray = Array.from(recommendations);
    
    // Shuffle the recommendations slightly to keep it fresh
    recArray = recArray.sort(() => 0.5 - Math.random());
    
    // Pad with other popular non-English / diverse songs if we don't have enough
    if (recArray.length < 5) {
      // Find songs that match the top genres, but weren't added by artist
      const moreGenreSongs = songs.filter(s => 
        !recommendations.has(s) && 
        topGenres.some(g => s.genre?.includes(g))
      ).sort(() => 0.5 - Math.random());
      
      recArray = [...recArray, ...moreGenreSongs];
      
      // If STILL not enough (e.g. they only played 1 Indian song and there are no other Indian songs?),
      // Then fallback to songs that share a similar non-English tag or just random songs
      if (recArray.length < 5) {
        const unused = songs.filter(s => !recArray.includes(s)).sort(() => 0.5 - Math.random());
        recArray = [...recArray, ...unused];
      }
    }
    
    return recArray.slice(0, 5);
  })();"""

content = content.replace(old_logic, new_logic)

with open('src/components/HomeView.tsx', 'w') as f:
    f.write(content)

