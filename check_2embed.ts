import fs from 'fs';

async function check() {
  const url = 'https://www.2embed.cc/embed/550';
  const res = await fetch(url);
  const text = await res.text();
  console.log(text.slice(0, 500));
}
check();
