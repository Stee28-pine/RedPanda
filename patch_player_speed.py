import re

with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

# Replace the advanced controls row in the mobile/full player
old_advanced = """                    <button onClick={() => {
                      const rates = [0.5, 1, 1.5, 2];
                      const nextRate = rates[(rates.indexOf(playbackRate) + 1) % rates.length];
                      onPlaybackRateChange?.(nextRate);
                    }} className="text-[11px] font-bold px-3 py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full transition-colors tracking-wider">{playbackRate}x Speed</button>"""

new_advanced = """                    {song.genre === 'Podcast' && (
                      <button onClick={() => {
                        const rates = [1, 1.25, 1.5, 2];
                        const currentIndex = rates.indexOf(playbackRate);
                        const nextRate = rates[currentIndex !== -1 ? (currentIndex + 1) % rates.length : 1];
                        onPlaybackRateChange?.(nextRate);
                      }} className="text-[11px] font-bold px-3 py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full transition-colors tracking-wider flex items-center gap-1">
                        <Timer size={12} /> {playbackRate}x
                      </button>
                    )}"""
content = content.replace(old_advanced, new_advanced)

with open('src/components/Player.tsx', 'w') as f:
    f.write(content)
print("Patched Player.tsx for speed control")
