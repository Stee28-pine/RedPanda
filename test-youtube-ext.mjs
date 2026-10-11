import ytExt from "youtube-ext";
async function run() {
  const info = await ytExt.videoInfo("yleXPEPJIgI");
  console.log(info.streamingData.formats[0].url);
}
run();
