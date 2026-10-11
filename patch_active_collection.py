import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Add effect to sync activeCollection
sync_effect = """  useEffect(() => {
    if (activeCollection?.type === 'playlist' && activeCollection.id !== 'liked-songs') {
      const updated = playlists.find(p => p.id === activeCollection.id);
      if (updated && updated.songs.length !== activeCollection.songs.length) {
        setActiveCollection(updated);
      }
    }
  }, [playlists, activeCollection?.id]);"""

insert_point = "  const { results: searchResults, isLoading: isSearchLoading } = useSearch(searchQuery);"

content = content.replace(insert_point, sync_effect + "\n\n" + insert_point)

with open('src/App.tsx', 'w') as f:
    f.write(content)
