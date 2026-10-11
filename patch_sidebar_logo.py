import re

with open('src/components/Sidebar.tsx', 'r') as f:
    content = f.read()

search = """    <aside className={`${isCollapsed ? 'w-64 md:w-20' : 'w-64'} flex-shrink-0 flex flex-col h-full bg-[#EBEBEB] md:bg-transparent py-4 overflow-y-auto hide-scrollbar text-sm font-medium transition-all duration-300 z-40 relative`}>
      
      <div className="mb-6 px-3">"""

replace = """    <aside className={`${isCollapsed ? 'w-64 md:w-20' : 'w-64'} flex-shrink-0 flex flex-col h-full bg-[#EBEBEB] md:bg-transparent py-4 overflow-y-auto hide-scrollbar text-sm font-medium transition-all duration-300 z-40 relative`}>
      
      {/* Brand Logo */}
      <div className={`mb-8 px-4 flex items-center ${isCollapsed ? 'justify-center' : 'gap-3'}`}>
        <img src="/698481-removebg-preview.png" alt="RedPanda Logo" className="h-8 w-auto object-contain flex-shrink-0" onError={(e) => { e.currentTarget.style.display = 'none'; }} />
        {!isCollapsed && <span className="text-2xl font-black tracking-tighter text-[#fe5f64]">RedPanda</span>}
      </div>

      <div className="mb-6 px-3">"""

# More robust regex
content = re.sub(
    r"(<aside[^>]+>)\s*<div className=\"mb-6 px-3\">",
    r"\1\n\n      {/* Brand Logo */}\n      <div className={`mb-8 px-4 flex items-center ${isCollapsed ? 'justify-center' : 'gap-3'}`}>\n        <img src=\"/698481-removebg-preview.png\" alt=\"RedPanda Logo\" className=\"h-8 w-auto object-contain flex-shrink-0\" onError={(e) => { e.currentTarget.style.display = 'none'; }} />\n        {!isCollapsed && <span className=\"text-2xl font-black tracking-tighter text-[#fe5f64]\">RedPanda</span>}\n      </div>\n\n      <div className=\"mb-6 px-3\">",
    content
)

with open('src/components/Sidebar.tsx', 'w') as f:
    f.write(content)
