async function test() {
  const instances = [
    "https://pipedapi.kavin.rocks",
    "https://pipedapi.tokhmi.xyz",
    "https://pipedapi.lunar.icu",
    "https://piped-api.garudalinux.org"
  ];
  for (const url of instances) {
    try {
      const res = await fetch(url + "/streams/BjL7AuPsmEk");
      const data = await res.json();
      console.log(url, "success! audioStreams:", data.audioStreams?.length);
      return;
    } catch(e) {
      console.error(url, "failed");
    }
  }
}
test();
