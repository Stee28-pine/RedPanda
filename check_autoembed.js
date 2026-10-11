import https from 'https';

async function test() {
  const get = async (url) => {
      const r = await fetch(url, { headers: { "User-Agent": "Mozilla/5.0" }});
      const t = await r.text();
      console.log(r.status, t.substring(0, 500));
  };
  await get("https://autoembed.co/tv/tmdb/1396-1-1");
}
test();
