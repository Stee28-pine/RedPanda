import re

with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

# Replace ListMusic button with ListMusic + Minimize2
options_patch = """              <button onClick={onToggleRightSidebar} className="text-gray-700 hover:text-black transition-colors" title="Queue">
                <ListMusic size={16} />
              </button>
              
              <button onClick={() => setIsCollapsed(true)} className="text-gray-700 hover:text-black transition-colors ml-1 hidden md:block" title="Minimize">
                <Minimize2 size={16} />
              </button>"""

content = content.replace(
    """              <button onClick={onToggleRightSidebar} className="text-gray-700 hover:text-black transition-colors" title="Queue">
                <ListMusic size={16} />
              </button>""",
    options_patch
)

with open('src/components/Player.tsx', 'w') as f:
    f.write(content)
print("Minimize button added")
