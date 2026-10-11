async function test() {
  try {
    const res = await fetch("https://spotifyapi.caliph.dev/api/search/tracks?q=shape+of+you");
    const data = await res.json();
    console.log(data);
  } catch(e) {}
}
test();
