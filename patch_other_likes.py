import re

components = ['src/components/AlbumView.tsx', 'src/components/ArtistView.tsx', 'src/components/SearchView.tsx']

for file in components:
    with open(file, 'r') as f:
        content = f.read()

    # Search for like buttons inside map loops
    old_btn = """                  <button 
                    onClick={(e) => { e.stopPropagation(); onToggleLike(song); }}
                    className={`transition-colors ${isLiked ? 'text-[#CA5A2C]' : 'text-gray-400 hover:text-gray-700'}`}
                  >
                    <Heart size={18} className={isLiked ? 'fill-[#CA5A2C]' : ''} />
                  </button>"""
                  
    new_btn = """                  <button 
                    onClick={(e) => { e.stopPropagation(); onToggleLike(song); }}
                    className={`transition-colors ${isLiked ? 'text-[#CA5A2C]' : 'text-gray-400 hover:text-gray-700'}`}
                  >
                    <motion.div animate={isLiked ? { scale: [1, 1.4, 1] } : { scale: 1 }} transition={{ duration: 0.3 }}>
                       <Heart size={18} className={isLiked ? 'fill-[#CA5A2C]' : ''} />
                    </motion.div>
                  </button>"""
                  
    content = content.replace(old_btn, new_btn)

    with open(file, 'w') as f:
        f.write(content)

