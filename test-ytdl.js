import ytdl from '@distube/ytdl-core';
async function test() {
  try {
    const info = await ytdl.getInfo('BjL7AuPsmEk');
    const format = ytdl.chooseFormat(info.formats, { quality: 'highestaudio' });
    console.log("Stream URL:", format.url);
  } catch (e) {
    console.error(e);
  }
}
test();
