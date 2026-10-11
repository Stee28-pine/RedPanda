import os
import re

directory = 'src'
old_color = re.compile(r'#ca5a2c', re.IGNORECASE)
new_color = '#fe5f64'

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(('.tsx', '.ts', '.css')):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if old_color.search(content):
                new_content = old_color.sub(new_color, content)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)

print("Color replacement complete.")
