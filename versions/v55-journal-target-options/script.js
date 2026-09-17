/* AC-MOT interactive presentation engine.
   No external libraries — works offline. Charts are drawn as SVG from
   assets/data/results.js so every number has one source. */
(function () {
  'use strict';
  var W = 1600, H = 900;
  var stage = document.getElementById('stage');
  var slides = Array.prototype.slice.call(stage.querySelectorAll('.slide'));
  var N = slides.length;
  var D = window.ACMOT || {};
  var CUE = window.CUE_EXAMPLES || {};
  var cur = -1;

  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }

  /* ------------------------------------------------ scale to screen */
  function fit() {
    var s = Math.min(window.innerWidth / W, window.innerHeight / H);
    stage.style.transform = 'translate(-50%,-50%) scale(' + s + ')';
  }
  window.addEventListener('resize', fit);
  fit();

  /* ------------------------------------------------ data binding */
  function resolve(path) {
    var root = D, p = path;
    if (p.indexOf('CUE.') === 0) { root = CUE; p = p.slice(4); }
    return p.split('.').reduce(function (o, k) { return o == null ? undefined : o[k]; }, root);
  }
  function bindAll(root) {
    $$('[data-bind]', root).forEach(function (e) {
      var v = resolve(e.getAttribute('data-bind'));
      if (v == null) return;
      if (typeof v === 'number') {
        var d = e.getAttribute('data-dec');
        if (e.hasAttribute('data-k')) v = v.toLocaleString('en-US', { maximumFractionDigits: d == null ? 0 : +d, minimumFractionDigits: d == null ? 0 : +d });
        else if (d !== null) v = v.toFixed(+d);
      }
      e.textContent = (e.getAttribute('data-pre') || '') + v + (e.getAttribute('data-suf') || '');
    });
  }
  /* ------------------------------------------------ v5: big "main idea" box at the top of every content slide
     (same style as the metric slides; the old bottom strip is gone) */
  var MEAN = window.MEANING || {};
  slides.forEach(function (s) {
    var d = MEAN[s.getAttribute('data-title')], body = $('.s-body', s);
    if (!d || !body || $('.meaning', body)) return;
    var inner = document.createElement('div');
    inner.className = (body.className.replace(/\bs-body\b/, '') + ' grow').trim();
    if (body.getAttribute('style')) inner.setAttribute('style', body.getAttribute('style'));
    if (body.hasAttribute('data-tabs')) { inner.setAttribute('data-tabs', ''); body.removeAttribute('data-tabs'); }
    while (body.firstChild) inner.appendChild(body.firstChild);
    if (d.r && inner.firstElementChild) inner.removeChild(inner.firstElementChild);
    var m = document.createElement('div'); m.className = 'meaning';
    m.innerHTML = '<div class="tag">' + (d.tag || 'The main idea') + '</div><p>' + d.t + '</p>';
    body.className = 's-body col'; body.removeAttribute('style');
    body.appendChild(m); body.appendChild(inner);
  });
  bindAll(document);

  /* ------------------------------------------------ v4: write the full name next to each abbreviation
     (first time it appears on a slide; sentences first; never in titles, formulas, code or charts;
     skipped when the slide already spells the full name) */
  var ABBR = [
    ['AC-MOT', 'Adaptive Control for Multi-Object Tracking'],
    ['MOTA', 'Multiple Object Tracking Accuracy'],
    ['MOT', 'Multi-Object Tracking'],
    ['IDF1', 'Identity F1 score'],
    ['IDS', 'identity switches'],
    ['HOTA', 'Higher Order Tracking Accuracy', 'HOTA\\*?'],
    ['DetA', 'Detection Accuracy'],
    ['AssA', 'Association Accuracy'],
    ['FPS', 'frames per second'],
    ['IoU', 'Intersection over Union'],
    ['NMS', 'Non-Maximum Suppression'],
    ['TP', 'true positive'],
    ['FP', 'false positive'],
    ['FN', 'false negative'],
    ['TN', 'true negative'],
    ['mAP', 'mean Average Precision'],
    ['AP', 'Average Precision'],
    ['GT', 'ground truth'],
    ['SCI', 'Scene Complexity Index'],
    ['ReID', 're-identification'],
    ['TPE', 'Tree-structured Parzen Estimator'],
    ['GPU', 'graphics processing unit'],
    ['CPU', 'central processing unit'],
    ['YOLO', 'You Only Look Once'],
    ['SSD', 'Single Shot Detector'],
    ['R-CNN', 'Region-based Convolutional Neural Network'],
    ['RT-DETR', 'Real-Time DEtection TRansformer'],
    ['DETR', 'DEtection TRansformer'],
    ['OC-SORT', 'Observation-Centric SORT'],
    ['BoT-SORT', 'Bag of Tricks SORT'],
    ['SORT', 'Simple Online and Realtime Tracking'],
    ['JDE', 'Joint Detection and Embedding'],
    ['COCO', 'Common Objects in Context'],
    ['UAVDT', 'UAV Detection and Tracking benchmark'],
    ['UAV', 'unmanned aerial vehicle, a drone'],
    ['FP16', '16-bit floating point'],
    ['CMC', 'camera motion compensation'],
    ['ICCV', 'International Conference on Computer Vision'],
    ['ECCV', 'European Conference on Computer Vision']
  ].map(function (a) {
    var src = a[2] || a[0].replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    return { re: new RegExp('(?<![\\w-])' + src + '(?![\\w-])'), full: a[1] };
  });
  var ABBR_SKIP = 'svg,.code,.formula,.s-foot,.notes,.s-head,h1,.qmark,.dv-num,.tabs,.lbl,.kpi .v,.big,.cap,[data-bind],.abbr-x,.prov,.newtag,.adapt,.lock,#u2setup,.ol-card .n,.ol-ppt,.tbl th,.noabbr,.node small';
  var ABBR_PROSE = 'p,li,.callout,.note,.lead';
  function expandAbbr(s) {
    var text = s.textContent.toLowerCase();
    var done = ABBR.map(function (a) { return text.indexOf(a.full.toLowerCase()) > -1; });
    [true, false].forEach(function (prosePass) {
      var w = document.createTreeWalker(s, NodeFilter.SHOW_TEXT), list = [];
      while (w.nextNode()) list.push(w.currentNode);
      list.forEach(function (tn) {
        var el = tn.parentElement;
        if (!el || el.closest(ABBR_SKIP) || !!el.closest(ABBR_PROSE) !== prosePass) return;
        var node = tn;
        while (node) {
          var best = null;
          for (var i = 0; i < ABBR.length; i++) {
            if (done[i]) continue;
            var m = ABBR[i].re.exec(node.nodeValue);
            if (!m) continue;
            if (m.index + m[0].length === node.nodeValue.length && node.nextSibling && node.nextSibling.nodeName === 'SUB') continue;
            /* inside brackets with other words, e.g. "(37.0 vs 37.3 mAP)": skip, use a later mention */
            var pre = node.nodeValue.slice(0, m.index), opens = (pre.match(/\(/g) || []).length - (pre.match(/\)/g) || []).length;
            var exact = pre.charAt(pre.length - 1) === '(' && node.nodeValue.charAt(m.index + m[0].length) === ')';
            if (opens > 0 && !exact) continue;
            if (!best || m.index < best.m.index) best = { i: i, m: m };
          }
          if (!best) break;
          done[best.i] = true;
          var v = node.nodeValue, st = best.m.index, en = st + best.m[0].length;
          var inParens = v.charAt(st - 1) === '(' && v.charAt(en) === ')';
          var after = node.splitText(en);
          var sp = document.createElement('span');
          sp.className = 'abbr-x'; sp.textContent = inParens ? ' = ' + ABBR[best.i].full : ' (' + ABBR[best.i].full + ')';
          node.parentNode.insertBefore(sp, after);
          node = after;
        }
      });
    });
  }
  slides.forEach(expandAbbr);

  /* ------------------------------------------------ footers */
  var EX = {};
  slides.forEach(function (s, i) {
    var f = $('.s-foot', s);
    if (!f) { f = document.createElement('footer'); f.className = 's-foot'; s.appendChild(f); }
    (s.getAttribute('data-explain') || '').split(';').forEach(function (item) {
      if (!item) return;
      var p = item.split('|'), b = document.createElement('button');
      b.type = 'button'; b.className = 'xbtn'; b.setAttribute('data-x', p[0]);
      b.title = 'Open a detailed explanation (Esc returns to this slide)';
      b.innerHTML = '<span class="xi">?</span>' + p[1];
      f.appendChild(b);
    });
    var n = document.createElement('span'); n.className = 'num'; n.textContent = (i + 1) + ' / ' + N;
    f.appendChild(n);
  });

  /* ------------------------------------------------ UI chrome */
  var ICON = {
    prev: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M15 5l-7 7 7 7"/></svg>',
    next: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M9 5l7 7-7 7"/></svg>',
    grid: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>',
    notes: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M5 4h14v16H5z"/><path d="M8 9h8M8 13h8M8 17h5"/></svg>',
    full: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg>',
    menu: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h10"/></svg>',
    help: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1 .8-1 1.5v.4M12 17h.01"/></svg>'
  };
  var ui = document.createElement('div');
  ui.className = 'ui';
  ui.innerHTML =
    '<div class="progress"><i></i></div>' +
    '<div class="bar">' +
      '<span class="secname"></span>' +
      '<button data-act="prev" title="Previous (←)" aria-label="Previous slide">' + ICON.prev + '</button>' +
      '<span class="count">1 / ' + N + '</span>' +
      '<button data-act="next" title="Next (→ or Space)" aria-label="Next slide">' + ICON.next + '</button>' +
      '<button data-act="menu" title="Go to a section (S)" aria-label="Sections">' + ICON.menu + '</button>' +
      '<button data-act="overview" title="Slide navigator (O)" aria-label="Slide navigator">' + ICON.grid + '</button>' +
      '<button data-act="notes" title="Speaker notes (N)" aria-label="Speaker notes">' + ICON.notes + '</button>' +
      '<button class="present-btn" data-act="full" title="Presentation mode: full screen (F or P)" aria-label="Presentation mode">' + ICON.full + '<span>Present</span></button>' +
      '<button data-act="help" title="Keyboard help (H)" aria-label="Help">' + ICON.help + '</button>' +
    '</div>';
  document.body.appendChild(ui);
  var barEl = $('.bar', ui), countEl = $('.count', ui), secEl = $('.secname', ui), progEl = $('.progress i', ui);

  var ov = document.createElement('div'); ov.className = 'overlay overview';
  ov.innerHTML = '<div class="ov-panel"><h2>Slide navigator</h2><div class="muted" style="font-size:15px">Click a slide to jump. Press O or Esc to close.</div><div class="ov-body"></div></div>';
  document.body.appendChild(ov);

  var secmenu = document.createElement('div'); secmenu.className = 'overlay secmenu';
  secmenu.innerHTML = '<div class="ov-panel sec-panel"><h2>Sections</h2>' +
    '<div class="muted" style="font-size:15px">Click a section to jump there. Press S or Esc to close.</div>' +
    '<div class="sec-list"></div></div>';
  document.body.appendChild(secmenu);
  (function buildSecMenu() {
    var list = $('.sec-list', secmenu);
    slides.forEach(function (s, i) {
      if (!/^sec-\d+$/.test(s.id || '')) return;
      var name = s.getAttribute('data-secname') || s.getAttribute('data-title') || 'Section';
      var num = (name.split('\u00b7')[0] || '').trim();
      var rest = name.indexOf('\u00b7') > -1 ? name.split('\u00b7').slice(1).join('\u00b7').trim() : name;
      var head = $('h1', s);
      var col = getComputedStyle(s).getPropertyValue('--sec').trim() || '#4F46E5';
      var b = document.createElement('button');
      b.className = 'sec-item';
      b.setAttribute('data-slide', i);
      b.innerHTML = '<span class="sn" style="color:' + col + '">' + num + '</span>' +
        '<span class="st"><b>' + (head ? head.textContent : rest) + '</b>' +
        '<i>' + rest + ' \u00b7 slide ' + (i + 1) + '</i></span>';
      b.addEventListener('click', function () { closeOverlays(); go(i); });
      list.appendChild(b);
    });
  })();

  /* v21: a button on every slide that returns to the Outline slide */
  var outlineIdx = -1;
  slides.forEach(function (s, i) { if (outlineIdx < 0 && (s.getAttribute('data-title') || '') === 'Outline') outlineIdx = i; });
  var toOutline = document.createElement('button');
  toOutline.className = 'to-outline';
  toOutline.type = 'button';
  toOutline.title = 'Back to the outline (M)';
  toOutline.setAttribute('aria-label', 'Back to the outline');
  toOutline.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h10"/></svg><span>Outline</span>';
  toOutline.addEventListener('click', function () { closeOverlays(); if (outlineIdx >= 0) go(outlineIdx); });
  /* v24: previous / next slide buttons beside the Outline button */
  var topNav = document.createElement('div'); topNav.className = 'top-nav';
  var toPrev = document.createElement('button'); toPrev.type = 'button'; toPrev.className = 'nav-btn to-prev';
  toPrev.title = 'Previous slide'; toPrev.setAttribute('aria-label', 'Previous slide');
  toPrev.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg>';
  var toNext = document.createElement('button'); toNext.type = 'button'; toNext.className = 'nav-btn to-next';
  toNext.title = 'Next slide'; toNext.setAttribute('aria-label', 'Next slide');
  toNext.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg>';
  toPrev.addEventListener('click', function () { closeOverlays(); if (cur > 0) go(cur - 1); });
  toNext.addEventListener('click', function () { closeOverlays(); if (cur < N - 1) go(cur + 1); });
  topNav.appendChild(toPrev);
  if (outlineIdx >= 0) topNav.appendChild(toOutline);
  topNav.appendChild(toNext);
  stage.appendChild(topNav);

  var help = document.createElement('div'); help.className = 'overlay help';
  help.innerHTML = '<div class="help-box"><h2 style="margin:0 0 12px">Keyboard controls</h2><table>' +
    '<tr><td><kbd>→</kbd> <kbd>Space</kbd> <kbd>PgDn</kbd></td><td>Next step / next slide</td></tr>' +
    '<tr><td><kbd>←</kbd> <kbd>PgUp</kbd></td><td>Previous step / previous slide</td></tr>' +
    '<tr><td><kbd>Home</kbd> / <kbd>End</kbd></td><td>First / last slide</td></tr>' +
    '<tr><td><kbd>F</kbd> <kbd>P</kbd></td><td>Full-screen presentation mode (like PowerPoint)</td></tr>' +
    '<tr><td><kbd>M</kbd></td><td>Back to the outline slide</td></tr>' +
    '<tr><td><kbd>S</kbd></td><td>Sections menu - jump to any section</td></tr>' +
    '<tr><td><kbd>O</kbd></td><td>Slide navigator (overview)</td></tr>' +
    '<tr><td><kbd>N</kbd></td><td>Show / hide speaker notes</td></tr>' +
    '<tr><td><kbd>H</kbd> <kbd>?</kbd></td><td>This help</td></tr>' +
    '<tr><td><kbd>Esc</kbd></td><td>Close any panel</td></tr>' +
    '<tr><td>Mouse</td><td>Hover dotted terms for definitions · click images and diagrams to enlarge</td></tr>' +
    '</table></div>';
  document.body.appendChild(help);

  var lb = document.createElement('div'); lb.className = 'overlay lightbox';
  lb.innerHTML = '<button class="lb-close" aria-label="Close">×</button><div class="lb-inner"></div>';
  document.body.appendChild(lb);

  var ex = document.createElement('div'); ex.className = 'overlay explain';
  ex.innerHTML = '<div class="ex-box" role="dialog" aria-label="Explain this slide"></div>';
  document.body.appendChild(ex);
  var exBox = $('.ex-box', ex);

  var notesPanel = document.createElement('div'); notesPanel.className = 'notes-panel';
  notesPanel.innerHTML = '<h4>Speaker notes</h4><div class="nb"></div>';
  document.body.appendChild(notesPanel);
  var notesBody = $('.nb', notesPanel);

  var tip = document.createElement('div'); tip.className = 'tip'; document.body.appendChild(tip);

  /* overview contents */
  (function buildOverview() {
    var body = $('.ov-body', ov), lastSec = null, grid = null;
    slides.forEach(function (s, i) {
      var sec = s.getAttribute('data-secname') || '';
      if (sec !== lastSec) {
        var wrap = document.createElement('div'); wrap.className = 'ov-sec';
        var col = getComputedStyle(s).getPropertyValue('--sec') || '#4F46E5';
        wrap.innerHTML = '<h4 style="color:' + col + '">' + sec + '</h4><div class="ov-grid"></div>';
        body.appendChild(wrap); grid = $('.ov-grid', wrap); lastSec = sec;
      }
      var t = s.getAttribute('data-title') || ($('h2', s) || $('h1', s) || { textContent: 'Slide' }).textContent;
      var b = document.createElement('button'); b.innerHTML = '<b>' + (i + 1) + '</b><span>' + t + '</span>';
      b.addEventListener('click', function () { closeOverlays(); go(i); });
      grid.appendChild(b);
    });
  })();

  /* ------------------------------------------------ navigation */
  function frags(s) { return $$('.frag', s); }
  function setStep(s, k) {
    frags(s).forEach(function (e, j) { e.classList.toggle('on', j < k); });
    s.setAttribute('data-step', k);
  }
  function go(i, atEnd) {
    i = Math.max(0, Math.min(N - 1, i));
    var old = slides[cur];
    if (old && i !== cur) { old.classList.remove('active'); leave(old); }
    slides.forEach(function (s, j) { s.classList.toggle('past', j < i); });
    var changed = i !== cur;
    cur = i;
    var s = slides[i];
    setStep(s, atEnd ? frags(s).length : 0);
    s.classList.add('active');
    if (changed) enter(s);
    update();
  }
  function next() {
    var s = slides[cur], k = +s.getAttribute('data-step') || 0, f = frags(s);
    if (k < f.length) { setStep(s, k + 1); return; }
    if (cur < N - 1) go(cur + 1);
  }
  function prev() {
    var s = slides[cur], k = +s.getAttribute('data-step') || 0;
    if (k > 0) { setStep(s, k - 1); return; }
    if (cur > 0) go(cur - 1, true);
  }
  function update() {
    var s = slides[cur];
    countEl.textContent = (cur + 1) + ' / ' + N;
    secEl.textContent = s.getAttribute('data-secname') || '';
    var col = getComputedStyle(s).getPropertyValue('--sec').trim() || '#4F46E5';
    document.documentElement.style.setProperty('--pbar', col);
    progEl.style.width = (100 * (cur + 1) / N) + '%';
    $$('.ov-grid button', ov).forEach(function (b, j) { b.classList.toggle('cur', j === cur); });
    toOutline.hidden = (cur === outlineIdx);
    toPrev.disabled = (cur === 0); toNext.disabled = (cur === N - 1);
    var items = $$('.sec-item', secmenu), at = -1;
    items.forEach(function (b, k) { if (+b.getAttribute('data-slide') <= cur) at = k; });
    items.forEach(function (b, k) { b.classList.toggle('cur', k === at); });
  }
  function loadMedia(s) {
    if (!s) return;
    $$('[data-src]', s).forEach(function (m) {
      if (m.tagName === 'IMG') m.loading = 'lazy';
      m.src = m.getAttribute('data-src');
      m.removeAttribute('data-src');
    });
  }
  var nextMediaTimer = 0;
  function enter(s) {
    if (nextMediaTimer) clearTimeout(nextMediaTimer);
    loadMedia(s);
    /* Keep the first view light. Prefetch only after the current slide settles. */
    nextMediaTimer = setTimeout(function () {
      if (slides[cur + 1]) loadMedia(slides[cur + 1]);
    }, 1400);
    $$('[data-chart]', s).forEach(drawChart);
    $$('video[data-autoplay]', s).forEach(function (v) {
      if (v.closest('[hidden]')) return;
      var p = v.play(); if (p && p.catch) p.catch(function () {});
    });
    var n = $('.notes', s);
    notesBody.innerHTML = n ? n.innerHTML : '<p>No notes for this slide.</p>';
    if (history.replaceState) history.replaceState(null, '', '#' + (cur + 1));
  }
  function leave(s) {
    $$('video', s).forEach(function (v) { v.pause(); });
    hideTip(true);
  }

  /* ------------------------------------------------ overlays */
  function overlayOpen() { return !!$('.overlay.open') || notesPanel.classList.contains('open'); }
  function closeOverlays() {
    $$('.overlay.open').forEach(function (o) { o.classList.remove('open'); });
    $('.lb-inner', lb).innerHTML = '';
    hideTip(true);
  }
  function toggleSecMenu() { var o = secmenu.classList.contains('open'); closeOverlays(); if (!o) secmenu.classList.add('open'); }
  function toggleOverview() { var o = ov.classList.contains('open'); closeOverlays(); if (!o) ov.classList.add('open'); }
  function toggleHelp() { var o = help.classList.contains('open'); closeOverlays(); if (!o) help.classList.add('open'); }
  function toggleNotes() { notesPanel.classList.toggle('open'); }
  var KIND = { toy: 'Made-up numbers — only to explain the idea', real: 'Real numbers from this thesis', pub: 'Published numbers', none: 'Idea only — no numbers' };
  function openExplain() {
    var s = slides[cur], t = s.getAttribute('data-title'), d = EX[t];
    if (!d) return;
    closeOverlays();
    var h = $('.s-head h2', s) || $('h1', s);
    exBox.innerHTML = '<button class="ex-close" aria-label="Close">×</button>' +
      '<div class="ex-kicker">Slide ' + (cur + 1) + ' · explained simply</div>' +
      '<h2>' + (h ? h.textContent : t) + '</h2>' +
      '<div class="ex-simple"><h3>In simple words</h3>' + d.simple + '</div>' +
      '<div class="ex-example"><h3>Simple example <span class="ex-kind ' + (d.kind || 'none') + '">' + (KIND[d.kind] || KIND.none) + '</span></h3>' + d.example + '</div>' +
      (d.remember ? '<div class="ex-remember"><b>Remember:</b> ' + d.remember + '</div>' : '') +
      '<div class="ex-hint">Press E or Esc to close.</div>';
    bindAll(exBox);
    ex.classList.add('open');
    exBox.scrollTop = 0;
  }
  function toggleExplain() { if (ex.classList.contains('open')) closeOverlays(); else openExplain(); }
  function toggleFull() {
    var d = document;
    if (!d.fullscreenElement && !d.webkitFullscreenElement) {
      var el = d.documentElement; (el.requestFullscreen || el.webkitRequestFullscreen).call(el);
    } else { (d.exitFullscreen || d.webkitExitFullscreen).call(d); }
  }
  /* v7: presentation mode = full screen that looks like PowerPoint (black letterbox, no page chrome) */
  function syncPresent() {
    var on = !!(document.fullscreenElement || document.webkitFullscreenElement);
    document.body.classList.toggle('present', on);
    fit();
  }
  document.addEventListener('fullscreenchange', syncPresent);
  document.addEventListener('webkitfullscreenchange', syncPresent);
  var startBtn = document.createElement('button');
  startBtn.type = 'button'; startBtn.className = 'start-present';
  startBtn.innerHTML = '▶ Start full-screen presentation';
  startBtn.title = 'Presentation mode (F or P) · Esc leaves full screen';
  startBtn.addEventListener('click', toggleFull);
  document.body.appendChild(startBtn);
  var idleT = null;
  document.addEventListener('mousemove', function () {
    document.body.classList.remove('idle'); clearTimeout(idleT);
    idleT = setTimeout(function () { document.body.classList.add('idle'); }, 2500);
  });
  [ov, help, lb, ex].forEach(function (o) {
    o.addEventListener('click', function (e) {
      if (e.target === o || e.target.classList.contains('lb-close') || e.target.classList.contains('ex-close')) closeOverlays();
    });
  });

  barEl.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    var a = b.getAttribute('data-act');
    if (a === 'prev') prev(); else if (a === 'next') next();
    else if (a === 'overview') toggleOverview(); else if (a === 'menu') toggleSecMenu(); else if (a === 'notes') toggleNotes();
    else if (a === 'full') toggleFull(); else if (a === 'help') toggleHelp();
    else if (a === 'explain') toggleExplain();
  });

  document.addEventListener('keydown', function (e) {
    if (e.target.closest && e.target.closest('input,textarea,select')) return;
    var k = e.key;
    if (k === 'Escape') { closeOverlays(); notesPanel.classList.remove('open'); return; }
    if ($('.overlay.open')) return;
    if (k === 'ArrowRight' || k === 'PageDown' || k === ' ' || k === 'ArrowDown') { e.preventDefault(); next(); }
    else if (k === 'ArrowLeft' || k === 'PageUp' || k === 'ArrowUp' || k === 'Backspace') { e.preventDefault(); prev(); }
    else if (k === 'Home') { go(0); } else if (k === 'End') { go(N - 1, true); }
    else if (k === 'f' || k === 'F' || k === 'p' || k === 'P') toggleFull();
    else if (k === 'o' || k === 'O') toggleOverview();
    else if (k === 's' || k === 'S') toggleSecMenu();
    else if (k === 'm' || k === 'M') { closeOverlays(); if (outlineIdx >= 0) go(outlineIdx); }
    else if (k === 'n' || k === 'N') toggleNotes();
    else if (k === 'h' || k === 'H' || k === '?') toggleHelp();
  });

  var tx = null;
  stage.addEventListener('touchstart', function (e) { tx = e.touches[0].clientX; }, { passive: true });
  stage.addEventListener('touchend', function (e) {
    if (tx == null) return; var dx = e.changedTouches[0].clientX - tx; tx = null;
    if (Math.abs(dx) > 50) { if (dx < 0) next(); else prev(); }
  });
  var hideT = null;
  document.addEventListener('mousemove', function () {
    barEl.classList.add('show'); clearTimeout(hideT); hideT = setTimeout(function () { barEl.classList.remove('show'); }, 2200);
  });

  /* jump links */
  stage.addEventListener('click', function (e) {
    var xb = e.target.closest('.xbtn');
    if (xb) { openX(xb.getAttribute('data-x').split('#')[0], 0); return; }  /* always start at part 1 */
    if (e.target.closest('.ex-btn')) { openExplain(); return; }
    var g = e.target.closest('[data-goto]');
    if (g) { var t = document.getElementById(g.getAttribute('data-goto')); if (t) go(slides.indexOf(t)); return; }
    var z = e.target.closest('.zoomable');
    if (z) openZoom(z);
  });

  /* tabs (video switcher etc.) */
  $$('[data-tabs]').forEach(function (box) {
    var btns = $$('[data-tab]', box), panes = $$('[data-pane]', box);
    btns.forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation();
        var key = b.getAttribute('data-tab');
        btns.forEach(function (x) { x.classList.toggle('on', x === b); });
        panes.forEach(function (p) {
          var on = p.getAttribute('data-pane') === key;
          p.hidden = !on;
          $$('video', p).forEach(function (v) { if (on) { var pr = v.play(); if (pr && pr.catch) pr.catch(function () {}); } else v.pause(); });
        });
      });
    });
  });

  /* lightbox */
  /* v30: a chart is redrawn at full lightbox size - its own layout, no stretching - and animates again */
  function openChartZoom(src, inner) {
    var r = Math.min(0.9, Math.max(0.5, (src.clientHeight || 1) / (src.clientWidth || 1)));
    var w = Math.min(window.innerWidth * 0.9, 1500, window.innerHeight * 0.82 / r), hgt = w * r;
    var host = document.createElement('div');
    host.className = 'chart zoomed';
    host.setAttribute('data-chart', src.getAttribute('data-chart'));
    if (src.getAttribute('aria-label')) host.setAttribute('aria-label', src.getAttribute('aria-label'));
    host.style.width = Math.round(w) + 'px'; host.style.height = Math.round(hgt) + 'px';
    host.title = 'Click the chart to play the animation again';
    inner.appendChild(host);
    lb.classList.add('open');
    requestAnimationFrame(function () { if (host.isConnected && lb.classList.contains('open')) drawChart(host); });  /* closed before the first frame: draw nothing */
    host.addEventListener('click', function (e) {
      e.stopPropagation();
      host.classList.remove('play'); void host.getBoundingClientRect();
      requestAnimationFrame(function () { requestAnimationFrame(function () { host.classList.add('play'); }); });
    });
  }
  function openZoom(z) {
    var inner = $('.lb-inner', lb); inner.innerHTML = '';
    var media = z.matches('img,video') ? z : $('img,video', z);
    var chartEl = z.matches('[data-chart]') ? z : (media ? null : $('[data-chart]', z));
    if (chartEl) { openChartZoom(chartEl, inner); return; }
    if (media && !$('svg', z)) {
      var c = media.cloneNode(true); c.removeAttribute('style');
      if (c.tagName === 'VIDEO') { c.controls = true; c.muted = true; c.autoplay = true; }
      inner.appendChild(c);
    } else {
      var w = z.offsetWidth, h = z.offsetHeight;
      var sc = Math.min(window.innerWidth * 0.9 / w, window.innerHeight * 0.86 / h);
      var holder = document.createElement('div');
      holder.style.width = (w * sc) + 'px'; holder.style.height = (h * sc) + 'px'; holder.style.overflow = 'hidden';
      var clone = z.cloneNode(true);
      clone.classList.remove('zoomable');
      clone.style.width = w + 'px'; clone.style.height = h + 'px';
      clone.style.transform = 'scale(' + sc + ')'; clone.style.transformOrigin = '0 0';
      $$('.frag', clone).forEach(function (f) { f.classList.add('on'); });
      $$('.chart', clone).forEach(function (c) { c.classList.add('play'); });
      if (clone.classList.contains('chart')) clone.classList.add('play');
      holder.appendChild(clone); inner.appendChild(holder);
    }
    lb.classList.add('open');
  }

  /* tooltips + click definitions */
  var pinned = null;
  function showTip(el, pin) {
    var html = el.getAttribute('data-tip') || el.getAttribute('data-def');
    if (!html) return;
    tip.innerHTML = html; tip.classList.add('show'); tip.classList.toggle('pinned', !!pin);
    var r = el.getBoundingClientRect(), tw = tip.offsetWidth, th = tip.offsetHeight;
    var x = Math.min(window.innerWidth - tw - 10, Math.max(10, r.left + r.width / 2 - tw / 2));
    var y = r.top - th - 10; if (y < 10) y = r.bottom + 10;
    tip.style.left = x + 'px'; tip.style.top = y + 'px';
  }
  function hideTip(force) { if (pinned && !force) return; pinned = null; tip.classList.remove('show', 'pinned'); }
  document.addEventListener('mouseover', function (e) { var t = e.target.closest && e.target.closest('[data-tip]'); if (t && !pinned) showTip(t); });
  document.addEventListener('mouseout', function (e) { var t = e.target.closest && e.target.closest('[data-tip]'); if (t && !pinned) hideTip(); });
  document.addEventListener('click', function (e) {
    var d = e.target.closest && e.target.closest('[data-def]');
    if (d) { e.stopPropagation(); if (pinned === d) { hideTip(true); } else { pinned = d; showTip(d, true); } return; }
    if (pinned && !e.target.closest('.tip')) hideTip(true);
  }, true);

  /* ================================================ SVG charts */
  var NS = 'http://www.w3.org/2000/svg';
  var COL = { base: '#94A3B8', old: '#0EA5E9', full: '#4F46E5', match: '#F59E0B', v1: '#7C3AED', v2: '#0D9488',
              u2: '#E11D48', a0: '#94A3B8', a1: '#60A5FA', a2: '#818CF8', a3: '#4F46E5', a4: '#C4B5FD',
              crowd: '#2563EB', tiny: '#F59E0B', edge: '#7C3AED', night: '#0F766E', blur: '#E11D48' };
  function E(tag, at, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in at) if (at[k] != null) e.setAttribute(k, at[k]);
    if (parent) parent.appendChild(e); return e;
  }
  function T(parent, x, y, s, cls, at) { var e = E('text', Object.assign({ x: x, y: y, 'class': cls || '' }, at || {}), parent); e.textContent = s; return e; }
  function frame(h) {
    h.innerHTML = '';
    var w = Math.max(240, h.clientWidth), hh = Math.max(160, h.clientHeight);
    var s = E('svg', { viewBox: '0 0 ' + w + ' ' + hh, width: '100%', height: '100%', 'class': 'cs', role: 'img' }, h);
    if (h.getAttribute('aria-label')) s.setAttribute('aria-label', h.getAttribute('aria-label'));
    return { s: s, w: w, h: hh };
  }
  function niceStep(raw) { var e = Math.pow(10, Math.floor(Math.log10(raw))), m = raw / e; return (m <= 1 ? 1 : m <= 2 ? 2 : m <= 2.5 ? 2.5 : m <= 5 ? 5 : 10) * e; }
  function niceMax(v, n) { var st = niceStep(v / (n || 5)); return Math.ceil(v / st) * st; }
  function ticks(min, max, n) { var st = niceStep((max - min) / (n || 5)), a = [], t = Math.ceil(min / st - 1e-9) * st; for (; t <= max + st * 1e-6; t += st) a.push(+t.toFixed(10)); return a; }
  function fm(v, d) {
    if (v == null || isNaN(v)) return '';
    if (Math.abs(v) >= 10000) return Number(v).toLocaleString('en-US', { maximumFractionDigits: d || 0 });
    return (d == null ? String(v) : Number(v).toFixed(d)).replace(/^-/, '\u2212');  /* v30: a real minus sign */
  }
  function badge(s, w, better) {
    if (!better) return;
    var lo = better === 'lower', lab = lo ? '↓ lower is better' : '↑ higher is better', tw = lab.length * 9.4 + 28;
    var g = E('g', { 'class': 'cbadge ' + (lo ? 'lo' : 'hi') }, s);
    E('rect', { x: w - tw - 2, y: 2, width: tw, height: 32, rx: 16 }, g);
    T(g, w - tw / 2 - 2, 23.5, lab, '', { 'text-anchor': 'middle' });
  }
  function multi(parent, x, y, label, cls, anchor, lh) {
    String(label).split('\n').forEach(function (p, i) { T(parent, x, y + i * (lh || 22), p, cls, { 'text-anchor': anchor || 'middle' }); });
  }

  function bars(h, o) {
    var F = frame(h), s = F.s, w = F.w, hh = F.h;
    if (o.title) T(s, 2, 21, o.title, 'ctitle');
    badge(s, w, o.better);
    var tickW = String(fm(o.max || niceMax(Math.max.apply(null, o.values.concat(o.ref ? [o.ref.v] : [])) * 1.14, 5), o.tdec)).length * 12;  /* v30: room for 4-digit ticks next to the axis title */
    var m = { l: Math.max(o.ml || 66, o.ylabel ? tickW + 44 : 0), r: 14, t: (o.title || o.better) ? (o.ref && !o.title ? 84 : 60) : 24, b: o.mb || 66 };
    var iw = w - m.l - m.r, ih = hh - m.t - m.b;
    var vmax = o.max || niceMax(Math.max.apply(null, o.values.concat(o.ref ? [o.ref.v] : [])) * 1.14, 5);
    ticks(0, vmax, o.nt || (ih < 80 ? 1 : ih < 130 ? 2 : 4)).forEach(function (t) {  /* v30: fewer ticks on short charts */
      var y = m.t + ih - ih * t / vmax;
      E('line', { x1: m.l, x2: w - m.r, y1: y, y2: y, 'class': 'cgrid' }, s);
      if (!(o.ref && Math.abs(t - o.ref.v) * ih / vmax < 26)) T(s, m.l - 9, y + 5, fm(t, o.tdec), 'ctick', { 'text-anchor': 'end' });  /* v30: no tick on top of the reference label */
    });
    if (o.ylabel) T(s, 14, m.t + ih / 2, o.ylabel, 'caxis', { transform: 'rotate(-90 14 ' + (m.t + ih / 2) + ')', 'text-anchor': 'middle' });
    E('line', { x1: m.l, x2: w - m.r, y1: m.t + ih, y2: m.t + ih, 'class': 'cbase' }, s);
    var n = o.values.length, slot = iw / n, bw = Math.min(o.bw || 92, slot * 0.62);
    o.values.forEach(function (v, i) {
      var cx = m.l + slot * (i + 0.5), bh = Math.max(0, ih * v / vmax), y = m.t + ih - bh;
      E('rect', { x: cx - bw / 2, y: y, width: bw, height: bh, rx: 6, fill: (o.colors && o.colors[i]) || o.color || '#4F46E5',
        'class': 'bar' + (o.hl === i ? ' hl' : ''), style: 'transition-delay:' + (i * 70) + 'ms' }, s);
      T(s, cx, y - 9, o.vtext && o.vtext[i] ? o.vtext[i] : fm(v, o.dec) + (o.unit || ''), 'cval' + (n > 5 ? ' sm' : ''), { 'text-anchor': 'middle' });
      multi(s, cx, m.t + ih + 22, o.labels[i], 'clabel', 'middle', 22);
    });
    if (o.ref) {
      var ry = m.t + ih - ih * o.ref.v / vmax;
      E('line', { x1: m.l, x2: w - m.r, y1: ry, y2: ry, 'class': 'cref' }, s);
      T(s, m.l - 9, ry + 5, fm(o.ref.v), 'creft', { 'text-anchor': 'end' });
      if (!o.title) { var ly = o.better ? 54 : 16; E('line', { x1: 4, x2: 30, y1: ly, y2: ly, 'class': 'cref' }, s); T(s, 36, ly + 6, o.ref.label, 'creft'); }
    }
  }

  function grouped(h, o) {
    var F = frame(h), s = F.s, w = F.w, hh = F.h;
    if (o.title) T(s, 2, 21, o.title, 'ctitle');
    badge(s, w, o.better);
    var m = { l: o.ml || 62, r: 12, t: 82, b: o.mb || 52 };
    var iw = w - m.l - m.r, ih = hh - m.t - m.b, all = [];
    o.series.forEach(function (se) { se.values.forEach(function (v) { if (v != null) all.push(v); }); });
    var vmax = o.max || niceMax(Math.max.apply(null, all) * 1.14, 5);
    ticks(0, vmax, ih < 80 ? 1 : ih < 130 ? 2 : 4).forEach(function (t) {  /* v30: fewer ticks on short charts */
      var y = m.t + ih - ih * t / vmax;
      E('line', { x1: m.l, x2: w - m.r, y1: y, y2: y, 'class': 'cgrid' }, s);
      T(s, m.l - 9, y + 5, fm(t), 'ctick', { 'text-anchor': 'end' });
    });
    if (o.ylabel) T(s, 14, m.t + ih / 2, o.ylabel, 'caxis', { transform: 'rotate(-90 14 ' + (m.t + ih / 2) + ')', 'text-anchor': 'middle' });
    E('line', { x1: m.l, x2: w - m.r, y1: m.t + ih, y2: m.t + ih, 'class': 'cbase' }, s);
    var lx = m.l;
    o.series.forEach(function (se) {
      E('rect', { x: lx, y: 38, width: 16, height: 16, rx: 4, fill: se.color }, s);
      T(s, lx + 22, 52, se.name, 'clegend'); lx += 22 + se.name.length * 10.4 + 26;
    });
    var G = o.groups.length, S = o.series.length, slot = iw / G, gap = 6;
    var bw = Math.min(o.bw || 64, (slot * 0.84 - (S - 1) * gap) / S);
    o.groups.forEach(function (g, gi) {
      var gx = m.l + slot * (gi + 0.5), start = gx - (S * bw + (S - 1) * gap) / 2;
      o.series.forEach(function (se, si) {
        var v = se.values[gi]; if (v == null) return;
        var x = start + si * (bw + gap), bh = ih * v / vmax, y = m.t + ih - bh;
        E('rect', { x: x, y: y, width: bw, height: bh, rx: 5, fill: se.color, 'class': 'bar', style: 'transition-delay:' + (gi * 90 + si * 45) + 'ms' }, s);
        if (!o.novals) T(s, x + bw / 2, y - 7, fm(v, o.dec), 'cval sm', { 'text-anchor': 'middle' });
      });
      multi(s, gx, m.t + ih + 24, g, 'clabel', 'middle', 22);
    });
  }

  function hbars(h, o) {
    var F = frame(h), s = F.s, w = F.w, hh = F.h;
    if (o.title) T(s, 2, 21, o.title, 'ctitle');
    badge(s, w, o.better);
    var m = { l: o.ml || 136, r: o.mr || 108, t: (o.title || o.better) ? 44 : 10, b: o.xlabel ? 50 : 26 };
    var iw = w - m.l - m.r, ih = hh - m.t - m.b, n = o.values.length, slot = ih / n, bh = Math.min(o.bh || 30, slot * 0.68);
    var vmax = o.max || niceMax(Math.max.apply(null, o.values.concat(o.ref ? [o.ref.v] : [])) * 1.04, 5);
    ticks(0, vmax, 5).forEach(function (t) {
      var x = m.l + iw * t / vmax;
      E('line', { x1: x, x2: x, y1: m.t, y2: m.t + ih, 'class': 'cgrid' }, s);
      T(s, x, m.t + ih + 18, fm(t), 'ctick', { 'text-anchor': 'middle' });
    });
    if (o.xlabel) T(s, m.l + iw / 2, hh - 6, o.xlabel, 'caxis', { 'text-anchor': 'middle' });
    o.values.forEach(function (v, i) {
      var y = m.t + slot * (i + 0.5), bw = iw * v / vmax, hl = o.hl && o.labels[i] === o.hl;
      T(s, m.l - 10, y + 6, o.labels[i], 'clabel' + (hl ? ' strong' : ''), { 'text-anchor': 'end' });
      E('rect', { x: m.l, y: y - bh / 2, width: bw, height: bh, rx: 5, fill: hl ? (o.hlColor || '#4F46E5') : ((o.colors && o.colors[i]) || o.color || '#CBD5E1'),
        'class': 'hbar' + (hl ? ' hl' : ''), style: 'transition-delay:' + (i * 45) + 'ms' }, s);
      T(s, m.l + bw + 8, y + 6, fm(v, o.dec) + (o.unit || ''), 'cval sm' + (hl ? ' strong' : ''));
    });
    if (o.ref) {
      var rx = m.l + iw * o.ref.v / vmax;
      E('line', { x1: rx, x2: rx, y1: m.t - 4, y2: m.t + ih, 'class': 'cref' }, s);
      T(s, rx + 6, m.t + 12, o.ref.label, 'creft');
    }
  }

  function stacked(h, o) {
    var F = frame(h), s = F.s, w = F.w, hh = F.h;
    if (o.title) T(s, 2, 21, o.title, 'ctitle');
    var m = { l: o.ml || 196, r: 12, t: o.title ? 40 : 8, b: 64 };
    var iw = w - m.l - m.r, ih = hh - m.t - m.b, n = o.rows.length, slot = ih / n, bh = Math.min(o.bh || 62, slot * 0.66);
    o.rows.forEach(function (r, ri) {
      var y = m.t + slot * (ri + 0.5) - bh / 2, tot = r.parts.reduce(function (a, p) { return a + p.v; }, 0), x = m.l;
      multi(s, m.l - 14, y + bh / 2 + (r.label.indexOf('\n') > -1 ? -3 : 6), r.label, 'clabel strong', 'end', 22);
      r.parts.forEach(function (p, pi) {
        var pw = iw * p.v / tot;
        E('rect', { x: x, y: y, width: Math.max(0, pw - 2), height: bh, rx: 4, fill: p.c, 'class': 'hbar', style: 'transition-delay:' + (ri * 140 + pi * 90) + 'ms' }, s);
        var pct = (100 * p.v / tot).toFixed(1) + '%';
        if (pw > 88) { T(s, x + pw / 2, y + bh / 2 - 4, p.k, 'cin', { 'text-anchor': 'middle' }); T(s, x + pw / 2, y + bh / 2 + 20, pct, 'cin b', { 'text-anchor': 'middle' }); }
        else { T(s, x + pw / 2, y + bh / 2 + 6, pct, 'cin b', { 'text-anchor': 'middle', style: 'font-size:15px' }); }
        x += pw;
      });
    });
    var lx = m.l;
    (o.keys || []).forEach(function (k) {
      E('rect', { x: lx, y: hh - 30, width: 16, height: 16, rx: 4, fill: k[1] }, s);
      T(s, lx + 22, hh - 16, k[0], 'clegend'); lx += 22 + k[0].length * 10.4 + 28;
    });
  }

  function linec(h, o) {
    var F = frame(h), s = F.s, w = F.w, hh = F.h;
    if (o.title) T(s, 2, 21, o.title, 'ctitle');
    badge(s, w, o.better);
    var m = { l: o.ml || 66, r: o.mr || 22, t: o.mt || 70, b: o.xlabel ? 62 : 38 };
    var iw = w - m.l - m.r, ih = hh - m.t - m.b, xs = o.x, num = typeof xs[0] === 'number';
    var xmin = num ? (o.xmin != null ? o.xmin : Math.min.apply(null, xs)) : 0;
    var xmax = num ? (o.xmax != null ? o.xmax : Math.max.apply(null, xs)) : xs.length - 1;
    var pad = o.pad || (num ? 0 : 40);
    function X(v, i) { var t = num ? (v - xmin) / (xmax - xmin) : (xs.length === 1 ? 0.5 : i / (xs.length - 1)); return m.l + pad + t * (iw - 2 * pad); }
    var all = []; o.series.forEach(function (se) { se.values.forEach(function (v) { if (v != null) all.push(v); }); });
    var ymin = o.ymin != null ? o.ymin : 0, ymax = o.ymax != null ? o.ymax : niceMax(Math.max.apply(null, all) * 1.1, 5);
    function Y(v) { return m.t + ih - (v - ymin) / (ymax - ymin) * ih; }
    ticks(ymin, ymax, o.nt || 5).forEach(function (t) {
      E('line', { x1: m.l, x2: w - m.r, y1: Y(t), y2: Y(t), 'class': 'cgrid' }, s);
      T(s, m.l - 9, Y(t) + 5, fm(t, o.ydec), 'ctick', { 'text-anchor': 'end' });
    });
    E('line', { x1: m.l, x2: w - m.r, y1: m.t + ih, y2: m.t + ih, 'class': 'cbase' }, s);
    if (num) (o.xticks || ticks(xmin, xmax, 5)).forEach(function (t) { T(s, X(t), m.t + ih + 22, fm(t, o.xdec), 'ctick', { 'text-anchor': 'middle' }); });
    else xs.forEach(function (lab, i) { multi(s, X(0, i), m.t + ih + 26, lab, 'clabel', 'middle', 21); });
    if (o.xlabel) T(s, m.l + iw / 2, hh - 8, o.xlabel, 'caxis', { 'text-anchor': 'middle' });
    if (o.ylabel) T(s, 14, m.t + ih / 2, o.ylabel, 'caxis', { transform: 'rotate(-90 14 ' + (m.t + ih / 2) + ')', 'text-anchor': 'middle' });
    var lx = m.l;
    if (o.legend !== false) o.series.forEach(function (se) {
      E('line', { x1: lx, x2: lx + 26, y1: 45, y2: 45, stroke: se.color, 'stroke-width': 4, 'stroke-dasharray': se.dash ? '8 6' : null }, s);
      T(s, lx + 34, 52, se.name, 'clegend'); lx += 34 + se.name.length * 10.4 + 30;
    });
    (o.bands || []).forEach(function (b) {
      E('rect', { x: X(b.from), y: m.t, width: X(b.to) - X(b.from), height: ih, fill: b.color, opacity: 0.5 }, s);
      if (b.label) T(s, (X(b.from) + X(b.to)) / 2, m.t + 20, b.label, 'cptl', { 'text-anchor': 'middle' });
    });
    o.series.forEach(function (se, si) {
      var d = '', prevPt = null;
      se.values.forEach(function (v, i) {
        if (v == null) { prevPt = null; return; }
        var px = X(num ? xs[i] : 0, i), py = Y(v);
        if (!prevPt) d += 'M' + px + ' ' + py;
        else if (se.step) d += 'L' + px + ' ' + prevPt[1] + 'L' + px + ' ' + py;
        else d += 'L' + px + ' ' + py;
        prevPt = [px, py];
      });
      var path = E('path', { d: d, stroke: se.color, 'class': 'cline' + (se.dash ? ' dash' : '') }, s);
      if (!se.dash) { var L = Math.ceil(path.getTotalLength ? path.getTotalLength() : 2000) + 2; path.style.setProperty('--len', L); path.style.transitionDelay = (si * 250) + 'ms'; }
      if (se.dots) se.values.forEach(function (v, i) {
        if (v == null) return;
        var px = X(num ? xs[i] : 0, i), py = Y(v);
        E('circle', { cx: px, cy: py, r: 6.5, fill: '#fff', stroke: se.color, 'stroke-width': 3.5, 'class': 'cdot' }, s);
        if (se.labels !== false) T(s, px + (se.ldx || 0), py + (se.below ? 28 : -14), fm(v, se.dec != null ? se.dec : o.ydec), 'cval sm', { 'text-anchor': 'middle', fill: se.color });
      });
    });
    (o.notes || []).forEach(function (a) {
      var px = X(a.x, a.x), py = Y(a.y);
      T(s, px + (a.dx || 0), py + (a.dy || 0), a.text, 'cptl strong cann', { 'text-anchor': a.anchor || 'middle', fill: a.color || '#0F1B33' });
    });
  }

  function scatter(h, o) {
    var F = frame(h), s = F.s, w = F.w, hh = F.h;
    if (o.title) T(s, 2, 21, o.title, 'ctitle');
    var m = { l: 70, r: 26, t: 36, b: 62 };
    var iw = w - m.l - m.r, ih = hh - m.t - m.b;
    function X(v) { return m.l + (v - o.xmin) / (o.xmax - o.xmin) * iw; }
    function Y(v) { return m.t + ih - (v - o.ymin) / (o.ymax - o.ymin) * ih; }
    ticks(o.ymin, o.ymax, 5).forEach(function (t) { E('line', { x1: m.l, x2: w - m.r, y1: Y(t), y2: Y(t), 'class': 'cgrid' }, s); T(s, m.l - 9, Y(t) + 5, fm(t), 'ctick', { 'text-anchor': 'end' }); });
    ticks(o.xmin, o.xmax, 6).forEach(function (t) { E('line', { x1: X(t), x2: X(t), y1: m.t, y2: m.t + ih, 'class': 'cgrid' }, s); T(s, X(t) + (t === o.xmin ? 4 : 0), m.t + ih + 20, fm(t), 'ctick', { 'text-anchor': t === o.xmin ? 'start' : 'middle' }); });  /* v30: no corner overlap */
    E('line', { x1: m.l, x2: w - m.r, y1: m.t + ih, y2: m.t + ih, 'class': 'cbase' }, s);
    T(s, m.l + iw / 2, hh - 10, o.xlabel, 'caxis', { 'text-anchor': 'middle' });
    T(s, 16, m.t + ih / 2, o.ylabel, 'caxis', { transform: 'rotate(-90 16 ' + (m.t + ih / 2) + ')', 'text-anchor': 'middle' });
    if (o.front) {
      var fp = o.front.slice().sort(function (a, b) { return a[0] - b[0]; });
      var d = fp.map(function (p, i) { return (i ? 'L' : 'M') + X(p[0]) + ' ' + Y(p[1]); }).join('');
      E('path', { d: d, 'class': 'cfront cann' }, s);
    }
    if (o.vline) {
      E('line', { x1: X(o.vline.x), x2: X(o.vline.x), y1: m.t, y2: m.t + ih, 'class': 'cref' }, s);
      T(s, X(o.vline.x) + 8, m.t + ih - 10, o.vline.label, 'creft');
    }
    if (o.better) {
      var g = E('g', { 'class': 'cann' }, s);
      T(g, m.l + 14, m.t + 20, o.better, 'cptl strong', { fill: '#15803D' });
    }
    o.points.forEach(function (p, i) {
      var px = X(p.x), py = Y(p.y), r = p.r || 7;
      var g = E('g', { 'class': 'cpt', style: 'transition-delay:' + (300 + i * 40) + 'ms' }, s);
      if (p.shape === 'diamond') E('path', { d: 'M' + px + ' ' + (py - r - 3) + 'L' + (px + r + 3) + ' ' + py + 'L' + px + ' ' + (py + r + 3) + 'L' + (px - r - 3) + ' ' + py + 'Z', fill: p.color, stroke: '#fff', 'stroke-width': 2 }, g);
      else E('circle', { cx: px, cy: py, r: r, fill: p.color, stroke: p.ring ? '#0F1B33' : '#fff', 'stroke-width': p.ring ? 3 : 2 }, g);
      if (p.ring) E('circle', { cx: px, cy: py, r: r + 8, fill: 'none', stroke: p.color, 'stroke-width': 2.5 }, g);
      if (p.label) multi(g, px + (p.dx || 12), py + (p.dy || -10), p.label, 'cptl' + (p.strong ? ' strong' : ''), p.anchor || 'start', 18);
    });
  }

  function forest(h, o) {
    var F = frame(h), s = F.s, w = F.w, hh = F.h;
    if (o.title) T(s, 2, 21, o.title, 'ctitle');
    var m = { l: o.ml || 200, r: o.mr || 196, t: o.title ? 46 : 14, b: 52 };
    var iw = w - m.l - m.r, ih = hh - m.t - m.b, n = o.rows.length, slot = ih / n;
    var lo = Math.min(0, Math.min.apply(null, o.rows.map(function (r) { return r.lo; })));
    var hi = Math.max(0, Math.max.apply(null, o.rows.map(function (r) { return r.hi; })));
    var padv = (hi - lo) * 0.08; lo -= padv; hi += padv;
    function X(v) { return m.l + (v - lo) / (hi - lo) * iw; }
    ticks(lo, hi, 6).forEach(function (t) { E('line', { x1: X(t), x2: X(t), y1: m.t, y2: m.t + ih, 'class': 'cgrid' }, s); T(s, X(t), m.t + ih + 20, fm(t), 'ctick', { 'text-anchor': 'middle' }); });
    E('line', { x1: X(0), x2: X(0), y1: m.t - 6, y2: m.t + ih, 'class': 'czero' }, s);
    T(s, m.l + iw / 2, hh - 8, o.xlabel, 'caxis', { 'text-anchor': 'middle' });
    o.rows.forEach(function (r, i) {
      var y = m.t + slot * (i + 0.5), sig = r.lo > 0 || r.hi < 0;
      var col = r.color || '#4F46E5';
      multi(s, m.l - 14, y + 6, r.label, 'clabel strong', 'end', 22);
      var g = E('g', { 'class': 'cpt', style: 'transition-delay:' + (200 + i * 120) + 'ms' }, s);
      E('line', { x1: X(r.lo), x2: X(r.hi), y1: y, y2: y, stroke: col, 'class': 'cci' }, g);
      E('line', { x1: X(r.lo), x2: X(r.lo), y1: y - 9, y2: y + 9, stroke: col, 'class': 'cci' }, g);
      E('line', { x1: X(r.hi), x2: X(r.hi), y1: y - 9, y2: y + 9, stroke: col, 'class': 'cci' }, g);
      E('circle', { cx: X(r.est), cy: y, r: 9, fill: col, 'class': 'cest' }, g);
      T(g, w - m.r + 14, y - 6, fm(r.est, o.dec) + (o.unit || ''), 'cptl strong');
      T(g, w - m.r + 14, y + 21, '[' + fm(r.lo, o.dec) + ', ' + fm(r.hi, o.dec) + ']' + (sig ? '' : '  n.s.'), 'cptl', { fill: sig ? '#15803D' : '#B45309' });
    });
  }

  /* ------------------------------------------------ chart registry */
  function tdRow(id) { return D.testdev.rows.filter(function (r) { return r.id === id; })[0]; }
  function uvRow(id) { return D.uavdt.rows.filter(function (r) { return r.id === id; })[0]; }
  function sysBars(h, rows, key, better, dec, ref, ylabel) {
    bars(h, { labels: rows.map(function (r) { return r.name.replace(' Trial ', '\nTrial ').replace('Initial AC-MOT', 'Initial\nAC-MOT'); }), values: rows.map(function (r) { return r[key]; }),
      colors: rows.map(function (r) { return COL[r.id] || '#4F46E5'; }), better: better, dec: dec, ref: ref, ylabel: ylabel, mb: 76, bw: 84 });
  }
  function wparts(wt) {
    return [['Crowd', wt.crowd, COL.crowd], ['Tiny', wt.tiny, COL.tiny], ['Edge', wt.edge, COL.edge], ['Night', wt.night, COL.night], ['Blur', wt.blur, COL.blur]]
      .map(function (a) { return { k: a[0], v: a[1], c: a[2] }; });
  }
  var WKEYS = [['Crowd', COL.crowd], ['Tiny objects', COL.tiny], ['Edge complexity', COL.edge], ['Night', COL.night], ['Blur', COL.blur]];
  var REF25 = { v: 25, label: 'real-time 25 FPS' };

  var CHARTS = {
    'det-lat': function (h) {
      var r = D.detectorTiming.rows;
      hbars(h, { labels: r.map(function (x) { return x[0]; }), values: r.map(function (x) { return x[1]; }), dec: 2, unit: ' ms',
        better: 'lower', hl: 'YOLOv8n', xlabel: 'Detector latency per frame (ms)', color: '#CBD5E1' });
    },
    'det-fps': function (h) {
      var r = D.detectorTiming.rows;
      hbars(h, { labels: r.map(function (x) { return x[0]; }), values: r.map(function (x) { return 1000 / x[1]; }), dec: 1, unit: ' FPS',
        better: 'higher', hl: 'YOLOv8n', xlabel: 'Detector-only speed = 1000 / latency', color: '#99F6E4', hlColor: '#0D9488' });
    },
    'det-tier': function (h) {
      var m = {}; D.detectorTiming.rows.forEach(function (x) { m[x[0]] = x[1]; });
      linec(h, { x: ['nano', 'small', 'medium', 'large', 'x-large'], ylabel: 'Latency (ms)', xlabel: 'Model size tier', better: 'lower', ymax: 90,
        series: [
          { name: 'YOLOv8', color: '#4F46E5', dots: true, dec: 1, values: [m.YOLOv8n, m.YOLOv8s, m.YOLOv8m, m.YOLOv8l, m.YOLOv8x] },
          { name: 'YOLOv10', color: '#0D9488', dots: true, dec: 1, below: true, values: [m.YOLOv10n, m.YOLOv10s, m.YOLOv10m, null, null] }
        ] });
    },
    /* v6: original AC-MOT ablation (separate experiment) */
    'oab-quality': function (h) {
      var r = D.oldAblation.rows, cols = ['#94A3B8', '#60A5FA', '#818CF8', '#F59E0B', '#4F46E5'];
      grouped(h, { groups: ['MOTA', 'HOTA', 'IDF1'], better: 'higher', dec: 1, ylabel: 'percent', max: 40, novals: true,
        series: r.map(function (x, i) { return { name: x.id, color: cols[i], values: [x.mota, x.hota, x.idf1] }; }) });
    },
    'oab-ids': function (h) {
      var r = D.oldAblation.rows;
      bars(h, { labels: r.map(function (x) { return x.id; }), values: r.map(function (x) { return x.ids; }),
        colors: ['#94A3B8', '#60A5FA', '#818CF8', '#F59E0B', '#4F46E5'], better: 'lower', dec: 0, ylabel: 'ID switches', bw: 64 });
    },
    'oab-fps': function (h) {
      var r = D.oldAblation.rows;
      bars(h, { labels: r.map(function (x) { return x.id; }), values: r.map(function (x) { return x.fps; }),
        colors: ['#94A3B8', '#60A5FA', '#818CF8', '#F59E0B', '#4F46E5'], better: 'higher', dec: 1, ref: REF25, ylabel: 'FPS', bw: 64, max: 50 });
    },
    /* v6: the four systems on the test set, quality metrics in one chart */
    'td4-quality': function (h) {
      grouped(h, { groups: ['MOTA', 'HOTA', 'IDF1'], better: 'higher', dec: 1, ylabel: 'percent',
        series: ['base', 'old', 'v1', 'v2'].map(tdRow).map(function (x) { return { name: x.name, color: COL[x.id], values: [x.mota, x.hota, x.idf1] }; }) });
    },
    'smooth': function (h) {
      var raw = [0.25, 0.27, 0.80, 0.29, 0.31], sm = [];
      raw.forEach(function (v, i) { var a = raw.slice(Math.max(0, i - 6), i + 1); sm.push(a.reduce(function (p, q) { return p + q; }, 0) / a.length); });
      linec(h, { x: ['reading 1', 'reading 2', 'reading 3', 'reading 4', 'reading 5'], ymin: 0, ymax: 1, ydec: 1, ylabel: 'SCI', pad: 60,
        series: [{ name: 'Raw SCI (one reading)', color: '#F87171', dots: true, dec: 2, ldx: -26, values: raw },
                 { name: 'Smoothed SCI (mean of last ≤ 7)', color: '#4F46E5', dots: true, dec: 2, ldx: 26, values: sm }],
        notes: [{ x: 2, y: 0.80, dy: -40, text: 'one hard frame', color: '#B91C1C' }] });
    },
    'calib-conf': function (h) {
      var c = D.original.calibrator, xs = [], cf = [], io = [];
      for (var i = 0; i <= 20; i++) { var x = i / 20; xs.push(x); cf.push(Math.min(c.confMax, Math.max(c.confMin, c.conf0 - c.confSlope * x))); io.push(Math.min(c.iouMax, Math.max(c.iouMin, c.iou0 - c.iouSlope * x))); }
      linec(h, { x: xs, xmin: 0, xmax: 1, xticks: [0, 0.2, 0.4, 0.6, 0.8, 1], xdec: 1, ymin: 0.15, ymax: 0.55, ydec: 2, nt: 4, xlabel: 'SCI (0 = easy, 1 = hard)', mt: 64,
        series: [{ name: 'NMS IoU = 0.490 − 0.050·SCI', color: '#0D9488', values: io }, { name: 'confidence = 0.245 − 0.050·SCI', color: '#4F46E5', values: cf }] });
    },
    'calib-size': function (h) {
      var c = D.original.calibrator, xs = [], sz = [];
      for (var i = 0; i <= 100; i++) { var x = i / 100; xs.push(x); sz.push(x > c.sciHigh ? c.sizes[2] : x > c.sciMid ? c.sizes[1] : c.sizes[0]); }
      linec(h, { x: xs, xmin: 0, xmax: 1, xticks: [0, 0.35, 0.6, 1], xdec: 2, ymin: 560, ymax: 880, nt: 4, xlabel: 'SCI (0 = easy, 1 = hard)', ylabel: 'input size (px)', mt: 64,
        series: [{ name: 'input size', color: '#D97706', step: true, values: sz }],
        bands: [{ from: 0, to: c.sciMid, color: '#DCFCE7', label: '640' }, { from: c.sciMid, to: c.sciHigh, color: '#FEF3C7', label: '736' }, { from: c.sciHigh, to: 1, color: '#FEE2E2', label: '832' }] });
    },
    'weights-v1': function (h) {
      stacked(h, { rows: [{ label: 'Original\n(hand-set)', parts: wparts(D.original.weights) }, { label: 'V1 Trial 24\n(learned)', parts: wparts(D.v1.weights) }], keys: WKEYS });
    },
    'weights-all': function (h) {
      stacked(h, { rows: [{ label: 'Original\n(hand-set)', parts: wparts(D.original.weights) }, { label: 'V1 Trial 24', parts: wparts(D.v1.weights) }, { label: 'V2 Trial 22', parts: wparts(D.v2.weights) }], keys: WKEYS, bh: 54 });
    },
    'weights-transfer': function (h) {
      stacked(h, { rows: [{ label: 'V1 SCI weights\n(transferred)', parts: wparts(D.v1.weights) }], keys: WKEYS, bh: 80 });
    },
    'v1t-quality': function (h) {
      var r = ['base', 'old', 'v1'].map(tdRow);
      grouped(h, { groups: ['MOTA', 'HOTA', 'IDF1'], better: 'higher', dec: 1, ylabel: 'percent',
        series: r.map(function (x) { return { name: x.name, color: COL[x.id], values: [x.mota, x.hota, x.idf1] }; }) });
    },
    'v1t-ids': function (h) { sysBars(h, ['base', 'old', 'v1'].map(tdRow), 'ids', 'lower', 0, null, 'ID switches'); },
    'v1t-fps': function (h) { sysBars(h, ['base', 'old', 'v1'].map(tdRow), 'fps', 'higher', 1, REF25, 'FPS'); },
    'td-mota': function (h) { sysBars(h, ['base', 'old', 'v1', 'v2'].map(tdRow), 'mota', 'higher', 1, null, 'MOTA (%)'); },
    'td-hota': function (h) { sysBars(h, ['base', 'old', 'v1', 'v2'].map(tdRow), 'hota', 'higher', 1, null, 'HOTA (%)'); },
    'td-idf1': function (h) { sysBars(h, ['base', 'old', 'v1', 'v2'].map(tdRow), 'idf1', 'higher', 1, null, 'IDF1 (%)'); },
    'td-ids': function (h) { sysBars(h, ['base', 'old', 'v1', 'v2'].map(tdRow), 'ids', 'lower', 0, null, 'ID switches'); },
    'td-fps': function (h) { sysBars(h, ['base', 'old', 'v1', 'v2'].map(tdRow), 'fps', 'higher', 1, REF25, 'FPS'); },
    'boot-vis': function (h) {
      var b = D.testdev.bootstrap;
      forest(h, { xlabel: 'MOTA difference (percentage points)', dec: 2, unit: ' pp', ml: 170, rows: [
        { label: 'V1 − Baseline', est: b.v1_vs_base.mota[0], lo: b.v1_vs_base.mota[1], hi: b.v1_vs_base.mota[2], color: COL.v1 },
        { label: 'V2 − Baseline', est: b.v2_vs_base.mota[0], lo: b.v2_vs_base.mota[1], hi: b.v2_vs_base.mota[2], color: COL.v2 },
        { label: 'V2 − V1', est: b.v2_vs_v1.mota[0], lo: b.v2_vs_v1.mota[1], hi: b.v2_vs_v1.mota[2], color: '#64748B' }] });
    },
    'boot-vis-ids': function (h) {
      var b = D.testdev.bootstrap;
      forest(h, { xlabel: 'ID switches removed (positive = fewer IDS)', dec: 0, ml: 170, rows: [
        { label: 'V1 vs Baseline', est: b.v1_vs_base.idsRed[0], lo: b.v1_vs_base.idsRed[1], hi: b.v1_vs_base.idsRed[2], color: COL.v1 },
        { label: 'V2 vs Baseline', est: b.v2_vs_base.idsRed[0], lo: b.v2_vs_base.idsRed[1], hi: b.v2_vs_base.idsRed[2], color: COL.v2 },
        { label: 'V2 vs V1', est: b.v2_vs_v1.idsRed[0], lo: b.v2_vs_v1.idsRed[1], hi: b.v2_vs_v1.idsRed[2], color: '#64748B' }] });
    },
    'pareto': function (h) {
      var v2 = D.v2, pts = v2.pareto.map(function (p) {
        var o = { x: p[2], y: p[1], color: '#5EEAD4', r: 7 };
        if (p[0] === 22) { o.color = COL.v2; o.r = 10; o.ring = true; o.label = 'T22 · selected\n(balanced rule)'; o.strong = true; o.dx = 20; o.dy = 30; }
        if (p[0] === 16) { o.color = '#14B8A6'; o.label = 'T16 · highest MOTA'; o.dx = 14; o.dy = 6; }
        if (p[0] === 8) { o.color = '#14B8A6'; o.label = 'T8 · lowest IDS'; o.dx = 14; o.dy = 6; }
        return o;
      });
      pts.push({ x: D.v1.val.ids, y: D.v1.val.mota, color: COL.v1, shape: 'diamond', r: 8, label: 'V1 T24 (V1 study, same validation split)', dx: 0, dy: 34, anchor: 'middle', strong: true });
      pts.push({ x: D.v1.oldA3val.ids, y: D.v1.oldA3val.mota, color: '#94A3B8', shape: 'diamond', r: 7, label: 'Initial AC-MOT (Old-A3) reference', dx: -14, dy: 24, anchor: 'end' });
      scatter(h, { xmin: 100, xmax: 360, ymin: 10, ymax: 25, xlabel: 'ID switches on validation  (lower is better →  left)', ylabel: 'MOTA on validation (%)',
        points: pts, front: v2.pareto.map(function (p) { return [p[2], p[1]]; }), better: '↖ better: more MOTA, fewer ID switches' });
    },
    'uav-quality': function (h) {
      var r = D.uavdt.rows;
      grouped(h, { groups: ['MOTA', 'HOTA', 'IDF1'], better: 'higher', dec: 1, ylabel: 'percent',
        series: r.map(function (x) { return { name: x.name, color: COL[x.id], values: [x.mota, x.hota, x.idf1] }; }) });
    },
    'uav-ids': function (h) { sysBars(h, D.uavdt.rows, 'ids', 'lower', 0, null, 'ID switches'); },
    'uav-fps': function (h) { sysBars(h, D.uavdt.rows, 'fps', 'higher', 1, REF25, 'FPS'); },
    'boot-uav': function (h) {
      var b = D.uavdt.bootstrap;
      forest(h, { xlabel: 'MOTA difference on UAVDT (percentage points)', dec: 2, unit: ' pp', ml: 170, rows: [
        { label: 'V1 − Baseline', est: b.v1_vs_base.mota[0], lo: b.v1_vs_base.mota[1], hi: b.v1_vs_base.mota[2], color: COL.v1 },
        { label: 'V2 − Baseline', est: b.v2_vs_base.mota[0], lo: b.v2_vs_base.mota[1], hi: b.v2_vs_base.mota[2], color: COL.v2 },
        { label: 'V2 − V1', est: b.v2_vs_v1.mota[0], lo: b.v2_vs_v1.mota[1], hi: b.v2_vs_v1.mota[2], color: '#64748B' }] });
    },
    /* v15: charts for the full research story */
    'baseline-quality': function (h) { var x = tdRow('base'); grouped(h, { groups: ['MOTA', 'HOTA', 'IDF1'], better: 'higher', dec: 1, ylabel: 'percent', series: [{ name: x.name, color: COL[x.id], values: [x.mota, x.hota, x.idf1] }] }); },
    'baseline-ids': function (h) { sysBars(h, [tdRow('base')], 'ids', 'lower', 0, null, 'ID switches'); },
    'baseline-fps': function (h) { sysBars(h, [tdRow('base')], 'fps', 'higher', 1, REF25, 'FPS'); },
    'init-quality': function (h) { grouped(h, { groups: ['MOTA', 'HOTA', 'IDF1'], better: 'higher', dec: 1, ylabel: 'percent',
      series: ['base', 'old'].map(tdRow).map(function (x) { return { name: x.name, color: COL[x.id], values: [x.mota, x.hota, x.idf1] }; }) }); },
    'init-ids': function (h) { sysBars(h, ['base', 'old'].map(tdRow), 'ids', 'lower', 0, null, 'ID switches'); },
    'init-fps': function (h) { sysBars(h, ['base', 'old'].map(tdRow), 'fps', 'higher', 1, REF25, 'FPS'); },
    'v1b-quality': function (h) { grouped(h, { groups: ['MOTA', 'HOTA', 'IDF1'], better: 'higher', dec: 1, ylabel: 'percent',
      series: ['base', 'v1'].map(tdRow).map(function (x) { return { name: x.name, color: COL[x.id], values: [x.mota, x.hota, x.idf1] }; }) }); },
    'v1b-ids': function (h) { sysBars(h, ['base', 'v1'].map(tdRow), 'ids', 'lower', 0, null, 'ID switches'); },
    'v1b-fps': function (h) { sysBars(h, ['base', 'v1'].map(tdRow), 'fps', 'higher', 1, REF25, 'FPS'); },
    'td3-quality': function (h) { grouped(h, { groups: ['MOTA', 'HOTA', 'IDF1'], better: 'higher', dec: 1, ylabel: 'percent',
      series: ['base', 'v1', 'v2'].map(tdRow).map(function (x) { return { name: x.name, color: COL[x.id], values: [x.mota, x.hota, x.idf1] }; }) }); },
    'td3-ids': function (h) { sysBars(h, ['base', 'v1', 'v2'].map(tdRow), 'ids', 'lower', 0, null, 'ID switches'); },
    'td3-fps': function (h) { sysBars(h, ['base', 'v1', 'v2'].map(tdRow), 'fps', 'higher', 1, REF25, 'FPS'); },
    'val-quality': function (h) { var a = D.v1.val, b = D.v2.val;
      grouped(h, { groups: ['MOTA', 'HOTA', 'IDF1'], better: 'higher', dec: 1, ylabel: 'percent',
        series: [{ name: 'V1 Trial 24', color: COL.v1, values: [a.mota, a.hota, a.idf1] }, { name: 'V2 Trial 22', color: COL.v2, values: [b.mota, b.hota, b.idf1] }] }); },
    'val-ids': function (h) { bars(h, { labels: ['V1\nTrial 24', 'V2\nTrial 22'], values: [D.v1.val.ids, D.v2.val.ids], colors: [COL.v1, COL.v2], better: 'lower', dec: 0, ylabel: 'ID switches', mb: 76, bw: 84 }); },
    'val-fps': function (h) { bars(h, { labels: ['V1\nTrial 24', 'V2\nTrial 22'], values: [D.v1.val.fps, D.v2.val.fps], colors: [COL.v1, COL.v2], better: 'higher', dec: 1, ref: REF25, ylabel: 'FPS', mb: 76, bw: 84 }); },
    'boot-v1q': function (h) { var b = D.testdev.bootstrap.v1_vs_base;
      forest(h, { xlabel: 'V1 − Baseline (points) · 95% confidence interval', dec: 2, ml: 110, mr: 180, rows: [
        { label: 'MOTA', est: b.mota[0], lo: b.mota[1], hi: b.mota[2], color: COL.v1 },
        { label: 'HOTA', est: b.hota[0], lo: b.hota[1], hi: b.hota[2], color: COL.v1 },
        { label: 'IDF1', est: b.idf1[0], lo: b.idf1[1], hi: b.idf1[2], color: COL.v1 }] }); },
    'boot-ids2': function (h) { var b = D.testdev.bootstrap, n = tdRow('base').ids, P = function (v) { return v / n * 100; };
      forest(h, { xlabel: 'ID switches removed vs Baseline (% of its ' + n + '; positive = fewer)', dec: 1, unit: '%', ml: 90, mr: 170, rows: [
        { label: 'V1', est: P(b.v1_vs_base.idsRed[0]), lo: P(b.v1_vs_base.idsRed[1]), hi: P(b.v1_vs_base.idsRed[2]), color: COL.v1 },
        { label: 'V2', est: P(b.v2_vs_base.idsRed[0]), lo: P(b.v2_vs_base.idsRed[1]), hi: P(b.v2_vs_base.idsRed[2]), color: COL.v2 }] }); },
    'lit-quality': function (h) { var p = D.published.droneMOTByteTrack, v = tdRow('v1');
      grouped(h, { groups: ['MOTA', 'IDF1'], better: 'higher', dec: 1, ylabel: 'percent', bw: 90,
        series: [{ name: 'ByteTrack (DroneMOT)', color: '#F59E0B', values: [p.mota, p.idf1] }, { name: 'V1 (old custom protocol)', color: COL.v1, values: [v.mota, v.idf1] }] }); },
    'lit-ids': function (h) { var p = D.published.droneMOTByteTrack, v = tdRow('v1');
      bars(h, { labels: ['ByteTrack\n(DroneMOT)', 'V1\n(old protocol)'], values: [p.ids, v.ids], colors: ['#F59E0B', COL.v1], better: 'lower', dec: 0, ylabel: 'ID switches', mb: 76, bw: 84 }); },
    /* v24: ablation A0 vs A3, and why V1 Trial 24 was selected */
    'oab-a0a3': function (h) { var r = D.oldAblation.rows, a0 = r[0], a3 = r[r.length - 1];
      grouped(h, { groups: ['MOTA', 'HOTA', 'IDF1'], better: 'higher', dec: 1, ylabel: 'percent', max: 40, bw: 90,
        series: [{ name: 'OLD-A0 · Baseline', color: '#94A3B8', values: [a0.mota, a0.hota, a0.idf1] }, { name: 'OLD-A3 · Full AC-MOT', color: '#4F46E5', values: [a3.mota, a3.hota, a3.idf1] }] }); },
    'v1-rule-fps': function (h) { bars(h, { labels: ['Trial 24'], values: [D.v1.val.fps], colors: [COL.v1], better: 'higher', dec: 2, ref: { v: 25, label: 'rule: at least 25 FPS' }, ylabel: 'FPS', max: 50, bw: 120 }); },
    'v1-rule-ids': function (h) { bars(h, { labels: ['Old-A3\nlimit', 'Trial 24'], values: [D.v1.oldA3val.ids, D.v1.val.ids], colors: ['#94A3B8', COL.v1], better: 'lower', dec: 0, ylabel: 'ID switches', max: 320, bw: 100, mb: 76 }); },
    'v1-rule-mota': function (h) { bars(h, { labels: ['Old-A3\nreference', 'Trial 24'], values: [D.v1.oldA3val.mota, D.v1.val.mota], colors: ['#94A3B8', COL.v1], better: 'higher', dec: 3, ylabel: 'MOTA (%)', max: 30, bw: 100, mb: 76 }); },
    /* v26: every completed V1 Optuna trial on validation */
    'v1-trials': function (h) {
      var t = D.v1trials.rows, front = [], best = -1;
      t.slice().sort(function (a, b) { return a[2] - b[2] || b[1] - a[1]; }).forEach(function (p) { if (p[1] > best) { front.push([p[2], p[1]]); best = p[1]; } });
      var pts = t.map(function (p) {
        var o = { x: p[2], y: p[1], color: p[4] ? '#A78BFA' : '#CBD5E1', r: 7 };
        if (p[0] === 24) { o.color = COL.v1; o.r = 10; o.ring = true; o.label = 'T24 · selected\nhighest MOTA · IDS 270'; o.strong = true; o.dx = -26; o.dy = 112; o.anchor = 'end'; }
        return o;
      });
      scatter(h, { xmin: 100, xmax: 360, ymin: 10, ymax: 25, xlabel: 'ID switches on validation  (lower is better →  left)', ylabel: 'MOTA on validation (%)',
        points: pts, front: front, vline: { x: 271, label: 'rule: IDS ≤ 271' }, better: '↖ better: more MOTA, fewer ID switches' });
    },
    'pub-mota': function (h) {
      var p = D.published.mot17Mota;
      hbars(h, { labels: p.map(function (x) { return x[0]; }), values: p.map(function (x) { return x[1]; }), dec: 1, unit: '%', max: 100, bh: 46,
        better: 'higher', hl: 'ByteTrack', hlColor: '#0D9488', color: '#94A3B8', xlabel: 'MOTA on the MOT17 test set (%)' });
    },
    'pub-ids': function (h) {
      var p = D.published.mot17Ids;
      hbars(h, { labels: p.map(function (x) { return x[0]; }), values: p.map(function (x) { return x[1]; }), dec: 0, bh: 50,
        better: 'lower', hl: 'ByteTrack', hlColor: '#0D9488', color: '#94A3B8', xlabel: 'ID switches on the MOT17 test set' });
    }
  };

  function drawChart(h) {
    var id = h.getAttribute('data-chart'), fn = CHARTS[id];
    if (!fn) { h.innerHTML = '<div class="chart-missing">Chart “' + id + '” is not defined.</div>'; return; }
    if (!h.getAttribute('data-built')) {
      try { fn(h); h.setAttribute('data-built', '1'); }
      catch (err) { h.innerHTML = '<div class="chart-missing">Chart error: ' + err.message + '</div>'; if (window.console) console.error(err); return; }
    }
    h.classList.remove('play'); void h.getBoundingClientRect();
    requestAnimationFrame(function () { requestAnimationFrame(function () { h.classList.add('play'); }); });
  }
  window.ACMOT_CHARTS = CHARTS;

  /* ------------------------------------------------ v7: optional detailed explanations
     Pages live in #xstage, outside the main slide list: they never appear in Next / Previous,
     do not change slide numbers, and closing returns to the slide that opened them. */
  var xview = document.getElementById('xview'), xstage = document.getElementById('xstage');
  var xdeck = null, xpages = [], xi = 0, xFrom = -1;
  function fitX() {
    if (!xstage) return;
    var s = Math.min(window.innerWidth / W, window.innerHeight / H);
    xstage.style.transform = 'translate(-50%,-50%) scale(' + s + ')';
  }
  window.addEventListener('resize', fitX);
  if (xstage) {
    $$('.xdeck', xstage).forEach(function (d) {
      var pages = $$('.xpage', d), label = d.getAttribute('data-label') || 'Detailed explanation';
      pages.forEach(function (p, i) {
        p.classList.add('slide');
        var bar = document.createElement('div'); bar.className = 'xnav';
        bar.innerHTML = '<button class="xback" type="button">← Back to main slide <span class="xfrom"></span></button>' +
          '<span class="xtag">Detailed explanation · ' + label + '</span>' +
          '<span class="xpager"><button class="xprev" type="button" aria-label="Previous part">‹</button>' +
          '<span class="xcount">' + (i + 1) + ' / ' + pages.length + '</span>' +
          '<button class="xnext" type="button" aria-label="Next part">›</button></span>';
        p.appendChild(bar);
      });
    });
    bindAll(xstage);
  }
  function xShow(i) {
    if (!xpages.length) return;
    xi = Math.max(0, Math.min(xpages.length - 1, i));
    xpages.forEach(function (p, j) { p.classList.toggle('active', j === xi); p.classList.toggle('past', j < xi); });
    loadMedia(xpages[xi]);
    $$('.xprev', xdeck).forEach(function (b) { b.disabled = xi === 0; });
    $$('.xnext', xdeck).forEach(function (b) { b.disabled = xi === xpages.length - 1; });
  }
  function openX(id, pageIndex) {
    var d = document.getElementById(id);
    if (!d || !xview) return;
    closeOverlays();
    if (xdeck) xdeck.classList.remove('open');
    xdeck = d; xpages = $$('.xpage', d); xFrom = cur;
    $$('.xfrom', d).forEach(function (e) { e.textContent = '(slide ' + (cur + 1) + ')'; });
    $$('video', slides[cur]).forEach(function (v) { v.pause(); });
    d.classList.add('open'); xview.classList.add('open'); fitX(); xShow(pageIndex || 0);
  }
  function closeX() {
    if (!xview || !xview.classList.contains('open')) return false;
    xview.classList.remove('open');
    if (xdeck) xdeck.classList.remove('open');
    xpages.forEach(function (p) { p.classList.remove('active', 'past'); });
    xdeck = null; xpages = [];
    if (xFrom > -1 && xFrom !== cur) go(xFrom);
    return true;
  }
  window.ACMOT_X = { open: openX, close: closeX, show: function (i) { xShow(i); } };
  if (xview) xview.addEventListener('click', function (e) {
    if (e.target.closest('.xback') || e.target === xview) closeX();
    else if (e.target.closest('.xprev')) xShow(xi - 1);
    else if (e.target.closest('.xnext')) xShow(xi + 1);
  });
  document.addEventListener('keydown', function (e) {
    if (!xview || !xview.classList.contains('open')) return;
    var k = e.key;
    if (k === 'f' || k === 'F') return;
    e.stopImmediatePropagation();
    if (k === 'Escape' || k === 'Backspace') { e.preventDefault(); closeX(); }
    else if (k === 'ArrowRight' || k === 'PageDown' || k === ' ' || k === 'ArrowDown') { e.preventDefault(); xShow(xi + 1); }
    else if (k === 'ArrowLeft' || k === 'PageUp' || k === 'ArrowUp') { e.preventDefault(); xShow(xi - 1); }
  }, true);

  /* ------------------------------------------------ v3: fit each slide body above its strip */
  function fitSlide(s) {
    var body = $('.s-body', s), strip = null;
    for (var c = s.firstElementChild; c; c = c.nextElementSibling) if (c.classList.contains('xs')) strip = c;
    if (!body) return;
    body.style.transform = ''; body.style.width = ''; body.style.height = ''; body.style.right = ''; body.style.bottom = '';
    if (strip) body.style.bottom = (H - strip.offsetTop + 12) + 'px';
    /* v25: a title on two lines must not run into the content — shrink it a little, then move the content down */
    var head = $('.s-head', s), h2 = head && $('h2', head);
    body.style.top = '';
    if (h2) {
      h2.style.fontSize = '';
      var fs = 52;
      while (fs > 40 && head.offsetTop + head.offsetHeight > body.offsetTop - 8) { fs -= 2; h2.style.fontSize = fs + 'px'; }
      var hb = head.offsetTop + head.offsetHeight;
      if (hb > body.offsetTop - 8) body.style.top = (hb + 12) + 'px';
    }
    var bw = body.offsetWidth, bh = body.offsetHeight, sc = 1;
    function over() {
      var B = body.getBoundingClientRect(), tol = 3 * B.width / bw, all = body.getElementsByTagName('*');
      for (var i = 0; i < all.length; i++) {
        var e = all[i];
        if (e.ownerSVGElement || e.closest('[hidden]')) continue;
        var r = e.getBoundingClientRect();
        if (r.height && (r.bottom > B.bottom + tol || r.right > B.right + tol)) return true;
        /* text or a chart spilling out of its own box (card, note, callout, kpi) */
        if (/\b(card|note|callout|kpi)\b/.test(e.className) && e.scrollHeight > e.clientHeight + 4) return true;
      }
      return false;
    }
    while (sc > 0.72 && over()) {
      sc = Math.round((sc - 0.02) * 100) / 100;
      body.style.right = 'auto'; body.style.transformOrigin = '0 0';
      body.style.width = (bw / sc) + 'px'; body.style.height = (bh / sc) + 'px';
      body.style.transform = 'scale(' + sc + ')';
    }
    s.setAttribute('data-fit', sc);
  }
  function fitAll() {
    /* measure at full stage size, so a hidden or zero-size window cannot break the fit */
    var oldT = stage.style.transform;
    stage.style.transform = 'none';
    stage.classList.add('fitting');
    slides.forEach(fitSlide);
    stage.classList.remove('fitting');
    stage.style.transform = oldT;
    $$('[data-chart]').forEach(function (h) { h.removeAttribute('data-built'); });
    if (slides[cur]) $$('[data-chart]', slides[cur]).forEach(drawChart);
  }
  window.ACMOT_FIT = fitAll;

  /* ------------------------------------------------ start */
  fitAll();
  var start = parseInt((location.hash || '').replace('#', ''), 10);
  go(isNaN(start) ? 0 : start - 1);
  if (document.readyState !== 'complete') window.addEventListener('load', fitAll);
})();
