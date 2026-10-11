import re

with open('src/components/Sidebar.tsx', 'r') as f:
    content = f.read()

# Replace the logo section in Sidebar to remove the text and increase image size
search_logo = r"\{/\* Brand Logo \*/\}\n\s*<div className=\{`mb-8 px-4 flex items-center \$\{isCollapsed \? 'justify-center' : 'justify-start'\}`\}>\n\s*<img src=\"/698481-removebg-preview\.png\" alt=\"RedPanda Logo\" className=\"h-10 w-auto object-contain\" />\n\s*</div>"

replace_logo = """{/* Brand Logo */}
      <div className={`mb-8 px-4 flex items-center justify-start h-12`}>
        <img src="/698481-removebg-preview.png" alt="RedPanda Logo" className="h-full w-auto object-contain max-w-[180px]" />
      </div>"""

content = re.sub(search_logo, replace_logo, content)

# Make sidebar fixed width w-64
content = re.sub(
    r"<aside className=\{\`\$\{isCollapsed \? 'w-64 md:w-20' : 'w-64'\} flex-shrink-0 flex flex-col h-full bg-\[#EBEBEB\]",
    r"<aside className={`w-64 min-w-[16rem] flex-shrink-0 flex flex-col h-full bg-[#EBEBEB]",
    content
)

with open('src/components/Sidebar.tsx', 'w') as f:
    f.write(content)

with open('src/components/TopBar.tsx', 'r') as f:
    content = f.read()

# Replace TopBar logo section
search_topbar = r"\{/\* Mobile Brand Logo \*/\}\n\s*<div className=\"md:hidden flex items-center gap-2 mr-1\">\n\s*<img src=\"/698481-removebg-preview\.png\" alt=\"RedPanda Logo\" className=\"h-8 w-auto object-contain\" />\n\s*</div>"

replace_topbar = """{/* Mobile Brand Logo */}
        <div className="md:hidden flex items-center mr-2 h-8">
          <img src="/698481-removebg-preview.png" alt="RedPanda Logo" className="h-full w-auto object-contain" />
        </div>"""

content = re.sub(search_topbar, replace_topbar, content)

with open('src/components/TopBar.tsx', 'w') as f:
    f.write(content)
