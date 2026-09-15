#!/usr/bin/env python3
"""v23 (from v22):
 1. 'ByteTrack baseline' slide: the paper figure is replaced by a worked example (car ID 7, frames 100–106)
    that shows the second chance for a weak box and the track buffer when there is no box;
 2. 'ID switches on MOT17': states the trade-off between tracking accuracy (MOTA) and ID switches;
 3. 'Conclusions of the survey': every headline number says exactly what changed, from what to what."""
import os, re

ROOT = os.path.expanduser("~/Desktop/ACMOT-Presentation-Versions/versions/v23-bytetrack-worked-example")


def load(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def save(p, s): open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)


def rep(s, old, new, n=1):
    assert s.count(old) == n, (s.count(old), old[:110])
    return s.replace(old, new)


def slide_span(h, title):
    i = h.index(f'data-title="{title}"')
    a = h.rindex('<section', 0, i)
    return a, h.index('</section>', i) + len('</section>')


h = load("index.html")

# ------------------------------------------------------------ 1. ByteTrack worked example on the slide
bytetrack = '''<section class="slide" data-sec="2" data-secname="II · Related work" data-title="ByteTrack baseline" data-explain="x-bytetrack|How ByteTrack Works">
  <header class="s-head"><div class="kicker">Section II · Trackers</div><h2>ByteTrack: The Baseline of This Work</h2></header>
  <div class="s-body col" style="gap:14px">
    <div class="row grow" style="gap:22px">
      <div class="col" style="flex:0 0 560px;gap:8px">
        <div class="ex-label">Every frame, step by step</div>
        <table class="tbl" style="font-size:21px">
          <tr><th>Step</th><th style="text-align:left">What happens</th></tr>
          <tr><td class="strong">1</td><td style="text-align:left">split the boxes: <b>strong</b> (score ≥ high) and <b>weak</b> (between low and high)</td></tr>
          <tr><td class="strong">2</td><td style="text-align:left"><b>predict</b> where each track moved (Kalman filter)</td></tr>
          <tr><td class="strong">3</td><td style="text-align:left"><b>round 1:</b> match <b>strong</b> boxes to the tracks by overlap (IoU)</td></tr>
          <tr><td class="strong">4</td><td style="text-align:left"><b>round 2:</b> give <b>weak</b> boxes a <b>second chance</b> with the tracks still left</td></tr>
          <tr><td class="strong">5</td><td style="text-align:left">no box at all → keep the track for the <b>track buffer</b>; too long → delete it</td></tr>
        </table>
        <div class="pills"><span class="pill">example settings: high 0.50</span><span class="pill">low 0.10</span><span class="pill">buffer 30 frames</span></div>
      </div>
      <div class="col grow" style="gap:8px;min-width:0">
        <div class="ex-label">Example · one car with ID 7</div>
        <table class="tbl" style="font-size:21px">
          <tr><th>Frame</th><th>Score</th><th style="text-align:left">What ByteTrack does</th><th>ID</th></tr>
          <tr><td>100</td><td>0.85</td><td style="text-align:left"><b class="good">strong</b> (≥ 0.50) → matched in round 1</td><td class="strong">7</td></tr>
          <tr><td>101</td><td>0.72</td><td style="text-align:left"><b class="good">strong</b> → matched in round 1</td><td class="strong">7</td></tr>
          <tr class="sel"><td>102</td><td>0.30</td><td style="text-align:left">half hidden → <b style="color:#B45309">weak</b> (0.10–0.50) · <b>second chance</b>: overlap with the predicted box IoU 0.75 → same car</td><td class="strong">7</td></tr>
          <tr><td>103–105</td><td>—</td><td style="text-align:left"><b class="bad">no box at all</b> → track kept in the <b>track buffer</b></td><td class="strong">7 <span class="muted" style="font-weight:600">(waiting)</span></td></tr>
          <tr class="sel"><td>106</td><td>box</td><td style="text-align:left">the car comes back near the predicted place → <b>matched to the old track</b></td><td class="strong">7</td></tr>
        </table>
      </div>
    </div>
    <div class="g2" style="gap:18px">
      <div class="card" style="border-left:6px solid #B45309;padding:10px 18px"><h3 style="margin:0 0 4px;font-size:26px">Second chance</h3><p style="font-size:23px">A box <b>exists</b>, but its score is <b>low</b>. ByteTrack still uses it instead of throwing it away.</p></div>
      <div class="card" style="border-left:6px solid #4F46E5;padding:10px 18px"><h3 style="margin:0 0 4px;font-size:26px">Track buffer</h3><p style="font-size:23px">There is <b>no box at all</b>. The track is <b>kept for up to 30 frames</b>; if the car is gone longer, it later gets a <b>new ID</b>.</p></div>
    </div>
  </div>
  <footer class="s-foot"><span class="prov p-illus">Worked example · illustration settings 0.50 / 0.10 / 30 · our tuned ByteTrack uses 0.18 / 0.04 / 45</span></footer>
  <aside class="notes"><p><b>Say:</b> "In every frame ByteTrack does two things. First it matches the strong boxes. Then, if some tracks are still unmatched, it gives the weak boxes a second chance."</p><p><b>Example:</b> "Take a car with ID 7 and example settings high 0.50, low 0.10, buffer 30. Frames 100 and 101: scores 0.85 and 0.72 — strong, so it keeps ID 7. Frame 102: the car is half hidden and the score drops to 0.30. That is below 0.50, so it is not in round 1, but above 0.10, so ByteTrack keeps it as a weak box. Round 2 compares it with the predicted place: IoU 0.75, so it is the same car — still ID 7. That is the second chance."</p><p><b>Then:</b> "Frames 103 to 105: no box at all. The second chance cannot help, because there is nothing to match. Now the track buffer works: ByteTrack keeps ID 7 for up to 30 frames. In frame 106 the car comes back near the predicted place and gets ID 7 again, not a new ID. If it had been gone longer than the buffer, the old track would be deleted and the car would get a new ID."</p><p><b>Key difference:</b> "Second chance: a box exists but its score is low. Track buffer: there is no box, so the tracker keeps the track for a while."</p></aside>
</section>'''
a, b = slide_span(h, "ByteTrack baseline")
h = h[:a] + bytetrack + h[b:]

