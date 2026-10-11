import re

with open('src/components/RightSidebar.tsx', 'r') as f:
    content = f.read()

# Change nextUp to show more songs so user can see what they added to the queue
content = content.replace("queue.slice(currentIdx + 1, currentIdx + 11)", "queue.slice(currentIdx + 1)")

with open('src/components/RightSidebar.tsx', 'w') as f:
    f.write(content)
