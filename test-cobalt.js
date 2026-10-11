async function test() {
  try {
    const res = await fetch("https://co.wuk.sh/api/json", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      body: JSON.stringify({
        url: "https://www.youtube.com/watch?v=BjL7AuPsmEk",
        isAudioOnly: true
      })
    });
    const data = await res.json();
    console.log("cobalt:", data);
  } catch(e) {
    console.error("cobalt error:", e.message);
  }
}
test();
