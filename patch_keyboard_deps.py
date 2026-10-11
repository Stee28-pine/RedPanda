import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace("  }, [handleNext, handlePrev]);", "  }, [handleNext, handlePrev, nowPlaying, likedSongs, volume]);")

with open('src/App.tsx', 'w') as f:
    f.write(content)
