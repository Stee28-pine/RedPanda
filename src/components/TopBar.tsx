import { ChevronLeft, ChevronRight, Search, X, Menu } from 'lucide-react';

export function TopBar({ 
  onBack, 
  canGoBack,
  searchQuery,
  onSearchChange,
  onToggleSidebar,
  onSearchFocus
}: { 
  onBack: () => void;
  canGoBack: boolean;
  searchQuery?: string;
  onSearchChange?: (q: string) => void;
  onSearchFocus?: () => void;
  onToggleSidebar?: () => void;
}) {
  return (
    <div className="flex items-center gap-4 px-4 md:px-8 py-5 sticky top-0 z-10 bg-[#F9F9F9]/90 backdrop-blur-md">
      <div className="flex items-center gap-2">
        <button 
          onClick={onToggleSidebar}
          className="md:hidden p-2 -ml-2 rounded-full flex items-center justify-center text-gray-700 hover:bg-gray-100"
        >
          <Menu size={20} strokeWidth={2.5} />
        </button>
        
        {/* Mobile Brand Logo */}
        <div className="md:hidden flex items-center mr-2 h-8">
          <img src="/698481-removebg-preview.png" alt="RedPanda Logo" className="h-full w-auto object-contain" onContextMenu={(e) => e.preventDefault()} />
        </div>

        <button 
          onClick={onBack}
          disabled={!canGoBack}
          className={`p-2 rounded-full bg-white shadow-sm border border-gray-100 flex items-center justify-center transition-colors ${canGoBack ? 'text-gray-700 hover:bg-gray-50' : 'text-gray-300'}`}
        >
          <ChevronLeft size={20} strokeWidth={2.5} />
        </button>
        <button className="p-2 rounded-full bg-white shadow-sm border border-gray-100 flex items-center justify-center text-gray-700 hover:bg-gray-50">
          <ChevronRight size={20} strokeWidth={2.5} />
        </button>
      </div>

      <div className="flex-1 max-w-3xl relative ml-2">
        <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none">
          <Search size={18} strokeWidth={2.5} />
        </div>
        <input 
          type="text" 
          value={searchQuery || ''}
          onChange={(e) => onSearchChange?.(e.target.value)}
          onFocus={() => onSearchFocus?.()}
          placeholder="Search for songs, artists, or albums to play" 
          className="w-full bg-white border border-gray-200 text-sm font-medium text-gray-900 rounded-full py-2.5 pl-11 pr-10 focus:outline-none focus:ring-2 focus:ring-gray-200 transition-shadow shadow-sm placeholder:text-gray-400"
        />
        {searchQuery && (
          <button 
            onClick={() => onSearchChange?.('')}
            className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X size={16} strokeWidth={2.5} />
          </button>
        )}
      </div>
    </div>
  );
}
