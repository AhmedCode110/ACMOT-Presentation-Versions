#!/usr/bin/env python3
"""v21 (from v20): a small "Outline" button at the top of every slide that goes back to the Outline slide,
so any section can be picked from there. The M key does the same."""
import os

ROOT = os.path.expanduser("~/Desktop/ACMOT-Presentation-Versions/versions/v21-outline-button")


def load(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def save(p, s): open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)


def rep(s, old, new, n=1):
    assert s.count(old) == n, (s.count(old), old[:110])
    return s.replace(old, new)


j = load("script.js")

j = rep(j, "  var help = document.createElement('div'); help.className = 'overlay help';",
        """  /* v21: a button on every slide that returns to the Outline slide */
  var outlineIdx = -1;
  slides.forEach(function (s, i) { if (outlineIdx < 0 && (s.getAttribute('data-title') || '') === 'Outline') outlineIdx = i; });
  var toOutline = document.createElement('button');
  toOutline.className = 'to-outline';
  toOutline.type = 'button';
  toOutline.title = 'Back to the outline (M)';
  toOutline.setAttribute('aria-label', 'Back to the outline');
  toOutline.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h10"/></svg><span>Outline</span>';
  toOutline.addEventListener('click', function () { closeOverlays(); if (outlineIdx >= 0) go(outlineIdx); });
  if (outlineIdx >= 0) stage.appendChild(toOutline);

  var help = document.createElement('div'); help.className = 'overlay help';""")

# hide it on the Outline slide itself
j = rep(j, "    var items = $$('.sec-item', secmenu), at = -1;",
        "    toOutline.hidden = (cur === outlineIdx);\n    var items = $$('.sec-item', secmenu), at = -1;")

# M key
j = rep(j, "    else if (k === 's' || k === 'S') toggleSecMenu();",
        "    else if (k === 's' || k === 'S') toggleSecMenu();\n"
        "    else if (k === 'm' || k === 'M') { closeOverlays(); if (outlineIdx >= 0) go(outlineIdx); }")

j = rep(j, "<tr><td><kbd>S</kbd></td><td>Sections menu - jump to any section</td></tr>",
        "<tr><td><kbd>M</kbd></td><td>Back to the outline slide</td></tr>' +\n    '<tr><td><kbd>S</kbd></td><td>Sections menu - jump to any section</td></tr>")
save("script.js", j)

c = load("styles.css")
assert '.to-outline' not in c
c += """
/* v21: back-to-outline button, top right of every slide */
.s-head{padding-right:170px}   /* keep long titles clear of the button */
.to-outline{position:absolute;right:34px;top:30px;z-index:6;display:inline-flex;align-items:center;gap:8px;
  padding:8px 16px 8px 12px;border-radius:999px;border:2px solid var(--line2);background:rgba(255,255,255,.94);
  color:#334155;font-family:var(--font);font-size:20px;font-weight:800;cursor:pointer;
  box-shadow:var(--shadow-sm);transition:background .15s,color .15s,border-color .15s,transform .15s}
.to-outline svg{width:20px;height:20px}
.to-outline:hover{background:var(--sec);border-color:var(--sec);color:#fff;transform:translateY(-1px)}
.to-outline[hidden]{display:none!important}
.divider .to-outline,.title-slide .to-outline{background:rgba(255,255,255,.92)}
"""
save("styles.css", c)
print("ok · outline button added")
