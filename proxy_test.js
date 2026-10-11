import fs from 'fs';
import https from 'https';
const req = https.get('https://vidlink.pro/movie/550', (res) => {
  let body = '';
  res.on('data', c => body += c);
  res.on('end', () => fs.writeFileSync('vidlink.html', body));
});
