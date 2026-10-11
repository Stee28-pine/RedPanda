import https from 'https';
function check(url) {
  const req = https.get(url, (res) => {
    let body = '';
    res.on('data', chunk => body += chunk);
    res.on('end', () => console.log(url, res.statusCode, body.includes('Disable Sandbox') ? 'Blocks Sandbox' : 'Allows Sandbox (Maybe)'));
  });
}
check('https://www.2embed.cc/embed/550');
check('https://vidsrc.to/embed/movie/550');
