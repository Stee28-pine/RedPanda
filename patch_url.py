with open('src/App.tsx', 'r') as f:
    content = f.read()

search = """  useEffect(() => {
    if (!nowPlaying) {
      setYoutubeId(null);
      return;
    }
    
    // Attempt to use existing youtubeId or fetch a new one
    if (nowPlaying.youtubeId) {
      setYoutubeId(nowPlaying.youtubeId);
      setIsBuffering(false);
      return;
    }
    setYoutubeId(null);
    const fetchYtId = async () => {
      setIsBuffering(true);
      try {
        const res = await fetch(`/api/youtube-search?q=${encodeURIComponent(nowPlaying.title + ' ' + nowPlaying.artist)}`);
        const data = await res.json();
        if (data.videoId) {
          setYoutubeId(data.videoId);
          nowPlaying.youtubeId = data.videoId;
        }
      } catch (err) {
        console.error("Failed to fetch YT ID", err);
      } finally {
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
  }, [nowPlaying, youtubeId]);"""

replace = """  const [nowPlayingUrl, setNowPlayingUrl] = useState<string | null>(null);

  useEffect(() => {
    if (!nowPlaying) {
      setNowPlayingUrl(null);
      setYoutubeId(null);
      return;
    }
    
    let isCurrent = true;

    const resolveUrl = async () => {
      // 1. Check Offline DB (async)
      const blobUrl = await getOfflineAudioUrl(nowPlaying.id);
      if (!isCurrent) return;
      if (blobUrl) {
         setNowPlayingUrl(blobUrl);
         return;
      }
      
      // 2. Resolve YouTube ID
      let currentYtId = nowPlaying.youtubeId;
      if (!currentYtId) {
         setIsBuffering(true);
         try {
           const res = await fetch(`/api/youtube-search?q=${encodeURIComponent(nowPlaying.title + ' ' + nowPlaying.artist)}`);
           const data = await res.json();
           if (data.videoId) {
             currentYtId = data.videoId;
             nowPlaying.youtubeId = currentYtId;
           }
         } catch (err) {
           console.error("Failed to fetch YT ID", err);
         } finally {
           if (isCurrent) setIsBuffering(false);
         }
      }
      
      if (!isCurrent) return;
      
      // 3. Set the final URL
      if (currentYtId) {
         setYoutubeId(currentYtId);
         setNowPlayingUrl(`https://www.youtube.com/watch?v=${currentYtId}`);
      } else {
         setNowPlayingUrl(nowPlaying.audioUrl || "");
      }
    };

    resolveUrl();

    return () => { isCurrent = false; };
  }, [nowPlaying]);"""

content = content.replace(search, replace)

with open('src/App.tsx', 'w') as f:
    f.write(content)
