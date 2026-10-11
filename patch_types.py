with open('src/types.ts', 'r') as f:
    content = f.read()

if 'Bookmark' not in content:
    content += """
export interface Bookmark {
  id: string;
  songId: string;
  timestamp: number;
  note: string;
  createdAt: number;
}
"""
    with open('src/types.ts', 'w') as f:
        f.write(content)
    print("Added Bookmark to types.ts")
