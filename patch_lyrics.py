with open('src/components/LyricsOverlay.tsx', 'r') as f:
    content = f.read()

import re

search_mock = r"const MOCK_LYRICS = \[.*?\];"

replace_mock = """const MOCK_LYRICS = [
  { time: 0, text: "(Instrumental Intro)" },
  { time: 5000, text: "I've been running through the jungle" },
  { time: 9000, text: "I've been running with the wolves" },
  { time: 13000, text: "To get to you, to get to you" },
  { time: 18000, text: "I've been down the darkest alleys" },
  { time: 22000, text: "Saw the dark side of the moon" },
  { time: 26000, text: "To get to you, to get to you" },
  { time: 31000, text: "I've looked for love in every stranger" },
  { time: 35000, text: "Took too much to ease the anger" },
  { time: 39000, text: "All for you, yeah, all for you" },
  { time: 44000, text: "Let it play, let it play, let it play" },
  { time: 49000, text: "(Chorus)" },
  { time: 55000, text: "Oh, it's just a placeholder lyric" },
  { time: 60000, text: "Since we don't have the real ones" },
  { time: 65000, text: "But it looks amazing" },
  { time: 70000, text: "Doesn't it?" },
];"""

content = re.sub(search_mock, replace_mock, content, flags=re.DOTALL)

with open('src/components/LyricsOverlay.tsx', 'w') as f:
    f.write(content)
