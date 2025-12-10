const CACHE_NAME = 'ocalamap-v1';
const ASSETS_TO_CACHE = [
    '/',
    '/index.html',
    '/map.html',
    '/terms.html',
    '/privacy.html',
    '/logo.png',
    '/favicon.png',
    '/manifest.json'
];

// Install event: Cache core assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('[Service Worker] Caching all: app shell and content');
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
    self.skipWaiting();
});

// Activate event: Clean up old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keyList) => {
            return Promise.all(
                keyList.map((key) => {
                    if (key !== CACHE_NAME) {
                        console.log('[Service Worker] Removing old cache', key);
                        return caches.delete(key);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// Fetch event: Network first, fall back to cache
self.addEventListener('fetch', (event) => {
    // Skip cross-origin requests like Google Analytics or non-GET requests
    if ((!event.request.url.startsWith('https') && !event.request.url.startsWith('http')) || event.request.method !== 'GET') {
        return;
    }

    // Strategy: Stale-While-Revalidate for most things to ensure updates
    event.respondWith(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.match(event.request).then((response) => {
                const fetchPromise = fetch(event.request).then((networkResponse) => {
                    // Check if valid response
                    if (networkResponse && networkResponse.status === 200) {
                        // Clone and cache the new response
                        cache.put(event.request, networkResponse.clone());
                    }
                    return networkResponse;
                }).catch(() => {
                    // Network failed
                    // If we have a cached response, return it (handled by return response || fetchPromise logic below if strict SWR)
                    // But here we want to return cached IF network fails (Network First / Revalidate)
                });

                // Return cached response immediately if available, else wait for network
                return response || fetchPromise;
            });
        })
    );
});
