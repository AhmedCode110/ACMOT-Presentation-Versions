#!/usr/bin/env python3
"""v25 (from v24):
 1. titles that wrap onto two lines no longer run into the slide content: fitSlide() in script.js first shrinks the
    title a little (52 → at most 40 px) and, if still needed, moves the content down (edited directly in script.js);
 2. the slide "Before Deep Learning: Traditional Detectors" is removed (author request); Outline ranges updated."""
import os, re

P = os.path.expanduser("~/Desktop/ACMOT-Presentation-Versions/versions/v25-titles-fit/index.html")
h = open(P, encoding="utf-8").read()

if 'data-title="Traditional detectors"' in h:
    i = h.index('data-title="Traditional detectors"')
    a = h.rindex('<section', 0, i)
    b = h.index('</section>', i) + len('</section>')
    b = b + len(h[b:]) - len(h[b:].lstrip('\n'))
    h = h[:a] + h[b:]
assert 'data-title="Traditional detectors"' not in h

mm = h[:h.index('<div class="overlay xview"')]
tags = re.findall(r'<section class="slide[^"]*"[^>]*>', mm)
start = {re.search(r'id="(sec-\d+)"', t).group(1): k for k, t in enumerate(tags, 1) if re.search(r'id="(sec-\d+)"', t)}
od = sorted(start.items(), key=lambda kv: kv[1])
rng = {k: (v, (od[j + 1][1] - 1) if j + 1 < len(od) else len(tags) - 1) for j, (k, v) in enumerate(od)}


def fix_range(m):
    g = m.group(1)
    return f'<button class="ol-row" data-goto="{g}">' + re.sub(r'slides \d+ - \d+', f'slides {rng[g][0]} - {rng[g][1]}', m.group(2))


h, n = re.subn(r'<button class="ol-row" data-goto="(sec-\d+)">(.*?</button>)', fix_range, h)
assert n == 9, n
open(P, "w", encoding="utf-8").write(h)
print("ok · slides:", len(tags), rng)

# ------------------------------------------------------------ 3. bigger text: the deep-learning detector table and every tiny size
h = open(P, encoding="utf-8").read()
i = h.index('data-title="Deep learning detectors"')
a = h.rindex('<section', 0, i)
b = h.index('</section>', i)
seg = h[a:b]
table = '''<table class="tbl noabbr" style="font-size:24px">
      <tr><th>Year</th><th style="text-align:left">Detector</th><th style="text-align:left">Family</th><th style="text-align:left">How it works</th><th>mAP · time</th><th style="text-align:left">Strong / weak</th></tr>
      <tr><td>2014</td><td style="text-align:left" class="strong">R-CNN</td><td style="text-align:left">two-stage</td><td style="text-align:left">regions → a CNN on each</td><td>—</td><td style="text-align:left"><span class="good">+ big accuracy jump</span> · <span class="bad">− very slow</span></td></tr>
      <tr><td>2015</td><td style="text-align:left" class="strong">Faster R-CNN</td><td style="text-align:left">two-stage</td><td style="text-align:left">one network finds and checks</td><td>37.0 · 172 ms</td><td style="text-align:left"><span class="good">+ accurate</span> · <span class="bad">− too slow for video</span></td></tr>
      <tr><td>2016</td><td style="text-align:left" class="strong">YOLO</td><td style="text-align:left">one-stage</td><td style="text-align:left">one look, a grid of boxes</td><td>—</td><td style="text-align:left"><span class="good">+ very fast</span> · <span class="bad">− misses small objects</span></td></tr>
      <tr><td>2018</td><td style="text-align:left" class="strong">YOLOv3</td><td style="text-align:left">one-stage</td><td style="text-align:left">boxes at three sizes</td><td>31.0 · 28.6 ms</td><td style="text-align:left"><span class="good">+ real-time</span> · <span class="bad">− lower accuracy</span></td></tr>
      <tr><td>2020</td><td style="text-align:left" class="strong">DETR R101</td><td style="text-align:left">transformer</td><td style="text-align:left">attention on the whole image</td><td>42.9 · 145 ms</td><td style="text-align:left"><span class="good">+ simple design</span> · <span class="bad">− very slow</span></td></tr>
      <tr class="sel"><td>2023</td><td style="text-align:left" class="strong">YOLOv8n</td><td style="text-align:left">one-stage</td><td style="text-align:left">small YOLO, no anchor boxes</td><td>37.3 · 3.2 ms</td><td style="text-align:left"><span class="good">+ tiny, fast</span> · <span class="bad">− less accurate</span></td></tr>
      <tr><td>2025</td><td style="text-align:left" class="strong">YOLO12m</td><td style="text-align:left">one-stage</td><td style="text-align:left">YOLO with attention</td><td>52.5 · 4.86 ms</td><td style="text-align:left"><span class="good">+ accurate, real-time</span> · <span class="bad">− bigger</span></td></tr>
      <tr><td>2025</td><td style="text-align:left" class="strong">RF-DETR-S</td><td style="text-align:left">transformer</td><td style="text-align:left">a real-time DETR</td><td class="best">52.9 · 3.5 ms</td><td style="text-align:left"><span class="good">+ best trade-off</span> · <span class="bad">− bigger</span></td></tr>
    </table>'''
