with open('src/components/HomeView.tsx', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.strip() == '<motion.section':
        if i + 1 < len(lines) and '{hasEnoughHistory && (' in lines[i+1]:
            lines[i] = ""

with open('src/components/HomeView.tsx', 'w') as f:
    f.writelines(lines)
