(function () {
  var T = window.TRIP, Y = T.year, MON = T.month - 1;

  /* ---------- 圖示（改自 Lucide，ISC 授權） ---------- */
  var IC = {
    plane: '<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>',
    ship: '<path d="M12 10.2V14"/><path d="M12 2v3"/><path d="M19 13V7a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v6"/><path d="M19.4 20A11.6 11.6 0 0 0 21 14l-8.2-3.6a2 2 0 0 0-1.6 0L3 14a11.6 11.6 0 0 0 2.8 7.8"/><path d="M2 21c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1s1.2 1 2.5 1c2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/>',
    car: '<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/>',
    walk: '<path d="M4 16v-2.4C4 11.5 3 10.5 3 8c0-2.7 1.5-6 4.5-6C9.4 2 10 3.8 10 5.5c0 3.1-2 5.7-2 8.7V16a2 2 0 1 1-4 0Z"/><path d="M20 20v-2.4c0-2.1 1-3.1 1-5.6 0-2.7-1.5-6-4.5-6C14.6 6 14 7.8 14 9.5c0 3.1 2 5.7 2 8.7V20a2 2 0 1 0 4 0Z"/><path d="M16 17h4"/><path d="M4 13h4"/>',
    ticket: '<path d="M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M13 5v2"/><path d="M13 17v2"/><path d="M13 11v2"/>',
    bed: '<path d="M2 20v-8a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v8"/><path d="M4 10V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v4"/><path d="M12 4v6"/><path d="M2 18h20"/>',
    food: '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>',
    home: '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .7-1.5l7-6a2 2 0 0 1 2.6 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    camera: '<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/>',
    spa: '<path d="M9.9 15.5a2 2 0 0 0-1.4-1.4l-6.1-1.6a.5.5 0 0 1 0-1l6.1-1.6a2 2 0 0 0 1.4-1.4l1.6-6.1a.5.5 0 0 1 1 0l1.6 6.1a2 2 0 0 0 1.4 1.4l6.1 1.6a.5.5 0 0 1 0 1l-6.1 1.6a2 2 0 0 0-1.4 1.4l-1.6 6.1a.5.5 0 0 1-1 0z"/>',
    tea: '<path d="M10 2v2"/><path d="M14 2v2"/><path d="M16 8a1 1 0 0 1 1 1v8a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V9a1 1 0 0 1 1-1h14a4 4 0 1 1 0 8h-1"/><path d="M6 2v2"/>',
    basket: '<path d="m15 11-1 9"/><path d="m19 11-4-7"/><path d="M2 11h20"/><path d="m3.5 11 1.6 7.4a2 2 0 0 0 2 1.6h9.8a2 2 0 0 0 2-1.6l1.7-7.4"/><path d="M4.5 15.5h15"/><path d="m5 11 4-7"/><path d="m9 11 1 9"/>',
    show: '<path d="M11.5 2.3a.5.5 0 0 1 1 0l2.3 4.7a2.1 2.1 0 0 0 1.6 1.2l5.2.7a.5.5 0 0 1 .3.9l-3.7 3.6a2.1 2.1 0 0 0-.6 1.9l.9 5.1a.5.5 0 0 1-.8.6l-4.6-2.4a2.1 2.1 0 0 0-2 0l-4.6 2.4a.5.5 0 0 1-.8-.6l.9-5.1a2.1 2.1 0 0 0-.6-1.9L2.2 9.8a.5.5 0 0 1 .3-.9l5.2-.7a2.1 2.1 0 0 0 1.6-1.2z"/>',
    bag: '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/>',
    speaker: '<path d="M11 4.7a.7.7 0 0 0-1.2-.5L6.4 7.6a1.4 1.4 0 0 1-1 .4H3a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2.4a1.4 1.4 0 0 1 1 .4l3.4 3.4a.7.7 0 0 0 1.2-.5z"/><path d="M16 9a5 5 0 0 1 0 6"/><path d="M19.4 18.4a9 9 0 0 0 0-12.8"/>',
    stop: '<rect x="6" y="6" width="12" height="12" rx="2"/>',
    pin: '<path d="M20 10c0 5-5.5 10.2-7.4 11.8a1 1 0 0 1-1.2 0C9.5 20.2 4 15 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    map: '<path d="M14.1 5.6a2 2 0 0 0 1.8 0l3.7-1.9A1 1 0 0 1 21 4.6v12.8a1 1 0 0 1-.6.9l-4.5 2.3a2 2 0 0 1-1.8 0l-4.2-2.1a2 2 0 0 0-1.8 0l-3.7 1.9A1 1 0 0 1 3 19.4V6.6a1 1 0 0 1 .6-.9l4.5-2.3a2 2 0 0 1 1.8 0z"/><path d="M15 5.8v15"/><path d="M9 3.2v15"/>'
  };
  function icon(k, cls) { return '<svg class="' + (cls || 'ic') + '" viewBox="0 0 24 24" aria-hidden="true">' + (IC[k] || IC.pin) + '</svg>'; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  /* ---------- 語音：播放事先錄好的台灣國語女聲（audio/*.mp3），失敗才改用手機內建語音 ---------- */
  var audio = new Audio(), playing = null, queue = [];
  audio.preload = 'none';
  var synth = window.speechSynthesis, voice = null;
  function pickVoice() {
    if (!synth) return;
    var vs = synth.getVoices();
    function find(re) { for (var i = 0; i < vs.length; i++) if (re.test(vs[i].lang.replace('_', '-'))) return vs[i]; return null; }
    voice = find(/^zh-TW/i) || find(/^zh-Hant/i) || find(/^zh/i) || null;
  }
  if (synth) { pickVoice(); if (synth.addEventListener) synth.addEventListener('voiceschanged', pickVoice); }

  function setBtn(btn, on) {
    if (!btn) return;
    btn.classList.toggle('on', on);
    btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    var lab = btn.querySelector('.spk-l');
    btn.querySelector('svg').innerHTML = on ? IC.stop : IC.speaker;
    if (lab) lab.textContent = on ? (btn.dataset.off || '停止') : (btn.dataset.on || '聽');
  }
  function done(btn) { if (playing === btn) { setBtn(btn, false); playing = null; } }
  function stopSpeak() {
    queue = [];
    audio.pause();
    if (synth) synth.cancel();
    setBtn(playing, false);
    playing = null;
  }
  function speak(btn) {
    var same = playing === btn;
    stopSpeak();
    if (same) return;
    playing = btn; setBtn(btn, true);
    if (!btn.dataset.audio) { speakTTS(btn); return; }
    audio.onended = function () { done(btn); };
    audio.onerror = function () { if (playing === btn) speakTTS(btn); };
    var v = window.AUDIO_V && window.AUDIO_V[btn.dataset.audio];
    audio.src = 'audio/' + btn.dataset.audio + '.mp3' + (v ? '?v=' + v : '');
    var pr = audio.play();
    if (pr && pr.catch) pr.catch(function (e) { if (playing === btn && e && e.name !== 'AbortError') speakTTS(btn); });
  }
  function speakTTS(btn) {
    audio.pause();
    if (!synth || !window.SpeechSynthesisUtterance) { done(btn); showNoVoice(); return; }
    queue = (btn.dataset.say.match(/[^。！？]+[。！？]?/g) || [btn.dataset.say]).map(function (s) { return s.trim(); }).filter(Boolean);
    next(btn);
  }
  function next(btn) {
    if (playing !== btn) return;
    if (!queue.length) { done(btn); return; }
    var u = new SpeechSynthesisUtterance(queue.shift());
    u.lang = 'zh-TW';
    if (voice) u.voice = voice;
    u.rate = 0.9;
    u.onend = function () { next(btn); };
    u.onerror = function () { done(btn); };
    synth.speak(u);
  }
  function showNoVoice() {
    var m = document.getElementById('novoice');
    m.hidden = false;
    setTimeout(function () { m.hidden = true; }, 6000);
  }
  document.addEventListener('visibilitychange', function () { if (document.hidden) stopSpeak(); });

  function spkBtn(text, id, extra, on, off) {
    return '<button type="button" class="spk' + (extra ? ' ' + extra : '') + '" data-say="' + esc(text) + '" data-audio="' + esc(id) + '"' +
      (on ? ' data-on="' + esc(on) + '"' : '') + (off ? ' data-off="' + esc(off) + '"' : '') +
      ' aria-pressed="false">' + icon('speaker') + '<span class="spk-l">' + esc(on || '聽') + '</span></button>';
  }
  var how = document.getElementById('howtoSpk');
  how.dataset.say = T.howto; how.dataset.audio = 'howto';
  var hs = document.getElementById('hotelSpk');
  if (hs) { hs.dataset.say = T.hotel.say; hs.dataset.audio = 'hotel'; }

  /* ---------- 地點：店名、地址、給司機看、地圖連結 ---------- */
  var PL = [];
  function enc(x) { return encodeURIComponent(x); }
  function amapURL(pl) {
    // callnative=1：手機有裝高德地圖 App 就直接打開 App，沒裝才開網頁版
    return 'https://uri.amap.com/search?keyword=' + enc(pl.kw || pl.sc) + '&city=' + enc(pl.city || '厦门') + '&view=map&src=trip&callnative=1';
  }
  function dpURL(pl) {
    // 大眾點評 App 的搜尋（只有裝了 App 的手機才打得開）
    return 'dianping://searchshoplist?keyword=' + enc(pl.dp || pl.kw || pl.sc);
  }
  function gURL(pl) {
    return 'https://www.google.com/maps/search/?api=1&query=' + enc(pl.g || (pl.tw ? pl.sc : (pl.kw || pl.sc) + ' 厦门'));
  }
  function mapLinks(pl) {
    return (pl.tw ? '' : '<a class="pl-l amap" href="' + amapURL(pl) + '" target="_blank" rel="noopener">' + icon('map') + '高德地圖</a>' +
      '<a class="pl-l dp" href="' + dpURL(pl) + '">' + icon('food') + '大眾點評</a>') +
      '<a class="pl-l gmap" href="' + gURL(pl) + '" target="_blank" rel="noopener">' + icon('map') + 'Google 地圖</a>';
  }
  function placeHTML(pl) {
    var i = PL.push(pl) - 1;
    return '<div class="place"><div class="pl-n">' + icon('pin') + '<b>' + esc(pl.n) + '</b></div>' +
      '<div class="pl-a" lang="' + (pl.tw ? 'zh-Hant-TW' : 'zh-Hans') + '">' + esc(pl.addr) + '</div>' +
      '<div class="pl-b"><button type="button" class="pl-drv" data-place="' + i + '">' + icon('car') + '給司機看</button>' + mapLinks(pl) + '</div></div>';
  }

  /* ---------- 畫出每天的行程 ---------- */
  var MODE = { car: '坐車', ship: '坐船', walk: '走路', plane: '飛機' };
  function itemHTML(it, day) {
    if (it.kind === 'move') {
      return '<li class="it move m-' + it.mode + '"' + (it.id ? ' id="' + it.id + '"' : '') + '>' +
        '<div class="rail"></div><div class="mv"><span class="mv-i">' + icon(it.mode) + '</span>' +
        (it.t ? '<b class="mv-t">' + it.t + '</b>' : '') + '<span>' + esc(it.text) + '</span></div></li>';
    }
    if (it.kind === 'mini') {
      return '<li class="it mini" id="' + it.id + '"><div class="rail"><span class="dot"></span></div>' +
        '<div class="card mini-c"><span class="mini-i">' + icon(it.icon) + '</span>' +
        '<div class="mini-t"><b class="time">' + it.t + '</b><span class="mini-n">' + esc(it.title) + '</span></div>' +
        spkBtn(it.say, it.id, 'sm') + '</div></li>';
    }
    var opt = it.kind === 'opt';
    var h = '<li class="it ' + (opt ? 'opt' : 'stop') + '"' + (it.id ? ' id="' + it.id + '"' : '') + '>' +
      '<div class="rail"><span class="dot"></span></div><article class="card">';
    if (it.img) h += '<div class="ph-w"><img class="ph" src="img/' + it.img + '.webp" alt="" loading="lazy" decoding="async" width="960" height="540">' + spkBtn(it.say, it.id, 'float') + '</div>';
    h += '<div class="cb' + (it.img ? ' has-float' : '') + '"><div class="ch"><div class="ct">';
    if (opt) h += '<span class="tag-opt">沒累再去</span>';
    else h += '<b class="time">' + it.t + '</b>' + (it.tbd ? '<span class="tag-tbd">時間待確認</span>' : '');
    if (it.book) h += '<span class="tag-book">' + icon('ticket') + esc(it.book === true ? '怡君代訂' : it.book) + '</span>';
    h += '<h3>' + icon(it.icon, 'ic h-ic') + '<span>' + esc(it.title) + '</span></h3>';
    if (it.sub) h += '<div class="sub">' + esc(it.sub) + '</div>';
    h += '</div>' + (it.img ? '' : spkBtn(it.say, it.id)) + '</div>';
    if (it.pts && it.pts.length) h += '<ul class="pts">' + it.pts.map(function (p) { return '<li>' + esc(p) + '</li>'; }).join('') + '</ul>';
    if (it.at) h += placeHTML(T.places[it.at]);
    h += '</div></article></li>';
    return h;
  }

  var daysEl = document.getElementById('days');
  daysEl.innerHTML = T.days.map(function (d, i) {
    return '<section class="day" id="' + d.id + '" style="--c:' + d.color + '">' +
      '<header class="day-hd"><div class="seal"><small>第</small>' + (i + 1) + '<small>天</small></div>' +
      '<div class="dh-t"><div class="dh-date">' + T.month + '/' + d.d + '（' + d.wk + '）</div><h2>' + esc(d.title) + '</h2></div></header>' +
      '<div class="day-say">' + spkBtn(d.say, d.id, 'wide', '聽今天的行程', '停止播放') + '</div>' +
      '<ol class="tl">' + d.items.map(function (it) { return itemHTML(it, d); }).join('') + '</ol></section>';
  }).join('');

  /* ---------- 廈門必吃：左右滑動的卡片 ---------- */
  var track = document.getElementById('foodTrack'), FN = T.foods.length;
  track.innerHTML = T.foods.map(function (f, i) {
    var pl = typeof f.at === 'string' ? T.places[f.at] : f.at;
    return '<article class="fd card" style="--c:var(--brick)" aria-roledescription="卡片" aria-label="' + (i + 1) + ' / ' + FN + ' ' + esc(f.name) + '">' +
      '<div class="ph-w' + (f.img ? '' : ' ph-none') + '">' +
      (f.img ? '<img class="ph" src="img/' + f.img + '.webp" alt="' + esc(f.name) + '" loading="lazy" decoding="async" width="960" height="540">' : '<span aria-hidden="true">' + esc(f.name) + '</span>') +
      spkBtn(f.say, f.id, 'float') + '</div>' +
      '<div class="cb has-float"><div class="ct"><h3><span>' + esc(f.name) + '</span></h3><div class="sub fd-what">' + esc(f.what) + '</div></div>' +
      '<ul class="pts">' + f.pts.map(function (p) { return '<li>' + esc(p) + '</li>'; }).join('') + '</ul>' +
      (pl ? '<div class="fd-where">想吃可以去</div>' + placeHTML(pl) : '') + '</div></article>';
  }).join('');
  var slides = track.children, fPrev = document.getElementById('foodPrev'), fNext = document.getElementById('foodNext'), fCount = document.getElementById('foodCount');
  function curSlide() {
    var best = 0, bd = 1e9, mid = track.scrollLeft + track.clientWidth / 2;
    for (var i = 0; i < slides.length; i++) {
      var c = slides[i].offsetLeft + slides[i].offsetWidth / 2, d = Math.abs(c - mid);
      if (d < bd) { bd = d; best = i; }
    }
    return best;
  }
  function goSlide(i) {
    i = Math.max(0, Math.min(FN - 1, i));
    var el = slides[i];
    track.scrollTo({ left: el.offsetLeft - (track.clientWidth - el.offsetWidth) / 2, behavior: 'smooth' });
  }
  function syncCar() {
    var i = curSlide();
    fCount.textContent = (i + 1) + ' / ' + FN;
    fPrev.disabled = i === 0;
    fNext.disabled = i === FN - 1;
  }
  var st;
  track.addEventListener('scroll', function () { clearTimeout(st); st = setTimeout(syncCar, 60); }, { passive: true });
  fPrev.addEventListener('click', function () { goSlide(curSlide() - 1); });
  fNext.addEventListener('click', function () { goSlide(curSlide() + 1); });
  track.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') { e.preventDefault(); goSlide(curSlide() - 1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); goSlide(curSlide() + 1); }
  });
  syncCar();

  /* ---------- 給司機看：全螢幕大字地址 ---------- */
  var hov = document.getElementById('hotelCard');
  var HOTEL = PL.push(T.places.hotel) - 1;
  document.getElementById('hotelLinks').innerHTML = mapLinks(T.places.hotel);
  function openPlace(pl) {
    var cut = pl.sc.indexOf('（');
    document.getElementById('hcK').textContent = pl.tw ? '請送我到這裡，謝謝' : '请送我到这里，谢谢';
    document.getElementById('hcName').innerHTML = cut > 0 ? esc(pl.sc.slice(0, cut)) + '<small>' + esc(pl.sc.slice(cut)) + '</small>' : esc(pl.sc);
    document.getElementById('hcAddr').textContent = pl.addr;
    hov.querySelector('.hc-in').setAttribute('lang', pl.tw ? 'zh-Hant-TW' : 'zh-Hans');
    hov.hidden = false; document.body.classList.add('lock'); hov.querySelector('.hc-close').focus();
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-place]');
    if (b) { openPlace(PL[b.dataset.place === 'hotel' ? HOTEL : +b.dataset.place]); return; }
    if (e.target.closest('[data-close-hotel]') || e.target === hov) { hov.hidden = true; document.body.classList.remove('lock'); }
    var s = e.target.closest('.spk');
    if (s) speak(s);
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !hov.hidden) { hov.hidden = true; document.body.classList.remove('lock'); } });

  /* ---------- 上方「現在」列 ---------- */
  function at(d, hm) { var p = hm.split(':'); return Date.UTC(Y, MON, d, +p[0] - 8, +p[1]); }
  var E = [];
  T.days.forEach(function (d) {
    d.items.forEach(function (it) {
      if (!it.t || !it.id) return;
      E.push({ d: d.d, t: it.t, n: it.nb || it.title, id: it.id, move: it.kind === 'move', s: at(d.d, it.t) });
    });
  });
  E.sort(function (a, b) { return a.s - b.s; });
  var END = at(T.endAt.d, T.endAt.t);

  // 測試用：網址加上 ?now=2026-12-17T10:30（當地時間）
  var fake = null, q = /[?&]now=(\d{4})-(\d\d)-(\d\d)T(\d\d):(\d\d)/.exec(location.search);
  if (q) fake = Date.UTC(+q[1], +q[2] - 1, +q[3], +q[4] - 8, +q[5]);
  var t0 = Date.now();
  function now() { return fake === null ? Date.now() : fake + (Date.now() - t0); }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function parts(ms) { var d = new Date(ms + 8 * 3600e3); return { d: d.getUTCDate(), m: d.getUTCMonth(), y: d.getUTCFullYear(), h: d.getUTCHours(), mi: d.getUTCMinutes() }; }

  var nb = { prev: document.getElementById('nbPrev'), cur: document.getElementById('nbCur'), next: document.getElementById('nbNext') };
  function put(el, time, name, target, empty) {
    el.querySelector('.nb-time').textContent = time || '';
    el.querySelector('.nb-name').textContent = name || '';
    el.dataset.target = target || '';
    el.classList.toggle('empty', !!empty);
    el.disabled = !target;
  }
  function stamp(e, today) { return (e.d !== today ? T.month + '/' + e.d + ' ' : '') + e.t; }
  var flow = [].slice.call(document.querySelectorAll('.tl > .it[id]'));
  function mark(id) {
    var idx = -1;
    flow.forEach(function (el, i) { if (el.id === id) idx = i; });
    flow.forEach(function (el, i) { el.classList.toggle('is-now', i === idx); el.classList.toggle('is-past', idx >= 0 && i < idx); });
  }
  function render() {
    var ms = now(), p = parts(ms), today = (p.y === Y && p.m === MON) ? p.d : 0;
    var clock = pad(p.h) + ':' + pad(p.mi);
    var i = -1;
    E.forEach(function (e, k) { if (ms >= e.s) i = k; });
    document.querySelectorAll('nav a[data-day]').forEach(function (a) { a.classList.toggle('today', +a.dataset.day === today); });
    if (i < 0) {
      // 用日曆天算：今天是幾號、出發是幾號
      var dd = Math.round((Date.UTC(Y, MON, E[0].d) - Date.UTC(p.y, p.m, p.d)) / 864e5);
      put(nb.prev, '', '', '', true);
      put(nb.cur, dd > 1 ? '還有 ' + dd + ' 天出發' : dd === 1 ? '明天出發' : '今天出發', T.month + '/' + E[0].d + ' ' + E[0].n, E[0].id);
      put(nb.next, stamp(E[1], today), E[1].n, E[1].id);
      mark(null); return;
    }
    if (ms >= END) {
      var L = E[E.length - 1];
      put(nb.prev, stamp(L, today), L.n, L.id);
      put(nb.cur, '旅程結束', '平安回家，辛苦了', 'top');
      put(nb.next, '', '', '', true);
      mark(null); return;
    }
    var e = E[i], nx = E[i + 1], pv = E[i - 1];
    if (pv) put(nb.prev, stamp(pv, today), pv.n, pv.id); else put(nb.prev, '', '', '', true);
    put(nb.cur, (e.move ? '移動中 ' : '現在 ') + clock, e.n, e.id);
    if (nx) put(nb.next, stamp(nx, today), nx.n, nx.id); else put(nb.next, '', '', '', true);
    mark(e.id);
  }
  [nb.prev, nb.cur, nb.next].forEach(function (el) {
    el.addEventListener('click', function () {
      var t = el.dataset.target && document.getElementById(el.dataset.target);
      if (t) t.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });
  render();
  setInterval(render, 30000);
  document.addEventListener('visibilitychange', function () { if (!document.hidden) render(); });

  /* ---------- 地圖：旅行中預設只看今天 ---------- */
  var pn = parts(now()), todayDay = null;
  T.days.forEach(function (d) { if (pn.y === Y && pn.m === MON && pn.d === d.d) todayDay = d.id; });
  window.initMap(todayDay ? [todayDay] : T.days.map(function (d) { return d.id; }));

  /* ---------- 照片來源 ---------- */
  var cr = document.getElementById('credits');
  if (cr && window.IMG_CREDITS) {
    cr.innerHTML = window.IMG_CREDITS.map(function (c) {
      return '<li>' + esc(c.what) + '：<a href="' + esc(c.page) + '" target="_blank" rel="noopener">' + esc(c.author) + '</a>，' + esc(c.lic) + '</li>';
    }).join('');
  }

  /* ---------- 離線也能看 ---------- */
  if ('serviceWorker' in navigator && location.protocol === 'https:') {
    navigator.serviceWorker.register('sw.js').catch(function () {});
  }
})();
