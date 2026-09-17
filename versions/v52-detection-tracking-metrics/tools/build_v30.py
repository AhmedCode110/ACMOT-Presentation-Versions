#!/usr/bin/env python3
"""v30 (from v29), requested by the author on 2026-09-15:
Clicking a chart used to copy the small chart and stretch it with a CSS scale, so a flat chart stayed flat, labels
stayed on top of each other and nothing animated. Now a click on a chart REDRAWS it from its data at lightbox size:
its own layout (ticks, labels, values spaced for the big size), a sensible shape (height / width kept between 0.5
and 0.9), the grow / fade animation plays again, and a click on the big chart replays it. The lightbox pops in with
a short zoom animation. Pictures, videos and diagrams keep the old zoom."""
import os

ROOT = os.path.expanduser("~/Desktop/ACMOT-Presentation-Versions/versions/v30-chart-zoom-redraw")


def load(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def save(p, s): open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)


def rep(s, old, new, n=1):
    assert s.count(old) == n, (s.count(old), old[:110])
    return s.replace(old, new)


j = load("script.js")
assert 'openChartZoom' not in j
j = rep(j, """  /* lightbox */
  function openZoom(z) {
    var inner = $('.lb-inner', lb); inner.innerHTML = '';
    var media = z.matches('img,video') ? z : $('img,video', z);
""", """  /* lightbox */
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
""")
# chart layout fixes found while testing the big charts (they also help the small ones)
j = rep(j, "    var m = { l: o.ml || 66, r: 14, t: (o.title || o.better) ? (o.ref && !o.title ? 84 : 60) : 24, b: o.mb || 66 };",
        "    var tickW = String(fm(o.max || niceMax(Math.max.apply(null, o.values.concat(o.ref ? [o.ref.v] : [])) * 1.14, 5), o.tdec)).length * 12;  /* v30: room for 4-digit ticks next to the axis title */\n"
        "    var m = { l: Math.max(o.ml || 66, o.ylabel ? tickW + 44 : 0), r: 14, t: (o.title || o.better) ? (o.ref && !o.title ? 84 : 60) : 24, b: o.mb || 66 };")
j = rep(j, "      T(s, m.l - 9, y + 5, fm(t, o.tdec), 'ctick', { 'text-anchor': 'end' });",
        "      if (!(o.ref && Math.abs(t - o.ref.v) * ih / vmax < 26)) T(s, m.l - 9, y + 5, fm(t, o.tdec), 'ctick', { 'text-anchor': 'end' });  /* v30: no tick on top of the reference label */")
j = rep(j, "      T(g, w - m.r + 14, y - 2, fm(r.est, o.dec) + (o.unit || ''), 'cptl strong');",
        "      T(g, w - m.r + 14, y - 6, fm(r.est, o.dec) + (o.unit || ''), 'cptl strong');")
j = rep(j, "      T(g, w - m.r + 14, y + 17, '[' + fm(r.lo, o.dec)", "      T(g, w - m.r + 14, y + 21, '[' + fm(r.lo, o.dec)")
j = rep(j, "    return d == null ? String(v) : Number(v).toFixed(d);",
        "    return (d == null ? String(v) : Number(v).toFixed(d)).replace(/^-/, '\\u2212');  /* v30: a real minus sign */")
# tick count follows the chart height, so short charts on the slides do not stack their tick numbers
j = rep(j, "    ticks(0, vmax, o.nt || 4).forEach(function (t) {",
        "    ticks(0, vmax, o.nt || (ih < 80 ? 1 : ih < 130 ? 2 : 4)).forEach(function (t) {  /* v30: fewer ticks on short charts */")
gi = j.index('  function grouped(h, o) {')
ge = j.index('\n  }\n', gi)
blk = j[gi:ge]
assert blk.count("    ticks(0, vmax, 4).forEach(function (t) {") == 1
j = j[:gi] + blk.replace("    ticks(0, vmax, 4).forEach(function (t) {",
                         "    ticks(0, vmax, ih < 80 ? 1 : ih < 130 ? 2 : 4).forEach(function (t) {  /* v30: fewer ticks on short charts */") + j[ge:]
# scatter: the first x tick starts right of the corner so it does not touch the lowest y tick
si = j.index('  function scatter(h, o) {')
se = j.index('\n  }\n', si)
sblk = j[si:se]
assert sblk.count("T(s, X(t), m.t + ih + 20, fm(t), 'ctick', { 'text-anchor': 'middle' }); });") == 1
j = j[:si] + sblk.replace("T(s, X(t), m.t + ih + 20, fm(t), 'ctick', { 'text-anchor': 'middle' }); });",
    "T(s, X(t) + (t === o.xmin ? 4 : 0), m.t + ih + 20, fm(t), 'ctick', { 'text-anchor': t === o.xmin ? 'start' : 'middle' }); });  /* v30: no corner overlap */") + j[se:]
# pareto: the V1 T24 label goes under its diamond (it ran into the "better" note) and the Old-A3 label goes left of its point
j = rep(j, "label: 'V1 T24 (V1 study, same validation split)', dx: 0, dy: -30, anchor: 'middle'",
        "label: 'V1 T24 (V1 study, same validation split)', dx: 0, dy: 34, anchor: 'middle'")
j = rep(j, "label: 'Initial AC-MOT (Old-A3) reference', dx: 14, dy: 22",
        "label: 'Initial AC-MOT (Old-A3) reference', dx: -14, dy: 24, anchor: 'end'")
save("script.js", j)

c = load("styles.css")
assert '.chart.zoomed' not in c
save("styles.css", c.rstrip() + """
/* v30: zoomed charts are redrawn at full size and animate */
.lightbox .chart.zoomed{min-height:0;cursor:pointer}
.lightbox.open .lb-inner{animation:lbZoomIn .35s cubic-bezier(.2,.8,.2,1)}
@keyframes lbZoomIn{from{opacity:0;transform:translate(-50%,-50%) scale(.9)}to{opacity:1;transform:translate(-50%,-50%) scale(1)}}
@media (prefers-reduced-motion: reduce){.lightbox.open .lb-inner{animation:none}}
""")
print("ok · openChartZoom added, CSS added")
