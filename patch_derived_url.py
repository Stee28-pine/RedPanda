with open('src/App.tsx', 'r') as f:
    content = f.read()

search = """  const [nowPlayingUrl, setNowPlayingUrl] = useState<string | null>(null);

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

replace = """  const [asyncBlobUrl, setAsyncBlobUrl] = useState<string | null>(null);
  
  useEffect(() => {
    if (!nowPlaying) {
      setAsyncBlobUrl(null);
      setYoutubeId(null);
      return;
    }
    
    let isCurrent = true;

    const resolveUrl = async () => {
      // 1. Check Offline DB (async)
      const blobUrl = await getOfflineAudioUrl(nowPlaying.id);
      if (!isCurrent) return;
      if (blobUrl) {
         setAsyncBlobUrl(blobUrl);
         return;
      }
      
      // 2. Resolve YouTube ID if missing
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
      
      if (currentYtId) {
         setYoutubeId(currentYtId);
      }
    };

    resolveUrl();
    return () => { isCurrent = false; };
  }, [nowPlaying]);

  // Compute URL synchronously so it never drops to null between songs if we already have the youtubeId
  let nowPlayingUrl = "";
  if (nowPlaying) {
    if (asyncBlobUrl && downloadedSongs.some(d => d.id === nowPlaying.id)) {
      nowPlayingUrl = asyncBlobUrl;
    } else if (nowPlaying.youtubeId) {
      nowPlayingUrl = `https://www.youtube.com/watch?v=${nowPlaying.youtubeId}`;
    } else if (youtubeId) {
      nowPlayingUrl = `https://www.youtube.com/watch?v=${youtubeId}`;
    } else if (nowPlaying.audioUrl) {
      nowPlayingUrl = nowPlaying.audioUrl;
    }
  }"""

content = content.replace(search, replace)

with open('src/App.tsx', 'w') as f:
    f.write(content)
