import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace("setIsRightSidebarOpen(prev => !prev);", "setShowRightSidebar(prev => !prev);")

with open('src/App.tsx', 'w') as f:
    f.write(content)
