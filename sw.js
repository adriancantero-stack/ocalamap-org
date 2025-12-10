const CACHE_NAME = 'ocalamap-v8';
const ASSETS_TO_CACHE = [
    '/',
    '/map',
    '/terms',
    '/privacy',
    '/logo.png',
    '/favicon.png',
    '/manifest.json'
];

// Helper to remove "redirected" status from response which Safari hates
function cleanResponse(response) {
    const clonedResponse = response.clone();
    const bodyPromise = clonedResponse.body;
    return new Response(bodyPromise, {
        headers: clonedResponse.headers,
        status: clonedResponse.status,
        statusText: clonedResponse.statusText,
    });
}

// Install event: Cache core assets manually to clean them
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(async (cache) => {
            console.log('[Service Worker] Caching all: app shell and content');
            // We manually fetch to clean responses
            for (const requestUrl of ASSETS_TO_CACHE) {
                try {
                    const response = await fetch(requestUrl);
                    if (response.status === 200) {
                        await cache.put(requestUrl, cleanResponse(response));
                    }
                } catch (error) {
                    console.error(`[Service Worker] Failed to cache ${requestUrl}:`, error);
                }
            }
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
    // Skip cross-origin requests or non-GET requests
    if ((!event.request.url.startsWith('https') && !event.request.url.startsWith('http')) || event.request.method !== 'GET') {
        return;
    }

    event.respondWith(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.match(event.request).then((response) => {
                const fetchPromise = fetch(event.request).then((networkResponse) => {
                    // Check if valid response
                    if (networkResponse && networkResponse.status === 200) {
                        // Clone, clean, and cache the new response
                        cache.put(event.request, cleanResponse(networkResponse));
                    }
                    return networkResponse;
                }).catch(() => {
                    // Network failed
                });

                // Return cached response immediately if available, else wait for network
                if (response) {
                    // Ensure cached response is also clean (though it should be)
                    return response;
                }
                return fetchPromise;
            });
        })
    );
});
