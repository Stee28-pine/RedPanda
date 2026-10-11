import https from 'https';

async function check(url) {
  try {
    const r = await fetch(url, { headers: { "User-Agent": "Mozilla/5.0" }});
    const t = await r.text();
    console.log(url, r.status, 'Histats:', t.includes('histats'), 'vidapi:', t.toLowerCase().includes('vidapi'));
  } catch(e) {
    console.log(url, e.message);
  }
}

async function run() {
  await check("https://autoembed.co/movie/tmdb/550");
  await check("https://vidsrc.to/embed/movie/550");
  await check("https://vidsrc.me/embed/movie?tmdb=550");
  await check("https://vidsrc.in/embed/movie?tmdb=550");
  await check("https://vidsrc.net/embed/movie?tmdb=550");
  await check("https://multiembed.mov/directstream.php?video_id=550&tmdb=1");
  await check("https://player.smashy.stream/movie/550");
  await check("https://vidsrc.pro/embed/movie/550");
}
run();
