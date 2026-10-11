import re

with open('src/components/ArtistView.tsx', 'r') as f:
    content = f.read()

search = """        <img 
          src={popularSongs[0]?.coverUrl || FALLBACK_IMG} 
          alt={artistName} 
          className="w-full h-full object-cover"
        />"""

replace = """        <img 
          src={getArtistImage(artistName)} 
          alt={artistName} 
          className="w-full h-full object-cover"
        />"""

content = content.replace(search, replace)

with open('src/components/ArtistView.tsx', 'w') as f:
    f.write(content)
