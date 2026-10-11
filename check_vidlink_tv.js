import https from 'https';
function check(url) {
  const req = https.get(url, (res) => {
    let body = '';
    res.on('data', chunk => body += chunk);
    res.on('end', () => console.log(url, res.statusCode));
  });
}
check('https://vidlink.pro/tv/1416/1/1');
check('https://vidlink.pro/tv/1416?season=1&episode=1');
