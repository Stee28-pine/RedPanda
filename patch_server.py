import re

with open('server.ts', 'r') as f:
    content = f.read()

# Add the /api/search-podcasts endpoint
new_endpoint = """
  app.get("/api/search-podcasts", async (req, res) => {
    const query = req.query.q as string;
    if (!query) return res.json({ results: [] });
    try {
      const ytSearch = (await import('yt-search')).default;
      const r = await ytSearch(query);
      const results = r.videos.slice(0, 50).map((v: any) => {
        let durationStr = "0:00";
        if (v.seconds) {
            const m = Math.floor(v.seconds / 60);
            const s = v.seconds % 60;
            durationStr = `${m}:${s.toString().padStart(2, '0')}`;
        }
        return {
            id: v.videoId,
            title: v.title,
            artist: v.author?.name || "Unknown",
            album: "Podcast",
            duration: durationStr,
            durationSeconds: v.seconds,
            coverUrl: v.thumbnail,
            youtubeId: v.videoId
        };
      });
      res.json({ results });
    } catch (e: any) {
      console.error(e);
      res.status(500).json({ error: e.message });
    }
  });

  app.get("/api/search-tracks", async (req, res) => {"""

content = content.replace('  app.get("/api/search-tracks", async (req, res) => {', new_endpoint)

with open('server.ts', 'w') as f:
    f.write(content)
