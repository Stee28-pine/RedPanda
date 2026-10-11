import https from 'https';
function check(url) {
  const req = https.get(url, (res) => {
    let body = '';
    res.on('data', chunk => body += chunk);
    res.on('end', () => {
      if (body.includes("Sandbox")) {
         console.log("FOUND SANDBOX:", body.substring(body.indexOf("Sandbox") - 20, body.indexOf("Sandbox") + 20));
      }
    });
  });
}
check('https://www.2embed.cc/embedtv/1416&s=1&e=1');
