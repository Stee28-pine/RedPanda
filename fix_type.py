with open('src/components/Sidebar.tsx', 'r') as f:
    sb = f.read()

sb = sb.replace("  onNavigateStats?: () => void,\n    isOfflineMode?: boolean,", "  onNavigateStats?: () => void,\n  onNavigateDownloads?: () => void,\n  isOfflineMode?: boolean,")

with open('src/components/Sidebar.tsx', 'w') as f:
    f.write(sb)
