import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

old_rp = """    setRecentlyPlayed(prev => {
      const filtered = prev.filter(s => s.id !== song.id);
      return [song, ...filtered].slice(0, 10);
    });"""

new_rp = """    setRecentlyPlayed(prev => {
      const filtered = prev.filter(s => s.id !== song.id);
      return [song, ...filtered]; // Unbounded history!
    });"""

if old_rp in content:
    content = content.replace(old_rp, new_rp)
    with open('src/App.tsx', 'w') as f:
        f.write(content)
    print("Patched setRecentlyPlayed")
else:
    print("Could not find old_rp")

