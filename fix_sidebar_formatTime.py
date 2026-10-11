with open('src/components/Sidebar.tsx', 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False
found = False

for line in lines:
    if "const formatTime =" in line and not found:
        # skip this and the next 6 lines
        skip = True
        skip_count = 7
        found = True
    
    if skip:
        skip_count -= 1
        if skip_count == 0:
            skip = False
        continue
    
    new_lines.append(line)

with open('src/components/Sidebar.tsx', 'w') as f:
    f.writelines(new_lines)
