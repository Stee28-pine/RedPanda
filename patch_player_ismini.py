import re

with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    '{(isCollapsed || isMini) ? (',
    '{(isCollapsed || (isMini && !isMobile)) ? ('
)

with open('src/components/Player.tsx', 'w') as f:
    f.write(content)
print("done")
