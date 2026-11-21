/* 離線也能看：頁面、程式先上網拿最新的，沒網路就用存下來的；照片和語音存起來重複用 */
var CACHE = 'xiamen-v44';
var CORE = ['./', 'index.html', 'assets/style.css?v=44', 'assets/data.js?v=44', 'assets/audio-version.js?v=44', 'assets/credits.js?v=44', 'assets/land.js?v=44', 'assets/map.js?v=44', 'assets/app.js?v=44'];

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) {
    // cache: 'reload'：略過瀏覽器的暫存，一定拿伺服器上最新的檔案
    return c.addAll(CORE.map(function (u) { return new Request(u, { cache: 'reload' }); }));
  }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});
self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  var isImg = /\/(img|audio)\//.test(req.url);
  if (isImg) {
    e.respondWith(caches.match(req).then(function (hit) {
      return hit || fetch(req).then(function (res) {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(req, copy); });
        return res;
      });
    }));
    return;
  }
  // cache: 'no-cache'：每次都跟伺服器確認有沒有新版，行程一改，手機就看得到
  e.respondWith(fetch(req, { cache: 'no-cache' }).then(function (res) {
    var copy = res.clone();
    caches.open(CACHE).then(function (c) { c.put(req, copy); });
    return res;
  }).catch(function () {
    return caches.match(req, { ignoreSearch: true }).then(function (hit) { return hit || caches.match('index.html'); });
  }));
});
