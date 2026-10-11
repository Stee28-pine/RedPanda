import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Add import
if 'getOfflineAudioUrl' not in content:
    content = content.replace("} from './lib/offlineStorage';", ", getOfflineAudioUrl } from './lib/offlineStorage';")

# Add state
state_search = "  const [nowPlaying, setNowPlaying] = useState<Song | null>(null);"
state_replace = "  const [nowPlaying, setNowPlaying] = useState<Song | null>(null);\n  const [nowPlayingUrl, setNowPlayingUrl] = useState<string | null>(null);"
content = content.replace(state_search, state_replace)

# Add effect
effect_search = """  useEffect(() => {
    if (nowPlaying) {
      recordPlay(nowPlaying);
    }
  }, [nowPlaying?.id]);"""

effect_replace = """  useEffect(() => {
    if (nowPlaying) {
      recordPlay(nowPlaying);
      getOfflineAudioUrl(nowPlaying.id).then(blobUrl => {
         if (blobUrl) {
            setNowPlayingUrl(blobUrl);
         } else {
            setNowPlayingUrl(nowPlaying.audioUrl || (youtubeId ? `https://www.youtube.com/watch?v=${youtubeId}` : ""));
         }
      });
    } else {
      setNowPlayingUrl(null);
    }
  }, [nowPlaying?.id, youtubeId]);"""

content = content.replace(effect_search, effect_replace)

# Update ReactPlayer
player_search = """<ReactPlayer
            ref={playerRef}
            url={nowPlaying?.audioUrl || (youtubeId ? `https://www.youtube.com/watch?v=${youtubeId}` : "")}"""
player_replace = """<ReactPlayer
            ref={playerRef}
            url={nowPlayingUrl || ""}"""
content = content.replace(player_search, player_replace)

with open('src/App.tsx', 'w') as f:
    f.write(content)

