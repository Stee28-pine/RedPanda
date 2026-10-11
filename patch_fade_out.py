import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

fade_out_fn = """  const handleFadeOut = () => {
    if (!isPlaying) return;
    const duration = 3000;
    const steps = 30;
    const stepTime = duration / steps;
    let currentStep = 0;

    if (fadeOutIntervalRef.current) clearInterval(fadeOutIntervalRef.current);

    fadeOutIntervalRef.current = setInterval(() => {
      currentStep++;
      if (currentStep >= steps) {
        if (fadeOutIntervalRef.current) clearInterval(fadeOutIntervalRef.current);
        setIsPlaying(false);
        setCrossfadeVolume(1);
      } else {
        setCrossfadeVolume(1 - (currentStep / steps));
      }
    }, stepTime);
  };
"""

content = content.replace("  const handlePlaySong = (song: Song, context?: { songs: Song[] } | Collection) => {", fade_out_fn + "\n  const handlePlaySong = (song: Song, context?: { songs: Song[] } | Collection) => {")

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("handleFadeOut injected")
