import re

with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

# 1. Add SoundLevelIndicator before the Player function
sound_level_component = """
const SoundLevelIndicator = ({ isPlaying, volume }: { isPlaying: boolean, volume: number }) => {
  return (
    <div className="flex items-end gap-[2px] h-4 w-6 overflow-hidden">
      {[1, 2, 3, 4].map((i) => (
        <motion.div
          key={i}
          className="w-[3px] bg-[#CA5A2C] rounded-sm"
          animate={{
            height: isPlaying && volume > 0 ? [`${20 * volume}%`, `${100 * volume}%`, `${40 * volume}%`, `${80 * volume}%`, `${30 * volume}%`] : '10%'
          }}
          transition={{
            repeat: Infinity,
            duration: 0.4 + (i * 0.1),
            repeatType: 'mirror',
            ease: "easeInOut"
          }}
          style={{ originY: 1 }}
        />
      ))}
    </div>
  );
};

export function Player({ 
"""
content = content.replace("export function Player({ \n", sound_level_component)

# 2. Add extra controls and sound level to landscape volume
landscape_vol_old = """                  {/* Volume */}
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1, duration: 0.3 }} className="flex items-center gap-4 px-2">
                    <VolumeX size={20} className="text-gray-400" />
                    <input type="range" min="0" max="1" step="0.01" value={volume} onChange={(e) => onVolumeChange(parseFloat(e.target.value))} className="flex-1 h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-[#CA5A2C]" />
                    <Volume2 size={20} className="text-gray-400" />
                  </motion.div>
                </div>"""

landscape_vol_new = """                  {/* Volume & Advanced */}
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1, duration: 0.3 }} className="flex flex-col gap-4 px-2">
                    <div className="flex items-center gap-4">
                      <VolumeX size={20} className="text-gray-400" />
                      <input type="range" min="0" max="1" step="0.01" value={volume} onChange={(e) => onVolumeChange(parseFloat(e.target.value))} className="flex-1 h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-[#CA5A2C]" />
                      <Volume2 size={20} className="text-gray-400" />
                      <SoundLevelIndicator isPlaying={isPlaying} volume={volume} />
                    </div>
                    <div className="flex items-center justify-between mt-1">
                      <button onClick={onFadeOut} className="text-[11px] font-bold px-3 py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full transition-colors uppercase tracking-wider">Fade Out</button>
                      <button onClick={() => {
                        const rates = [0.5, 1, 1.5, 2];
                        const nextRate = rates[(rates.indexOf(playbackRate) + 1) % rates.length];
                        onPlaybackRateChange?.(nextRate);
                      }} className="text-[11px] font-bold px-3 py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full transition-colors tracking-wider">{playbackRate}x Speed</button>
                    </div>
                  </motion.div>
                </div>"""
content = content.replace(landscape_vol_old, landscape_vol_new)

# 3. Add extra controls and sound level to portrait volume
portrait_vol_old = """                {/* Volume */}
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1, duration: 0.3 }} className="flex items-center gap-4 px-2">
                  <VolumeX size={20} className="text-gray-400" />
                  <input type="range" min="0" max="1" step="0.01" value={volume} onChange={(e) => onVolumeChange(parseFloat(e.target.value))} className="flex-1 h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-[#CA5A2C]" />
                  <Volume2 size={20} className="text-gray-400" />
                </motion.div>
              </>"""

portrait_vol_new = """                {/* Volume & Advanced */}
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1, duration: 0.3 }} className="flex flex-col gap-4 px-2 mt-4 mb-4">
                  <div className="flex items-center gap-4">
                    <VolumeX size={20} className="text-gray-400" />
                    <input type="range" min="0" max="1" step="0.01" value={volume} onChange={(e) => onVolumeChange(parseFloat(e.target.value))} className="flex-1 h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-[#CA5A2C]" />
                    <Volume2 size={20} className="text-gray-400" />
                    <SoundLevelIndicator isPlaying={isPlaying} volume={volume} />
                  </div>
                  <div className="flex items-center justify-between mt-2">
                    <button onClick={onFadeOut} className="text-[11px] font-bold px-3 py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full transition-colors uppercase tracking-wider">Fade Out</button>
                    <button onClick={() => {
                      const rates = [0.5, 1, 1.5, 2];
                      const nextRate = rates[(rates.indexOf(playbackRate) + 1) % rates.length];
                      onPlaybackRateChange?.(nextRate);
                    }} className="text-[11px] font-bold px-3 py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full transition-colors tracking-wider">{playbackRate}x Speed</button>
                  </div>
                </motion.div>
              </>"""
content = content.replace(portrait_vol_old, portrait_vol_new)

# 4. Add to desktop Pill 3
pill_3_old = """              <button onClick={onToggleRightSidebar} className="text-gray-700 hover:text-black transition-colors" title="Queue">
                <ListMusic size={16} />
              </button>
              
              <button onClick={() => setIsCollapsed(true)} className="text-gray-700 hover:text-black transition-colors ml-1 hidden md:block" title="Minimize">
                <Minimize2 size={16} />
              </button>
            </div>"""

pill_3_new = """              <button onClick={onToggleRightSidebar} className="text-gray-700 hover:text-black transition-colors" title="Queue">
                <ListMusic size={16} />
              </button>
              <button onClick={onFadeOut} className="text-[10px] uppercase font-bold text-gray-700 hover:text-black transition-colors tracking-wider" title="Fade Out">
                Fade
              </button>
              <button onClick={() => {
                const rates = [0.5, 1, 1.5, 2];
                const nextRate = rates[(rates.indexOf(playbackRate) + 1) % rates.length];
                onPlaybackRateChange?.(nextRate);
              }} className="text-[11px] font-bold text-gray-700 hover:text-black transition-colors min-w-[24px] text-center" title="Playback Speed">
                {playbackRate}x
              </button>
              <div className="ml-1 pl-3 border-l border-gray-200 flex items-center">
                 <SoundLevelIndicator isPlaying={isPlaying} volume={volume} />
              </div>
              <button onClick={() => setIsCollapsed(true)} className="text-gray-700 hover:text-black transition-colors ml-2 hidden md:block" title="Minimize">
                <Minimize2 size={16} />
              </button>
            </div>"""
content = content.replace(pill_3_old, pill_3_new)


with open('src/components/Player.tsx', 'w') as f:
    f.write(content)

print("Player UI elements added")
