import re

with open('src/components/ArtistView.tsx', 'r') as f:
    content = f.read()

if 'createPortal' not in content:
    content = content.replace("import { useState } from 'react';", "import { useState } from 'react';\nimport { createPortal } from 'react-dom';")

start_search = """      <AnimatePresence>
        {contextMenu && ("""
start_replace = """      {typeof document !== 'undefined' && createPortal(
        <AnimatePresence>
        {contextMenu && ("""
content = content.replace(start_search, start_replace)

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

with open('src/components/ArtistView.tsx', 'w') as f:
    f.write(content)

