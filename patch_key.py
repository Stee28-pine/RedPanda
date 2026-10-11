with open('src/components/HistoryView.tsx', 'r') as f:
    content = f.read()

content = content.replace("key={`${song.id}-${idx}`}", "key={song.id}")

with open('src/components/HistoryView.tsx', 'w') as f:
    f.write(content)
print("Patched key")
