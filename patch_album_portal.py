import re

with open('src/components/AlbumView.tsx', 'r') as f:
    content = f.read()

# Make sure createPortal is imported
if 'createPortal' not in content:
    content = content.replace("import { useState } from 'react';", "import { useState } from 'react';\nimport { createPortal } from 'react-dom';")

# Wrap context menus in createPortal
# AlbumContextMenu
album_search = """      <AnimatePresence>
              {albumContextMenu && ("""
album_replace = """      {typeof document !== 'undefined' && createPortal(
        <AnimatePresence>
              {albumContextMenu && ("""
content = content.replace(album_search, album_replace)

context_menu_close = """              <Share2 size={16} /> Share Album
            </button>
          </div>
        </div>
      )}
      {contextMenu && ("""
context_menu_close_replace = """              <Share2 size={16} /> Share Album
            </button>
          </div>
        </div>
      )}
      </AnimatePresence>, document.body)}
      
      {typeof document !== 'undefined' && createPortal(
        <AnimatePresence>
      {contextMenu && ("""
content = content.replace(context_menu_close, context_menu_close_replace)

end_search = """            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}"""
end_replace = """            </button>
          </motion.div>
        )}
      </AnimatePresence>, document.body)}
    </div>
  );
}"""
content = content.replace(end_search, end_replace)

with open('src/components/AlbumView.tsx', 'w') as f:
    f.write(content)
