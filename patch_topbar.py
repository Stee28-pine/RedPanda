import re

with open('src/components/TopBar.tsx', 'r') as f:
    content = f.read()

search = """  onSearchChange?: (q: string) => void;
  onToggleSidebar?: () => void;
}) {"""

replace = """  onSearchChange?: (q: string) => void;
  onSearchFocus?: () => void;
  onToggleSidebar?: () => void;
}) {"""

content = content.replace(search, replace)

search2 = """          onChange={(e) => onSearchChange?.(e.target.value)}
          placeholder="Search for songs, artists, or albums to play\""""

replace2 = """          onChange={(e) => onSearchChange?.(e.target.value)}
          onFocus={() => onSearchFocus?.()}
          placeholder="Search for songs, artists, or albums to play\""""

content = content.replace(search2, replace2)

with open('src/components/TopBar.tsx', 'w') as f:
    f.write(content)
