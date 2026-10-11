import re

with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

content = re.sub(r'  if \(\!song\) \{\n    return \(\n    \);\n  \}', '  if (!song) {\n    return null;\n  }', content)

with open('src/components/Player.tsx', 'w') as f:
    f.write(content)
