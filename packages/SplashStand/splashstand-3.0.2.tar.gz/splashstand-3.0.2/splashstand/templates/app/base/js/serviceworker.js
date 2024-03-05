const staticCacheName = "[[ config.APP_NAME ]]-[[ sw_timestamp ]]";

const urlsToCache = [
    '/',
[%- for page in config.SITE_PAGES %]
    '/[[ page|lstrip('_') ]]',
[%- endfor %]
'/offline',
'/dashboard_offline',
'/manifest.json'
];

const networkOnlyUrls = [
'googleusercontent.com',
[%- for ext in config.VIDEO_EXTS + config.AUDIO_EXTS %]
    '[[ ext ]]',
[%- endfor %]
'/verify',
'/admin',
'/form',
'/widget',
    '/__'
];

const cacheFirstUrls = [
'.css',
'.js',
'.json'];

function networkOnlyUrl(event) {
var only = false;
    for (const url of networkOnlyUrls) {
        if (event.request.url.indexOf(url) !== -1 && event.request.url.indexOf('.css') === -1 && event.request.url.indexOf('.js') === -1) {
            only = true;
            break;
        }
    }
    return only;
}

[ % -
if ac.debug.serviceworker %]
console.log('Site t.URL: [[ config.DOMAIN ]]');
console.log('Invocation: [[ get_invocation ]]');
[ % -endif %
]

self.addEventListener('install', function (event) {
    event.waitUntil(
        caches.open(staticCacheName).then(function (cache) {
            [ % -
            if ac.debug.serviceworker %]
            console.log('Opened app cache');
            console.log('Caching: ' + urlsToCache);
            [ % -endif %
        ]
            return cache.addAll(urlsToCache);
        }).then(function () {
return self.skipWaiting();
})
);
});

self.addEventListener('fetch', function (event) {
    [ % -
    if ac.debug.serviceworker %]
    console.log('Fetching: ', event.request.url);
    [ % -endif %
]
    if (event.request.method !== 'GET') {
        return;
    }
    if (networkOnlyUrl(event)) {
        [ % -
        if ac.debug.serviceworker %]
        console.log('Fetch network only: ', event.request.url);
        [ % -endif %
    ]
        return;
    } else if (event.request.url.indexOf('[[ config.DOMAIN ]]') !== -1
[%- if not site.is_deployed %]
    || event.request.url.indexOf('.css') !== -1
    || event.request.url.indexOf('.js') !== -1
    || event.request.url.indexOf('.json') !== -1
[%- endif %]
)
    {
        [ % -
        if ac.debug.serviceworker %]
        console.log('Fetch network first: ', event.request.url);
        [ % -endif %
    ]
        event.respondWith(fetch(event.request).catch(function () {
                return caches.match(event.request);
            }).catch(function () {
                console.log('Failed to get ', event.request.url);
                return caches.match('/offline');
            })
        );
    }else
    {
        [ % -
        if ac.debug.serviceworker %]
        console.log('Fetch cache first: ', event.request.url);
        [ % -endif %
    ]
        event.respondWith(
            caches.open(staticCacheName)
                .then(function (cache) {
                    return cache.match(event.request)
                        .then(function (response) {
                            return response || fetch(event.request)
                                .then(function (response) {
                                    if (!(event.request.url.indexOf('http') === 0)) return;
cache.put(event.request, response.clone());
return response;
});
});
})
.catch(function () {
console.log('Failed to get ', event.request.url);
return caches.match('/offline');
})
);
}
});


self.addEventListener('activate', function (event) {
    [ % -
    if ac.debug.serviceworker %]
    console.log('Activating app service worker...');
    [ % -endif %
]
    event.waitUntil(
        caches.keys().then(function (cacheNames) {
            return Promise.all(
                cacheNames.map(function (cacheName) {
                    if (staticCacheName !== cacheName && cacheName.startsWith("[[ config.APP_NAME ]]-")) {
                        return caches.delete(cacheName);
                    }
                })
);
})
);
});
