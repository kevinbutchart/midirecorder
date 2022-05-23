// Establish a cache name
const cacheName = 'pianorecordercache';

self.addEventListener( "install", function( event ){
    event.waitUntil(
        caches.open( cacheName )
              .then(function( cache ){
            return cache.addAll([
                "/static/css/main.css",
                "/static/css/bootstrap.min.css",
                "/static/js/main.js",
                "/static/js/jquery.min.js",
                "/static/js/bootstrap.min.js",
                "/static/js/long-press-event.min.js",
                "/static/images/favicon.png"
            ]);
        })
    );
});

self.addEventListener('fetch', function (event) {
    event.respondWith(
        fetch(event.request).catch(function() {
            return caches.match(event.request)
        })
    )
})

function removeUrlFromCache(url) {
    caches.open(cacheName).then(function(cache) {
        cache.matchAll(url).then(function(response) {
            response.forEach(function(element, index, array) {
                cache.delete(element);
            });
        });
    })
}
