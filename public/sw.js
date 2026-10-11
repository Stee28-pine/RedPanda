const CACHE_NAME = 'media-cache-v1';

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  
  // Cache TMDB images or API responses for offline use
  if (event.request.url.includes('tmdb.org') || event.request.url.includes('/api/')) {
    event.respondWith(
      caches.open(CACHE_NAME).then((cache) => {
        return fetch(event.request)
          .then((response) => {
             // Only cache successful responses
             if (response.ok) {
               cache.put(event.request, response.clone());
             }
             return response;
          })
          .catch(() => {
            // Fallback to cache if network fails
            return cache.match(event.request);
          });
      })
    );
  }
});
