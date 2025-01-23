self.addEventListener('install', function(event){
  console.log('[Service Worker] Installing Service Worker ...', event)
  event.waitUntil(
    caches.open('static')
      .then(function(cache) {
        console.log('[Service Worker] Precaching App Shell');
        cache.addAll([
          '/',
          'index.html',
          'src/index.tsx',
          'src/index.css',
          'src/App.tsx',
          'src/App.css',
          'src/components/EnhancedTable.tsx',
          'src/components/Header.tsx',
          'alarm-bell-icon.jpg',
          'logo192.webp',
          'logo512.webp',
          '.././src/android-launchericon-512-512.webp'
        ]);
      })
  )
});

self.addEventListener('activate', function(event) {
  console.log('[Service Worker] Activating Service Worker ...', event);
  return self.clients.claim();
});

self.addEventListener('fetch', function(event){
  event.respondWith(
    caches.match(event.request)
      .then(function(response){
        if(response){
          return response;
        } else {
          return fetch(event.request)
            .then(function(res) {
              return caches.open('dynamic')
                .then(function(cache) {
                  cache.put(event.request.url, res.clone());
                  return res;
                })
            });
        }
      })
  );
});

self.addEventListener('push', (event) => {
    const data = event.data ? event.data.text() : 'No payload';
    const options = {
      body: data,
      icon: '/alarm-bell-icon.jpg',
      badge: '/logo192.png'
      
      //icon: '/icon.png', // Add a relevant icon
      //badge: '/badge.png', // Add a badge image
    };
  
    event.waitUntil(
      self.registration.showNotification('Push Notification', options)
    );
  });
  
  self.addEventListener('notificationclick', (event) => {
    event.notification.close();
    event.waitUntil(
      clients.openWindow('/') // Navigate to a specific URL if required
    );
  });