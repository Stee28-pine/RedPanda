import re

with open('src/components/Sidebar.tsx', 'r') as f:
    content = f.read()

# Replace icon import
content = content.replace("Download,", "History, Download,")
content = content.replace("onNavigateDownloads", "onNavigateHistory")
content = content.replace('label="Downloads"', 'label="History"')
content = content.replace('<Download size={18} />', '<History size={18} />')
content = content.replace("currentView === 'downloads'", "currentView === 'history'")

with open('src/components/Sidebar.tsx', 'w') as f:
    f.write(content)
print("Sidebar patched")
