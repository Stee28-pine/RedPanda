import re

with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

desktop_controls = """              <button onClick={onToggleRightSidebar} className="text-gray-700 hover:text-black transition-colors" title="Queue">
                <ListMusic size={16} />
              </button>"""

desktop_controls_new = """              <button onClick={onToggleRightSidebar} className="text-gray-700 hover:text-black transition-colors" title="Queue">
                <ListMusic size={16} />
              </button>
              {song.genre === 'Podcast' && (
                <button 
                  onClick={() => {
                    const rates = [1, 1.25, 1.5, 2];
                    const currentIndex = rates.indexOf(playbackRate);
                    const nextRate = rates[currentIndex !== -1 ? (currentIndex + 1) % rates.length : 1];
                    onPlaybackRateChange?.(nextRate);
                  }}
                  className="text-gray-700 hover:text-black transition-colors flex items-center justify-center font-bold text-[11px] leading-none tracking-tight h-4 w-6 rounded hover:bg-gray-200" 
                  title="Playback Speed"
                >
                  {playbackRate}x
                </button>
              )}"""

content = content.replace(desktop_controls, desktop_controls_new)

with open('src/components/Player.tsx', 'w') as f:
    f.write(content)
print("Patched Player.tsx for desktop speed control")
