import re

with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

# I replaced opening <div className="bg-[#F5F5F5]/90 backdrop-blur-xl rounded-2xl with <motion.div layout
# But in my script, I left the closing tags alone except replacing one `</div>\n        )\n        </motion.div>`
# Let's just undo my previous layout changes and apply them properly.
content = content.replace('</motion.div>\n        )\n        </motion.div>', '</div>\n        )\n        </motion.div>')

content = content.replace(
    '<motion.div layout className="bg-[#F5F5F5]/90 backdrop-blur-xl rounded-2xl shadow-[0_8px_30px_rgba(0,0,0,0.12)] border border-white flex items-center px-4 w-[min(90vw,340px)] h-14 pointer-events-auto">',
    '<div className="bg-[#F5F5F5]/90 backdrop-blur-xl rounded-2xl shadow-[0_8px_30px_rgba(0,0,0,0.12)] border border-white flex items-center px-4 w-[min(90vw,340px)] h-14 pointer-events-auto">'
)

content = content.replace(
    '</motion.div>\n        )}\n        </motion.div>',
    '</div>\n        )}\n        </motion.div>'
)

content = content.replace(
    '<motion.div layout className="bg-[#F5F5F5]/90 backdrop-blur-xl p-3 md:px-5 md:py-3.5',
    '<div className="bg-[#F5F5F5]/90 backdrop-blur-xl p-3 md:px-5 md:py-3.5'
)

# Wait, if I just want layout on the outermost motion element:
# `key="player"\n          layout` is perfectly fine. The inner ones don't strictly need layout if I don't use it, but `layout` on the outer `motion.div` will smoothly transition its own bounds.

with open('src/components/Player.tsx', 'w') as f:
    f.write(content)

print("done")
