import re

with open('src/components/Sidebar.tsx', 'r') as f:
    sb = f.read()

sb = sb.replace("  onNavigateStats,  \n  currentView,", "  onNavigateStats,\n  onNavigateDownloads,\n  currentView,")
sb = sb.replace("  onNavigateStats, \n  currentView,", "  onNavigateStats,\n  onNavigateDownloads,\n  currentView,")
sb = sb.replace("  onNavigateStats,\n  currentView,", "  onNavigateStats,\n  onNavigateDownloads,\n  currentView,")
sb = sb.replace("  onNavigateStats: () => void,\n  currentView: string,", "  onNavigateStats: () => void,\n  onNavigateDownloads?: () => void,\n  currentView: string,")
sb = sb.replace("  onNavigateStats?: () => void,\n  isOfflineMode", "  onNavigateStats?: () => void,\n  onNavigateDownloads?: () => void,\n  isOfflineMode")

# Just to be safe, brute force replacing the specific function parameters
sb = re.sub(r"onNavigateStats,\s*currentView,", "onNavigateStats, onNavigateDownloads, currentView,", sb)

with open('src/components/Sidebar.tsx', 'w') as f:
    f.write(sb)
