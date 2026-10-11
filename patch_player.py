import re

with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

# Add import
content = content.replace("import { LyricsOverlay } from './LyricsOverlay';", "import { LyricsOverlay } from './LyricsOverlay';\nimport { Visualizer } from './Visualizer';")

# Add prop interface
content = content.replace("  onVolumeChange: (vol: number) => void;", "  onVolumeChange: (vol: number) => void;\n  analyzerNode?: any;")

# Add prop destructuring
content = content.replace("  onVolumeChange\n", "  onVolumeChange,\n  analyzerNode\n")

# Add Visualizer near the volume control or song info for the mini player
mini_visualizer = """                <div className="flex flex-col truncate mr-4">
                  <span className="text-[14px] font-semibold text-gray-900 truncate leading-tight tracking-tight">{song.title}</span>
                  <span className="text-[12px] font-medium text-gray-500 truncate mt-0.5">{song.artist}</span>
                </div>
                {analyzerNode && <Visualizer analyzer={analyzerNode} />}"""

# Let's just find the song title and artist and put the Visualizer in the Player.
# In the Expanded Player we could also add it. Let's just add it where the `song.title` is in mini player, maybe inside a relative container.

with open('src/components/Player.tsx', 'w') as f:
    f.write(content)
