import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

search = """          onSearchChange={handleSearchChange}
          onToggleSidebar={() => setIsSidebarCollapsed(!isSidebarCollapsed)}"""

replace = """          onSearchChange={handleSearchChange}
          onSearchFocus={() => setCurrentView('search')}
          onToggleSidebar={() => setIsSidebarCollapsed(!isSidebarCollapsed)}"""

content = content.replace(search, replace)

with open('src/App.tsx', 'w') as f:
    f.write(content)
