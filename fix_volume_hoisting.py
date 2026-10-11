with open('src/App.tsx', 'r') as f:
    content = f.read()

bad_effect = """  useEffect(() => {
    if (gainNodeRef.current) {
      // Smoothly transition volume
      gainNodeRef.current.gain.setTargetAtTime(volume * crossfadeVolume, audioCtxRef.current?.currentTime || 0, 0.1);
    }
  }, [volume, crossfadeVolume]);

  const [searchQuery, setSearchQuery] = useState('');"""

fixed_content = content.replace(bad_effect, "  const [searchQuery, setSearchQuery] = useState('');")

insert_point = """  const [youtubeId, setYoutubeId] = useState<string | null>(null);

  useEffect(() => {"""

replacement = """  const [youtubeId, setYoutubeId] = useState<string | null>(null);

  useEffect(() => {
    if (gainNodeRef.current) {
      // Smoothly transition volume
      gainNodeRef.current.gain.setTargetAtTime(volume * crossfadeVolume, audioCtxRef.current?.currentTime || 0, 0.1);
    }
  }, [volume, crossfadeVolume]);

  useEffect(() => {"""

fixed_content = fixed_content.replace(insert_point, replacement)

with open('src/App.tsx', 'w') as f:
    f.write(fixed_content)
