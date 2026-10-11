async function test() {
  const get = async (url) => {
    try {
      const r = await fetch(url);
      const t = await r.text();
      console.log(url, r.status, t.substring(0, 150));
    } catch(e) {
      console.log(url, e.message);
    }
  };
  await get("https://vidlink.pro/api/movie/550");
  await get("https://vidlink.pro/api/video/movie/550");
  await get("https://vidlink.pro/api/source/movie/550");
}
test();
