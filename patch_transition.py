import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

search = """  const transitionTrack = (action: () => void) => {
    if (isCrossfading.current || document.hidden) {
       setCrossfadeVolume(1);
       action();
       isCrossfading.current = false;
       return;
    }
    isCrossfading.current = true;
    let start = performance.now();
    const duration = 500;
    
    const animate = (time: number) => {
      let progress = (time - start) / duration;
      if (progress >= 1 || document.hidden) {
        setCrossfadeVolume(0);
        action();
        
        let inStart = performance.now();
        const animateIn = (t: number) => {
           let p = (t - inStart) / duration;
           if (p >= 1 || document.hidden) {
             setCrossfadeVolume(1);
             isCrossfading.current = false;
           } else {
             setCrossfadeVolume(p);
             requestAnimationFrame(animateIn);
           }
        };
        requestAnimationFrame(animateIn);
      } else {
        setCrossfadeVolume(1 - progress);
        requestAnimationFrame(animate);
      }
    };
    requestAnimationFrame(animate);
  };"""

replace = """  const transitionTrack = (action: () => void) => {
    if (isCrossfading.current || document.hidden) {
       setCrossfadeVolume(1);
       action();
       isCrossfading.current = false;
       return;
    }
    isCrossfading.current = true;
    
    const duration = 500;
    const steps = 10;
    const stepTime = duration / steps;
    let currentStep = 0;
    
    const fadeOut = setInterval(() => {
      currentStep++;
      if (currentStep >= steps || document.hidden) {
        clearInterval(fadeOut);
        setCrossfadeVolume(0);
        action();
        
        let inStep = 0;
        const fadeIn = setInterval(() => {
          inStep++;
          if (inStep >= steps || document.hidden) {
            clearInterval(fadeIn);
            setCrossfadeVolume(1);
            isCrossfading.current = false;
          } else {
            setCrossfadeVolume(inStep / steps);
          }
        }, stepTime);
      } else {
        setCrossfadeVolume(1 - (currentStep / steps));
      }
    }, stepTime);
  };"""

content = content.replace(search, replace)

with open('src/App.tsx', 'w') as f:
    f.write(content)
