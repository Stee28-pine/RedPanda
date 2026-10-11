import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace("setToast({ message: `Added to ${p.title}` });", "showToast(`Added to ${p.title}`);")

with open('src/App.tsx', 'w') as f:
    f.write(content)

