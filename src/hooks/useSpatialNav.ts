import { useEffect } from 'react';

const playClickSound = () => {
  try {
    const audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)();
    const oscillator = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();
    
    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(800, audioCtx.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(300, audioCtx.currentTime + 0.05);
    
    gainNode.gain.setValueAtTime(0.05, audioCtx.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.05);
    
    oscillator.connect(gainNode);
    gainNode.connect(audioCtx.destination);
    
    oscillator.start();
    oscillator.stop(audioCtx.currentTime + 0.05);
  } catch (e) {
    // Ignore if audio context fails
  }
};

export function useSpatialNav(onBack?: () => void, isActive: boolean = true) {
  useEffect(() => {
    if (!isActive) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      const targetTag = (e.target as HTMLElement)?.tagName;
      if (e.key === 'Escape' || (e.key === 'Backspace' && targetTag !== 'INPUT' && targetTag !== 'TEXTAREA')) {
        if (onBack) onBack();
        return;
      }

      if (e.key === 'Enter') {
        const active = document.activeElement as HTMLElement;
        if (active && active.tagName !== 'BUTTON' && active.tagName !== 'A' && active.tagName !== 'INPUT') {
          active.click();
        }
        return;
      }

      const directionMap: Record<string, 'UP' | 'DOWN' | 'LEFT' | 'RIGHT'> = {
        ArrowUp: 'UP',
        ArrowDown: 'DOWN',
        ArrowLeft: 'LEFT',
        ArrowRight: 'RIGHT'
      };

      const direction = directionMap[e.key];
      if (!direction) return;

      const active = document.activeElement as HTMLElement;
      
      if (active && active.tagName === 'INPUT' && (direction === 'LEFT' || direction === 'RIGHT')) {
        return; // Allow native text navigation inside inputs
      }

      let focusable = Array.from(
        document.querySelectorAll('button, a, input, [tabindex]:not([tabindex="-1"])')
      ) as HTMLElement[];

      focusable = focusable.filter(el => {
        const rect = el.getBoundingClientRect();
        return el.offsetParent !== null && rect.width > 0 && rect.height > 0 && window.getComputedStyle(el).visibility !== 'hidden';
      });

      if (!active || !focusable.includes(active)) {
        if (focusable.length > 0) focusable[0].focus();
        e.preventDefault();
        return;
      }

      const activeRect = active.getBoundingClientRect();
      let bestMatch: HTMLElement | null = null;
      let minDistance = Infinity;

      focusable.forEach(el => {
        if (el === active) return;
        const rect = el.getBoundingClientRect();
        let isCandidate = false;
        let distance = Infinity;

        const tolerance = 40;

        if (direction === 'LEFT' && rect.right <= activeRect.left + tolerance) {
          isCandidate = true;
          // Heavily penalize vertical distance so we prefer items strictly to the left
          distance = Math.pow(activeRect.left - rect.right, 2) + Math.pow(activeRect.top - rect.top, 2) * 10;
        } else if (direction === 'RIGHT' && rect.left >= activeRect.right - tolerance) {
          isCandidate = true;
          distance = Math.pow(rect.left - activeRect.right, 2) + Math.pow(activeRect.top - rect.top, 2) * 10;
        } else if (direction === 'UP' && rect.bottom <= activeRect.top + tolerance) {
          isCandidate = true;
          // Heavily penalize horizontal distance so we prefer items strictly above
          distance = Math.pow(activeRect.top - rect.bottom, 2) + Math.pow(activeRect.left - rect.left, 2) * 10;
        } else if (direction === 'DOWN' && rect.top >= activeRect.bottom - tolerance) {
          isCandidate = true;
          distance = Math.pow(rect.top - activeRect.bottom, 2) + Math.pow(activeRect.left - rect.left, 2) * 10;
        }

        if (isCandidate && distance < minDistance) {
          minDistance = distance;
          bestMatch = el;
        }
      });

      if (bestMatch) {
        e.preventDefault();
        (bestMatch as HTMLElement).focus();
        playClickSound();
        (bestMatch as HTMLElement).scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onBack, isActive]);
}
