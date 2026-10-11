import https from 'https';
async function test() {
  const res = await fetch("https://player.autoembed.cc/embed/movie/550");
  const text = await res.text();
  console.log(text.includes('Sandbox'));
}
test();
