with open('src/App.tsx', 'r') as f:
    content = f.read()

old_url = 'url={nowPlaying?.audioUrl || (youtubeId ? `/api/play?videoId=${youtubeId}` : "")}'
new_url = 'url={nowPlaying?.audioUrl || (youtubeId ? `https://www.youtube.com/watch?v=${youtubeId}` : "")}'

content = content.replace(old_url, new_url)

with open('src/App.tsx', 'w') as f:
    f.write(content)
