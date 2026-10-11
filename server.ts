import express from "express";
import path from "path";
import { createServer as createViteServer } from "vite";

const TMDB_API_KEY = "e6333b32409e02a4a6eba6fb7ff866bb";
const TMDB_BASE_URL = "https://api.themoviedb.org/3";

async function fetchTmdb(endpoint: string, queryParams: Record<string, any> = {}, retries = 3): Promise<any> {
  const url = new URL(`${TMDB_BASE_URL}${endpoint}`);
  url.searchParams.append("api_key", TMDB_API_KEY);
  for (const [key, value] of Object.entries(queryParams)) {
    if (value !== undefined && value !== null) {
      url.searchParams.append(key, value.toString());
    }
  }

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const response = await fetch(url.toString(), {
        headers: {
          "Accept": "application/json"
        }
      });

      if (!response.ok) {
        if (attempt < retries) {
          await new Promise(res => setTimeout(res, 500 * attempt));
          continue;
        }
        console.error(`TMDB error: ${response.statusText} for ${url.pathname}`);
        return { results: [] };
      }

      return await response.json();
    } catch (e) {
      if (attempt < retries) {
        await new Promise(res => setTimeout(res, 500 * attempt));
        continue;
      }
      console.error(`Fetch failed for ${url.pathname}:`, e);
      return { results: [] };
    }
  }
}

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // API routes FIRST
  app.get("/api/health", (req, res) => {
    res.json({ status: "ok" });
  });

  app.get("/api/home", async (req, res) => {
    try {
        const [discoverMovies, discoverSeries, topMovies, topSeries, trending, hollywoodNew, bollywoodNew, globalContent, hindiDubbed] = await Promise.all([
          fetchTmdb("/movie/now_playing", { page: 1 }),
          fetchTmdb("/tv/on_the_air", { page: 1 }),
          fetchTmdb("/movie/top_rated", { page: 1, region: "US" }),
          fetchTmdb("/tv/top_rated", { page: 1 }),
          fetchTmdb("/trending/all/day"),
          fetchTmdb("/discover/movie", { sort_by: "popularity.desc", "primary_release_date.gte": new Date(Date.now() - 90*24*60*60*1000).toISOString().split("T")[0], with_original_language: "en" }),
          fetchTmdb("/discover/movie", { sort_by: "popularity.desc", "primary_release_date.gte": new Date(Date.now() - 90*24*60*60*1000).toISOString().split("T")[0], with_original_language: "hi" }),
          fetchTmdb("/discover/movie", { sort_by: "popularity.desc", without_original_language: "en|hi" }),
          fetchTmdb("/discover/movie", { sort_by: "popularity.desc", with_original_language: "te|ta|ml|kn" })
        ]);

        // Merge Hollywood and Bollywood for the trending row to satisfy global viewing patterns
        const mingledTrending = [];
        const tResults = trending.results || [];
        const bResults = bollywoodNew.results || [];
        for (let i = 0; i < Math.max(tResults.length, bResults.length); i++) {
          if (tResults[i]) mingledTrending.push(tResults[i]);
          if (bResults[i] && i % 3 === 0) mingledTrending.push(bResults[i]); // Inject Bollywood blockbusters
        }

      res.json({
        discoverMovies: discoverMovies.results,
        discoverSeries: discoverSeries.results,
        topMovies: topMovies.results,
        topSeries: topSeries.results,
        trending: mingledTrending,
        hollywoodNew: hollywoodNew.results,
        bollywoodNew: bollywoodNew.results,
        globalContent: globalContent.results,
        hindiDubbed: hindiDubbed.results
      });
    } catch (e: any) {
      res.status(500).json({ error: e.message });
    }
  });

  app.get("/api/search", async (req, res) => {
    const query = req.query.q;
    if (!query) return res.json({ results: [] });
    try {
      const data = await fetchTmdb("/search/multi", { query, page: 1, include_adult: false });
      res.json(data);
    } catch (e: any) {
      res.status(500).json({ error: e.message });
    }
  });

  app.get("/api/details/:mediaType/:id", async (req, res) => {
     const { mediaType, id } = req.params;
     try {
       const data = await fetchTmdb(`/${mediaType}/${id}`, { append_to_response: "videos,credits,recommendations" });
       res.json(data);
     } catch (e: any) {
       res.status(500).json({ error: e.message });
     }
  });

  app.get("/api/season/:tvId/:seasonNum", async (req, res) => {
     const { tvId, seasonNum } = req.params;
     try {
       const data = await fetchTmdb(`/tv/${tvId}/season/${seasonNum}`);
       res.json(data);
     } catch (e: any) {
       res.status(500).json({ error: e.message });
     }
  });

  app.get("/api/person/:id", async (req, res) => {
     const { id } = req.params;
     try {
       const data = await fetchTmdb(`/person/${id}`, { append_to_response: "movie_credits,tv_credits" });
       res.json(data);
     } catch (e: any) {
       res.status(500).json({ error: e.message });
     }
  });

  app.get("/api/download/:mediaType/:id", async (req, res) => {
     const { mediaType, id } = req.params;
     try {
       const data = await fetchTmdb(`/${mediaType}/${id}`);
       const title = mediaType === 'movie' ? (data.title || data.original_title) : (data.name || data.original_name);
       const year = mediaType === 'movie' && data.release_date ? data.release_date.split('-')[0] : '';
       
       if (!title) {
          return res.status(404).json({ error: "Title not found" });
       }
       
       const apibayRes = await fetch(`https://apibay.org/q.php?q=${encodeURIComponent(title)} ${year}`);
       let apibayData;
       try {
         apibayData = await apibayRes.json();
       } catch (err) {
         apibayData = [];
       }
       
       let magnetUrl = null;
       if (Array.isArray(apibayData) && apibayData.length > 0 && apibayData[0].id !== "0") {
         const sorted = apibayData.sort((a: any, b: any) => parseInt(b.seeders) - parseInt(a.seeders));
         const best = sorted.find((t: any) => t.name.includes("1080p") || t.name.includes("720p")) || sorted[0];
         magnetUrl = `magnet:?xt=urn:btih:${best.info_hash}&dn=${encodeURIComponent(best.name)}&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337`;
       }
       
       res.json({ 
         title: title,
         torrentUrl: magnetUrl, 
         webUrl: `https://vidsrc.to/embed/${mediaType}/${id}`
       });
     } catch (e: any) {
       res.status(500).json({ error: e.message });
     }
  });

  app.get("/api/youtube-search", async (req, res) => {
    const query = req.query.q as string;
    if (!query) return res.json({ videoId: null });
    try {
      const ytSearch = (await import('yt-search')).default;
      const r = await ytSearch(query + ' audio');
      const video = r.videos[0];
      const thumbnail = video?.thumbnail || (video?.videoId ? `https://i.ytimg.com/vi/${video.videoId}/hqdefault.jpg` : null);
      res.json({ videoId: video?.videoId || null, thumbnail });
    } catch (e: any) {
      res.status(500).json({ error: e.message });
    }
  });

  const artworkCache = new Map<string, string>();

  app.get("/api/song-artwork", async (req, res) => {
    const title = (req.query.title as string || '').trim();
    const artist = (req.query.artist as string || '').trim();
    if (!title) return res.json({ artwork: null });

    const key = `${title.toLowerCase()}---${artist.toLowerCase()}`;
    if (artworkCache.has(key)) {
      return res.json({ artwork: artworkCache.get(key) });
    }

    try {
      // 1. Try iTunes search
      const q = encodeURIComponent(`${title} ${artist}`);
      const itunesRes = await fetch(`https://itunes.apple.com/search?term=${q}&entity=song&limit=1`);
      const itunesData = await itunesRes.json();
      if (itunesData.results && itunesData.results[0] && itunesData.results[0].artworkUrl100) {
        const art = itunesData.results[0].artworkUrl100.replace('100x100bb.jpg', '600x600bb.jpg').replace('100x100bb.png', '600x600bb.png');
        artworkCache.set(key, art);
        return res.json({ artwork: art });
      }

      // 2. Try YouTube search
      const ytSearch = (await import('yt-search')).default;
      const r = await ytSearch(`${title} ${artist} audio`);
      const video = r.videos[0];
      const thumbnail = video?.thumbnail || (video?.videoId ? `https://i.ytimg.com/vi/${video.videoId}/hqdefault.jpg` : null);
      if (thumbnail) {
        artworkCache.set(key, thumbnail);
        return res.json({ artwork: thumbnail });
      }

      res.json({ artwork: null });
    } catch (e: any) {
      res.json({ artwork: null });
    }
  });

  let ytmusic: any = null;
  const getYTMusic = async () => {
    if (!ytmusic) {
      const YTMusic = (await import('ytmusic-api')).default;
      ytmusic = new YTMusic();
      await ytmusic.initialize();
    }
    return ytmusic;
  };


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

  app.get("/api/search-tracks", async (req, res) => {
    const query = req.query.q as string;
    if (!query) return res.json({ results: [] });
    try {
      const ytm = await getYTMusic();
      const r = await ytm.searchSongs(query);
      
      const results = r.slice(0, 50).map((v: any) => {
        let durationStr = "0:00";
        if (v.duration) {
            const m = Math.floor(v.duration / 60);
            const s = v.duration % 60;
            durationStr = `${m}:${s.toString().padStart(2, '0')}`;
        }
        let bestThumbnail = (v.videoId ? `https://i.ytimg.com/vi/${v.videoId}/hqdefault.jpg` : "");
        if (v.thumbnails && v.thumbnails.length > 0) {
          const rawUrl = v.thumbnails[v.thumbnails.length - 1].url;
          bestThumbnail = rawUrl ? rawUrl.replace(/=w\d+-h\d+/, '=w600-h600') : bestThumbnail;
        }

        return {
            id: v.videoId,
            title: v.name,
            artist: v.artist.name,
            album: v.album?.name || "Single",
            duration: durationStr,
            durationSeconds: v.duration || 0,
            coverUrl: bestThumbnail,
            youtubeId: v.videoId
        };
      });
      res.json({ results });
    } catch (e: any) {
      res.status(500).json({ error: e.message });
    }
  });

  app.all('/api/*', (req, res) => {
    res.status(404).json({ error: "API route not found" });
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*all', (req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer();
