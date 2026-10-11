import re

with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

# Extract the ReactPlayer block
react_player_block_match = re.search(r'(<div className="absolute opacity-\[0\.01\].*?</div>)', content, re.DOTALL)
if react_player_block_match:
    react_player_block = react_player_block_match.group(1)
    # Remove it from its current position
    content = content.replace(react_player_block, '')
    
    # Insert it right before <AnimatePresence>\n        <motion.div
    content = content.replace('<AnimatePresence>\n        <motion.div', react_player_block + '\n      <AnimatePresence>\n        {song && (\n        <motion.div')
    
    # Add closing brace for {song && (
    content = content.replace('</motion.div>\n    </AnimatePresence>', '</motion.div>\n        )}\n    </AnimatePresence>')

    with open('src/components/Player.tsx', 'w') as f:
        f.write(content)
    print("Done")
else:
    print("Not found")

