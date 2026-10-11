async function checkEmbeds() {
  const urls = [
    "https://vidsrc.to/embed/movie/550",
    "https://vidsrc.me/embed/movie?tmdb=550",
    "https://vidsrc.in/embed/movie?tmdb=550",
    "https://vidsrc.pm/embed/movie?tmdb=550",
    "https://vidsrc.net/embed/movie?tmdb=550",
    "https://vidsrc.xyz/embed/movie?tmdb=550",
    "https://autoembed.to/movie/tmdb/550",
    "https://autoembed.co/movie/tmdb/550",
    "https://player.smashy.stream/movie/550",
    "https://multiembed.mov/directstream.php?video_id=550&tmdb=1"
  ];
  for (const url of urls) {
    try {
      const res = await fetch(url, { headers: { "User-Agent": "Mozilla/5.0" }});
      const text = await res.text();
      console.log(url, res.status, text.includes('top') ? 'HAS_TOP' : 'NO_TOP', text.includes('sandbox') ? 'HAS_SANDBOX' : 'NO_SANDBOX');
    } catch(e) {
      console.log(url, e.message);
    }
  }
}
checkEmbeds();
