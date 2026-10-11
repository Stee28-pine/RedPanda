import re
with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    '  const [volume, setVolume] = useState(1);',
    '  const [volume, setVolume] = useState(1);\n  const [crossfadeVolume, setCrossfadeVolume] = useState(1);\n  const isCrossfading = useRef(false);'
)

with open('src/App.tsx', 'w') as f:
    f.write(content)
print("Hooks patched")
