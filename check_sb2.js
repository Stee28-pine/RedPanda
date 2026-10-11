import https from 'https';
function check(url) {
  const req = https.get(url, (res) => {
    let body = '';
    res.on('data', chunk => body += chunk);
    res.on('end', () => console.log(url, res.statusCode, body.includes('Sandbox') ? 'Blocks Sandbox' : 'Allows Sandbox (Maybe)'));
  });
}
check('https://autoembed.co/movie/tmdb/550');
check('https://multiembed.mov/?video_id=550&tmdb=1');
