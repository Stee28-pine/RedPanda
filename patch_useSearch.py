import re

with open('src/hooks/useSearch.ts', 'r') as f:
    content = f.read()

search = """        const localMatches = SONGS.filter(s => 
           s.title.toLowerCase().includes(q) || 
           s.artist.toLowerCase().includes(q)
        );"""

replace = """        const localMatches = SONGS.filter(s => 
           s.title.toLowerCase().includes(q) || 
           s.artist.toLowerCase().includes(q) ||
           (s.album && s.album.toLowerCase().includes(q)) ||
           (s.genre && s.genre.toLowerCase().includes(q))
        );"""

content = content.replace(search, replace)

# Let's also change the itunes API call to make it broader, maybe by not using entity=song, but using term. 
# Actually, entity=song works for movies and artists if the result is a song. So it's fine. 
# But just in case, wait, if the user searches for a movie name on iTunes, will entity=song return the songs?
# Yes, because album name is indexed.

with open('src/hooks/useSearch.ts', 'w') as f:
    f.write(content)
