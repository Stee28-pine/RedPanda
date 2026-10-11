import re

with open('src/App.tsx', 'r') as f:
    app = f.read()

# Fix App.tsx youtubeId issue
app_search = """  useEffect(() => {
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

app_replace = """  useEffect(() => {
    if (nowPlaying) {
      recordPlay(nowPlaying);
      getOfflineAudioUrl(nowPlaying.id).then(blobUrl => {
         if (blobUrl) {
            setNowPlayingUrl(blobUrl);
         } else {
            setNowPlayingUrl(nowPlaying.audioUrl || "");
         }
      });
    } else {
      setNowPlayingUrl(null);
    }
  }, [nowPlaying?.id]);"""
app = app.replace(app_search, app_replace)
with open('src/App.tsx', 'w') as f:
    f.write(app)

with open('src/components/SearchView.tsx', 'r') as f:
    sv = f.read()
sv = sv.replace("isOfflineMode, downloadedSongs,\n  onToggleLike", "downloadedSongs,\n  onToggleLike")
with open('src/components/SearchView.tsx', 'w') as f:
    f.write(sv)

with open('src/components/Sidebar.tsx', 'r') as f:
    sb = f.read()
sb = sb.replace("  onNavigateStats,\n  currentView,", "  onNavigateStats,\n  onNavigateDownloads,\n  currentView,")
sb = sb.replace("  onNavigateStats: () => void,\n  currentView: string,", "  onNavigateStats: () => void,\n  onNavigateDownloads?: () => void,\n  currentView: string,")
with open('src/components/Sidebar.tsx', 'w') as f:
    f.write(sb)
