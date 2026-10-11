with open('src/components/HomeView.tsx', 'r') as f:
    lines = f.readlines()

new_rp = """      {hasEnoughHistory && (
        <motion.section 
          className="mb-12"
          initial="hidden"
          animate="show"
          variants={{
            hidden: { opacity: 0 },
            show: { opacity: 1, transition: { staggerChildren: 0.08, delayChildren: 0.2 } }
          }}
        >
          <h2 className="text-[22px] font-bold text-gray-900 mb-5 tracking-tight">Recently Played</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
            {recentlyPlayedHistory.slice(0, 5).map((song, idx) => (
              <motion.div 
                key={`${song.id}-${idx}`}
                variants={{
                  hidden: { opacity: 0, y: 15, scale: 0.95 },
                  show: { opacity: 1, y: 0, scale: 1, transition: { type: "spring", stiffness: 200, damping: 20 } }
                }}
                whileHover={{ y: -6, scale: 1.03, transition: { duration: 0.2 } }}
                className="cursor-pointer group"
                onClick={() => onPlaySong?.(song, { songs: recentlyPlayedHistory })}
              >
                <div className="aspect-square rounded-2xl overflow-hidden mb-3 shadow-[0_8px_20px_rgb(0,0,0,0.12)] relative">
                  <img 
                    src={song.coverUrl} 
                    onError={(e) => { e.currentTarget.src = FALLBACK_IMG }}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" 
                    alt={song.title} 
                  />
                  <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <div className="w-10 h-10 rounded-full bg-white/90 backdrop-blur shadow-sm flex items-center justify-center pl-1 text-gray-900">
                      <Play size={20} fill="currentColor" />
                    </div>
                  </div>
                </div>
                <h3 className="font-semibold text-gray-900 truncate leading-tight tracking-tight">{song.title}</h3>
                <p className="text-[13px] font-medium text-gray-500 truncate mt-0.5">{song.artist}</p>
              </motion.div>
            ))}
          </div>
        </motion.section>
      )}"""

# Find the start of the recently played section
start_idx = -1
for i, line in enumerate(lines):
    if 'Recently Played' in line:
        start_idx = i - 8  # Back up to <motion.section>
        break

# Find the end of the recently played section
end_idx = -1
for i in range(start_idx, len(lines)):
    if '</motion.section>' in lines[i]:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    lines[start_idx:end_idx+1] = [new_rp + '\\n']

with open('src/components/HomeView.tsx', 'w') as f:
    f.writelines(lines)
