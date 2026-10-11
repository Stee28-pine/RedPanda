import re
with open('src/App.tsx', 'r') as f:
    content = f.read()

content = re.sub(
    r'onClick=\{\(\) => setIsSidebarCollapsed\(true\)\}\n\s*\/>\n\s*<div className=\{`fixed',
    r'onClick={() => setIsSidebarCollapsed(true)}\n        />\n      )}\n      <div className={`fixed',
    content
)

with open('src/App.tsx', 'w') as f:
    f.write(content)
print("Done")
