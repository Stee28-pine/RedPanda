import re

with open('src/components/SearchView.tsx', 'r') as f:
    content = f.read()

# Add state variable
pattern_state = re.compile(r'(const \{ recentSearches.*?useRecentSearches\(\);)', re.DOTALL)
new_state = r'\1\n  const [filterByArtist, setFilterByArtist] = useState(false);\n  const displayResults = filterByArtist && query ? results.filter(s => s.artist.toLowerCase().includes(query.toLowerCase())) : results;'
content = pattern_state.sub(new_state, content)

# Replace the Top Results section and the mapping over results
old_top_results = """        <>
          <h2 className="text-xl font-bold text-gray-900 mb-6 tracking-tight">Top Results</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {results.map((song) => {"""

new_top_results = """        <>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-900 tracking-tight">Top Results</h2>
            <button 
              onClick={(e) => { e.stopPropagation(); setFilterByArtist(!filterByArtist); }}
              className={`text-[13px] font-medium px-4 py-1.5 rounded-full transition-colors border ${filterByArtist ? 'bg-[#fe5f64] text-white border-[#fe5f64]' : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'}`}
            >
              Filter by Artist
            </button>
          </div>
          {displayResults.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {displayResults.map((song) => {"""

if old_top_results in content:
    content = content.replace(old_top_results, new_top_results)
else:
    print("WARNING: Could not find old_top_results")

# Now we need to close the displayResults.length > 0 ternary check
old_closing = """                  </div>
                </div>
              );
            })}
          </div>
        </>
      ) : ("""

new_closing = """                  </div>
                </div>
              );
            })}
          </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <p className="text-gray-500 text-sm">No results match this artist filter.</p>
            </div>
          )}
        </>
      ) : ("""

if old_closing in content:
    content = content.replace(old_closing, new_closing)
else:
    print("WARNING: Could not find old_closing")

with open('src/components/SearchView.tsx', 'w') as f:
    f.write(content)
print("Patch applied")
