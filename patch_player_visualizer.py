import re

with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

# Expanded portrait
portrait_album = """            <div className="flex-1 flex flex-col justify-center items-center w-full relative">
              <motion.img 
                layoutId="album-art"
                transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                src={song.coverUrl} 
                onError={(e) => { e.currentTarget.src = FALLBACK_IMG }}
                className="w-full max-w-[min(100vw-48px,40vh)] aspect-square rounded-2xl shadow-2xl object-cover mb-8" 
                alt={song.title} 
              />"""

portrait_album_new = """            <div className="flex-1 flex flex-col justify-center items-center w-full relative">
              <div className="relative w-full max-w-[min(100vw-48px,40vh)] aspect-square mb-8">
                {analyzerNode && (
                   <div className="absolute inset-0 z-0 opacity-40 scale-110 flex items-center justify-center pointer-events-none">
                     <Visualizer analyzer={analyzerNode} />
                   </div>
                )}
                <motion.img 
                  layoutId="album-art"
                  transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                  src={song.coverUrl} 
                  onError={(e) => { e.currentTarget.src = FALLBACK_IMG }}
                  className="w-full h-full rounded-2xl shadow-[0_20px_40px_rgb(0,0,0,0.12)] object-cover relative z-10" 
                  alt={song.title} 
                />
              </div>"""

content = content.replace(portrait_album, portrait_album_new)

with open('src/components/Player.tsx', 'w') as f:
    f.write(content)
