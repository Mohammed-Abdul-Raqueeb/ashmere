/* ══════════════════════════════════════════════════════════════════
   Ashmere
   Native scrolling stays intact. Every module is guarded, so a page
   only pays for the interactives it actually has.
   ══════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var $  = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return v < a ? a : v > b ? b : v; };
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', function (e) { reduce = e.matches; });
  var NS = 'http://www.w3.org/2000/svg';
  function el(t, a) { var n = document.createElementNS(NS, t); for (var k in a) n.setAttribute(k, a[k]); return n; }

  /* ── shared rAF ───────────────────────────────────────────── */
  var jobs = [], running = false, frame = { y: 0, vh: 0 };
  function tick() {
    frame.y = window.scrollY || 0; frame.vh = window.innerHeight;
    var busy = false;
    for (var i = 0; i < jobs.length; i++) if (jobs[i](frame) === true) busy = true;
    if (busy) requestAnimationFrame(tick); else running = false;
  }
  function kick() { if (!running) { running = true; requestAnimationFrame(tick); } }
  addEventListener('scroll', kick, { passive: true });
  addEventListener('resize', kick, { passive: true });

  /* ── bar ──────────────────────────────────────────────────── */
  (function () {
    var bar = $('#bar'); if (!bar) return;
    var on = null;
    jobs.push(function (f) {
      var want = f.y > 24;
      if (want !== on) { on = want; bar.classList.toggle('is-lifted', want); }
      return false;
    });
  })();

  /* ── "open today" chip: real opening hours, not decoration ── */
  (function () {
    var chip = $('#openChip'), txt = $('#openText'); if (!chip) return;
    function paint() {
      var d = new Date(), h = d.getHours() + d.getMinutes() / 60, day = d.getDay(), m = d.getMonth();
      // gardens, park and meadow: every day, 09:00 to dusk (taken as 20:00 summer, 16:30 winter)
      var dusk = (m >= 3 && m <= 8) ? 20 : 16.5;
      var groundsOpen = h >= 9 && h < dusk;
      // house: Wed–Sun, late March to end of October, 11:00–17:00
      var season = m >= 2 && m <= 9;
      var houseDay = day === 0 || day >= 3;
      var houseOpen = season && houseDay && h >= 11 && h < 17;
      chip.classList.toggle('is-shut', !groundsOpen);
      txt.textContent = houseOpen ? 'House open until 5'
        : groundsOpen ? (season && houseDay ? 'Grounds open, house from 11' : 'Grounds open until dusk')
        : 'Grounds open from 9';
    }
    paint(); setInterval(paint, 60000);
  })();

  /* ── mobile sheet ─────────────────────────────────────────── */
  (function () {
    var b = $('#burger'), s = $('#sheet'); if (!b || !s) return;
    var open = false, last = null;
    function set(v) {
      if (v === open) return;
      open = v;
      b.setAttribute('aria-expanded', String(v));
      b.setAttribute('aria-label', v ? 'Close menu' : 'Open menu');
      document.body.style.overflow = v ? 'hidden' : '';
      if (v) {
        last = document.activeElement; s.hidden = false;
        requestAnimationFrame(function () { s.classList.add('is-open'); });
        var a = s.querySelector('a'); if (a) a.focus({ preventScroll: true });
      } else {
        s.classList.remove('is-open');
        setTimeout(function () { if (!open) s.hidden = true; }, 300);
        if (last) last.focus({ preventScroll: true });
      }
    }
    b.addEventListener('click', function () { set(!open); });
    document.addEventListener('keydown', function (e) {
      if (!open) return;
      if (e.key === 'Escape') return set(false);
      if (e.key !== 'Tab') return;
      var f = $$('a,button', s); if (!f.length) return;
      var fi = f[0], la = f[f.length - 1];
      if (e.shiftKey && document.activeElement === fi) { e.preventDefault(); la.focus(); }
      else if (!e.shiftKey && document.activeElement === la) { e.preventDefault(); fi.focus(); }
    });
    matchMedia('(min-width: 1081px)').addEventListener('change', function (e) { if (e.matches) set(false); });
  })();

  /* ── hero ─────────────────────────────────────────────────── */
  if (window.ASH_HERO) {
    (function () {
      var v = $('#heroVideo'); if (!v) return;
      var m = matchMedia, c = navigator.connection || {};
      var thin = c.saveData === true || /^(slow-2g|2g)$/.test(c.effectiveType || '');
      var name = 'meadow-1600', poster = 'poster-meadow';
      if (m('(max-width: 720px)').matches) { name = 'meadow-mobile'; poster = 'poster-mobile'; }
      else if (m('(max-width: 1200px)').matches) { name = 'meadow-1280'; }
      v.poster = 'assets/media/' + poster + '.webp';
      v.dataset.src = 'assets/media/' + name + '.mp4';
      if (reduce || thin) document.documentElement.classList.add('still');
      else { v.setAttribute('src', v.dataset.src); v.preload = 'auto'; }
    })();

    (function () {
      var media = $('.hero__media'); if (!media || reduce) return;
      var cur = 0;
      jobs.push(function (f) {
        var t = clamp(f.y / (f.vh || 1), 0, 1);
        var d = Math.abs(t - cur);
        cur += (t - cur) * (d > 0.15 ? 0.3 : 0.11);
        if (Math.abs(cur - t) < 0.0008) cur = t;
        media.style.transform = 'translate3d(0,' + (cur * 56).toFixed(1) + 'px,0) scale(' + (1 + cur * 0.055).toFixed(4) + ')';
        return cur !== t;
      });
    })();

    (function () {
      var seq = $$('.hero__h .ln > span').concat([$('.hero__lede'), $('.hero__acts')]).filter(Boolean);
      function play() {
        if (reduce) { seq.forEach(function (e) { e.style.opacity = 1; e.style.transform = 'none'; }); return; }
        seq.forEach(function (e, i) {
          e.style.transition = 'opacity 1s cubic-bezier(.16,1,.3,1) ' + (0.1 + i * 0.1) + 's,' +
                               'transform 1.15s cubic-bezier(.16,1,.3,1) ' + (0.1 + i * 0.1) + 's';
          requestAnimationFrame(function () { e.style.opacity = 1; e.style.transform = 'none'; });
        });
      }
      var fired = false, go = function () { if (!fired) { fired = true; play(); } };
      if (document.fonts && document.fonts.ready) { document.fonts.ready.then(go); setTimeout(go, 900); }
      else go();
    })();
  }

  /* ── video lifecycle + the one motion control ─────────────── */
  (function () {
    var root = document.documentElement;
    var vids = $$('video[data-src], #heroVideo');
    if (!vids.length) return;
    var btn = $('#motionBtn'), label = $('#motionLabel');
    var seen = new WeakMap(), armed = false;
    var wanted = function () { return !root.classList.contains('still'); };

    function arm(v) {
      if (!v.getAttribute('src') && v.dataset.src) { v.setAttribute('src', v.dataset.src); v.preload = 'auto'; }
      return !!v.getAttribute('src');
    }
    function play(v) {
      if (!wanted() || !seen.get(v) || !arm(v)) return;
      var p = v.play();
      if (p && p.catch) p.catch(function () {
        setMotion(false);
        if (armed) return;
        armed = true;
        ['pointerdown', 'keydown', 'touchstart'].forEach(function (t) {
          document.addEventListener(t, function once() {
            ['pointerdown', 'keydown', 'touchstart'].forEach(function (u) { document.removeEventListener(u, once); });
            setMotion(true);
          }, { once: true, passive: true });
        });
      });
    }
    function setMotion(on) {
      root.classList.toggle('still', !on);
      if (btn) { btn.setAttribute('aria-pressed', String(on)); label.textContent = on ? 'Playing' : 'Paused'; }
      vids.forEach(function (v) { on ? play(v) : (v.getAttribute('src') && v.pause()); });
    }
    if (btn) { setMotion(wanted()); btn.addEventListener('click', function () { setMotion(!wanted()); }); }

    vids.forEach(function (v) {
      seen.set(v, false);
      v.addEventListener('loadeddata', function () { v.classList.add('is-live'); play(v); });
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (es) {
          es.forEach(function (e) {
            seen.set(v, e.isIntersecting);
            if (e.isIntersecting) play(v); else if (v.getAttribute('src')) v.pause();
          });
        }, { rootMargin: '25% 0px' }).observe(v.closest('section') || v);
      } else { seen.set(v, true); play(v); }
    });
    document.addEventListener('visibilitychange', function () {
      vids.forEach(function (v) {
        if (!v.getAttribute('src')) return;
        document.hidden ? v.pause() : play(v);
      });
    });
  })();

  /* ── reveals ──────────────────────────────────────────────── */
  (function () {
    var items = $$('.reveal'); if (!items.length) return;
    if (!('IntersectionObserver' in window) || reduce)
      return items.forEach(function (e) { e.classList.add('is-in'); });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var t = e.target, i = Array.prototype.indexOf.call(t.parentNode.children, t);
        t.style.transitionDelay = (Math.min(i, 5) * 0.055) + 's';
        t.classList.add('is-in'); io.unobserve(t);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
    items.forEach(function (e) { io.observe(e); });
  })();

  /* ── THE LONG PLAN ────────────────────────────────────────── */
  if (window.ASH_PLAN) (function () {
    var svg = $('#planSvg'); if (!svg) return;
    var W = 900, Hh = 380, HORIZON = 248, NOW = 2026;

    var EVENTS = [
      [1583, 'The house is finished', 'Built on the footings of a grange, using stone from the same quarry that still supplies our repairs.'],
      [1690, 'The Yew Walk is planted', 'Two hundred and eight yews. All but four are still standing.'],
      [1771, 'The lake is dug', 'Along with the cascade, by a workforce of ninety over two summers.'],
      [1782, 'The west park oaks go in', 'Four hundred and ten of them, for timber nobody alive would see cut.'],
      [1908, 'The arboretum is started', 'A hedge against losing species we had not yet noticed we were losing.'],
      [1947, 'The estate is nearly sold', 'Death duties. Two farms went; the park did not.'],
      [1994, 'Meadow restoration begins', 'Green hay from a surviving meadow eight miles away, spread on ploughed ground.'],
      [2004, 'The cascade runs again', 'After three winters of dredging.'],
      [2011, 'The endowment is settled', 'Sized to cover the roof, the yews and the oaks in perpetuity, not the events diary.'],
      [2026, 'Where we are now', 'Two hundred and forty acres under restoration, nine hundred trees planted in the last decade.'],
      [2048, 'The 1994 meadows reach full richness', 'On current counts, around thirty-eight species per square metre.'],
      [2072, 'First thinning of the 2010 oaks', 'The last people to make a decision about these trees will not have met us.'],
      [2124, 'The plan horizon', 'Everything committed today is costed to here. Beyond it is somebody else\u2019s problem, deliberately.']
    ];
    // x, base y, planting year, mature crown radius, years to maturity
    var TREES = [
      [92, 258, 1690, 20, 120], [126, 264, 1690, 19, 120], [158, 256, 1690, 21, 120],
      [214, 268, 1782, 40, 140], [286, 274, 1782, 44, 140], [356, 266, 1782, 38, 140],
      [430, 276, 1782, 46, 140], [508, 264, 1908, 30, 110], [566, 276, 1908, 27, 110],
      [640, 268, 1908, 32, 110], [706, 280, 2010, 42, 130], [772, 272, 2010, 39, 130],
      [836, 282, 2010, 44, 130], [252, 300, 2010, 34, 130], [612, 302, 2010, 36, 130]
    ];
    var BUILDS = [
      [372, 1583, 96, 62, 'House'], [478, 1583, 40, 34, ''], [318, 1866, 44, 30, 'Yard']
    ];
    var LAKE = [1771, 560, 318, 190, 26];

    var gGround = $('#planGround'), gTrees = $('#planTrees'), gBuild = $('#planBuild'),
        gNear = $('#planNear'), gTags = $('#planTags');
    var yearEl = $('#planYear'), tenseEl = $('#planTense'),
        titleEl = $('#planTitle'), bodyEl = $('#planBody'), input = $('#planTime');

    // static ground
    gGround.appendChild(el('rect', { x: 0, y: HORIZON, width: W, height: Hh - HORIZON, fill: '#B9C6A6' }));
    gGround.appendChild(el('rect', { x: 0, y: HORIZON, width: W, height: 26, fill: '#C9D2B4' }));
    gGround.appendChild(el('line', { x1: 0, y1: HORIZON, x2: W, y2: HORIZON, stroke: '#9EAF8C', 'stroke-width': 1 }));

    var lakeEl = el('ellipse', { cx: LAKE[1], cy: LAKE[2], rx: LAKE[3] / 2, ry: LAKE[4],
      fill: '#8FA9AE', stroke: '#77939A', 'stroke-width': 1 });
    gGround.appendChild(lakeEl);

    var buildEls = BUILDS.map(function (b) {
      var g = el('g', {});
      g.appendChild(el('rect', { x: b[0] - b[2] / 2, y: HORIZON - b[3], width: b[2], height: b[3],
        fill: '#6E6459', stroke: '#574E45', 'stroke-width': 1 }));
      g.appendChild(el('path', { d: 'M' + (b[0] - b[2] / 2 - 5) + ' ' + (HORIZON - b[3]) +
        ' L' + b[0] + ' ' + (HORIZON - b[3] - 20) + ' L' + (b[0] + b[2] / 2 + 5) + ' ' + (HORIZON - b[3]) + ' Z',
        fill: '#544B43' }));
      gBuild.appendChild(g); return g;
    });

    // sort far-to-near so the canopy overlaps believably, and split around the
    // buildings: anything standing closer than the house is drawn in front of it
    var order = TREES.slice().sort(function (a, b) { return a[1] - b[1]; });
    var treeEls = order.map(function (t, i) {
      var near = t[1] > 276;
      var depth = clamp((t[1] - 250) / 60, 0, 1);          // 0 = far, 1 = near
      var g = el('g', {});
      var trunk = el('rect', { x: t[0] - 2, y: t[1] - 18, width: 4, height: 18,
        fill: near ? '#5E4F3B' : '#7A6A54' });
      // three lobes: a main crown and two smaller shoulders
      var lobes = [
        el('circle', { cx: t[0], cy: t[1] - 22, r: 4 }),
        el('circle', { cx: t[0], cy: t[1] - 22, r: 3 }),
        el('circle', { cx: t[0], cy: t[1] - 22, r: 3 })
      ];
      g.appendChild(trunk);
      lobes.forEach(function (l) { g.appendChild(l); });
      (near ? gNear : gTrees).appendChild(g);
      return { g: g, trunk: trunk, lobes: lobes, d: t, depth: depth, seed: (i * 37) % 11 };
    });

    function nearest(y) {
      var best = EVENTS[0];
      for (var i = 0; i < EVENTS.length; i++) if (EVENTS[i][0] <= y) best = EVENTS[i];
      return best;
    }

    function render(y) {
      var future = y > NOW;
      treeEls.forEach(function (t) {
        var planted = t.d[2], mature = t.d[4], rMax = t.d[3];
        if (y < planted) { t.g.style.display = 'none'; return; }
        t.g.style.display = '';
        var f = clamp((y - planted) / mature, 0.06, 1);
        var r = rMax * Math.pow(f, 0.62);              // fast early, slow later
        var trunkH = 14 + r * 0.85;
        var cy = t.d[1] - trunkH - r * 0.5;
        var tw = Math.max(3.2, r * 0.17);
        t.trunk.setAttribute('y', (t.d[1] - trunkH).toFixed(1));
        t.trunk.setAttribute('height', trunkH.toFixed(1));
        t.trunk.setAttribute('x', (t.d[0] - tw / 2).toFixed(1));
        t.trunk.setAttribute('width', tw.toFixed(1));

        // nearer trees are darker and cooler; far ones wash toward the sky
        var lit = 108 - t.depth * 34, sat = 46 + t.depth * 14;
        var fill = 'hsl(' + (98 + t.seed) + ' ' + sat + '% ' + (lit / 3.4).toFixed(0) + '%)';
        var planned = planted > NOW;                   // committed, not yet in the ground
        var wob = t.seed / 11;
        var geom = [
          [t.d[0], cy, r],
          [t.d[0] - r * (0.5 + wob * 0.18), cy + r * 0.26, r * (0.62 - wob * 0.1)],
          [t.d[0] + r * (0.48 - wob * 0.16), cy + r * 0.3,  r * (0.58 + wob * 0.12)]
        ];
        t.lobes.forEach(function (l, i) {
          l.setAttribute('cx', geom[i][0].toFixed(1));
          l.setAttribute('cy', geom[i][1].toFixed(1));
          l.setAttribute('r', Math.max(1, geom[i][2]).toFixed(1));
          l.setAttribute('fill', planned ? 'none' : fill);
          l.setAttribute('fill-opacity', planned ? '0' : (i ? '.9' : '1'));
          l.setAttribute('stroke', planned ? fill : 'none');
          l.setAttribute('stroke-width', planned ? '1.1' : '0');
          l.setAttribute('stroke-dasharray', planned ? '3 3' : '');
        });
        t.trunk.setAttribute('fill-opacity', planned ? '.35' : '1');
        t.g.setAttribute('opacity', future && planted <= NOW ? '.9' : '1');
      });
      buildEls.forEach(function (g, i) { g.style.display = y >= BUILDS[i][1] ? '' : 'none'; });
      lakeEl.style.display = y >= LAKE[0] ? '' : 'none';

      gTags.textContent = '';
      var ev = nearest(y);
      yearEl.textContent = y;
      tenseEl.textContent = y > NOW ? 'projected' : y === NOW ? 'today' : 'built';
      titleEl.textContent = ev[1];
      bodyEl.textContent = ev[2];

      // a marker on the horizon for the event we are sitting on
      if (Math.abs(y - ev[0]) < 40) {
        var t = el('text', { x: 18, y: 82, fill: '#5E6B60', 'font-size': 13, 'letter-spacing': '.08em' });
        t.textContent = ev[0]; gTags.appendChild(t);
      }
      svg.style.filter = y > NOW ? 'saturate(.82)' : '';
    }

    // decade ticks under the scale
    var ticks = $('#planTicks');
    [1600, 1700, 1800, 1900, 2000, 2100].forEach(function (d) {
      var li = document.createElement('li'); li.textContent = d; ticks.appendChild(li);
    });

    input.addEventListener('input', function () { render(+input.value); });
    render(+input.value);
  })();

  /* ── THE QUADRAT ──────────────────────────────────────────── */
  if (window.ASH_QUAD) (function () {
    var svg = $('#quadSvg'); if (!svg) return;
    var W = 720, Hh = 500, SIDE = 46;   // 46px reads as one metre at this scale

    // restoration blocks: older ground carries more species
    var BLOCKS = [
      { n: '1994 block', x: 40,  y: 40,  w: 300, h: 210, count: 34, tone: '#315C33',
        sp: ['Yellow rattle','Common knapweed','Oxeye daisy','Meadow buttercup','Bird\u2019s-foot trefoil',
             'Red clover','Lady\u2019s bedstraw','Yarrow','Sweet vernal grass','Crested dog\u2019s-tail','Pignut','Betony'] },
      { n: '2003 block', x: 360, y: 40,  w: 320, h: 200, count: 27, tone: '#3A6837',
        sp: ['Yellow rattle','Oxeye daisy','Meadow buttercup','Red clover','Ribwort plantain',
             'Common sorrel','Yarrow','Sweet vernal grass','Bird\u2019s-foot trefoil'] },
      { n: '2016 block', x: 40,  y: 270, w: 290, h: 190, count: 19, tone: '#477538',
        sp: ['Yellow rattle','Oxeye daisy','Meadow buttercup','Ribwort plantain','Common sorrel','Red clover','Yorkshire fog'] },
      { n: 'The wet corner', x: 350, y: 260, w: 200, h: 200, count: 31, tone: '#2C5735',
        sp: ['Ragged robin','Marsh marigold','Cuckooflower','Meadowsweet','Common spotted orchid',
             'Yellow rattle','Sneezewort','Water avens','Devil\u2019s-bit scabious'] },
      { n: 'The 1998 mistake', x: 566, y: 258, w: 116, h: 202, count: 9, tone: '#6A8748',
        sp: ['Yorkshire fog','Perennial rye-grass','Creeping buttercup','Ribwort plantain','Docks'] }
    ];

    var gZ = $('#quadZones'), gP = $('#quadPaths'), gL = $('#quadLabels'), gF = $('#quadFrame');
    BLOCKS.forEach(function (b, i) {
      gZ.appendChild(el('rect', { x: b.x, y: b.y, width: b.w, height: b.h, fill: b.tone }));
      var t = el('text', { x: b.x + 10, y: b.y + 20, fill: 'rgba(238,241,233,.6)',
        'font-size': 11, 'letter-spacing': '.09em' });
      t.textContent = b.n.toUpperCase(); gL.appendChild(t);
    });
    // mown paths, which is what visitors actually walk on
    [[0, 256, 720, 8], [336, 0, 8, 500]].forEach(function (p) {
      gP.appendChild(el('rect', { x: p[0], y: p[1], width: p[2], height: p[3], fill: '#8CA36B', opacity: .75 }));
    });

    var frame = el('rect', { width: SIDE, height: SIDE, fill: 'rgba(233,201,120,.16)',
      stroke: '#E9C978', 'stroke-width': 2 });
    var cross = el('path', { stroke: 'rgba(233,201,120,.7)', 'stroke-width': 1, fill: 'none' });
    gF.appendChild(frame); gF.appendChild(cross);

    var countEl = $('#quadCount'), zoneEl = $('#quadZone'), listEl = $('#quadList');
    var ix = $('#quadX'), iy = $('#quadY');

    function blockAt(cx, cy) {
      for (var i = 0; i < BLOCKS.length; i++) {
        var b = BLOCKS[i];
        if (cx >= b.x && cx <= b.x + b.w && cy >= b.y && cy <= b.y + b.h) return b;
      }
      return null;
    }
    function render() {
      var cx = clamp(+ix.value, SIDE / 2, W - SIDE / 2), cy = clamp(+iy.value, SIDE / 2, Hh - SIDE / 2);
      frame.setAttribute('x', (cx - SIDE / 2).toFixed(1));
      frame.setAttribute('y', (cy - SIDE / 2).toFixed(1));
      cross.setAttribute('d', 'M' + (cx - 7) + ' ' + cy + 'h14M' + cx + ' ' + (cy - 7) + 'v14');
      var b = blockAt(cx, cy);
      if (!b) {
        countEl.textContent = '—'; zoneEl.textContent = 'On a mown path';
        listEl.innerHTML = '<li>Cut short, walked on, and not surveyed</li>';
        return;
      }
      // a little variation so neighbouring squares are not identical
      var jitter = Math.round(Math.sin(cx * 0.07) * 1.6 + Math.cos(cy * 0.09) * 1.4);
      var n = Math.max(4, b.count + jitter);
      countEl.textContent = n;
      zoneEl.textContent = b.n + ', restored ' + (b.n.match(/\d{4}/) ? b.n.match(/\d{4}/)[0] : 'variously');
      var show = b.sp.slice(0, Math.min(b.sp.length, Math.max(4, Math.round(n / 3))));
      listEl.innerHTML = show.map(function (s) { return '<li>' + s + '</li>'; }).join('') +
        (n > show.length ? '<li>+ ' + (n - show.length) + ' more</li>' : '');
    }

    function fromPointer(e) {
      var r = svg.getBoundingClientRect();
      ix.value = Math.round((e.clientX - r.left) / r.width * W);
      iy.value = Math.round((e.clientY - r.top) / r.height * Hh);
      render();
    }
    var dragging = false;
    svg.addEventListener('pointerdown', function (e) {
      dragging = true; svg.setPointerCapture(e.pointerId); fromPointer(e); e.preventDefault();
    });
    svg.addEventListener('pointermove', function (e) { if (dragging) fromPointer(e); });
    ['pointerup', 'pointercancel'].forEach(function (t) {
      svg.addEventListener(t, function (e) {
        dragging = false;
        if (svg.hasPointerCapture && svg.hasPointerCapture(e.pointerId)) svg.releasePointerCapture(e.pointerId);
      });
    });
    ix.addEventListener('input', render); iy.addEventListener('input', render);
    render();
  })();

  /* ── THE ESTATE YEAR RING ─────────────────────────────────── */
  if (window.ASH_VISIT) {
    (function () {
      var wheel = $('#ringWheel'); if (!wheel) return;
      var M = [
        ['January','Park and meadow open. The house is shut and the yews are being cut.'],
        ['February','Snowdrops through the Yew Walk. Winter pruning in the walled garden.'],
        ['March','House opens late in the month. Blackthorn along the west park boundary.'],
        ['April','Cowslips in the meadow. The glasshouse fills up.'],
        ['May','Buttercups, and the best fortnight of the year. Paths only from mid-month.'],
        ['June','Orchids in the south meadow, if it has been wet enough. Roses in the walled garden.'],
        ['July','Yellow rattle sets seed. The meadow is cut in the last week.'],
        ['August','Hay lifted, aftermath grazing begins. Fruit in the walled garden.'],
        ['September','Arboretum starts to turn. Best month for the lake.'],
        ['October','House closes at the end of the month. Fungi in the west park.'],
        ['November','Tree planting starts. Park open, everything else winding down.'],
        ['December','Planting continues. The park on a hard frost is worth the drive.']
      ];
      var mEl = $('#ringMonth'), tEl = $('#ringText'), cur = new Date().getMonth();
      // the orbit radius must be a real length, measured from the wheel
      function radius() {
        var w = wheel.getBoundingClientRect().width;
        if (w) wheel.style.setProperty('--r', (w * 0.385).toFixed(1) + 'px');
      }
      radius();
      addEventListener('resize', radius, { passive: true });
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(radius);
      var btns = M.map(function (m, i) {
        var b = document.createElement('button');
        b.type = 'button';
        b.textContent = m[0].slice(0, 3);
        b.style.setProperty('--a', (i * 30) + 'deg');
        b.setAttribute('aria-pressed', 'false');
        b.setAttribute('aria-label', m[0]);
        b.addEventListener('click', function () { pick(i); });
        wheel.appendChild(b);
        return b;
      });
      function pick(i) {
        cur = (i + 12) % 12;
        btns.forEach(function (b, j) { b.setAttribute('aria-pressed', String(j === cur)); });
        mEl.textContent = M[cur][0];
        tEl.textContent = M[cur][1];
      }
      wheel.addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1
              : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : 0;
        if (!d) return;
        e.preventDefault(); pick(cur + d); btns[cur].focus();
      });
      pick(cur);
    })();

    /* ── FAQ ── */
    $$('.faq__q').forEach(function (q) {
      q.addEventListener('click', function () {
        var open = q.getAttribute('aria-expanded') === 'true';
        q.setAttribute('aria-expanded', String(!open));
        q.closest('.faq__i').classList.toggle('is-open', !open);
      });
    });

    /* ── enquiry (concept form: no backend, honest about it) ── */
    (function () {
      var form = $('#enquiry'); if (!form) return;
      var ok = $('#formOk');
      // take validation over only now that we are certainly running; without us the
      // browser's own required/type checks stay in force
      form.setAttribute('novalidate', '');
      function bad(f, msg) {
        var p = f.closest('.f');
        p.classList.add('is-bad'); f.setAttribute('aria-invalid', 'true');
        if (!p.querySelector('.err')) {
          var s = document.createElement('span'); s.className = 'err'; s.textContent = msg; p.appendChild(s);
        }
      }
      function clear(f) {
        var p = f.closest('.f');
        p.classList.remove('is-bad'); f.removeAttribute('aria-invalid');
        var e = p.querySelector('.err'); if (e) e.remove();
      }
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var name = $('#fName'), mail = $('#fMail'), first = null;
        [name, mail].forEach(clear);
        if (!name.value.trim()) { bad(name, 'We need a name to reply to.'); first = first || name; }
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(mail.value.trim())) {
          bad(mail, 'That email does not look right.'); first = first || mail;
        }
        if (first) { first.focus(); return; }
        ok.hidden = false;
        ok.textContent = 'Thank you, ' + name.value.trim().split(' ')[0] +
          '. This is a concept site, so nothing was actually sent \u2014 on the real one the estate ' +
          'office would answer within two working days.';
        form.querySelector('.form__foot').hidden = true;
        ok.scrollIntoView({ block: 'nearest', behavior: reduce ? 'auto' : 'smooth' });
      });
      [$('#fName'), $('#fMail')].forEach(function (f) {
        f.addEventListener('input', function () { if (f.closest('.f').classList.contains('is-bad')) clear(f); });
      });
    })();
  }

  /* ── in-page anchors ──────────────────────────────────────── */
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a || a.classList.contains('skip')) return;
    var id = a.getAttribute('href').slice(1); if (!id) return;
    var t = document.getElementById(id); if (!t) return;
    e.preventDefault();
    var top = t.getBoundingClientRect().top + scrollY -
      (parseInt(getComputedStyle(document.documentElement).getPropertyValue('--bar-h')) + 20);
    scrollTo({ top: Math.max(0, top), behavior: reduce ? 'auto' : 'smooth' });
    if (history.replaceState) history.replaceState(null, '', '#' + id);
    if (!t.hasAttribute('tabindex')) t.setAttribute('tabindex', '-1');
    setTimeout(function () { t.focus({ preventScroll: true }); }, reduce ? 0 : 520);
  });

  kick();
})();
