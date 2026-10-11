import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Setup GainNode in onReady
old_setup = """                        sourceNodeRef.current.connect(compressorNodeRef.current);
                        compressorNodeRef.current.connect(analyzerNodeRef.current);
                        analyzerNodeRef.current.connect(audioCtxRef.current.destination);"""

new_setup = """                        gainNodeRef.current = audioCtxRef.current.createGain();
                        gainNodeRef.current.gain.value = volume;
                        
                        sourceNodeRef.current.connect(compressorNodeRef.current);
                        compressorNodeRef.current.connect(gainNodeRef.current);
                        gainNodeRef.current.connect(analyzerNodeRef.current);
                        analyzerNodeRef.current.connect(audioCtxRef.current.destination);"""

content = content.replace(old_setup, new_setup)

# Update GainNode when volume changes
volume_effect = """  useEffect(() => {
    if (gainNodeRef.current) {
      // Smoothly transition volume
      gainNodeRef.current.gain.setTargetAtTime(volume * crossfadeVolume, audioCtxRef.current?.currentTime || 0, 0.1);
    }
  }, [volume, crossfadeVolume]);

  const [searchQuery, setSearchQuery] = useState('');"""

content = content.replace("  const [searchQuery, setSearchQuery] = useState('');", volume_effect)

with open('src/App.tsx', 'w') as f:
    f.write(content)
