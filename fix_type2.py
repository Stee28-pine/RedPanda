import re
with open('src/components/Sidebar.tsx', 'r') as f:
    sb = f.read()

sb = re.sub(r"onNavigateStats\?:\s*\(\)\s*=>\s*void,", "onNavigateStats?: () => void, onNavigateDownloads?: () => void,", sb)

with open('src/components/Sidebar.tsx', 'w') as f:
    f.write(sb)
