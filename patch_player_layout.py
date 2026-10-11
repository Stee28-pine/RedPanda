import re

with open('src/components/Player.tsx', 'r') as f:
    content = f.read()

# 1. Add isMobile state
is_mobile_state = """  const [isMobile, setIsMobile] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(false);"""

content = re.sub(
    r"  const \[isCollapsed, setIsCollapsed\] = useState\(false\);",
    is_mobile_state,
    content
)

resize_effect = """  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < 768;
      setIsMobile(mobile);
      if (mobile) {
        setIsCollapsed(true);
      }
    };
    window.addEventListener('resize', handleResize);
    handleResize();
    return () => window.removeEventListener('resize', handleResize);
  }, []);"""

content = re.sub(
    r"  useEffect\(\(\) => \{\n    const handleResize = \(\) => \{\n      if \(window\.innerWidth < 768\) \{\n        setIsCollapsed\(true\);\n      \}\n    \};\n    window\.addEventListener\('resize', handleResize\);\n    handleResize\(\);\n    return \(\) => window\.removeEventListener\('resize', handleResize\);\n  \}, \[\]\);",
    resize_effect,
    content
)

# 2. Add ChevronDown icon
content = content.replace("ListMusic, Minimize2, Maximize2,", "ListMusic, Minimize2, Maximize2, ChevronDown,")

# 3. Make mini player clickable to expand
mini_player_regex = r"          <div className=\"bg-\[\#F5F5F5\]/90 backdrop-blur-xl rounded-2xl shadow-\[0_8px_30px_rgba\(0,0,0,0\.12\)\] border border-white flex items-center px-4 w-\[min\(90vw,340px\)\] h-14 pointer-events-auto\">"
mini_player_replacement = """          <div 
            className="bg-[#F5F5F5]/90 backdrop-blur-xl rounded-2xl shadow-[0_8px_30px_rgba(0,0,0,0.12)] border border-white flex items-center px-4 w-[min(90vw,340px)] h-14 pointer-events-auto cursor-pointer"
            onClick={(e) => {
              // Prevent expanding if clicking on buttons
              if ((e.target as HTMLElement).closest('button')) return;
              if (isMobile) setIsCollapsed(false);
            }}
          >"""
content = re.sub(mini_player_regex, mini_player_replacement, content)

