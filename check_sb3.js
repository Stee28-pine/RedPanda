import https from 'https';
function check(url) {
  const req = https.get(url, (res) => {
    let body = '';
    res.on('data', chunk => body += chunk);
    res.on('end', () => console.log(url, res.statusCode, body.includes('Sandbox') ? 'Blocks Sandbox' : 'Allows Sandbox (Maybe)'));
  });
}
check('https://www.2embed.cc/embedtv/1416&s=1&e=1');
