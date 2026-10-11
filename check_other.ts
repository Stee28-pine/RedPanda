import fs from 'fs';

async function check() {
  const urls = [
    'https://player.smashy.stream/movie/550',
    'https://multiembed.mov/?video_id=550&tmdb=1',
    'https://moviesapi.club/movie/550',
  ];
  for (const url of urls) {
     const res = await fetch(url);
     console.log(url, res.status, res.headers.get('x-frame-options'));
  }
}
check();
