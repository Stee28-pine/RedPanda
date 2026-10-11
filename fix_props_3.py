import re

file = 'src/components/HomeView.tsx'
with open(file, 'r') as f:
    content = f.read()

content = content.replace("?}) {", "}) {")
with open(file, 'w') as f:
    f.write(content)
