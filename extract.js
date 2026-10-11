import https from 'https';
import fs from 'fs';

async function fetchM3u8() {
  const res = await fetch("https://vidlink.pro/movie/550");
  const html = await res.text();
  console.log(html.includes('.m3u8'));
  const match = html.match(/https:\/\/[^"']+\.m3u8/g);
  console.log(match);
}

fetchM3u8();
