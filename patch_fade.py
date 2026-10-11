import re

with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

# Replace the inner contents of Expanded Player with a fade-in wrapper for non-shared elements.
# Actually, the simplest way is to add the initial/animate props directly to the non-shared divs.
# E.g. <div className="mb-6"> (Scrubber) -> <motion.div initial={{opacity: 0}} animate={{opacity: 1}} ... className="mb-6">

fade_props = 'initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1, duration: 0.3 }}'

# Landscape controls
content = content.replace('<div className="mb-6">\n                    <div className="w-full h-8 flex items-center group cursor-pointer touch-none mb-1"',
                          f'<motion.div {fade_props} className="mb-6">\n                    <div className="w-full h-8 flex items-center group cursor-pointer touch-none mb-1"')
content = content.replace('<span>{formatTime(duration)}</span>\n                    </div>\n                  </div>\n                  {/* Controls */}\n                  <div className="flex items-center justify-between mb-8 px-2">',
                          '<span>{formatTime(duration)}</span>\n                    </div>\n                  </motion.div>\n                  {/* Controls */}\n                  <motion.div ' + fade_props + ' className="flex items-center justify-between mb-8 px-2">')
content = content.replace('</button>\n                  </div>\n                  {/* Volume */}\n                  <div className="flex items-center gap-4 px-2">',
                          '</button>\n                  </motion.div>\n                  {/* Volume */}\n                  <motion.div ' + fade_props + ' className="flex items-center gap-4 px-2">')
content = content.replace('<Volume2 size={20} className="text-gray-400" />\n                  </div>\n                </div>\n              </>\n            ) : (',
                          '<Volume2 size={20} className="text-gray-400" />\n                  </motion.div>\n                </div>\n              </>\n            ) : (')

# Portrait controls & header
content = content.replace('{/* Header */}\n                <div className="flex justify-between items-center mb-6">',
                          '{/* Header */}\n                <motion.div ' + fade_props + ' className="flex justify-between items-center mb-6">')
content = content.replace('<ListMusic size={24} />\n                   </button>\n                </div>\n                {/* Album Art with Glow */}',
                          '<ListMusic size={24} />\n                   </button>\n                </motion.div>\n                {/* Album Art with Glow */}')

content = content.replace('</button>\n                </div>\n                {/* Scrubber */}\n                <div className="mb-6">',
                          '</button>\n                </div>\n                {/* Scrubber */}\n                <motion.div ' + fade_props + ' className="mb-6">')

content = content.replace('<span>{formatTime(duration)}</span>\n                  </div>\n                </div>\n                {/* Controls */}\n                <div className="flex items-center justify-between mb-8 px-2">',
                          '<span>{formatTime(duration)}</span>\n                  </div>\n                </motion.div>\n                {/* Controls */}\n                <motion.div ' + fade_props + ' className="flex items-center justify-between mb-8 px-2">')

content = content.replace('</button>\n                </div>\n                {/* Volume */}\n                <div className="flex items-center gap-4 px-2">',
                          '</button>\n                </motion.div>\n                {/* Volume */}\n                <motion.div ' + fade_props + ' className="flex items-center gap-4 px-2">')

content = content.replace('<Volume2 size={20} className="text-gray-400" />\n                </div>\n              </>\n            )}',
                          '<Volume2 size={20} className="text-gray-400" />\n                </motion.div>\n              </>\n            )}')

# Top-left chevron in landscape
content = content.replace('{/* Left Side: Art */}\n                <div className="flex-1 flex justify-center items-center h-full relative">\n                  <div className="absolute top-0 left-0">',
                          '{/* Left Side: Art */}\n                <div className="flex-1 flex justify-center items-center h-full relative">\n                  <motion.div ' + fade_props + ' className="absolute top-0 left-0">')
content = content.replace('<ChevronDown size={32} />\n                    </button>\n                  </div>\n                  <div className="relative w-full max-w-[280px] aspect-square">',
                          '<ChevronDown size={32} />\n                    </button>\n                  </motion.div>\n                  <div className="relative w-full max-w-[280px] aspect-square">')

# Mini player controls (need to fade out, but actually let's just make them fade in too when minimizing, or just let them snap since they are tiny)
# Let's fade them in
content = content.replace('<button \n                onClick={onToggleLike}',
                          '<motion.button initial={{opacity:0}} animate={{opacity:1}} transition={{delay:0.1}} \n                onClick={onToggleLike}')
content = content.replace('</button>\n              <button \n                onClick={() => onShare && onShare({ type: \'song\', id: song.id, name: song.title })}',
                          '</motion.button>\n              <motion.button initial={{opacity:0}} animate={{opacity:1}} transition={{delay:0.1}}\n                onClick={() => onShare && onShare({ type: \'song\', id: song.id, name: song.title })}')
content = content.replace('<Share2 size={16} />\n              </button>\n              <div className="flex items-center gap-3 pr-1">',
                          '<Share2 size={16} />\n              </motion.button>\n              <motion.div initial={{opacity:0}} animate={{opacity:1}} transition={{delay:0.1}} className="flex items-center gap-3 pr-1">')
content = content.replace('<Maximize2 size={16} />\n                </button>\n              </div>\n            </div>\n          </motion.div>',
                          '<Maximize2 size={16} />\n                </button>\n              </motion.div>\n            </div>\n          </motion.div>')

with open('src/components/Player.tsx', 'w') as f:
    f.write(content)
print("Fade patch applied")
