#!/usr/bin/env python3
"""v28 (from v27), requested by the author on 2026-09-15:
1. 'Deep Learning Detectors: From Careful to Fast' (slide 19) moves after 'Three Families of Object Detectors' (slide 20),
   so the two slides swap places. Both stay inside Section II, so the Outline ranges do not change.
2. 'ByteTrack: The Baseline of This Work' was not clear with its example. Rebuilt around the same illustration
   (car ID 7, frames 100-106, settings 0.50 / 0.10 / 30): plain main idea, three rule cards (strong / weak / no box),
   a film strip of five frame pictures (the car goes behind a wall) with the decision and the ID under each frame,
   and a result line: ByteTrack keeps ID 7, a simple tracker without weak boxes and without a buffer gives a new ID
   (an ID switch - illustration). The technical step table moved to the speaker notes."""
import os, re

ROOT = os.path.expanduser("~/Desktop/ACMOT-Presentation-Versions/versions/v28-detector-families-first")


def load(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def save(p, s): open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)
def main_part(h): return h[:h.index('<div class="overlay xview"')]
def titles(h): return re.findall(r'<section class="slide[^"]*"[^>]*data-title="([^"]*)"', main_part(h))


def rep(s, old, new, n=1):
    assert s.count(old) == n, (s.count(old), old[:110])
    return s.replace(old, new)


def block(h, title):
    i = h.index('data-title="%s"' % title)
    a = h.rfind('<section', 0, i)
    b = h.index('</section>', i) + len('</section>')
    b += len(h[b:]) - len(h[b:].lstrip('\n'))
    return a, b


h = load("index.html")
t = titles(h)
assert len(t) == 94 and t[18] == 'Deep learning detectors' and t[19] == 'Detector families', t[17:21]
outline_before = re.findall(r'slides \d+ - \d+', h)

# ------------------------------------------------------------ 1. swap slides 19 and 20
a, b = block(h, 'Deep learning detectors')
moved = h[a:b]
h = h[:a] + h[b:]
a2, b2 = block(h, 'Detector families')
h = h[:b2] + moved + h[b2:]
t = titles(h)
assert t[17:21] == ['Detectors through the ages', 'Detector families', 'Deep learning detectors', 'Detector benchmark comparison'], t[17:21]

# ------------------------------------------------------------ 2. ByteTrack slide around a visual example
GREEN, AMBER, INDIGO, RED, GRAY = '#16A34A', '#D97706', '#4F46E5', '#DC2626', '#64748B'
ROAD = '<rect x="0" y="0" width="200" height="110" rx="10" fill="#E2E8F0"/><rect x="0" y="94" width="200" height="4" fill="#CBD5E1"/>'
WALL = '<rect x="100" y="12" width="65" height="90" rx="4" fill="#94A3B8"/>'


def car(x): return '<rect x="%d" y="48" width="30" height="14" rx="4" fill="#64748B"/><rect x="%d" y="58" width="50" height="26" rx="7" fill="#475569"/>' % (x + 10, x)
def box(x, w, col, dash=''): return '<rect x="%d" y="42" width="%d" height="48" fill="none" stroke="%s" stroke-width="%s"%s/>' % (x, w, col, '2.5' if dash == 'pred' else '4', ' stroke-dasharray="8 5"' if dash else '')
def label(x, txt, col): return '<text x="%d" y="34" font-family="Inter,Helvetica" font-weight="800" font-size="22" fill="%s">%s</text>' % (x, col, txt)


frames = [
    ('Frame 100', GREEN, ROAD + WALL + car(10) + box(4, 62, GREEN) + label(6, '0.85', GREEN),
     '<b style="color:#15803D">0.85 · strong</b><br>matched first', 'ID 7', True),
    ('Frame 101', GREEN, ROAD + WALL + car(40) + box(34, 62, GREEN) + label(36, '0.72', GREEN),
     '<b style="color:#15803D">0.72 · strong</b><br>matched first', 'ID 7', True),
    ('Frame 102', AMBER, ROAD + car(70) + WALL + box(64, 62, GRAY, 'pred') + box(64, 40, AMBER, 'weak') + label(8, '0.30', '#B45309'),
     '<b style="color:#B45309">0.30 · weak</b> — half hidden<br><b>second chance:</b> fits the dashed predicted box (overlap 0.75) → same car', 'ID 7', True),
    ('Frames 103–105', INDIGO, ROAD + car(105) + WALL + box(99, 62, GRAY, 'pred') + label(8, 'no box', RED),
     '<b style="color:#B91C1C">no box</b> — fully hidden<br><b>track buffer:</b> keep ID 7 and wait', 'ID 7 · waiting', False),
    ('Frame 106', GREEN, ROAD + WALL + car(140) + box(134, 62, GREEN) + label(136, 'box', GREEN),
     '<b style="color:#15803D">box again</b><br>near the predicted place → <b>the old track</b>', 'ID 7', True),
]
cells = []
for name, col, svg, text, idtxt, active in frames:
    pill = ('<span class="pill" style="background:#DCFCE7;color:#166534;font-size:22px">%s</span>' if active
            else '<span class="pill" style="background:#E0E7FF;color:#3730A3;font-size:22px">%s</span>') % idtxt
    cells.append('<div class="card col" style="padding:8px 10px;gap:6px;border-top:6px solid %s;min-width:0">'
                 '<div class="strong" style="font-size:22px">%s</div>'
                 '<svg viewBox="0 0 200 110" style="display:block;flex:0 0 auto;width:100%%;height:118px">%s</svg>'
                 '<p style="font-size:21px;line-height:1.25;margin:0">%s</p>'
                 '<div style="margin-top:auto">%s</div></div>' % (col, name, svg, text, pill))

