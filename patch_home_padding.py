import re

with open('src/components/HomeView.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    '<div className="px-8 pb-32 pt-6">',
    '<div className="px-4 md:px-8 pb-32 pt-6">'
)

with open('src/components/HomeView.tsx', 'w') as f:
    f.write(content)

with open('src/components/AlbumView.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    '<div className="p-8 pb-32">',
    '<div className="p-4 md:p-8 pb-32">'
)
content = content.replace(
    '<div className="px-6 md:px-10 mt-6">',
    '<div className="px-2 md:px-10 mt-6">'
)

with open('src/components/AlbumView.tsx', 'w') as f:
    f.write(content)

print("Paddings patched")
