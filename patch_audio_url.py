import re

with open('src/App.tsx', 'r') as f:
    app = f.read()

# 1. Remove the old nowPlayingUrl effect and state
old_nowplaying_effect = """  const [nowPlayingUrl, setNowPlayingUrl] = useState<string | null>(null);
  useEffect(() => {
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
app = app.replace(old_nowplaying_effect, "")

# 2. Insert it back after youtubeId
youtube_effect = """      } finally {
        setIsBuffering(false);
      }
    };
    fetchYtId();
  }, [nowPlaying]);"""

new_nowplaying_effect = """      } finally {
        setIsBuffering(false);
      }
    };
    fetchYtId();
  }, [nowPlaying]);

  const [nowPlayingUrl, setNowPlayingUrl] = useState<string | null>(null);
  useEffect(() => {
    if (!nowPlaying) {
      setNowPlayingUrl(null);
      return;
    }
    
    // Check if we just played a new song to record the play
    if (nowPlaying.id) {
       // We only want to record once per song change, but since we rely on youtubeId we might re-run.
       // Let's just put it in a separate effect or just rely on the existing one. Actually, let's just 
       // put recordPlay in a standalone effect to prevent double-recording.
    }
    
    getOfflineAudioUrl(nowPlaying.id).then(blobUrl => {
      if (blobUrl) {
         setNowPlayingUrl(blobUrl);
      } else {
         if (youtubeId) {
            setNowPlayingUrl(`https://www.youtube.com/watch?v=${youtubeId}`);
         } else {
            setNowPlayingUrl(nowPlaying.audioUrl || "");
         }
      }
    });
  }, [nowPlaying, youtubeId]);

  useEffect(() => {
    if (nowPlaying) {
       recordPlay(nowPlaying);
    }
  }, [nowPlaying?.id]);"""

app = app.replace(youtube_effect, new_nowplaying_effect)

with open('src/App.tsx', 'w') as f:
    f.write(app)
