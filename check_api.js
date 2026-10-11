import https from 'https';
https.get('https://vidsrc.cc/api/source/movie/550', (res) => {
  let body = '';
  res.on('data', c => body += c);
  res.on('end', () => console.log(res.statusCode, body));
});
