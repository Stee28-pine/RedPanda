import re

with open('src/hooks/useRecentSearches.ts', 'r') as f:
    content = f.read()

content = content.replace("slice(0, 10)", "slice(0, 5)")

with open('src/hooks/useRecentSearches.ts', 'w') as f:
    f.write(content)
