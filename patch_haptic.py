import re

with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

# The wrapper functions
wrappers = """
  // Haptic feedback wrappers
  const triggerHaptic = (pattern: number | number[] = 10) => {
    if (typeof navigator !== 'undefined' && navigator.vibrate) {
      try { navigator.vibrate(pattern); } catch(e) {}
    }
  };

  const handleTogglePlay = () => { triggerHaptic([15, 40, 15]); onTogglePlay(); };
  const handleNextTrack = () => { triggerHaptic(15); onNext?.(); };
  const handlePrevTrack = () => { triggerHaptic(15); onPrev?.(); };
  const handleToggleLike = () => { triggerHaptic(10); onToggleLike?.(); };
  const handleToggleShuffle = () => { triggerHaptic(10); onToggleShuffle?.(); };
  const handleToggleRepeat = () => { triggerHaptic(10); onToggleRepeat?.(); };
  
  return (
"""

# Insert wrappers right before `return (`
content = content.replace('  return (\n    <>', wrappers + '    <>')

# Replace exact strings for onClick
content = content.replace('onClick={onTogglePlay}', 'onClick={handleTogglePlay}')
content = content.replace('onClick={onNext}', 'onClick={handleNextTrack}')
content = content.replace('onClick={onPrev}', 'onClick={handlePrevTrack}')
content = content.replace('onClick={onToggleLike}', 'onClick={handleToggleLike}')
content = content.replace('onClick={onToggleShuffle}', 'onClick={handleToggleShuffle}')
content = content.replace('onClick={onToggleRepeat}', 'onClick={handleToggleRepeat}')

# Save back
with open('src/components/Player.tsx', 'w') as f:
    f.write(content)

print("Haptic patch applied")
