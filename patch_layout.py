import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    '<div className="flex h-screen bg-[#EBEBEB] text-gray-900 font-sans overflow-hidden p-2 gap-2 select-none relative">',
    '<div className="flex h-screen bg-[#EBEBEB] text-gray-900 font-sans overflow-hidden md:p-2 md:gap-2 select-none relative">'
)

content = content.replace(
    '<div className={`fixed inset-y-0 left-0 z-40 p-2 transition-transform duration-300 md:relative md:transform-none md:p-0 ${isSidebarCollapsed ? \'-translate-x-full md:translate-x-0\' : \'translate-x-0\'}`}>',
    '<div className={`fixed inset-y-0 left-0 z-40 p-0 md:p-0 transition-transform duration-300 md:relative md:transform-none ${isSidebarCollapsed ? \'-translate-x-full md:translate-x-0\' : \'translate-x-0\'}`}>'
)

content = content.replace(
    '<main className="flex-1 flex flex-col bg-[#F9F9F9] rounded-2xl shadow-sm border border-gray-200 overflow-hidden relative">',
    '<main className="flex-1 flex flex-col bg-[#F9F9F9] md:rounded-2xl shadow-sm md:border md:border-gray-200 overflow-hidden relative">'
)

with open('src/App.tsx', 'w') as f:
    f.write(content)
print("Layout patched")
