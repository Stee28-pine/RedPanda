import YTMusic from "ytmusic-api";

async function run() {
    const ytmusic = new YTMusic();
    await ytmusic.initialize();

    const searchResults = await ytmusic.search("Glory Yo Yo Honey Singh");
    console.log(JSON.stringify(searchResults.slice(0, 2), null, 2));
}
run();
