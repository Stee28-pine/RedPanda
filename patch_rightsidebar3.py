import re

with open('src/components/RightSidebar.tsx', 'r') as f:
    content = f.read()

content = content.replace("split('\n')", "split('\\n')")

with open('src/components/RightSidebar.tsx', 'w') as f:
    f.write(content)
