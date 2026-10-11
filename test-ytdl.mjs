import ytdl from "@distube/ytdl-core";
async function run() {
  const info = await ytdl.getInfo("yleXPEPJIgI");
  const format = ytdl.chooseFormat(info.formats, { quality: 'highestaudio' });
  console.log(format.url);
}
run();
