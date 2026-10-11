with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

insert_str = """
  if (!song) {
    return (
      <div className="absolute opacity-[0.01] pointer-events-none -z-10 w-[200px] h-[200px] overflow-hidden">
        <ReactPlayer
          ref={playerRef}
          url=""
        />
      </div>
    );
  }
"""

content = content.replace('  return (\n    <>\n      <AnimatePresence>', insert_str + '\n  return (\n    <>\n      <AnimatePresence>')

with open('src/components/Player.tsx', 'w') as f:
    f.write(content)
print("Done")
