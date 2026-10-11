import re

with open('src/components/PodcastsView.tsx', 'r') as f:
    content = f.read()

old_filter = """          finalResults = ytData.results.filter((podcast: any) => {
             const artistLower = podcast.artist.toLowerCase();
             
             // Very strict channel filtering as requested by user.
             // We only want episodes from the exact author/channel
             return artistLower.includes(channelLower) || channelLower.includes(artistLower);
          });"""

new_filter = """          finalResults = ytData.results.filter((podcast: any) => {
             const artistLower = podcast.artist.toLowerCase();
             const titleLower = podcast.title.toLowerCase();
             const showNameLower = targetChannel ? targetChannel.toLowerCase() : "";
             const rawShowName = query.replace(" podcast full episode", "").toLowerCase();
             
             // Very strict filtering as requested by user.
             // We only want episodes from the exact author/channel OR where the video explicitly titles itself as the show.
             return artistLower.includes(channelLower) || channelLower.includes(artistLower) || titleLower.includes(rawShowName);
          });"""

content = content.replace(old_filter, new_filter)

with open('src/components/PodcastsView.tsx', 'w') as f:
    f.write(content)
