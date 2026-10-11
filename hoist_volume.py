import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Add volume to App.tsx
content = content.replace(
    "const [duration, setDuration] = useState(0);",
    "const [duration, setDuration] = useState(0);\n  const [volume, setVolume] = useState(1);"
)

# Pass volume to ReactPlayer
content = content.replace(
    'playing={isPlaying}',
    'playing={isPlaying}\n            volume={volume}'
)

# Add ArrowUp and ArrowDown to keyboard hook
keyboard_new = """        case 'ArrowUp':
          e.preventDefault();
          setVolume(v => Math.min(v + 0.1, 1));
          break;
        case 'ArrowDown':
          e.preventDefault();
          setVolume(v => Math.max(v - 0.1, 0));
          break;"""

content = content.replace(
    "case 'KeyN':",
    keyboard_new + "\n        case 'KeyN':"
)

# Pass volume into Player
content = content.replace(
    'isMini={isScrolled}',
    'isMini={isScrolled}\n          volume={volume}\n          onVolumeChange={setVolume}'
)

with open('src/App.tsx', 'w') as f:
    f.write(content)

with open('src/components/Player.tsx', 'r') as f:
    p_content = f.read()

# Modify PlayerProps
p_content = p_content.replace(
    '  isMini?: boolean;\n}',
    '  isMini?: boolean;\n  volume: number;\n  onVolumeChange: (vol: number) => void;\n}'
)

# Modify Player function signature
p_content = p_content.replace(
    '  isMini = false\n}: PlayerProps) {',
    '  isMini = false,\n  volume,\n  onVolumeChange\n}: PlayerProps) {'
)

# Remove local volume
p_content = re.sub(r'  const \[volume, setVolume\] = useState\(1\);\n', '', p_content)
# Replace setVolume in Player.tsx
p_content = p_content.replace('setVolume(', 'onVolumeChange(')

with open('src/components/Player.tsx', 'w') as f:
    f.write(p_content)

print("done hoisting volume")
