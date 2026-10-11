import re

with open('src/components/Sidebar.tsx', 'r') as f:
    content = f.read()

# Replace Sidebar Logo area
# Find the Brand Logo section
search_sidebar = r"\{/\* Brand Logo \*/\}\n\s*<div className=\{`mb-8 px-4 flex items-center \$\{isCollapsed \? 'justify-center' : 'gap-3'\}`\}>\n\s*<img src=\"/698481-removebg-preview\.png\" alt=\"RedPanda Logo\" className=\"h-8 w-auto object-contain flex-shrink-0\" onError=\{\(e\) => \{ e\.currentTarget\.style\.display = 'none'; \}\} />\n\s*\{!isCollapsed && <span className=\"text-2xl font-black tracking-tighter text-\[#fe5f64\]\">RedPanda</span>\}\n\s*</div>"

replace_sidebar = """{/* Brand Logo */}
      <div className={`mb-8 px-4 flex items-center ${isCollapsed ? 'justify-center' : 'justify-start'}`}>
        <img src="/698481-removebg-preview.png" alt="RedPanda Logo" className="h-10 w-auto object-contain" />
      </div>"""

content = re.sub(search_sidebar, replace_sidebar, content)

with open('src/components/Sidebar.tsx', 'w') as f:
    f.write(content)

with open('src/components/TopBar.tsx', 'r') as f:
    content = f.read()

# Replace TopBar Logo area
search_topbar = r"\{/\* Mobile Brand Logo \*/\}\n\s*<div className=\"md:hidden flex items-center gap-2 mr-1\">\n\s*<img src=\"/698481-removebg-preview\.png\" alt=\"RedPanda Logo\" className=\"h-6 w-auto object-contain flex-shrink-0\" onError=\{\(e\) => \{ e\.currentTarget\.style\.display = 'none'; \}\} />\n\s*</div>"

replace_topbar = """{/* Mobile Brand Logo */}
        <div className="md:hidden flex items-center gap-2 mr-1">
          <img src="/698481-removebg-preview.png" alt="RedPanda Logo" className="h-8 w-auto object-contain" />
        </div>"""

content = re.sub(search_topbar, replace_topbar, content)

with open('src/components/TopBar.tsx', 'w') as f:
    f.write(content)
