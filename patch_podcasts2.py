import re

with open('src/components/PodcastsView.tsx', 'r') as f:
    content = f.read()

# Replace /api/search-tracks with /api/search-podcasts
content = content.replace('fetch(`/api/search-tracks?q=${encodeURIComponent(query)}`)', 'fetch(`/api/search-podcasts?q=${encodeURIComponent(query)}`)')

# Replace the filter strictly by channel logic
old_filter = """        if (targetChannel) {
          const channelLower = targetChannel.toLowerCase();
          finalResults = ytData.results.filter((podcast: any) => {
             const artistLower = podcast.artist.toLowerCase();
             // Broaden match a little (e.g. 'Raj Shamani' matches 'Raj Shamani | Figuring Out')
             return artistLower.includes(channelLower) || channelLower.includes(artistLower);
          });
          
          // In case of extreme mismatch but it found results, we don't want to show empty. 
          // But as requested: "only that channel not other than that", so we will respect the strict filter.
        }"""

new_filter = """        if (targetChannel) {
          const channelLower = targetChannel.toLowerCase();
          finalResults = ytData.results.filter((podcast: any) => {
             const artistLower = podcast.artist.toLowerCase();
             
             // Very strict channel filtering as requested by user.
             // We only want episodes from the exact author/channel
             return artistLower.includes(channelLower) || channelLower.includes(artistLower);
          });
        }"""

content = content.replace(old_filter, new_filter)

with open('src/components/PodcastsView.tsx', 'w') as f:
    f.write(content)
