import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace("      </main>\n      \n      <AnimatePresence>\n        {showRightSidebar", "      <AnimatePresence>\n        {showRightSidebar")

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("Fixed App.tsx")
