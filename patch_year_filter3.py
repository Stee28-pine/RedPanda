import re

with open('src/components/PodcastsView.tsx', 'r') as f:
    content = f.read()

# 1. Update signature
content = content.replace(
    'const fetchEpisodes = async (query: string, targetChannel?: string) => {',
    'const fetchEpisodes = async (query: string, targetChannel?: string, showNameStr?: string) => {'
)

# 2. Update filtering
old_filter = """             const rawShowName = query
               .replace(" podcast full episode", "")
               .replace(new RegExp(" " + YEARS.join("|"), "g"), "") // Remove year from title check
               .toLowerCase();"""

new_filter = """             const rawShowName = showNameStr ? showNameStr.toLowerCase() : query.replace(" podcast full episode", "").toLowerCase();"""

content = content.replace(old_filter, new_filter)

# 3. Update useEffect call
old_effect = """      fetchEpisodes(selectedShow + " podcast full episode" + yearQuery, showData?.channel);"""
new_effect = """      fetchEpisodes(selectedShow + " podcast full episode" + yearQuery, showData?.channel, selectedShow);"""
content = content.replace(old_effect, new_effect)

# Also need to update the other call to fetchEpisodes when NOT selectedShow, wait we only call fetchEpisodes when selectedShow is selected or when searching.
# When searching globally: fetchEpisodes(searchQuery + " podcast");
# So showNameStr is undefined, which is fine.

with open('src/components/PodcastsView.tsx', 'w') as f:
    f.write(content)
