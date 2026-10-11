import re

with open('src/components/RightSidebar.tsx', 'r') as f:
    content = f.read()

search = """    fetch(`https://api.lyrics.ovh/v1/${encodeURIComponent(nowPlaying.artist)}/${encodeURIComponent(nowPlaying.title)}`)
      .then(res => res.json())
      .then(data => {
        if (data.lyrics) {
          const lines = data.lyrics.split('\\n').filter((l: string) => l.trim().length > 0);
          const timePerLine = (nowPlaying.durationSeconds || 180) / (lines.length || 1);
          const synced = lines.map((line: string, idx: number) => ({
            time: idx * timePerLine,
            text: line
          }));
          setFetchedLyrics(synced);
        } else {
          setFetchedLyrics([]);
        }
      })"""

replace = """    fetch(`https://lrclib.net/api/get?artist_name=${encodeURIComponent(nowPlaying.artist)}&track_name=${encodeURIComponent(nowPlaying.title)}`)
      .then(res => res.json())
      .then(data => {
        if (data.syncedLyrics) {
          const lines = data.syncedLyrics.split('\\n');
          const synced = lines.map((line: string) => {
            const match = line.match(/^\\[(\\d{2}):(\\d{2}\\.\\d{2})\\]\\s*(.*)$/);
            if (match) {
              const minutes = parseInt(match[1]);
              const seconds = parseFloat(match[2]);
              return { time: minutes * 60 + seconds, text: match[3] || '...' };
            }
            return null;
          }).filter((l: any) => l !== null);
          setFetchedLyrics(synced);
        } else if (data.plainLyrics) {
          const lines = data.plainLyrics.split('\\n').filter((l: string) => l.trim().length > 0);
          const timePerLine = (nowPlaying.durationSeconds || 180) / (lines.length || 1);
          const synced = lines.map((line: string, idx: number) => ({
            time: idx * timePerLine,
            text: line
          }));
          setFetchedLyrics(synced);
        } else {
          setFetchedLyrics([]);
        }
      })"""

content = content.replace(search, replace)

with open('src/components/RightSidebar.tsx', 'w') as f:
    f.write(content)
