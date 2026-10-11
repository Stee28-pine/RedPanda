import re

with open('src/components/PodcastsView.tsx', 'r') as f:
    content = f.read()

search_raw = 'const rawShowName = query.replace(" podcast full episode", "").toLowerCase();'
replace_raw = '''const rawShowName = query
               .replace(" podcast full episode", "")
               .replace(new RegExp(" " + YEARS.join("|"), "g"), "") // Remove year from title check
               .toLowerCase();'''

content = content.replace(search_raw, replace_raw)

with open('src/components/PodcastsView.tsx', 'w') as f:
    f.write(content)
