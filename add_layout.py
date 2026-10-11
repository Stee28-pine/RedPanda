import re

with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

# Add layout property to the main motion.div
content = content.replace(
    'key="player"',
    'key="player"\n          layout'
)

# Also add layout property to the inner containers so they resize smoothly
content = content.replace(
    '<div className="bg-[#F5F5F5]/90 backdrop-blur-xl rounded-2xl',
    '<motion.div layout className="bg-[#F5F5F5]/90 backdrop-blur-xl rounded-2xl'
)
content = content.replace(
    'px-4 w-[min(90vw,340px)] h-14 pointer-events-auto">',
    'px-4 w-[min(90vw,340px)] h-14 pointer-events-auto">'
)
content = content.replace(
    '</div>\n        )\n        </motion.div>',
    '</motion.div>\n        )\n        </motion.div>'
)

content = content.replace(
    '<div className="bg-[#F5F5F5]/90 backdrop-blur-xl p-3 md:px-5 md:py-3.5',
    '<motion.div layout className="bg-[#F5F5F5]/90 backdrop-blur-xl p-3 md:px-5 md:py-3.5'
)
content = content.replace(
    '                  {/* Volume Control */}',
    '                  {/* Volume Control */}'
)
content = content.replace(
    '</div>\n        )}\n        </motion.div>',
    '</motion.div>\n        )}\n        </motion.div>'
)

with open('src/components/Player.tsx', 'w') as f:
    f.write(content)

print("done")
