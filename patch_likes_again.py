import re

with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

# 1. Desktop mini
mini_like_old = """                  <motion.button 
                    initial={{opacity:0}} animate={{opacity:1}} transition={{delay:0.1}} 
                    onClick={handleToggleLike}
                    className={`transition-colors flex items-center justify-center ${isLiked ? 'text-[#CA5A2C]' : 'text-gray-400 hover:text-gray-700'}`}
                  >
                    <motion.div animate={isLiked ? { scale: [1, 1.4, 1] } : { scale: 1 }} transition={{ duration: 0.3, type: "spring" }}>
                      <Heart size={16} className={isLiked ? 'fill-[#CA5A2C]' : ''} />
                    </motion.div>
                  </motion.button>"""

mini_like_new = """                  <motion.button 
                    initial={{opacity:0}} animate={{opacity:1}} 
                    whileTap={{ scale: 0.7 }}
                    transition={{ type: "spring", stiffness: 400, damping: 17 }}
                    onClick={handleToggleLike}
                    className={`transition-colors flex items-center justify-center ${isLiked ? 'text-[#CA5A2C]' : 'text-gray-400 hover:text-gray-700'}`}
                  >
                    <Heart size={16} className={isLiked ? 'fill-[#CA5A2C]' : ''} />
                  </motion.button>"""

content = content.replace(mini_like_old, mini_like_new)

# 2 & 3. Expanded player (Landscape and Portrait)
expanded_like_old = """                    <motion.button whileTap={{ scale: 0.9 }} onClick={handleToggleLike} className={`p-3 -m-3 min-w-[44px] min-h-[44px] flex items-center justify-center transition-colors mb-2 ${isLiked ? 'text-[#CA5A2C]' : 'text-gray-400'}`}>
                      <motion.div animate={isLiked ? { scale: [1, 1.3, 1] } : { scale: 1 }} transition={{ duration: 0.4, type: "spring", bounce: 0.5 }}>
                        <Heart size={28} className={isLiked ? 'fill-[#CA5A2C]' : ''} />
                      </motion.div>
                    </motion.button>"""

expanded_like_new = """                    <motion.button 
                      whileTap={{ scale: 0.7 }} 
                      transition={{ type: "spring", stiffness: 400, damping: 17 }}
                      onClick={handleToggleLike} 
                      className={`p-3 -m-3 min-w-[44px] min-h-[44px] flex items-center justify-center transition-colors mb-2 ${isLiked ? 'text-[#CA5A2C]' : 'text-gray-400'}`}
                    >
                      <Heart size={28} className={isLiked ? 'fill-[#CA5A2C]' : ''} />
                    </motion.button>"""

content = content.replace(expanded_like_old, expanded_like_new)

with open('src/components/Player.tsx', 'w') as f:
    f.write(content)
