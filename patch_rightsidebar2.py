import re

with open('src/components/RightSidebar.tsx', 'r') as f:
    content = f.read()

search = r"  const hasLyrics = nowPlaying\?\.lyrics && nowPlaying\.lyrics\.length > 0;.*?const currentLyricIdx = activeLyricIdx !== -1 \? \(nowPlaying!\.lyrics!\.length - 1\) - activeLyricIdx : -1;"

replace = """  const [fetchedLyrics, setFetchedLyrics] = useState<{ time: number; text: string }[] | null>(null);
  const [isLoadingLyrics, setIsLoadingLyrics] = useState(false);

  useEffect(() => {
    if (!nowPlaying) {
      setFetchedLyrics(null);
      return;
    }
    
    if (nowPlaying.lyrics && nowPlaying.lyrics.length > 0) {
      setFetchedLyrics(nowPlaying.lyrics);
      setIsLoadingLyrics(false);
      return;
    }

    setIsLoadingLyrics(true);
    setFetchedLyrics(null);
    
    fetch(`https://api.lyrics.ovh/v1/${encodeURIComponent(nowPlaying.artist)}/${encodeURIComponent(nowPlaying.title)}`)
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
      })
      .catch(() => {
        setFetchedLyrics([]);
      })
      .finally(() => {
        setIsLoadingLyrics(false);
      });
  }, [nowPlaying]);

  const hasLyrics = fetchedLyrics && fetchedLyrics.length > 0;
  
  const activeLyricIdx = hasLyrics
    ? [...(fetchedLyrics || [])].reverse().findIndex(lyric => currentTime >= lyric.time)
    : -1;
    
  const currentLyricIdx = activeLyricIdx !== -1 && fetchedLyrics ? (fetchedLyrics.length - 1) - activeLyricIdx : -1;"""

content = re.sub(search, replace, content, flags=re.DOTALL)

with open('src/components/RightSidebar.tsx', 'w') as f:
    f.write(content)
