import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Add playbackRate state and fadeOutIntervalRef
state_injection = """  const [volume, setVolume] = useState(1);
  const [crossfadeVolume, setCrossfadeVolume] = useState(1);
  const [playbackRate, setPlaybackRate] = useState(1);
  const fadeOutIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const isCrossfading = useRef(false);"""

content = content.replace("  const [volume, setVolume] = useState(1);\n  const [crossfadeVolume, setCrossfadeVolume] = useState(1);\n  const isCrossfading = useRef(false);", state_injection)

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

content = content.replace("  const handlePlaySong = (song: Song, collection?: Collection) => {", fade_out_fn + "\n  const handlePlaySong = (song: Song, collection?: Collection) => {")

player_props = """          isMini={isScrolled}
          volume={volume * crossfadeVolume}
          onVolumeChange={setVolume}
          playbackRate={playbackRate}
          onPlaybackRateChange={setPlaybackRate}
          onFadeOut={handleFadeOut}"""

content = content.replace("          isMini={isScrolled}\n          volume={volume * crossfadeVolume}\n          onVolumeChange={setVolume}", player_props)

react_player_props = """            volume={volume * crossfadeVolume}
            playbackRate={playbackRate}
            width="200px" """

content = content.replace('            volume={volume * crossfadeVolume}\n            width="200px"', react_player_props)

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("App.tsx states patched")
