import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Add state
state_search = "  const [showRightSidebar, setShowRightSidebar] = useState(false);"
state_replace = "  const [showRightSidebar, setShowRightSidebar] = useState(false);\n  const [showShortcuts, setShowShortcuts] = useState(false);"
content = content.replace(state_search, state_replace)

# Add keydown case
key_search = """        case 'KeyP':
          e.preventDefault();
          handlePrev();
          break;
      }
    };"""
key_replace = """        case 'KeyP':
          e.preventDefault();
          handlePrev();
          break;
        case 'Slash':
          if (e.shiftKey) {
            e.preventDefault();
            setShowShortcuts(prev => !prev);
          }
          break;
      }
    };"""
content = content.replace(key_search, key_replace)

# Add Modal UI
modal_ui = """      <AnimatePresence>
        {showShortcuts && (
          <motion.div 
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-[100] bg-black/40 backdrop-blur-sm flex items-center justify-center p-4"
            onClick={() => setShowShortcuts(false)}
          >
            <motion.div 
              initial={{ scale: 0.95 }} animate={{ scale: 1 }} exit={{ scale: 0.95 }}
              onClick={e => e.stopPropagation()}
              className="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-md"
            >
              <h3 className="text-xl font-bold mb-6">Keyboard Shortcuts</h3>
              <div className="space-y-4">
                <ShortcutRow keys={['Space']} label="Play / Pause" />
                <ShortcutRow keys={['N']} label="Next Track" />
                <ShortcutRow keys={['P']} label="Previous Track" />
                <ShortcutRow keys={['→']} label="Seek Forward 10s" />
                <ShortcutRow keys={['←']} label="Seek Backward 10s" />
                <ShortcutRow keys={['↑']} label="Volume Up" />
                <ShortcutRow keys={['↓']} label="Volume Down" />
                <ShortcutRow keys={['?']} label="Toggle Shortcuts" />
              </div>
              <button 
                onClick={() => setShowShortcuts(false)}
                className="w-full mt-8 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-800 font-bold rounded-lg transition-colors"
              >
                Close
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
"""

# Insert modal at the end before closing div
content = content.replace("    </div>\n  );\n}\n", modal_ui + "    </div>\n  );\n}\n")

# Add ShortcutRow component
row_component = """
function ShortcutRow({ keys, label }: { keys: string[], label: string }) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-sm font-semibold text-gray-600">{label}</span>
      <div className="flex gap-1.5">
        {keys.map(k => (
          <kbd key={k} className="px-2 py-1 bg-gray-100 border border-gray-200 rounded text-xs font-mono font-bold text-gray-800 min-w-[24px] text-center">
            {k}
          </kbd>
        ))}
      </div>
    </div>
  );
}
"""
content = content + row_component

with open('src/App.tsx', 'w') as f:
    f.write(content)