# 4. Create the expanded layout
expanded_layout = """        ) : isMobile ? (
          <div className="fixed inset-0 bg-[#F5F5F5] z-[100] flex flex-col pointer-events-auto overflow-hidden px-6 pt-12 pb-8">
            {/* Header */}
            <div className="flex justify-between items-center mb-8">
               <button onClick={() => setIsCollapsed(true)} className="text-gray-500 hover:text-gray-900 transition-colors">
                 <ChevronDown size={28} />
               </button>
               <span className="text-[11px] font-bold tracking-widest text-gray-400 uppercase">Now Playing</span>
               <button onClick={onToggleRightSidebar} className="text-gray-500 hover:text-gray-900 transition-colors">
                 <ListMusic size={24} />
               </button>
            </div>

            {/* Album Art with Glow */}
            <div className="relative flex-1 flex flex-col justify-center items-center mb-8 min-h-[300px]">
                <div 
                  className={`absolute inset-0 rounded-3xl blur-3xl transition-opacity duration-700 ${isPlaying && !isBuffering ? 'opacity-70 animate-audio-pulse' : 'opacity-0'}`} 
                  style={{ 
                    backgroundImage: `url(${song.coverUrl})`, 
                    backgroundSize: 'cover', 
                    backgroundPosition: 'center',
                    transform: 'scale(0.95)' 
                  }} 
                />
                <img 
                  src={song.coverUrl} 
                  onError={(e) => { e.currentTarget.src = FALLBACK_IMG }} 
                  className="relative w-full max-w-[340px] aspect-square rounded-3xl shadow-2xl object-cover z-10" 
                  alt={song.title} 
                />
            </div>

            {/* Info */}
            <div className="flex justify-between items-end mb-6">
              <div className="flex flex-col overflow-hidden pr-4">
                <span className="text-2xl font-bold text-gray-900 truncate mb-1">{song.title}</span>
                <span className="text-lg text-gray-500 truncate">{song.artist}</span>
              </div>
              <button 
                onClick={onToggleLike}
                className={`transition-colors mb-2 ${isLiked ? 'text-[#CA5A2C]' : 'text-gray-400 hover:text-gray-700'}`}
              >
                <Heart size={26} className={isLiked ? 'fill-[#CA5A2C]' : ''} />
              </button>
            </div>

            {/* Scrubber */}
            <div className="mb-8">
              <div 
                className="w-full h-2 bg-gray-200 rounded-full flex cursor-pointer shadow-inner relative group mb-2"
                onClick={handleSeek}
              >
                <div className="absolute inset-y-0 left-0 bg-[#CA5A2C] rounded-full pointer-events-none transition-all duration-[250ms] ease-linear" style={{ width: `${progressPercent}%` }}>
                   <div className="absolute right-0 top-1/2 -translate-y-1/2 w-4 h-4 bg-[#CA5A2C] rounded-full shadow-md border-2 border-white translate-x-1/2 scale-100"></div>
                </div>
              </div>
              <div className="flex justify-between text-[12px] font-semibold text-gray-400 tabular-nums">
                <span>{formatTime(currentTime)}</span>
                <span>{formatTime(duration)}</span>
              </div>
            </div>

            {/* Controls */}
            <div className="flex items-center justify-between mb-8 px-4">
               <button 
                onClick={onToggleShuffle}
                className={`transition-colors ${isShuffle ? 'text-[#CA5A2C]' : 'text-gray-400 hover:text-gray-700'}`}
              >
                <Shuffle size={24} />
              </button>
              
              <button onClick={onPrev} className="text-gray-800 hover:text-black transition-colors">
                <SkipBack size={36} fill="currentColor" />
              </button>
              
              <div className="relative flex items-center justify-center w-20 h-20">
                {isBuffering && (
                  <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                     <div className="w-20 h-20 rounded-full border-4 border-gray-100 border-t-[#CA5A2C] animate-spin absolute"></div>
                  </div>
                )}
                <button onClick={onTogglePlay} disabled={isBuffering} className={`text-gray-900 hover:scale-105 transition-transform active:scale-95 ${isBuffering ? 'opacity-[0.01]' : 'opacity-100'}`}>
                  {isPlaying ? <Pause size={48} fill="currentColor" /> : <Play size={48} fill="currentColor" />}
                </button>
              </div>

              <button onClick={onNext} className="text-gray-800 hover:text-black transition-colors">
                <SkipForward size={36} fill="currentColor" />
              </button>

              <button 
                onClick={onToggleRepeat}
                className={`transition-colors relative ${repeatMode !== 'none' ? 'text-[#CA5A2C]' : 'text-gray-400 hover:text-gray-700'}`}
              >
                <Repeat size={24} />
                {repeatMode === 'one' && (
                  <span className="absolute -top-1.5 -right-1.5 text-[10px] font-bold bg-[#CA5A2C] text-white rounded-full w-4 h-4 flex items-center justify-center">1</span>
                )}
              </button>
            </div>
            
            {/* Volume */}
            <div className="flex items-center gap-3 px-2">
              <VolumeX size={18} className="text-gray-400" />
              <input 
                type="range" 
                min="0" max="1" step="0.01" 
                value={volume} 
                onChange={(e) => onVolumeChange(parseFloat(e.target.value))}
                className="flex-1 h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-[#CA5A2C]" 
              />
              <Volume2 size={18} className="text-gray-400" />
            </div>
          </div>
        ) : (
          <div className="flex items-center gap-3 md:gap-4 pointer-events-auto">
            {/* Pill 1: Controls */}"""

content = content.replace(
    """        ) : (
          <div className="flex items-center gap-3 md:gap-4 pointer-events-auto">
            {/* Pill 1: Controls */}""",
    expanded_layout
)

with open('src/components/Player.tsx', 'w') as f:
    f.write(content)
print("done rewriting layout")
