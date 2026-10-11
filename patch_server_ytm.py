import re

with open('server.ts', 'r') as f:
    content = f.read()

search = """  app.get("/api/search-tracks", async (req, res) => {
    const query = req.query.q as string;
    if (!query) return res.json({ results: [] });
    try {
      const ytSearch = (await import('yt-search')).default;
      const r = await ytSearch(query + ' song audio');
      const results = r.videos.slice(0, 15).map(v => ({
        id: v.videoId,
        title: v.title.replace(/\\(Official.*\\)|\\[Official.*\\]|\\(Music Video\\)|\\[Music Video\\]/gi, '').trim(),
        artist: v.author.name.replace(/ - Topic/i, ''),
        album: "YouTube",
        duration: v.duration.timestamp,
        durationSeconds: v.duration.seconds,
        coverUrl: v.thumbnail,
        youtubeId: v.videoId
      }));
      res.json({ results });
    } catch (e: any) {
      res.status(500).json({ error: e.message });
    }
  });"""

replace = """  let ytmusic: any = null;
  const getYTMusic = async () => {
    if (!ytmusic) {
      const YTMusic = (await import('ytmusic-api')).default;
      ytmusic = new YTMusic();
      await ytmusic.initialize();
    }
    return ytmusic;
  };

  app.get("/api/search-tracks", async (req, res) => {
    const query = req.query.q as string;
    if (!query) return res.json({ results: [] });
    try {
      const ytm = await getYTMusic();
      const r = await ytm.searchSongs(query);
      
      const results = r.slice(0, 20).map((v: any) => {
        let durationStr = "0:00";
        if (v.duration) {
            const m = Math.floor(v.duration / 60);
            const s = v.duration % 60;
            durationStr = `${m}:${s.toString().padStart(2, '0')}`;
        }
        
        return {
            id: v.videoId,
            title: v.name,
            artist: v.artist.name,
            album: v.album?.name || "Single",
            duration: durationStr,
            durationSeconds: v.duration || 0,
            coverUrl: v.thumbnails && v.thumbnails.length > 0 ? v.thumbnails[v.thumbnails.length - 1].url : "",
            youtubeId: v.videoId
        };
      });
      res.json({ results });
    } catch (e: any) {
      res.status(500).json({ error: e.message });
    }
  });"""

content = content.replace(search, replace)

with open('server.ts', 'w') as f:
    f.write(content)
