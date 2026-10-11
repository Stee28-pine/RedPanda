with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    'onReorder={handleReorderQueue} />\n\n      <Player',
    'onReorder={handleReorderQueue} />\n      )}\n\n      <Player'
)

with open('src/App.tsx', 'w') as f:
    f.write(content)
print("Done")
