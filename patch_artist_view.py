import re

with open('src/components/ArtistView.tsx', 'r') as f:
    content = f.read()

# Make sure getArtistImage is imported
if 'getArtistImage' not in content:
    content = content.replace("import { createPortal } from 'react-dom';", "import { createPortal } from 'react-dom';\nimport { getArtistImage } from '../artistImages';")

# Patch image
search_img = '<img src={popularSongs[0]?.coverUrl || topAlbums[0]?.coverUrl} className="w-full h-full object-cover"'
replace_img = '<img src={getArtistImage(artistName)} className="w-full h-full object-cover"'
content = content.replace(search_img, replace_img)

# Fallback in case the search string was slightly different
search_img_2 = '<img src={popularSongs[0]?.coverUrl || topAlbums[0]?.coverUrl || FALLBACK_IMG} className="w-full h-full object-cover"'
content = content.replace(search_img_2, replace_img)

with open('src/components/ArtistView.tsx', 'w') as f:
    f.write(content)

