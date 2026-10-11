import re

with open('src/components/AllArtistsView.tsx', 'r') as f:
    content = f.read()

# Replace the fallback import with our getArtistImage
if 'getArtistImage' not in content:
    content = content.replace("import { Song, Collection } from '../types';", "import { Song, Collection } from '../types';\nimport { getArtistImage } from '../artistImages';")

search = "artistsMap.set(song.artist, { name: song.artist, cover: song.coverUrl, type: 'Artist' });"
replace = "artistsMap.set(song.artist, { name: song.artist, cover: getArtistImage(song.artist), type: 'Artist' });"
content = content.replace(search, replace)

search_album = "artistsMap.set(album.subtitle, { name: album.subtitle, cover: album.coverUrl, type: 'Artist' });"
replace_album = "artistsMap.set(album.subtitle, { name: album.subtitle, cover: getArtistImage(album.subtitle), type: 'Artist' });"
content = content.replace(search_album, replace_album)

with open('src/components/AllArtistsView.tsx', 'w') as f:
    f.write(content)
