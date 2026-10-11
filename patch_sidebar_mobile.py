import re

with open('src/components/Sidebar.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    '<aside className={`${isCollapsed ? \'w-64 md:w-20\' : \'w-64\'} flex-shrink-0 flex flex-col h-full bg-transparent py-4 overflow-y-auto hide-scrollbar text-sm font-medium transition-all duration-300 z-40 rounded-xl md:rounded-none relative`}>',
    '<aside className={`${isCollapsed ? \'w-64 md:w-20\' : \'w-64\'} flex-shrink-0 flex flex-col h-full bg-[#EBEBEB] md:bg-transparent py-4 overflow-y-auto hide-scrollbar text-sm font-medium transition-all duration-300 z-40 relative`}>'
)

with open('src/components/Sidebar.tsx', 'w') as f:
    f.write(content)
print("Sidebar mobile background patched")
