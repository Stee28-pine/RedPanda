import re

with open('src/components/TopBar.tsx', 'r') as f:
    content = f.read()

search = """export function TopBar({ 
  onBack, 
  canGoBack,
  searchQuery,
  onSearchChange,
  onToggleSidebar
}: {"""

replace = """export function TopBar({ 
  onBack, 
  canGoBack,
  searchQuery,
  onSearchChange,
  onToggleSidebar,
  onSearchFocus
}: {"""

content = content.replace(search, replace)

with open('src/components/TopBar.tsx', 'w') as f:
    f.write(content)
