import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Replace url={youtubeId ? ... : ""} with url={nowPlaying?.audioUrl || (youtubeId ? ... : "")}
content = content.replace(
    'url={youtubeId ? `https://www.youtube.com/watch?v=${youtubeId}` : ""}',
    'url={nowPlaying?.audioUrl || (youtubeId ? `https://www.youtube.com/watch?v=${youtubeId}` : "")}'
)

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("Updated App.tsx")
