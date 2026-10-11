import json

manifest = {
  "name": "Audio Player PWA",
  "short_name": "AudioApp",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#F5F5F5",
  "icons": [
    {
      "src": "https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?w=192&q=80",
      "sizes": "192x192",
      "type": "image/jpeg"
    },
    {
      "src": "https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?w=512&q=80",
      "sizes": "512x512",
      "type": "image/jpeg"
    }
  ]
}

with open('public/manifest.json', 'w') as f:
    json.dump(manifest, f, indent=2)

with open('index.html', 'r') as f:
    html = f.read()

meta_tags = """    <meta name="theme-color" content="#F5F5F5" />
    <link rel="manifest" href="/manifest.json" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover" />"""

html = html.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0" />', meta_tags)

with open('index.html', 'w') as f:
    f.write(html)
print("PWA patched")
