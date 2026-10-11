with open('src/components/LyricsOverlay.tsx', 'r') as f:
    content = f.read()

import re

search = """  const snapToActive = () => {
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
  };

  useEffect(() => {
    if (!isUserScrollingRef.current) {
      snapToActive();
    }
  }, [activeIndex]);

  const handleUserInteraction = () => {
    isUserScrollingRef.current = true;
    if (scrollTimeoutRef.current) clearTimeout(scrollTimeoutRef.current);
    
    scrollTimeoutRef.current = setTimeout(() => {
      isUserScrollingRef.current = false;
      snapToActive();
    }, 1500); // Snap back after 1.5s of no interaction
  };

  useEffect(() => {
    return () => {
      if (scrollTimeoutRef.current) clearTimeout(scrollTimeoutRef.current);
    };
  }, []);"""

replace = """  const targetScrollY = useRef<number | null>(null);
  const currentScrollY = useRef<number | null>(null);

  useEffect(() => {
    if (scrollRef.current) {
      const container = scrollRef.current;
      const activeElement = container.children[activeIndex] as HTMLElement;
      if (activeElement) {
        const elementTop = activeElement.offsetTop;
        const elementHeight = activeElement.offsetHeight;
        const containerHeight = container.clientHeight;
        
        targetScrollY.current = elementTop - (containerHeight / 2) + (elementHeight / 2);
      }
    }
  }, [activeIndex, duration]);

  useEffect(() => {
    let rafId: number;

    const loop = () => {
      const container = scrollRef.current;
      if (container && targetScrollY.current !== null) {
        if (!isUserScrollingRef.current) {
          if (currentScrollY.current === null) {
             currentScrollY.current = container.scrollTop;
          }
          
          const diff = targetScrollY.current - currentScrollY.current;
          
          if (Math.abs(diff) > 0.5) {
             currentScrollY.current += diff * 0.08; // Smooth easing factor
             container.scrollTop = currentScrollY.current;
          } else {
             currentScrollY.current = targetScrollY.current;
             container.scrollTop = currentScrollY.current;
          }
        } else {
           // Sync internal state to actual scroll position during user interaction
           currentScrollY.current = container.scrollTop;
        }
      }
      rafId = requestAnimationFrame(loop);
    };

    rafId = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(rafId);
  }, []);

  const handleUserInteraction = () => {
    isUserScrollingRef.current = true;
    if (scrollTimeoutRef.current) clearTimeout(scrollTimeoutRef.current);
    
    scrollTimeoutRef.current = setTimeout(() => {
      isUserScrollingRef.current = false;
    }, 1500); // Snap back after 1.5s of no interaction
  };

  useEffect(() => {
    return () => {
      if (scrollTimeoutRef.current) clearTimeout(scrollTimeoutRef.current);
    };
  }, []);"""

content = content.replace(search, replace)

with open('src/components/LyricsOverlay.tsx', 'w') as f:
    f.write(content)
