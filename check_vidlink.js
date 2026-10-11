import https from 'https';
function check(url) {
  const req = https.get(url, (res) => {
    let body = '';
    res.on('data', chunk => body += chunk);
    res.on('end', () => {
      console.log(url, res.statusCode);
      if (body.toLowerCase().includes("sandbox")) {
         console.log("BLOCKS SANDBOX! ", body.substring(body.toLowerCase().indexOf("sandbox") - 40, body.toLowerCase().indexOf("sandbox") + 40));
      } else {
         console.log("DOES NOT BLOCK SANDBOX (probably)");
      }
    });
  });
}
check('https://vidlink.pro/movie/550');
