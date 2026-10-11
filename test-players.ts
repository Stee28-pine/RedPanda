import fetch from "node-fetch";

const urls = [
  "https://vidsrc.to/embed/movie/550",
  "https://vidsrc.me/embed/movie?tmdb=550",
  "https://vidsrc.in/embed/movie?tmdb=550",
  "https://vidsrc.pm/embed/movie?tmdb=550",
  "https://vidsrc.xyz/embed/movie?tmdb=550",
  "https://vidsrc.net/embed/movie?tmdb=550",
  "https://embed.su/embed/movie/550",
  "https://moviesapi.club/movie/550",
  "https://autoembed.co/movie/tmdb/550",
  "https://multiembed.mov/directstream.php?video_id=550&tmdb=1"
];
urls.forEach(async url => {
  try {
    const res = await fetch(url);
    console.log(url, res.status, res.headers.get("x-frame-options"), res.headers.get("content-security-policy"));
  } catch(e) {
    console.log(url, e.message);
  }
});
