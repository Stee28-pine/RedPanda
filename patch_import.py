with open('src/components/HistoryView.tsx', 'r') as f:
    content = f.read()

content = content.replace("import React, { useState } from 'react';", "import React, { useState, useRef } from 'react';")

with open('src/components/HistoryView.tsx', 'w') as f:
    f.write(content)
print("Patched import")
