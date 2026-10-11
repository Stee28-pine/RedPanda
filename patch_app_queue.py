import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace("      if (prev.some(s => s.id === song.id)) return prev;\n", "")

with open('src/App.tsx', 'w') as f:
    f.write(content)
