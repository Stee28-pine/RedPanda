import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

old_keyl = """        case 'KeyL':
          e.preventDefault();
          if (nowPlaying) {
             toggleLike(nowPlaying);
          }
          break;"""

new_keyl = """        case 'KeyL':
          e.preventDefault();
          if (nowPlaying) {
             toggleLike(nowPlaying);
             const isLiked = likedSongs.some(s => s.id === nowPlaying.id);
             showToast(isLiked ? 'Removed from Liked Songs' : 'Added to Liked Songs');
          }
          break;"""

content = content.replace(old_keyl, new_keyl)

with open('src/App.tsx', 'w') as f:
    f.write(content)
