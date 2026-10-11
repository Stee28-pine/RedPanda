import re

with open('src/components/RightSidebar.tsx', 'r') as f:
    content = f.read()

# Add layout prop if missing
content = content.replace("<Reorder.Item \n                  key={song.id}", "<Reorder.Item \n                  layout\n                  key={song.id}")

with open('src/components/RightSidebar.tsx', 'w') as f:
    f.write(content)