seg, n = re.subn(r'<table class="tbl" style="font-size:22px">.*?</table>', table, seg, count=1, flags=re.S)
assert n == 1, n
h = h[:a] + seg + h[b:]

# inline sizes below 20 px on slides and explanation pages → at least 20 px
bump = {'15px': '19px', '16px': '20px', '17px': '20px', '18px': '20px', '19px': '21px'}
h, n_inline = re.subn(r'font-size:(1[5-9]px)', lambda m: 'font-size:' + bump[m.group(1)], h)
# SVG drawing labels below 20 → +2
h, n_svg = re.subn(r'font-size="(1[4-8])"', lambda m: f'font-size="{int(m.group(1)) + 2}"', h)
open(P, "w", encoding="utf-8").write(h)

C = os.path.join(os.path.dirname(P), "styles.css")
c = open(C, encoding="utf-8").read()
assert "v25: no tiny text" not in c
c += """
/* v25: no tiny text (author request) */
.s-foot .prov,.prov{font-size:20px}
.xbtn,.s-foot .ex-btn{font-size:21px}
.xbtn .xi,.s-foot .ex-btn .ex-i{font-size:19px}
.origin{font-size:19px}
.img .lbl{font-size:21px}
.abbr-x{font-size:.9em}
.cval.sm{font-size:21px}.ctick{font-size:21px}
"""
open(C, "w", encoding="utf-8").write(c)
print("ok · inline sizes bumped:", n_inline, "· svg labels bumped:", n_svg)

# ------------------------------------------------------------ 4. Old AC-MOT on the test set, after the validation ablation
h = open(P, encoding="utf-8").read()
if 'data-title="Old AC-MOT on the test set"' not in h:
    test_slide = '''<section class="slide" data-sec="5" data-secname="V · Setup &amp; first result" data-title="Old AC-MOT on the test set">
  <header class="s-head"><div class="kicker">Section V · Test set</div><h2>Old AC-MOT on the Test Set</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>After the ablation on <b>validation</b>, the full old AC-MOT was run <b>once on the test set</b>. It beat the baseline on every metric.</p></div>
    <div class="row grow" style="gap:16px"><div class="card" style="flex:1.6;padding:10px 14px"><div class="chart zoomable" data-chart="init-quality"></div></div><div class="card grow" style="padding:10px 14px"><div class="chart zoomable" data-chart="init-ids"></div></div><div class="card grow" style="padding:10px 14px"><div class="chart zoomable" data-chart="init-fps"></div></div></div>
    <table class="tbl" style="font-size:25px">
      <tr><th style="text-align:left">System</th><th>MOTA ↑</th><th>HOTA ↑</th><th>IDF1 ↑</th><th>IDS ↓</th><th>FPS ↑</th></tr>
      <tr><td>Baseline</td><td>19.729</td><td>28.430</td><td>32.724</td><td>1235</td><td>36.53</td></tr>
      <tr class="sel"><td>Old AC-MOT</td><td class="best">23.236</td><td class="best">32.698</td><td class="best">39.516</td><td class="best">1061</td><td class="best">41.96</td></tr>
      <tr><td class="strong">Change</td><td class="best">+3.507</td><td class="best">+4.268</td><td class="best">+6.792</td><td class="best">174 fewer</td><td class="best">+5.43</td></tr>
    </table>
  </div>
  <footer class="s-foot"><span class="prov p-test">Test set · VisDrone2019-MOT test-dev · 17 sequences · our custom AC-MOT protocol</span></footer>
  <aside class="notes"><p><b>Say:</b> "The ablation was done on the validation videos. Then the full old AC-MOT was run once on the 17 test videos: MOTA went from 19.729 to 23.236, HOTA from 28.430 to 32.698, IDF1 from 32.724 to 39.516, ID switches from 1235 to 1061, and speed from 36.53 to 41.96 FPS."</p></aside>
</section>

'''
    i = h.index('data-title="Ablation result"')
    a = h.rindex('<section', 0, i)
    b = h.index('</section>', i) + len('</section>')
    b = b + len(h[b:]) - len(h[b:].lstrip('\n'))
    h = h[:b] + test_slide + h[b:]
    # say "validation" clearly on the two ablation slides
    h = h.replace('<div class="kicker">Section V · Ablation study</div>', '<div class="kicker">Section V · Ablation study · validation</div>', 1)
    h = h.replace('<div class="kicker">Section V · Ablation result</div>', '<div class="kicker">Section V · Ablation result · validation</div>', 1)
    mm = h[:h.index('<div class="overlay xview"')]
    tags = re.findall(r'<section class="slide[^"]*"[^>]*>', mm)
    start = {re.search(r'id="(sec-\d+)"', t).group(1): k for k, t in enumerate(tags, 1) if re.search(r'id="(sec-\d+)"', t)}
    od = sorted(start.items(), key=lambda kv: kv[1])
    rng = {k: (v, (od[j + 1][1] - 1) if j + 1 < len(od) else len(tags) - 1) for j, (k, v) in enumerate(od)}
    h, n = re.subn(r'<button class="ol-row" data-goto="(sec-\d+)">(.*?</button>)', fix_range, h)
    assert n == 9
    open(P, "w", encoding="utf-8").write(h)
    print("ok · old AC-MOT test slide added · slides:", len(tags), rng)
