import re

with open('src/components/RightSidebar.tsx', 'r') as f:
    content = f.read()

old_next_up = """      {localNextUp.length > 0 && (
        <div>
          <h3 className="text-lg font-bold text-gray-900 mb-3 tracking-tight">Next Up</h3>
          <Reorder.Group axis="y" values={localNextUp} onReorder={handleReorder} className="space-y-1">
            <AnimatePresence>
              {localNextUp.map((song) => ("""

new_next_up = """      {localNextUp.length > 0 && (
        <div className="mb-8">
          <h3 className="text-lg font-bold text-gray-900 mb-3 tracking-tight">Up Next</h3>
          
          <div className="bg-white/80 backdrop-blur-md p-3 rounded-2xl shadow-sm border border-[#CA5A2C]/40 flex items-center gap-3 mb-4 relative overflow-hidden">
             <div className="absolute top-0 left-0 w-1 h-full bg-[#CA5A2C]" />
             <img src={localNextUp[0].coverUrl} onError={(e) => { e.currentTarget.src = FALLBACK_IMG }} className="w-12 h-12 rounded-lg object-cover shadow-sm" alt={localNextUp[0].title} />
             <div className="flex flex-col flex-1 overflow-hidden">
                <span className="text-[14px] font-bold text-gray-900 truncate leading-tight">{localNextUp[0].title}</span>
                <span className="text-[12px] text-gray-500 truncate mt-0.5 font-medium">{localNextUp[0].artist}</span>
             </div>
             <div className="flex flex-col items-end">
                 <span className="text-[10px] uppercase font-bold tracking-wider text-[#CA5A2C]">Next</span>
                 <span className="text-[12px] font-medium text-gray-400 mt-1">{localNextUp[0].duration}</span>
             </div>
          </div>

          {localNextUp.length > 1 && (
             <Reorder.Group axis="y" values={localNextUp.slice(1)} onReorder={(newSlice) => handleReorder([localNextUp[0], ...newSlice])} className="space-y-1">
               <AnimatePresence>
                 {localNextUp.slice(1).map((song) => ("""

content = content.replace(old_next_up, new_next_up)

content = content.replace("                </Reorder.Item>\n              ))}\n            </AnimatePresence>\n          </Reorder.Group>\n        </div>\n      )}", "                </Reorder.Item>\n              ))}\n            </AnimatePresence>\n          </Reorder.Group>\n          )}\n        </div>\n      )}")

with open('src/components/RightSidebar.tsx', 'w') as f:
    f.write(content)

print("RightSidebar Next Up patched")
