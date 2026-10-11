import fs from 'fs';

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
  'https://moviesapi.club/movie/550',
  'https://vidsrc.xyz/embed/movie/550'
];

async function checkUrls() {
  for (const url of urls) {
    try {
      const res = await fetch(url, { signal: AbortSignal.timeout(3000) });
      console.log(`${url} => Status: ${res.status}, X-Frame-Options: ${res.headers.get('x-frame-options') || 'None'}`);
    } catch (e) {
      console.log(`${url} => Error: ${e.message}`);
    }
  }
}

checkUrls();
