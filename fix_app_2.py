with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace('onClick={() => setIsSidebarCollapsed(true)}\n        />\n      <div', 'onClick={() => setIsSidebarCollapsed(true)}\n        />\n      )}\n      <div')

with open('src/App.tsx', 'w') as f:
    f.write(content)
print("Done")
