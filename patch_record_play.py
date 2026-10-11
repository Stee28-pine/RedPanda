with open('src/App.tsx', 'r') as f:
    content = f.read()

insert_point = "  const [nowPlaying, setNowPlaying] = useState<Song | null>(null);"
effect = """
  useEffect(() => {
    if (nowPlaying) {
      recordPlay(nowPlaying);
    }
  }, [nowPlaying?.id]);"""

content = content.replace(insert_point, insert_point + effect)

with open('src/App.tsx', 'w') as f:
    f.write(content)
