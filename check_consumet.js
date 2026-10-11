import https from 'https';
https.get('https://consumet-api.herokuapp.com/', (res) => {
  console.log(res.statusCode);
}).on('error', () => console.log('error'));
