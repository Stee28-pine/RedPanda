import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

share_fn_old = """  const handleShare = (item: { type: 'song' | 'album' | 'artist', id: string, name: string }) => {
    if (typeof navigator !== 'undefined' && navigator.clipboard) {
      navigator.clipboard.writeText(`https://music.applet.mock/${item.type}/${item.id}`);
    }
    showToast(`Link to ${item.name} copied`);
  };"""

share_fn_new = """  const handleShare = (item: { type: 'song' | 'album' | 'artist', id: string, name: string }) => {
    const url = `https://music.applet.mock/${item.type}/${item.id}`;
    if (typeof navigator !== 'undefined' && navigator.share) {
      navigator.share({ title: item.name, url }).catch(err => {
         // fallback
         if (navigator.clipboard) {
             navigator.clipboard.writeText(url).catch(() => {});
         }
      });
    } else if (typeof navigator !== 'undefined' && navigator.clipboard) {
      navigator.clipboard.writeText(url).catch(() => {});
    }
    showToast(`Link to ${item.name} copied`);
  };"""

content = content.replace(share_fn_old, share_fn_new)

with open('src/App.tsx', 'w') as f:
    f.write(content)
