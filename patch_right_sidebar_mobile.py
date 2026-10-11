import re

with open('src/components/RightSidebar.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    '<aside className="w-80 flex-shrink-0 flex flex-col h-full bg-transparent px-4 py-4 overflow-y-auto hide-scrollbar pb-32 relative z-10 border-l border-white/20">',
    '<aside className="w-full md:w-80 flex-shrink-0 flex flex-col h-full bg-[#EBEBEB] md:bg-transparent px-4 py-4 overflow-y-auto hide-scrollbar pb-32 absolute md:relative right-0 top-0 z-30 border-l border-white/20 shadow-xl md:shadow-none">'
)

with open('src/components/RightSidebar.tsx', 'w') as f:
    f.write(content)

print("RightSidebar mobile background patched")
