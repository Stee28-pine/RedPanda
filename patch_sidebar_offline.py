import re

with open('src/components/Sidebar.tsx', 'r') as f:
    content = f.read()

# Remove the props
content = re.sub(r"\s*isOfflineMode(?: = false)?,?\s*", "", content)
content = re.sub(r"\s*isOfflineMode\?: boolean,?\s*", "", content)
content = re.sub(r"\s*onToggleOfflineMode,?\s*", "", content)
content = re.sub(r"\s*onToggleOfflineMode\?: \(\) => void,?\s*", "", content)

# Remove the SETTINGS block entirely
settings_block = r"""      <div className={`mb-8 px-3 \$\{isCollapsed \? 'block md:hidden' : 'block'\}`}>
        <h3 className="text-\[11px\] font-bold text-gray-400 mb-2 px-3 tracking-widest uppercase">SETTINGS</h3>
        <nav className="space-y-0.5">
          <button 
            onClick=\{\(e\) => \{ e.preventDefault\(\); e.stopPropagation\(\); onToggleOfflineMode\?\.\(\); \}\}
            className=\{`w-full flex items-center justify-between px-3 py-2.5 rounded-lg transition-colors text-gray-700 \$\{isOfflineMode \? 'bg-\[#fe5f64\]\/10' : 'hover:bg-gray-300\/50'\}`\}
          >
            <div className="flex items-center gap-3">
              <div className=\{\`\$\{isOfflineMode \? 'text-\[#fe5f64\]' : 'text-gray-500'\}\`\}>
                \{isOfflineMode \? <WifiOff size=\{18\} /> : <Wifi size=\{18\} />\}
              </div>
              <span className="font-semibold text-\[15px\] tracking-tight">Offline Mode</span>
            </div>
            <div className=\{`w-8 h-4 rounded-full transition-colors relative \$\{isOfflineMode \? 'bg-\[#fe5f64\]' : 'bg-gray-300'\}`\}>
               <div className=\{`absolute top-0.5 w-3 h-3 rounded-full bg-white transition-transform \$\{isOfflineMode \? 'translate-x-4.5 right-0.5' : 'translate-x-0.5 left-0'\}`\} />
            </div>
          </button>
        </nav>
      </div>"""
      
# Try simple regex replacement first, if it fails we do string replacement
import sys

new_content = re.sub(r"<div className=\{`mb-8 px-3 \$\{isCollapsed \? 'block md:hidden' : 'block'\}`\}>\s*<h3 className=\"text-\[11px\] font-bold text-gray-400 mb-2 px-3 tracking-widest uppercase\">SETTINGS</h3>.*?</div>", "", content, flags=re.DOTALL)

with open('src/components/Sidebar.tsx', 'w') as f:
    f.write(new_content)
