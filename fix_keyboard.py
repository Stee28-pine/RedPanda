import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Replace the wrong playerRef logic
bad_logic = """        case 'ArrowRight':
          e.preventDefault();
          if (playerRef.current && playerRef.current.duration) {
            playerRef.current.currentTime = Math.min(playerRef.current.currentTime + 10, playerRef.current.duration);
          }
          break;
        case 'ArrowLeft':
          e.preventDefault();
          if (playerRef.current) {
            playerRef.current.currentTime = Math.max(playerRef.current.currentTime - 10, 0);
          }
          break;"""

good_logic = """        case 'ArrowRight':
          e.preventDefault();
          if (playerRef.current) {
            const current = playerRef.current.getCurrentTime();
            const dur = playerRef.current.getDuration();
            if (dur) {
                playerRef.current.seekTo(Math.min(current + 10, dur), 'seconds');
            }
          }
          break;
        case 'ArrowLeft':
          e.preventDefault();
          if (playerRef.current) {
            const current = playerRef.current.getCurrentTime();
            playerRef.current.seekTo(Math.max(current - 10, 0), 'seconds');
          }
          break;"""

content = content.replace(bad_logic, good_logic)

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("done")
