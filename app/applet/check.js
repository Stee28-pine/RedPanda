const https = require('https');

const urls = [
  'https://vidsrc.me/embed/movie?tmdb=550',
  'https://vidsrc.to/embed/movie/550',
  'https://vidsrc.pro/embed/movie/550',
  'https://vidsrc.vip/embed/movie/550',
  'https://embed.su/embed/movie/550',
  'https://multiembed.mov/?video_id=550&tmdb=1',
  'https://www.2embed.cc/embed/550',
  'https://vidsrc.icu/embed/movie/550',
  'https://vidsrc.net/embed/movie/550',
  'https://vidsrc.in/embed/movie/550',
  'https://player.smashy.stream/movie/550',
  'https://moviesapi.club/movie/550'
];

urls.forEach(url => {
  const req = https.get(url, { rejectUnauthorized: false }, (res) => {
    console.log(`${url} => Status: ${res.statusCode}, X-Frame-Options: ${res.headers['x-frame-options'] || 'None'}`);
  });
  req.on('error', (e) => {
    console.log(`${url} => Error: ${e.message}`);
  });
  req.setTimeout(5000, () => {
    console.log(`${url} => Timeout`);
    req.abort();
  });
});
