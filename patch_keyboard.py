import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

keyboard_old = """        case 'ArrowUp':
          e.preventDefault();
          setVolume(v => Math.min(v + 0.1, 1));
          break;
        case 'ArrowDown':
          e.preventDefault();
          setVolume(v => Math.max(v - 0.1, 0));
          break;
      }
    };
    
    window.addEventListener('keydown', handleKeyDown);"""

keyboard_new = """        case 'ArrowUp':
          e.preventDefault();
          setVolume(v => Math.min(v + 0.1, 1));
          break;
        case 'ArrowDown':
          e.preventDefault();
          setVolume(v => Math.max(v - 0.1, 0));
          break;
        case 'KeyM':
          e.preventDefault();
          setVolume(v => v === 0 ? 1 : 0);
          showToast('Mute toggled');
          break;
        case 'KeyL':
          e.preventDefault();
          if (nowPlaying) {
             toggleLike(nowPlaying);
          }
          break;
        case 'KeyQ':
          e.preventDefault();
          setIsRightSidebarOpen(prev => !prev);
          showToast('Queue toggled');
          break;
      }
    };
    
    window.addEventListener('keydown', handleKeyDown);"""

content = content.replace(keyboard_old, keyboard_new)

with open('src/App.tsx', 'w') as f:
    f.write(content)
