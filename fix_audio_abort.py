import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

new_hooks = """
  useEffect(() => {
    if (audioRef.current) {
      if (isPlaying) {
        const p = audioRef.current.play();
        if (p !== undefined) {
          p.catch(e => {
            if (e.name !== 'AbortError') {
              console.error("Playback error:", e);
            }
          });
        }
      } else {
        audioRef.current.pause();
      }
    }
  }, [isPlaying]);

  useEffect(() => {
    if (audioRef.current && nowPlaying?.audioUrl) {
      audioRef.current.src = nowPlaying.audioUrl;
      setIsBuffering(true);
      const p = audioRef.current.play();
      if (p !== undefined) {
        p.then(() => {
          setIsPlaying(true);
        }).catch(e => {
          if (e.name !== 'AbortError') {
            console.error("Autoplay prevented:", e);
            setIsPlaying(false);
          }
        });
      }
    }
  }, [nowPlaying]);
"""

# Replace the old hooks with the new ones
old_hooks_regex = r"  useEffect\(\(\) => \{\n    if \(audioRef\.current\) \{\n      if \(isPlaying\) \{\n        audioRef\.current\.play\(\)\.catch\(e => console\.error\(\"Playback error:\", e\)\);\n      \} else \{\n        audioRef\.current\.pause\(\);\n      \}\n    \}\n  \}, \[isPlaying\]\);\n\n  useEffect\(\(\) => \{\n    if \(audioRef\.current && nowPlaying\?\.audioUrl\) \{\n      audioRef\.current\.src = nowPlaying\.audioUrl;\n      setIsBuffering\(true\);\n      audioRef\.current\.play\(\)\.then\(\(\) => \{\n        setIsPlaying\(true\);\n      \}\)\.catch\(e => \{\n        console\.error\(\"Autoplay prevented:\", e\);\n        setIsPlaying\(false\);\n      \}\);\n    \}\n  \}, \[nowPlaying\]\);"

content = re.sub(old_hooks_regex, new_hooks.strip(), content)

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("Updated App.tsx")
