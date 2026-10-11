with open('src/components/HomeView.tsx', 'r') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if 'Recently Played' in line:
        # Find start of section
        for j in range(i, -1, -1):
            if '{hasEnoughHistory && (' in lines[j]:
                start_idx = j
                break
        
        # Find end of section
        for j in range(i, len(lines)):
            if '</motion.section>' in lines[j]:
                if j + 1 < len(lines) and ')}' in lines[j+1]:
                    end_idx = j + 1
                    break
        break

if start_idx != -1 and end_idx != -1:
    lines[start_idx:end_idx+1] = []
    with open('src/components/HomeView.tsx', 'w') as f:
        f.writelines(lines)
    print("Successfully removed Recently Played")
else:
    print("Could not find bounds:", start_idx, end_idx)
