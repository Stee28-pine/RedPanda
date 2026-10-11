import re

with open('src/data.ts', 'r') as f:
    content = f.read()

new_songs = """
  // Asian Artists
  { id: '101', title: 'Dynamite', artist: 'BTS', album: 'BE', duration: '3:19', durationSeconds: 199, coverUrl: 'https://images.unsplash.com/photo-1614113489855-66422ad300a4?w=400&q=80', genre: 'K-Pop' },
  { id: '102', title: 'Butter', artist: 'BTS', album: 'Butter', duration: '2:44', durationSeconds: 164, coverUrl: 'https://images.unsplash.com/photo-1614113489855-66422ad300a4?w=400&q=80', genre: 'K-Pop' },
  { id: '103', title: 'Slow Dancing In The Dark', artist: 'Joji', album: 'BALLADS 1', duration: '3:29', durationSeconds: 209, coverUrl: 'https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=400&q=80', genre: 'R&B' },
  { id: '104', title: 'Glimpse of Us', artist: 'Joji', album: 'SMITHEREENS', duration: '3:53', durationSeconds: 233, coverUrl: 'https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=400&q=80', genre: 'Pop' },
  { id: '105', title: 'How You Like That', artist: 'BLACKPINK', album: 'THE ALBUM', duration: '3:01', durationSeconds: 181, coverUrl: 'https://images.unsplash.com/photo-1614113489855-66422ad300a4?w=400&q=80', genre: 'K-Pop' },
  { id: '106', title: 'First Love', artist: 'Utada Hikaru', album: 'First Love', duration: '4:17', durationSeconds: 257, coverUrl: 'https://images.unsplash.com/photo-1528644342550-96693a74313d?w=400&q=80', genre: 'J-Pop' },
  
  // American Artists
  { id: '201', title: 'Cruel Summer', artist: 'Taylor Swift', album: 'Lover', duration: '2:58', durationSeconds: 178, coverUrl: 'https://images.unsplash.com/photo-1493225457124-a1a2a5f0f42b?w=400&q=80', genre: 'Pop' },
  { id: '202', title: 'Anti-Hero', artist: 'Taylor Swift', album: 'Midnights', duration: '3:20', durationSeconds: 200, coverUrl: 'https://images.unsplash.com/photo-1493225457124-a1a2a5f0f42b?w=400&q=80', genre: 'Pop' },
  { id: '203', title: 'Blinding Lights', artist: 'The Weeknd', album: 'After Hours', duration: '3:20', durationSeconds: 200, coverUrl: 'https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=400&q=80', genre: 'Synth-Pop' },
  { id: '204', title: 'Starboy', artist: 'The Weeknd', album: 'Starboy', duration: '3:50', durationSeconds: 230, coverUrl: 'https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=400&q=80', genre: 'R&B' },
  { id: '205', title: 'HUMBLE.', artist: 'Kendrick Lamar', album: 'DAMN.', duration: '2:57', durationSeconds: 177, coverUrl: 'https://images.unsplash.com/photo-1528644342550-96693a74313d?w=400&q=80', genre: 'Hip-Hop' },
  { id: '206', title: 'bad guy', artist: 'Billie Eilish', album: 'When We All Fall Asleep', duration: '3:14', durationSeconds: 194, coverUrl: 'https://images.unsplash.com/photo-1493225457124-a1a2a5f0f42b?w=400&q=80', genre: 'Alternative Pop' },
  { id: '207', title: 'Gods Plan', artist: 'Drake', album: 'Scorpion', duration: '3:18', durationSeconds: 198, coverUrl: 'https://images.unsplash.com/photo-1528644342550-96693a74313d?w=400&q=80', genre: 'Hip-Hop' },
"""

content = content.replace("];\n\nexport const ALBUMS: Collection[] = [", new_songs + "];\n\nexport const ALBUMS: Collection[] = [")

with open('src/data.ts', 'w') as f:
    f.write(content)
