with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

content = content.replace("  onFadeOut\n}: PlayerProps) {", "  onFadeOut,\n  analyzerNode\n}: PlayerProps) {")

with open('src/components/Player.tsx', 'w') as f:
    f.write(content)
