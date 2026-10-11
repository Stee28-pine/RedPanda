import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

replacement = """      </main>
      
      <AnimatePresence>
        {showRightSidebar && (
          <>
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="md:hidden fixed inset-0 z-40 bg-black/20 backdrop-blur-sm"
              onClick={() => setShowRightSidebar(false)}
            />
            <RightSidebar currentTime={currentPlaybackTime} nowPlaying={nowPlaying} queue={queue} onReorder={handleReorderQueue} />
          </>
        )}
      </AnimatePresence>
"""

# Wait, `RightSidebar` doesn't have an exit animation natively, but we can wrap it if we want, or just leave it.
# Actually it might be easier to just conditionally render the backdrop.
content = content.replace('      {showRightSidebar && (\n        <RightSidebar currentTime={currentPlaybackTime} nowPlaying={nowPlaying} queue={queue} onReorder={handleReorderQueue} />\n      )}', replacement)

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("Right sidebar backdrop patched")
