import re

with open('src/components/PodcastsView.tsx', 'r') as f:
    content = f.read()

# 1. Add YEARS constant
search_categories = "const CATEGORIES = ['All', 'Technology', 'Storytelling', 'Business', 'Comedy'];"
replace_categories = search_categories + "\nconst YEARS = ['All Time', '2024', '2023', '2022', '2021', '2020', '2019', '2018'];"
content = content.replace(search_categories, replace_categories)

# 2. Add selectedYear state
search_state = "const [selectedShow, setSelectedShow] = useState<string | null>(null);"
replace_state = search_state + "\n  const [selectedYear, setSelectedYear] = useState('All Time');"
content = content.replace(search_state, replace_state)

# 3. Update useEffect
search_useEffect = """  useEffect(() => {
    if (selectedShow) {
      const showData = PODCAST_SHOWS.find(s => s.name === selectedShow);
      fetchEpisodes(selectedShow + " podcast full episode", showData?.channel);
      if (onSearchChange) onSearchChange('');
    }
  }, [selectedShow]);"""

replace_useEffect = """  useEffect(() => {
    if (selectedShow) {
      const showData = PODCAST_SHOWS.find(s => s.name === selectedShow);
      const yearQuery = selectedYear === 'All Time' ? '' : ` ${selectedYear}`;
      fetchEpisodes(selectedShow + " podcast full episode" + yearQuery, showData?.channel);
      if (onSearchChange) onSearchChange('');
    }
  }, [selectedShow, selectedYear]);"""

content = content.replace(search_useEffect, replace_useEffect)

# 4. Update setSelectedShow to also reset year
search_select_show = "onClick={() => setSelectedShow(show.name)}"
replace_select_show = "onClick={() => { setSelectedShow(show.name); setSelectedYear('All Time'); }}"
content = content.replace(search_select_show, replace_select_show)

# 5. Update UI block for Episodes List View
search_ui = """          {/* Episodes List View */}
          <div className="flex items-center gap-4 mb-8">
            <button
               onClick={() => { 
                 setSelectedShow(null); 
                 if (onSearchChange) onSearchChange(''); 
               }}
               className="p-2.5 rounded-full bg-white shadow-sm border border-gray-200 text-gray-700 hover:bg-gray-50 transition-colors"
            >
              <ChevronLeft size={20} strokeWidth={2.5} />
            </button>
            <div>
              <h1 className="text-2xl font-black text-gray-900 tracking-tight">
                {selectedShow ? selectedShow : `Results for "${searchQuery}"`}
              </h1>
              <p className="text-sm font-medium text-gray-500 mt-1">Audio Player Session Active</p>
            </div>
          </div>"""

replace_ui = """          {/* Episodes List View */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
            <div className="flex items-center gap-4">
              <button
                 onClick={() => { 
                   setSelectedShow(null); 
                   if (onSearchChange) onSearchChange(''); 
                 }}
                 className="p-2.5 rounded-full bg-white shadow-sm border border-gray-200 text-gray-700 hover:bg-gray-50 transition-colors"
              >
                <ChevronLeft size={20} strokeWidth={2.5} />
              </button>
              <div>
                <h1 className="text-2xl font-black text-gray-900 tracking-tight">
                  {selectedShow ? selectedShow : `Results for "${searchQuery}"`}
                </h1>
                <p className="text-sm font-medium text-gray-500 mt-1">Audio Player Session Active</p>
              </div>
            </div>
          </div>

          {selectedShow && (
             <div className="mb-8">
               <div className="flex gap-2 overflow-x-auto hide-scrollbar pb-2">
                 {YEARS.map(year => (
                   <button
                     key={year}
                     onClick={() => setSelectedYear(year)}
                     className={`px-5 py-2 rounded-full text-sm font-bold whitespace-nowrap transition-all ${
                       selectedYear === year 
                         ? 'bg-[#fe5f64] text-white shadow-md' 
                         : 'bg-white border border-gray-200 text-gray-700 hover:border-[#fe5f64] hover:text-[#fe5f64]'
                     }`}
                   >
                     {year}
                   </button>
                 ))}
               </div>
             </div>
          )}"""

content = content.replace(search_ui, replace_ui)

with open('src/components/PodcastsView.tsx', 'w') as f:
    f.write(content)