# ------------------------------------------------------------ 2. MOTA vs ID switches trade-off
h = rep(h, '<div class="note"><b>Note:</b> the order flipped. SORT is by far the worst on identity. ByteTrack has the best MOTA here but only average ID switches. One number is never enough.</div>',
        '<div class="note"><b>Trade-off:</b> the order flipped. ByteTrack has the <b>highest MOTA</b> of these trackers (80.3) but <b>not the fewest ID switches</b> (2,196 vs 784 for OC-SORT). Higher tracking accuracy does <b>not</b> always mean more stable IDs.</div>')

# ------------------------------------------------------------ 3. survey headline numbers, exactly
a, b = slide_span(h, "Conclusions of the survey")
seg = h[a:b]
kpis = '''<div class="g4" style="gap:16px">
      <div class="kpi"><div class="l">Speed · time per image</div><div class="v" style="font-size:34px">~49× faster</div><div class="s">Faster R-CNN (2015) <b>172 ms</b> → RF-DETR-S (2025) <b>3.5 ms</b> · 172 ÷ 3.5 ≈ 49</div></div>
      <div class="kpi"><div class="l">Accuracy · COCO mAP</div><div class="v" style="font-size:34px">+43% mAP</div><div class="s">Faster R-CNN (2015) <b>37.0</b> → RF-DETR-S (2025) <b>52.9</b> · (52.9 − 37.0) ÷ 37.0 ≈ 43%</div></div>
      <div class="kpi"><div class="l">Tracking accuracy · MOT17</div><div class="v" style="font-size:34px">81.7% MOTA</div><div class="s">the <b>highest MOTA</b> in our tracker table: <b>SMILEtrack</b></div></div>
      <div class="kpi"><div class="l">Fastest detector</div><div class="v" style="font-size:34px">3.5 ms</div><div class="s">per image: <b>RF-DETR-S</b>, the fastest in the detector table</div></div>
    </div>'''
seg, n = re.subn(r'<div class="g4" style="gap:16px">.*?</div>\n    </div>', kpis, seg, count=1, flags=re.S)
assert n == 1
seg = rep(seg, '<p><b>Say:</b> "The field got much faster and more accurate, but no model wins everywhere.',
          '<p><b>Say:</b> "From Faster R-CNN in 2015 to RF-DETR-S in 2025, the time per image dropped from 172 to 3.5 milliseconds — about 49 times faster — and COCO accuracy rose from 37.0 to 52.9 mAP, about 43 percent higher. The field got much faster and more accurate, but no model wins everywhere.')
h = h[:a] + seg + h[b:]
save("index.html", h)

m = load("assets/data/meaning.js")
m = rep(m, "t: 'Judged on <b>ID switches</b>, the ranking changes: the most accurate tracker is <b>not</b> the one that keeps IDs best. <b>One number is never enough.</b>' }",
        "t: 'Judged on <b>ID switches</b>, the ranking changes: the most accurate tracker is <b>not</b> the one that keeps IDs best. There is a <b>trade-off between tracking accuracy (MOTA) and ID switches</b> — <b>one number is never enough.</b>' }")
m = rep(m, "t: 'ByteTrack matches boxes to tracks in <b>two rounds</b>: strong boxes first, then <b>weak boxes get a second chance</b>. That is why the detector’s confidence setting matters so much.' }",
        "t: 'ByteTrack matches <b>strong boxes first</b>, then gives <b>weak boxes a second chance</b>. If there is <b>no box at all</b>, it keeps the track for a while (the <b>track buffer</b>) before giving a new ID.' }")
save("assets/data/meaning.js", m)
print("ok")
