import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

search = """  const handleSearchChange = (query: string) => {
    setSearchQuery(query);
    if (query.length > 0) {
      setCurrentView('search');
    } else if (currentView === 'search') {
      setCurrentView('home');
    }
  };"""

replace = """  const handleSearchChange = (query: string) => {
    setSearchQuery(query);
    if (query.length > 0) {
      setCurrentView('search');
    }
  };"""

content = content.replace(search, replace)

with open('src/App.tsx', 'w') as f:
    f.write(content)
