/* 地圖：勾選天數，地圖自動放大到那幾天的範圍 */
(function () {
  var NS = 'http://www.w3.org/2000/svg';
  function P(ll) { return [(ll[0] - 118) * 1820.6, (24.57 - ll[1]) * 2000]; }

  // 地標（pr 越小越重要，標籤擠不下時先藏 pr 大的）
  var PTS = {
    kmAir:   { n: '金門機場',   ll: [118.3594, 24.4285], pr: 1 },
    shuitou: { n: '水頭碼頭',   ll: [118.2871, 24.4157], pr: 1 },
    jincheng:{ n: '金城',       ll: [118.3180, 24.4310], pr: 3 },
    wutong:  { n: '五通碼頭',   ll: [118.1887, 24.5334], pr: 1 },
    hotel:   { n: '飯店・中山路', ll: [118.0749, 24.4561], pr: 0, hotel: true },
    heping:  { n: '小埕戲',   ll: [118.0726, 24.4521], pr: 4 },
    tea:     { n: '不只有茶', ll: [118.0708, 24.4556], pr: 5 },
    bashi:   { n: '八市',       ll: [118.0697, 24.4612], pr: 6 },
    xiagu:   { n: '廈鼓碼頭',   ll: [118.0698, 24.4829], pr: 3 },
    gly:     { n: '鼓浪嶼',     ll: [118.0632, 24.4470], pr: 1 },
    spw:     { n: '沙坡尾',     ll: [118.0829, 24.4399], pr: 2 },
    shimao:  { n: '一席（雙子塔）', ll: [118.0850, 24.4378], pr: 3 },
    zhcity:  { n: '中華城',     ll: [118.0777, 24.4553], pr: 6 },
    yujian:  { n: '嶼見閩南',   ll: [118.0711, 24.4935], pr: 2 },
    aoyuan:  { n: '鰲園',       ll: [118.0874, 24.5689], pr: 2 },
    longzhou:{ n: '龍舟池',     ll: [118.0936, 24.5672], pr: 3 }
  };

  // 每天的路線；via 是經過點，bend 是弧度；mode：car 坐車、ship 坐船、walk 走路
  var ROUTES = {
    d1: [
      { a: 'kmAir', b: 'shuitou', m: 'car', bend: -0.18 },
      { a: 'shuitou', b: 'wutong', m: 'ship', bend: -0.12 },
      { a: 'wutong', b: 'hotel', m: 'car', via: [[118.135, 24.505]] }
    ],
    d2: [
      { a: 'hotel', b: 'aoyuan', m: 'car', via: [[118.0880, 24.4800], [118.1040, 24.5300], [118.1000, 24.5560]] },
      { a: 'aoyuan', b: 'longzhou', m: 'walk', bend: 0.25 },
      { a: 'longzhou', b: 'hotel', m: 'car', via: [[118.1090, 24.5560], [118.1110, 24.5300], [118.0920, 24.4800]] },
      { a: 'hotel', b: 'heping', m: 'car', bend: 0.6 }
    ],
    d3: [
      { a: 'hotel', b: 'xiagu', m: 'car', via: [[118.0772, 24.470]] },
      { a: 'xiagu', b: 'gly', m: 'ship', via: [[118.0662, 24.4640], [118.0648, 24.4535]] },
      { a: 'gly', b: 'xiagu', m: 'ship', via: [[118.0592, 24.4560], [118.0610, 24.4700]] },
      { a: 'xiagu', b: 'bashi', m: 'car', bend: 0.25 },
      { a: 'bashi', b: 'hotel', m: 'walk', bend: 0.2 },
      { a: 'hotel', b: 'tea', m: 'walk', bend: 0.5 },
      { a: 'tea', b: 'zhcity', m: 'walk', bend: 0.3 }
    ],
    d4: [
      { a: 'hotel', b: 'spw', m: 'car', via: [[118.0800, 24.4480]] },
      { a: 'spw', b: 'shimao', m: 'walk', bend: 0.4 },
      { a: 'shimao', b: 'yujian', m: 'car', via: [[118.0880, 24.4700]] },
      { a: 'yujian', b: 'hotel', m: 'car', bend: -0.3 }
    ],
    d5: [
      { a: 'hotel', b: 'wutong', m: 'car', via: [[118.1300, 24.4880]] },
      { a: 'wutong', b: 'shuitou', m: 'ship', bend: 0.12 },
      { a: 'shuitou', b: 'jincheng', m: 'car', bend: 0.3 },
      { a: 'jincheng', b: 'kmAir', m: 'car', bend: 0.25 }
    ]
  };

  // 背景地名（淡色，擠不下就不顯示）
  var CTX = [
    { n: '廈門島', ll: [118.128, 24.497], fs: 22 },
    { n: '集美', ll: [118.070, 24.590], fs: 18, skip: 'aoyuan' },
    { n: '金門島', ll: [118.392, 24.478], fs: 20 },
    { n: '小金門', ll: [118.238, 24.448], fs: 16 },
    { n: '鼓浪嶼', ll: [118.0628, 24.4445], fs: 16, skip: 'gly' }
  ];

  var root, landG, overG, wrap, cur = null, anim = null;

  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }

  function legPoints(leg) {
    var a = P(PTS[leg.a].ll), b = P(PTS[leg.b].ll), pts = [a];
    if (leg.via) leg.via.forEach(function (v) { pts.push(P(v)); });
    else if (leg.bend) {
      var mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, dx = b[0] - a[0], dy = b[1] - a[1];
      pts.push([mx - dy * leg.bend, my + dx * leg.bend]);
    }
    pts.push(b);
    return pts;
  }

  // Catmull-Rom 轉成平滑曲線
  function smooth(pts) {
    if (pts.length === 2) return 'M' + pts[0] + 'L' + pts[1];
    var d = 'M' + pts[0][0] + ' ' + pts[0][1];
    for (var i = 0; i < pts.length - 1; i++) {
      var p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
      var c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
      var c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
      d += 'C' + c1[0].toFixed(2) + ' ' + c1[1].toFixed(2) + ' ' + c2[0].toFixed(2) + ' ' + c2[1].toFixed(2) + ' ' + p2[0].toFixed(2) + ' ' + p2[1].toFixed(2);
    }
    return d;
  }

  function selected() {
    return [].slice.call(document.querySelectorAll('.mapday input:checked')).map(function (c) { return c.value; });
  }

  // 依選到的天數算出要看的範圍
  function targetBox(days) {
    var xs = [], ys = [];
    function add(p) { xs.push(p[0]); ys.push(p[1]); }
    add(P(PTS.hotel.ll));
    days.forEach(function (d) {
      ROUTES[d].forEach(function (l) { legPoints(l).forEach(add); });
    });
    var x0 = Math.min.apply(0, xs), x1 = Math.max.apply(0, xs), y0 = Math.min.apply(0, ys), y1 = Math.max.apply(0, ys);
    return { x0: x0, x1: x1, y0: y0, y1: y1 };
  }

  function fit(b, W, H) {
    var pad = 46;
    var bw = Math.max(b.x1 - b.x0, 6), bh = Math.max(b.y1 - b.y0, 6);
    var s = Math.min((W - pad * 2) / bw, (H - pad * 2) / bh, 8.5);
    var cx = (b.x0 + b.x1) / 2, cy = (b.y0 + b.y1) / 2;
    return { x: cx - W / s / 2, y: cy - H / s / 2, w: W / s, h: H / s, s: s };
  }

  function textW(str, fs) {
    var w = 0;
    for (var i = 0; i < str.length; i++) w += /[\x00-\x7f]/.test(str[i]) ? 0.58 : 1.02;
    return w * fs;
  }

  function draw(v, days) {
    var s = v.s;
    root.setAttribute('viewBox', v.x + ' ' + v.y + ' ' + v.w + ' ' + v.h);
    landG.setAttribute('stroke-width', 1.2 / s);
    while (overG.firstChild) overG.removeChild(overG.firstChild);

    var used = {};
    days.forEach(function (d) {
      var c = TRIP_COLOR[d];
      var g = el('g', { 'data-day': d }, overG);
      ROUTES[d].forEach(function (l) {
        used[l.a] = used[l.b] = 1;
        var dash = l.m === 'ship' ? (9 / s) + ' ' + (6 / s) : l.m === 'walk' ? (1 / s) + ' ' + (6 / s) : 'none';
        el('path', { d: smooth(legPoints(l)), fill: 'none', stroke: '#fff', 'stroke-width': 7 / s, 'stroke-linecap': 'round', opacity: 0.85 }, g);
        var p = el('path', { d: smooth(legPoints(l)), fill: 'none', stroke: c, 'stroke-width': (l.m === 'walk' ? 4.4 : 3.6) / s,
          'stroke-linecap': 'round', 'stroke-dasharray': dash }, g);
        // 中間畫一個方向箭頭
        try {
          var L = p.getTotalLength();
          if (L * s > 46) {
            var m1 = p.getPointAtLength(L * 0.5), m2 = p.getPointAtLength(L * 0.5 + 0.5 / s);
            var ang = Math.atan2(m2.y - m1.y, m2.x - m1.x) * 180 / Math.PI;
            el('path', { d: 'M-5 -5.5 L4 0 L-5 5.5', fill: 'none', stroke: c, 'stroke-width': 3, 'stroke-linecap': 'round', 'stroke-linejoin': 'round',
              transform: 'translate(' + m1.x + ' ' + m1.y + ') rotate(' + ang + ') scale(' + (1 / s) + ')' }, g);
          }
        } catch (e) {}
      });
    });

    // 地標點
    var list = Object.keys(used).concat(used.hotel ? [] : ['hotel']).map(function (k) { return k; });
    list.sort(function (a, b) { return PTS[a].pr - PTS[b].pr; });
    var placed = [];
    var dots = list.map(function (k) { var p = P(PTS[k].ll); return { k: k, x: (p[0] - v.x) * s, y: (p[1] - v.y) * s }; });
    // 先畫次要的點，飯店最後畫，才會在最上面
    dots.slice().reverse().forEach(function (dt) {
      var pt = PTS[dt.k], p = P(pt.ll);
      if (pt.hotel) {
        var r = 13 / s;
        el('rect', { x: p[0] - r, y: p[1] - r, width: 2 * r, height: 2 * r, rx: 4 / s, fill: '#B23A26', stroke: '#fff', 'stroke-width': 2.5 / s }, overG);
        el('text', { x: p[0], y: p[1] + 5.6 / s, 'font-size': 16 / s, 'font-weight': 900, fill: '#fff', 'text-anchor': 'middle' }, overG).textContent = '住';
        placed.push({ x0: dt.x - 15, x1: dt.x + 15, y0: dt.y - 15, y1: dt.y + 15 });
      } else {
        el('circle', { cx: p[0], cy: p[1], r: 6.5 / s, fill: '#2B1A12', stroke: '#fff', 'stroke-width': 2.4 / s }, overG);
        placed.push({ x0: dt.x - 7, x1: dt.x + 7, y0: dt.y - 7, y1: dt.y + 7 });
      }
    });
    var W = v.w * s, H = v.h * s;
    function fits(bx) {
      if (bx.x0 < 2 || bx.x1 > W - 2 || bx.y0 < 2 || bx.y1 > H - 2) return false;
      return !placed.some(function (q) { return !(bx.x1 < q.x0 || bx.x0 > q.x1 || bx.y1 < q.y0 || bx.y0 > q.y1); });
    }
    dots.forEach(function (dt) {
      var pt = PTS[dt.k], fs = pt.pr <= 1 ? 17 : 15.5, tw = textW(pt.n, fs), th = fs * 1.2, gap = pt.hotel ? 18 : 11;
      var cands = [
        { x: dt.x + gap, y: dt.y - th / 2, a: 'start' },
        { x: dt.x - gap - tw, y: dt.y - th / 2, a: 'end' },
        { x: dt.x - tw / 2, y: dt.y - gap - th, a: 'middle' },
        { x: dt.x - tw / 2, y: dt.y + gap, a: 'middle' }
      ];
      var ok = null;
      for (var i = 0; i < cands.length && !ok; i++) {
        var c = cands[i], bx = { x0: c.x - 3, x1: c.x + tw + 3, y0: c.y - 2, y1: c.y + th + 2 };
        if (fits(bx)) ok = { c: c, bx: bx };
      }
      // 飯店一定要有名字：放不下就蓋在別的點上面
      for (i = 0; i < cands.length && !ok && pt.hotel; i++) {
        c = cands[i]; bx = { x0: c.x - 3, x1: c.x + tw + 3, y0: c.y - 2, y1: c.y + th + 2 };
        if (bx.x0 >= 2 && bx.x1 <= W - 2 && bx.y0 >= 2 && bx.y1 <= H - 2) ok = { c: c, bx: bx };
      }
      if (!ok) return;
      placed.push(ok.bx);
      var c = ok.c, tx = c.a === 'start' ? c.x : c.a === 'end' ? c.x + tw : c.x + tw / 2;
      el('text', { x: v.x + tx / s, y: v.y + (c.y + th * 0.82) / s, 'font-size': fs / s, 'font-weight': 900, fill: '#2B1A12',
        'text-anchor': c.a, stroke: '#fff', 'stroke-width': 4.5 / s, 'paint-order': 'stroke', 'stroke-linejoin': 'round' }, overG).textContent = pt.n;
    });
    var extra = CTX.slice();
    extra.forEach(function (c) {
      if (c.skip && used[c.skip]) return;
      var p = P(c.ll), x = (p[0] - v.x) * s, y = (p[1] - v.y) * s, tw = textW(c.n, c.fs);
      var bx = { x0: x - tw / 2 - 2, x1: x + tw / 2 + 2, y0: y - c.fs * 0.9, y1: y + c.fs * 0.3 };
      if (!fits(bx)) return;
      placed.push(bx);
      el('text', { x: p[0], y: p[1], 'font-size': c.fs / s, 'font-weight': c.color ? 900 : 800, fill: c.color || '#9A7E58', 'text-anchor': 'middle',
        'letter-spacing': (c.color ? 0 : 3) / s, stroke: c.color ? '#fff' : 'none', 'stroke-width': 4 / s, 'paint-order': 'stroke' }, overG).textContent = c.n;
    });
  }

  function update(instant) {
    var days = selected();
    var W = wrap.clientWidth, H = wrap.clientHeight;
    if (!W || !H) return;
    var tgt = fit(targetBox(days.length ? days : []), W, H);
    if (instant || !cur || matchMedia('(prefers-reduced-motion: reduce)').matches) {
      cur = tgt; draw(cur, days); return;
    }
    var from = cur, t0 = performance.now(), dur = 520;
    if (anim) cancelAnimationFrame(anim);
    (function step(now) {
      var k = Math.min(1, (now - t0) / dur), e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
      // 用對數內插縮放比例，放大縮小看起來比較順
      var s = Math.exp(Math.log(from.s) + (Math.log(tgt.s) - Math.log(from.s)) * e);
      var cx = (from.x + from.w / 2) + ((tgt.x + tgt.w / 2) - (from.x + from.w / 2)) * e;
      var cy = (from.y + from.h / 2) + ((tgt.y + tgt.h / 2) - (from.y + from.h / 2)) * e;
      cur = { s: s, w: W / s, h: H / s, x: cx - W / s / 2, y: cy - H / s / 2 };
      draw(cur, days);
      if (k < 1) anim = requestAnimationFrame(step); else anim = null;
    })(t0);
  }

  var TRIP_COLOR = {};
  window.initMap = function (defaultDays) {
    TRIP.days.forEach(function (d) { TRIP_COLOR[d.id] = d.color; });
    wrap = document.getElementById('mapbox');
    root = el('svg', { xmlns: NS, role: 'img', 'aria-label': '五天行程地圖', preserveAspectRatio: 'xMidYMid meet' }, wrap);
    el('rect', { x: -2000, y: -2000, width: 6000, height: 6000, fill: '#CFE5EE' }, root);
    landG = el('path', { d: window.LAND_PATH, fill: '#F4E8D2', stroke: '#C9B08A', 'stroke-linejoin': 'round' }, root);
    overG = el('g', {}, root);

    var inputs = [].slice.call(document.querySelectorAll('.mapday input'));
    inputs.forEach(function (cb) {
      cb.checked = defaultDays.indexOf(cb.value) >= 0;
      cb.addEventListener('change', function () {
        if (!selected().length) cb.checked = true; // 至少留一天
        update();
      });
    });
    var all = document.getElementById('mapAll');
    if (all) all.addEventListener('click', function () { inputs.forEach(function (c) { c.checked = true; }); update(); });
    var rt;
    window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { update(true); }, 120); });
    update(true);
  };
})();
