import express from 'express';
import ytdl from 'ytdl-core';
const app = express();
app.get('/stream', (req, res) => {
  try {
    ytdl('BjL7AuPsmEk', { filter: 'audioonly', quality: 'highestaudio' }).pipe(res);
  } catch (e) {
    res.status(500).send(e.message);
  }
});
const server = app.listen(3001, async () => {
  console.log("Server running");
  const fetch = await import('node-fetch');
  const res = await fetch.default('http://localhost:3001/stream');
  console.log("Status:", res.status, res.headers.get('content-type'));
  server.close();
});
