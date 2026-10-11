import re

with open('src/components/TopBar.tsx', 'r') as f:
    content = f.read()

search = """        <button 
          onClick={onToggleSidebar}
          className="md:hidden p-2 -ml-2 rounded-full flex items-center justify-center text-gray-700 hover:bg-gray-100"
        >
          <Menu size={20} strokeWidth={2.5} />
        </button>
        <button """

replace = """        <button 
          onClick={onToggleSidebar}
          className="md:hidden p-2 -ml-2 rounded-full flex items-center justify-center text-gray-700 hover:bg-gray-100"
        >
          <Menu size={20} strokeWidth={2.5} />
        </button>
        
        {/* Mobile Brand Logo */}
        <div className="md:hidden flex items-center gap-2 mr-1">
          <img src="/698481-removebg-preview.png" alt="RedPanda Logo" className="h-6 w-auto object-contain flex-shrink-0" onError={(e) => { e.currentTarget.style.display = 'none'; }} />
        </div>

        <button """

content = content.replace(search, replace)

with open('src/components/TopBar.tsx', 'w') as f:
    f.write(content)
