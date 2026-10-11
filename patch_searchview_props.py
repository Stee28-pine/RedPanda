import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

search = """                  onShare={handleShare}
                  
                />"""
replace = """                  onShare={handleShare}
                  isOfflineMode={isOfflineMode}
                />"""
content = content.replace(search, replace)
with open('src/App.tsx', 'w') as f:
    f.write(content)

with open('src/components/SearchView.tsx', 'r') as f:
    sv = f.read()

sv_search = "downloadedSongs,"
sv_replace = "isOfflineMode, downloadedSongs,"
sv = sv.replace(sv_search, sv_replace)

sv_search2 = "downloadedSongs?: Song[];"
sv_replace2 = "isOfflineMode?: boolean; downloadedSongs?: Song[];"
sv = sv.replace(sv_search2, sv_replace2)
with open('src/components/SearchView.tsx', 'w') as f:
    f.write(sv)
