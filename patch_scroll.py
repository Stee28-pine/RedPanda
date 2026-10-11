with open('src/components/LyricsOverlay.tsx', 'r') as f:
    content = f.read()

search_snap = """  const snapToActive = () => {
    if (scrollRef.current) {
      const activeElement = scrollRef.current.children[activeIndex] as HTMLElement;
      if (activeElement) {
        activeElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  };"""

replace_snap = """  const snapToActive = () => {
    if (scrollRef.current) {
      const activeElement = scrollRef.current.children[activeIndex] as HTMLElement;
      if (activeElement) {
        const container = scrollRef.current;
        const elementTop = activeElement.offsetTop;
        const elementHeight = activeElement.offsetHeight;
        const containerHeight = container.clientHeight;
        
        const targetScrollTop = elementTop - (containerHeight / 2) + (elementHeight / 2);
        container.scrollTo({ top: targetScrollTop, behavior: 'smooth' });
      }
    }
  };"""

content = content.replace(search_snap, replace_snap)

search_class = 'className="flex-1 overflow-y-auto hide-scrollbar py-[40vh] px-8 md:px-16"'
replace_class = 'className="relative flex-1 overflow-y-auto hide-scrollbar py-[40vh] px-8 md:px-16"'
content = content.replace(search_class, replace_class)

with open('src/components/LyricsOverlay.tsx', 'w') as f:
    f.write(content)
