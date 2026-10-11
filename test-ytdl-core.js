import ytdl from 'ytdl-core';
async function test() {
  try {
    const info = await ytdl.getInfo('BjL7AuPsmEk');
    console.log(info.formats.length);
  } catch (e) {
    console.error("ytdl-core error:", e.message);
  }
}
test();