body = '''<div class="s-body col" style="gap:12px">
    <div class="meaning"><div class="tag">The main idea</div><p>ByteTrack’s job is to keep the <b>same ID</b> for an object — even when the detector is <b>unsure</b> (low score) or <b>misses it</b> for a few frames.</p></div>
    <div class="g3" style="gap:14px">
      <div class="card" style="border-left:6px solid #16A34A;padding:8px 16px"><p style="font-size:23px;margin:0"><b>Strong box</b> · score ≥ 0.50<br>matched to the tracks <b>first</b></p></div>
      <div class="card" style="border-left:6px solid #D97706;padding:8px 16px"><p style="font-size:23px;margin:0"><b>Weak box</b> · score 0.10 – 0.50<br>gets a <b>second chance</b></p></div>
      <div class="card" style="border-left:6px solid #4F46E5;padding:8px 16px"><p style="font-size:23px;margin:0"><b>No box</b><br>keep the track and <b>wait</b> up to 30 frames</p></div>
    </div>
    <div class="ex-label">Example · one car with ID 7 drives behind a wall</div>
    <div class="noabbr" style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px">
      ''' + '\n      '.join(cells) + '''
    </div>
    <div class="g2" style="gap:14px">
      <div class="note" style="border-left-color:var(--good);font-size:22px;margin:0"><b>ByteTrack:</b> ID 7 → 7 → 7 → 7 → 7 · <b>the same ID the whole time</b> ✓</div>
      <div class="note" style="border-left-color:var(--bad);font-size:22px;margin:0"><b>A simple tracker</b> (drops weak boxes, no waiting): ID 7 → 7 → lost → lost → <b>new ID 8</b> ✗ = an <b>ID switch</b></div>
    </div>
  </div>
'''
i_bt = h.index('data-title="ByteTrack baseline"')
e_bt = h.index('</section>', i_bt)
b0 = h.index('<div class="s-body col" style="gap:14px">', i_bt)
b1 = h.index('  <footer class="s-foot">', i_bt)
assert i_bt < b0 < b1 < e_bt and 'Example · one car with ID 7' in h[b0:b1]
h = h[:b0] + body + h[b1:]
h = rep(h, '<span class="prov p-illus">Worked example · illustration settings 0.50 / 0.10 / 30 · our tuned ByteTrack uses 0.18 / 0.04 / 45</span>',
        '<span class="prov p-illus">Worked example · illustration settings 0.50 / 0.10 / 30 and the simple-tracker line are illustrations · our tuned ByteTrack uses 0.18 / 0.04 / 45</span>')
i_bt = h.index('data-title="ByteTrack baseline"')
n0 = h.index('<aside class="notes">', i_bt)
n1 = h.index('</aside>', n0) + len('</aside>')
assert n1 < h.index('</section>', i_bt)
h = h[:n0] + '''<aside class="notes"><p><b>Say:</b> "ByteTrack has one job: keep the same ID for each object, even when the detector is unsure or misses it for a moment. It sorts every box into three cases. A strong box, score 0.50 or more, is matched to the tracks first. A weak box, between 0.10 and 0.50, is not thrown away — it gets a second chance. And if there is no box at all, ByteTrack keeps the track and waits, up to 30 frames."</p><p><b>Example:</b> "Follow car ID 7. Frames 100 and 101: strong boxes, 0.85 and 0.72 — matched first, ID 7. Frame 102: the car goes half behind a wall and the score drops to 0.30. That is a weak box. ByteTrack compares it with the place where it predicted the car to be — the dashed box. The overlap is 0.75, so it is the same car: still ID 7. Frames 103 to 105: the car is fully hidden, there is no box. ByteTrack does not delete the track — it waits. Frame 106: the car comes out near the predicted place and gets its old ID 7 back."</p><p><b>Why it matters:</b> "A simple tracker that throws away weak boxes and does not wait would lose the car at frame 102 and give it a new ID, 8, when it comes back. That is an ID switch. ByteTrack avoids it."</p><p><b>If asked for the exact steps:</b> 1 split the boxes into strong and weak · 2 predict where each track moved (Kalman filter) · 3 round 1: match strong boxes by overlap (IoU) · 4 round 2: match weak boxes to the tracks still left · 5 no box → keep the track for the track buffer; too long → delete it. Our tuned ByteTrack uses high 0.18, low 0.04, buffer 45.</p></aside>''' + h[n1:]

t = titles(h)
assert len(t) == 94 and re.findall(r'slides \d+ - \d+', h) == outline_before
save("index.html", h)
print("ok · 19 =", t[18], "· 20 =", t[19], "· slides", len(t))
