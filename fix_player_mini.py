import re

with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

# Add isMini to PlayerProps
content = re.sub(
    r'  onSeek: \(time: number\) => void;\n}',
    '  onSeek: (time: number) => void;\n  isMini?: boolean;\n}',
    content
)

content = re.sub(
    r'  onSeek\n}: PlayerProps\) \{',
    '  onSeek,\n  isMini = false\n}: PlayerProps) {',
    content
)

# Force isCollapsed if isMini is true
# We can change the render logic:
# `isCollapsed` is currently local state. We can derive `effectiveIsCollapsed = isCollapsed || isMini`
content = content.replace(
    'isCollapsed ? (',
    '(isCollapsed || isMini) ? ('
)
content = content.replace(
    'setIsCollapsed(false)',
    '(!isMini && setIsCollapsed(false))'
)

with open('src/components/Player.tsx', 'w') as f:
    f.write(content)
print("done")
