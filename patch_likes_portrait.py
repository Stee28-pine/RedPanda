import re

with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

portrait_like_old = """                  <button onClick={handleToggleLike} className={`p-3 -m-3 min-w-[44px] min-h-[44px] flex items-center justify-center transition-colors mb-2 ${isLiked ? 'text-[#CA5A2C]' : 'text-gray-400'}`}>
                    <Heart size={28} className={isLiked ? 'fill-[#CA5A2C]' : ''} />
                  </button>"""

portrait_like_new = """                  <motion.button 
                    whileTap={{ scale: 0.7 }} 
                    transition={{ type: "spring", stiffness: 400, damping: 17 }}
                    onClick={handleToggleLike} 
                    className={`p-3 -m-3 min-w-[44px] min-h-[44px] flex items-center justify-center transition-colors mb-2 ${isLiked ? 'text-[#CA5A2C]' : 'text-gray-400'}`}
                  >
                    <Heart size={28} className={isLiked ? 'fill-[#CA5A2C]' : ''} />
                  </motion.button>"""

content = content.replace(portrait_like_old, portrait_like_new)

with open('src/components/Player.tsx', 'w') as f:
    f.write(content)
