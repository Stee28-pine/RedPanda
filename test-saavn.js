async function test() {
  try {
    const res = await fetch("https://saavn.me/search/songs?query=Shape+of+You+Ed+Sheeran");
    const data = await res.json();
    console.log("saavn.me:", JSON.stringify(data?.data?.results?.[0]?.downloadUrl));
  } catch(e) {
    console.error("saavn.me error:", e.message);
  }
  
  try {
    const res = await fetch("https://saavn.dev/api/search/songs?query=Shape+of+You+Ed+Sheeran");
    const data = await res.json();
    console.log("saavn.dev:", JSON.stringify(data?.data?.results?.[0]?.downloadUrl));
  } catch(e) {
    console.error("saavn.dev error:", e.message);
  }
}
test();
