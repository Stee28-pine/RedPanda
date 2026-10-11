import re

with open('src/components/Sidebar.tsx', 'r') as f:
    sidebar = f.read()

# Add to props
props_search = "  onNavigateStats,\n  currentView,"
props_replace = "  onNavigateStats,\n  onNavigateDownloads,\n  currentView,"
sidebar = sidebar.replace(props_search, props_replace)

type_search = "  onNavigateStats: () => void,\n  currentView: string,"
type_replace = "  onNavigateStats: () => void,\n  onNavigateDownloads?: () => void,\n  currentView: string,"
sidebar = sidebar.replace(type_search, type_replace)

# Add Download import
import_search = "import { Home, Mic2, Disc, Music, Plus, Heart, Star } from 'lucide-react';"
import_replace = "import { Home, Mic2, Disc, Music, Plus, Heart, Star, Download } from 'lucide-react';"
sidebar = sidebar.replace(import_search, import_replace)

# Add to nav
nav_search = """          <NavItem icon={<Home size={18} />} label="Home" active={currentView === 'home'} onClick={onNavigateHome} isCollapsed={isCollapsed} activeIconColor="text-[#fe5f64]" />
          <NavItem icon={<BarChart3 size={18} />} label="Stats" active={currentView === 'stats'} onClick={onNavigateStats} isCollapsed={isCollapsed} activeIconColor="text-[#fe5f64]" />"""
nav_replace = """          <NavItem icon={<Home size={18} />} label="Home" active={currentView === 'home'} onClick={onNavigateHome} isCollapsed={isCollapsed} activeIconColor="text-[#fe5f64]" />
          <NavItem icon={<Download size={18} />} label="Downloads" active={currentView === 'downloads'} onClick={onNavigateDownloads} isCollapsed={isCollapsed} activeIconColor="text-[#fe5f64]" />
          <NavItem icon={<BarChart3 size={18} />} label="Stats" active={currentView === 'stats'} onClick={onNavigateStats} isCollapsed={isCollapsed} activeIconColor="text-[#fe5f64]" />"""
sidebar = sidebar.replace(nav_search, nav_replace)

# In order to respect "when user click on download it must show in Offline Mode" 
# This was already covered in App.tsx by making the toggle Offline mode work,
# but the prompt specifically says:
# "ALSO CHECK OFFLINE OPTION IS NOT WORKING MAKE IT LIKE THAT WHEN USER CLICK ON DOWNLOAD IT MUST SHOW IN Offline Mode"
# Let's fix App.tsx offline mode skip logic and make sure the Offline Mode toggle is clearly visible.

with open('src/components/Sidebar.tsx', 'w') as f:
    f.write(sidebar)
