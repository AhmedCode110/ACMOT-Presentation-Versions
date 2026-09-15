#!/usr/bin/env python3
"""v20 (from v19):
 1. a Sections menu button in the control bar (and the S key) that jumps to any section;
 2. pictures load only when their slide is reached (plus the next slide), so the deck opens fast
    on the web instead of downloading 30 MB of pictures at once."""
import os, re

ROOT = os.path.expanduser("~/Desktop/ACMOT-Presentation-Versions/versions/v20-section-menu")


def load(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def save(p, s): open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)


def rep(s, old, new, n=1):
    assert s.count(old) == n, (s.count(old), old[:110])
    return s.replace(old, new)


# ------------------------------------------------------------------ 1. defer pictures
h = load("index.html")
first_end = h.index('</section>', h.index('<section class="slide')) + len('</section>')
head, tail = h[:first_end], h[first_end:]          # slide 1 keeps its real src
tail, n_img = re.subn(r'<img src="(assets/[^"]+)"', r'<img data-src="\1"', tail)
tail, n_vid = re.subn(r'<video src="(assets/[^"]+)"', r'<video data-src="\1"', tail)
h = head + tail
assert n_img > 50, n_img
save("index.html", h)

# ------------------------------------------------------------------ 2. engine: lazy media + sections menu
j = load("script.js")

j = rep(j, "    help: '<svg viewBox=\"0 0 24 24\"",
        "    menu: '<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.2\" stroke-linecap=\"round\"><path d=\"M4 7h16M4 12h16M4 17h10\"/></svg>',\n"
        "    help: '<svg viewBox=\"0 0 24 24\"")

j = rep(j, "'<button data-act=\"overview\" title=\"Slide navigator (O)\" aria-label=\"Slide navigator\">' + ICON.grid + '</button>' +",
        "'<button data-act=\"menu\" title=\"Go to a section (S)\" aria-label=\"Sections\">' + ICON.menu + '</button>' +\n"
        "      '<button data-act=\"overview\" title=\"Slide navigator (O)\" aria-label=\"Slide navigator\">' + ICON.grid + '</button>' +")

# the section menu overlay, built from the divider slides
j = rep(j, "  var help = document.createElement('div'); help.className = 'overlay help';",
        """  var secmenu = document.createElement('div'); secmenu.className = 'overlay secmenu';
  secmenu.innerHTML = '<div class="ov-panel sec-panel"><h2>Sections</h2>' +
    '<div class="muted" style="font-size:15px">Click a section to jump there. Press S or Esc to close.</div>' +
    '<div class="sec-list"></div></div>';
  document.body.appendChild(secmenu);
  (function buildSecMenu() {
    var list = $('.sec-list', secmenu);
    slides.forEach(function (s, i) {
      if (!/^sec-\\d+$/.test(s.id || '')) return;
      var name = s.getAttribute('data-secname') || s.getAttribute('data-title') || 'Section';
      var num = (name.split('\\u00b7')[0] || '').trim();
      var rest = name.indexOf('\\u00b7') > -1 ? name.split('\\u00b7').slice(1).join('\\u00b7').trim() : name;
      var head = $('h1', s);
      var col = getComputedStyle(s).getPropertyValue('--sec').trim() || '#4F46E5';
      var b = document.createElement('button');
      b.className = 'sec-item';
      b.setAttribute('data-slide', i);
      b.innerHTML = '<span class="sn" style="color:' + col + '">' + num + '</span>' +
        '<span class="st"><b>' + (head ? head.textContent : rest) + '</b>' +
        '<i>' + rest + ' \\u00b7 slide ' + (i + 1) + '</i></span>';
      b.addEventListener('click', function () { closeOverlays(); go(i); });
      list.appendChild(b);
    });
  })();

  var help = document.createElement('div'); help.className = 'overlay help';""")

j = rep(j, "  function toggleOverview() {",
        "  function toggleSecMenu() { var o = secmenu.classList.contains('open'); closeOverlays(); if (!o) secmenu.classList.add('open'); }\n"
        "  function toggleOverview() {")

j = rep(j, "else if (a === 'overview') toggleOverview(); else if (a === 'notes') toggleNotes();",
        "else if (a === 'overview') toggleOverview(); else if (a === 'menu') toggleSecMenu(); else if (a === 'notes') toggleNotes();")

j = rep(j, "    else if (k === 'o' || k === 'O') toggleOverview();",
        "    else if (k === 'o' || k === 'O') toggleOverview();\n    else if (k === 's' || k === 'S') toggleSecMenu();")

# load the pictures / videos of a slide when it is shown (and prepare the next one)
j = rep(j, "  function enter(s) {\n    $$('[data-chart]', s).forEach(drawChart);",
        """  function loadMedia(s) {
    if (!s) return;
    $$('[data-src]', s).forEach(function (m) { m.src = m.getAttribute('data-src'); m.removeAttribute('data-src'); });
  }
  function enter(s) {
    loadMedia(s); loadMedia(slides[cur + 1]); loadMedia(slides[cur - 1]);
    $$('[data-chart]', s).forEach(drawChart);""")

j = rep(j, "    xpages.forEach(function (p, j) { p.classList.toggle('active', j === xi); p.classList.toggle('past', j < xi); });",
        "    xpages.forEach(function (p, j) { p.classList.toggle('active', j === xi); p.classList.toggle('past', j < xi); });\n"
        "    loadMedia(xpages[xi]); loadMedia(xpages[xi + 1]);")

j = rep(j, "<tr><td><kbd>O</kbd></td><td>Slide navigator (overview)</td></tr>",
        "<tr><td><kbd>S</kbd></td><td>Sections menu - jump to any section</td></tr>' +\n    '<tr><td><kbd>O</kbd></td><td>Slide navigator (overview)</td></tr>")

# highlight the section we are inside
j = rep(j, "    $$('.ov-grid button', ov).forEach(function (b, j) { b.classList.toggle('cur', j === cur); });",
        "    $$('.ov-grid button', ov).forEach(function (b, j) { b.classList.toggle('cur', j === cur); });\n"
        "    var items = $$('.sec-item', secmenu), at = -1;\n"
        "    items.forEach(function (b, k) { if (+b.getAttribute('data-slide') <= cur) at = k; });\n"
        "    items.forEach(function (b, k) { b.classList.toggle('cur', k === at); });")
save("script.js", j)

# ------------------------------------------------------------------ 3. styles for the menu
c = load("styles.css")
assert '.sec-panel' not in c
c += """
/* v20: sections menu */
.sec-panel{inset:6vh 22vw;padding:26px 30px}
.sec-list{display:flex;flex-direction:column;gap:8px;margin-top:16px}
.sec-item{display:flex;align-items:center;gap:16px;text-align:left;background:#fff;border:1px solid var(--line);
  border-radius:12px;padding:12px 16px;cursor:pointer;font-family:var(--font);transition:background .15s,transform .15s}
.sec-item:hover{background:#EEF4FB;transform:translateX(2px)}
.sec-item.cur{border-color:#4F46E5;box-shadow:0 0 0 2px #E0E7FF}
.sec-item .sn{flex:0 0 58px;font-size:26px;font-weight:900;line-height:1}
.sec-item .st{display:flex;flex-direction:column;gap:2px;min-width:0}
.sec-item .st b{font-size:19px;color:var(--ink);font-weight:800}
.sec-item .st i{font-size:14px;color:var(--muted);font-style:normal}
@media (max-width:1100px){.sec-panel{inset:4vh 6vw}}
"""
save("styles.css", c)
print("ok · deferred", n_img, "pictures and", n_vid, "videos; sections menu added")
