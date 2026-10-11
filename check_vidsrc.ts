import fs from 'fs';

async function check() {
  const url = 'https://vidsrc.to/embed/movie/550';
  const res = await fetch(url);
  const text = await res.text();
  console.log(text.slice(0, 500));
}
check();
