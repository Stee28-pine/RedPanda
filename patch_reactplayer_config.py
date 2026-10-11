import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace("controls={false} config={{ youtube: { playerVars: { origin: typeof window !== 'undefined' ? window.location.origin : '' } } }}", "controls={false}")

with open('src/App.tsx', 'w') as f:
    f.write(content)
