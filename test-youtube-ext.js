import yt from 'youtube-ext';
async function test() {
  try {
    const info = await yt.videoInfo('https://www.youtube.com/watch?v=BjL7AuPsmEk');
    console.log(info.streams?.length > 0 ? info.streams[0].url : "no streams");
  } catch (e) {
    console.error(e);
  }
}
test();
