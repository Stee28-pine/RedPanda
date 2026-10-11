import fs from 'fs';

async function check() {
  const urls = [
    'https://www.2embed.cc/embed/1416',
    'https://www.2embed.cc/embedtv/1416&s=1&e=1',
    'https://www.2embed.cc/embedtv/1416',
    'https://www.2embed.cc/embed/tv/1416'
  ];
  for (const url of urls) {
     const res = await fetch(url);
     console.log(url, res.status);
  }
}
check();
