with open('src/App.tsx', 'r') as f:
    content = f.read()

search = "config={{ file: { forceAudio: true, attributes: { crossOrigin: 'anonymous' } } }}"
replace = "config={{ youtube: { playerVars: { playsinline: 1, autoplay: 1 } }, file: { forceAudio: true, attributes: { crossOrigin: 'anonymous' } } }}"

content = content.replace(search, replace)

with open('src/App.tsx', 'w') as f:
    f.write(content)
