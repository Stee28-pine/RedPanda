import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Add setYoutubeId(null)
replacement = """  useEffect(() => {
    if (!nowPlaying) {
      setYoutubeId(null);
      return;
    }
    
    // Attempt to use existing youtubeId or fetch a new one
    if (nowPlaying.youtubeId) {
      setYoutubeId(nowPlaying.youtubeId);
      setIsBuffering(false);
      return;
    }

    setYoutubeId(null);
    const fetchYtId = async () => {
"""
content = re.sub(
    r'  useEffect\(\(\) => \{\n    if \(!nowPlaying\) return;\n    \n    // Attempt to use existing youtubeId or fetch a new one\n    if \(nowPlaying\.youtubeId\) \{\n      setYoutubeId\(nowPlaying\.youtubeId\);\n      setIsBuffering\(false\);\n      return;\n    \}\n\n    const fetchYtId = async \(\) => \{',
    replacement,
    content
)

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("Updated App.tsx")
