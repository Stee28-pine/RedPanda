import re

with open('src/components/PodcastsView.tsx', 'r') as f:
    content = f.read()

# 1. Update hover animations
old_hover = "whileHover={{ y: -6, scale: 1.03, transition: { duration: 0.2 } }}"
new_hover = "whileHover={{ y: -8, scale: 1.05, transition: { duration: 0.25, ease: 'easeOut' } }}"
content = content.replace(old_hover, new_hover)

old_shadow = "className=\"aspect-square rounded-2xl overflow-hidden mb-3 shadow-[0_4px_15px_rgb(0,0,0,0.08)] bg-gray-100 flex items-center justify-center relative\""
new_shadow = "className=\"aspect-square rounded-2xl overflow-hidden mb-3 shadow-[0_4px_15px_rgb(0,0,0,0.08)] group-hover:shadow-[0_20px_40px_rgba(254,95,100,0.25)] transition-shadow duration-300 bg-gray-100 flex items-center justify-center relative\""
content = content.replace(old_shadow, new_shadow)

# 2. Add genre: 'Podcast' to mapped episodes so we can identify them in the player
# In fetchEpisodes
old_set_episodes = "setEpisodes(finalResults);"
new_set_episodes = "setEpisodes(finalResults.map((r: any) => ({ ...r, genre: 'Podcast' })));"
content = content.replace(old_set_episodes, new_set_episodes)

with open('src/components/PodcastsView.tsx', 'w') as f:
    f.write(content)
print("Patched PodcastsView.tsx for hover and genre")
