import YTMusic from "ytmusic-api";

async function run() {
    const ytmusic = new YTMusic();
    await ytmusic.initialize();

    const album = await ytmusic.getAlbum("MPREb_VXy1rdyyCvA");
    console.log(JSON.stringify(album, null, 2));
}
run();
