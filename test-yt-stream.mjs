import ytStream from "yt-stream";
async function run() {
  const info = await ytStream.stream("https://www.youtube.com/watch?v=yleXPEPJIgI", {
      quality: 'high',
      type: 'audio',
      highWaterMark: 1048576 * 32
  });
  console.log(info);
}
run();
