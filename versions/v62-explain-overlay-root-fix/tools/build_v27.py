#!/usr/bin/env python3
"""v27 (from v26), requested by the author on 2026-09-15:
1. 'IoU vs NMS' slide: the NMS half was not clear. It now shows a labelled before / after drawing (two close cars,
   a score on every box) and a decision table: each box -> its IoU with the kept 0.9 box -> keep or delete, plus the
   rule (big overlap = copy -> delete; small overlap = another object -> keep). Example numbers are an illustration.
2. 'From a Frame to SCI - All Steps Together' (slide 46) moves right after 'The Idea: Measure the Scene, Then Set the
   Detector' (slide 38), as the overview before the step details. The 'details: slides x-y' labels on the idea slide
   are recomputed from the new order (they were one slide off since v25).
3. 'The VisDrone2019-MOT Benchmark': says how big the whole VisDrone2019 benchmark is (288 video clips, 262K frames -
   the value already in the survey dataset table of the deck) and how many sequences this work uses (7 + 17 = 24).
4. 'How We Score Every System - the Same Way' (Section V, slide 57) deleted; its explanation topic stays reachable from
   the classes and ground-truth filtering slides. Outline ranges recomputed (94 slides).
5. Ablation table: next to every OLD-A1 ... OLD-A3 value, the change against OLD-A0 in percent of the A0 value
   (green = better, red = worse; for IDS fewer is better), a legend line and a notes sentence. Computed from the
   author's table, which is checked against results.js -> oldAblation."""
import os, re

ROOT = os.path.expanduser("~/Desktop/ACMOT-Presentation-Versions/versions/v27-nms-clear-sci-overview-first")


def load(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def save(p, s): open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)


def rep(s, old, new, n=1):
    assert s.count(old) == n, (s.count(old), old[:110])
    return s.replace(old, new)


def main_part(h): return h[:h.index('<div class="overlay xview"')]


def slide_tags(h): return re.findall(r'<section class="slide[^"]*"[^>]*>', main_part(h))


h = load("index.html")
assert len(slide_tags(h)) == 95

# ------------------------------------------------------------ 1. clearer NMS card
start_s = '<div class="card sec col" style="gap:8px"><div class="tag">NMS · Non-Maximum Suppression</div>'
assert h.count(start_s) == 1
a = h.index(start_s)
b = h.index('</g></svg></div>', a) + len('</g></svg></div>')
assert 'After NMS: 1 box' in h[a:b] and b - a < 3000

nms = '''<div class="card sec col" style="gap:10px"><div class="tag">NMS · Non-Maximum Suppression</div>
        <p>NMS keeps the <b>best box</b> and deletes its <b>copies</b> — it uses <b>IoU</b> to find them.</p>
        <svg viewBox="0 0 720 222" width="100%" height="216" style="flex:0 0 auto;display:block"><g font-family="Inter,Helvetica" font-weight="800" font-size="30">
          <text x="20" y="28" fill="#334155">Before NMS: 4 boxes</text>
          <rect x="20" y="40" width="300" height="172" rx="10" fill="#F1F5F9"/>
          <rect x="80" y="92" width="110" height="52" rx="8" fill="#475569"/><rect x="210" y="100" width="72" height="42" rx="8" fill="#64748B"/>
          <rect x="60" y="70" width="150" height="90" fill="none" stroke="#16A34A" stroke-width="5"/>
          <rect x="68" y="75" width="150" height="90" fill="none" stroke="#F59E0B" stroke-width="3"/>
          <rect x="77" y="80" width="150" height="90" fill="none" stroke="#EF4444" stroke-width="3"/>
          <rect x="195" y="85" width="100" height="70" fill="none" stroke="#2563EB" stroke-width="4"/>
          <text x="60" y="62" fill="#16A34A">0.9</text><text x="68" y="198" fill="#D97706">0.8</text><text x="150" y="198" fill="#DC2626">0.7</text><text x="250" y="78" fill="#2563EB">0.6</text>
          <path d="M328 126h40" stroke="#94A3B8" stroke-width="5"/><path d="M364 112l20 14-20 14z" fill="#94A3B8"/>
          <text x="400" y="28" fill="#15803D">After NMS: 2 boxes</text>
          <rect x="400" y="40" width="300" height="172" rx="10" fill="#F1F5F9"/>
          <rect x="460" y="92" width="110" height="52" rx="8" fill="#475569"/><rect x="590" y="100" width="72" height="42" rx="8" fill="#64748B"/>
          <rect x="440" y="70" width="150" height="90" fill="none" stroke="#16A34A" stroke-width="5"/>
          <rect x="575" y="85" width="100" height="70" fill="none" stroke="#2563EB" stroke-width="4"/>
          <text x="440" y="62" fill="#16A34A">0.9</text><text x="630" y="78" fill="#2563EB">0.6</text>
        </g></svg>
        <table class="tbl">
          <tr><th>Box</th><th>Score</th><th>IoU with 0.9 box</th><th style="text-align:left">Decision</th></tr>
          <tr><td class="strong" style="color:#16A34A">A · green</td><td>0.9</td><td>—</td><td style="text-align:left"><b class="good">keep</b> · best score</td></tr>
          <tr><td class="strong" style="color:#D97706">A · orange</td><td>0.8</td><td>0.80</td><td style="text-align:left"><b class="bad">delete</b> · copy</td></tr>
          <tr><td class="strong" style="color:#DC2626">A · red</td><td>0.7</td><td>0.65</td><td style="text-align:left"><b class="bad">delete</b> · copy</td></tr>
          <tr><td class="strong" style="color:#2563EB">B · blue</td><td>0.6</td><td>0.05</td><td style="text-align:left"><b class="good">keep</b> · other car</td></tr>
        </table>
        <div class="note" style="font-size:22px"><b>Rule:</b> IoU with the kept box <b>above 0.45</b> = a <b>copy</b> → delete. <b>Below 0.45</b> = a <b>different object</b> → keep. <b>Result: 2 cars → 2 boxes.</b></div></div>'''
h = h[:a] + nms + h[b:]

h = rep(h, '''<p><b>Then:</b> "NMS is a cleaning step inside the detector. When it draws several boxes on the same car, it keeps the one with the highest score and deletes the others that overlap it too much — and it measures that overlap with IoU."</p></aside>''',
        '''<p><b>Then:</b> "NMS is a cleaning step inside the detector. Here the detector drew three boxes on car A, with scores 0.9, 0.8 and 0.7, and one box on car B with score 0.6. NMS keeps the highest score, 0.9. Then it measures the IoU of every other box with that kept box. The orange box overlaps it 0.80 and the red box 0.65 — both above the limit 0.45, so they are copies of the same car and are deleted. The blue box overlaps it only 0.05 — it is a different car, so it stays. Two cars, two boxes."</p><p><b>Note:</b> the scores, IoU values and the 0.45 limit are an illustration.</p></aside>''')

# provenance label for the illustration numbers
i9 = h.index('data-title="IoU vs NMS"')
e9 = h.index('</section>', i9)
assert 's-foot' not in h[i9:e9]
h = h[:e9] + '  <footer class="s-foot"><span class="prov p-illus">Illustration · NMS example scores, IoU values and the 0.45 limit</span></footer>\n' + h[e9:]
h = rep(h, '''<table class="tbl">
          <tr><th>Box</th>''', '''<table class="tbl">
          <tr><th>Box</th>''')  # uniqueness check

# ------------------------------------------------------------ 2. move "All Steps Together" after the idea slide
mv_s = '<section class="slide" data-sec="4" data-secname="IV · AC-MOT" data-title="SCI from frame to score"'
assert h.count(mv_s) == 1
m0 = h.index(mv_s)
m1 = h.index('</section>', m0) + len('</section>')
m1 += len(h[m1:]) - len(h[m1:].lstrip('\n'))
block = h[m0:m1]
h = h[:m0] + h[m1:]
block = rep(block, '<div class="kicker">Section IV · Steps 1 and 2 together</div>', '<div class="kicker">Section IV · The whole path first</div>')
block = rep(block, '<p><b>Say:</b> "Seven small steps turn a frame into one stable difficulty number."</p>',
            '<p><b>Say:</b> "Before the details, here is the whole path at once. Seven small steps turn a frame into one stable difficulty number, and that number sets the detector. The next slides explain each step."</p>')

i38 = h.index('data-title="What we add"')
e38 = h.index('</section>', i38) + len('</section>')
e38 += len(h[e38:]) - len(h[e38:].lstrip('\n'))
h = h[:e38] + block + h[e38:]

mm = main_part(h)
secs = [mm[s.start():] for s in re.finditer(r'<section class="slide', mm)]
titles = [re.search(r'<h2>(.*?)</h2>', s).group(1) if re.search(r'<h2>(.*?)</h2>', s[:s.find('</section>')]) else '' for s in secs]
k_idea = next(k for k, s in enumerate(secs, 1) if s.startswith('<section class="slide" data-sec="4" data-secname="IV · AC-MOT" data-title="What we add"'))
assert 'All Steps Together' in titles[k_idea], titles[k_idea]
steps = {}
for n in (1, 2, 3):
    ks = [k for k, t in enumerate(titles, 1) if t.startswith(f'Step {n}:')]
    assert ks == list(range(ks[0], ks[-1] + 1)), (n, ks)
    steps[n] = (ks[0], ks[-1])
print('steps', steps)
old = re.findall(r'details: slides \d+–\d+', h)
assert len(old) == 3, old
for n, o in zip((1, 2, 3), old):
    h = rep(h, f'<p class="muted" style="margin-top:auto;font-size:21px;font-weight:700">{o}</p>',
            f'<p class="muted" style="margin-top:auto;font-size:21px;font-weight:700">details: slides {steps[n][0]}–{steps[n][1]}</p>')

# ------------------------------------------------------------ 3. VisDrone slide: size of the whole benchmark
assert h.count('288 videos, 262K frames') == 1  # survey dataset table (Related Work)
h = rep(h, '<tr><td>Resolution</td><td>1920 × 1080 (Full HD)</td></tr>',
        '<tr><td>Whole benchmark</td><td><b>288 video clips · 262K frames</b> (all VisDrone2019 tasks)</td></tr>\n        <tr><td>Resolution</td><td>1920 × 1080 (Full HD)</td></tr>')
h = rep(h, '<tr><td>Density</td>',
        '<tr><td>Used in this work</td><td>7 + 17 = <b>24 sequences</b> of the tracking (MOT) part</td></tr>\n        <tr><td>Density</td>')
h = rep(h, '<span class="prov p-test">Split sizes and box count from the final evaluation runs (TrackEval GT count)</span>',
        '<span class="prov p-test">Split sizes and box count from the final evaluation runs (TrackEval GT count) · whole-benchmark size from our survey table</span>')
h = rep(h, '<p><b>Say:</b> "VisDrone is full-HD drone video with objects only 5 to 30 pixels wide. We tune on 7 validation videos and test on 17 test-dev videos."</p>',
        '<p><b>Say:</b> "VisDrone2019 is a large drone benchmark: 288 video clips with about 262 thousand frames, for several tasks. It is full-HD drone video with objects only 5 to 30 pixels wide. For tracking we use 24 sequences: we tune on 7 validation videos and test on 17 test-dev videos."</p>')

# ------------------------------------------------------------ 5. ablation table: percent change vs OLD-A0
ab_rows = [('OLD-A0', 17.633, 29.837, 30.892, 283, 44.09), ('OLD-A1', 17.802, 30.864, 32.854, 217, 44.51),
           ('OLD-A2', 17.636, 31.384, 33.727, 210, 40.65), ('OLD-A2R', 18.425, 32.446, 35.669, 241, 39.56),
           ('OLD-A3', 18.165, 33.064, 36.296, 271, 37.96)]
rj = load("assets/data/results.js")
for sid, *v in ab_rows:  # the slide table must equal results.js -> oldAblation
    pat = r"name: '%s · [^']*',\s*mota: %s, hota: %s, idf1: %s, ids: %d, fps: %s " % (re.escape(sid), v[0], v[1], v[2], v[3], v[4])
    assert re.search(pat, rj), sid
better_up = [True, True, True, False, True]
base = ab_rows[0][1:]


def pct(v, b):
    x = (v - b) / b * 100
    return (('%+.2f%%' if abs(x) < 0.1 else '%+.1f%%') % x).replace('-', '−'), x


i_ab = h.index('data-title="Ablation study"')
t0 = h.index('<table class="tbl" style="font-size:22px">', i_ab)
t1 = h.index('</table>', t0)
tbl = h[t0:t1]
for sid, *v in ab_rows[1:]:
    fmt = ['%.3f%%' % v[0], '%.3f%%' % v[1], '%.3f%%' % v[2], '%d' % v[3], '%.2f' % v[4]]
    rs = tbl.index('<td>%s</td>' % sid)
    re_ = tbl.index('</tr>', rs)
    row = tbl[rs:re_]
    for k in range(5):
        txt, x = pct(v[k], base[k])
        span = '<span class="dlt %s">%s</span>' % ('good' if (x > 0) == better_up[k] else 'bad', txt)
        cell = re.compile(r'(<td(?: class="best")?>)%s(</td>)' % re.escape(fmt[k]))
        assert len(cell.findall(row)) == 1, (sid, fmt[k])
        row = cell.sub(lambda mm, f=fmt[k], sp=span: mm.group(1) + f + sp + mm.group(2), row)
    tbl = tbl[:rs] + row + tbl[re_:]
h = h[:t0] + tbl + h[t1:]
t1 = h.index('</table>', t0) + len('</table>')
h = h[:t1] + '\n    <p class="tiny muted" style="margin:0">Small numbers = change compared with <b>OLD-A0 (baseline)</b>, in percent of its value · <b class="good">green = better</b> · <b class="bad">red = worse</b></p>' + h[t1:]
a3 = ab_rows[4][1:]
ch = [abs(pct(a3[k], base[k])[1]) for k in range(5)]
h = rep(h, '— four different stages win the five metrics."</p></aside>',
        '— four different stages win the five metrics."</p><p><b>Then:</b> "The small numbers show the change against A0 in percent of the A0 value. The full AC-MOT raises MOTA by %.1f%%, HOTA by %.1f%% and IDF1 by %.1f%%, has %.1f%% fewer ID switches, and runs %.1f%% slower."</p><p><b>Note:</b> these are percent of the A0 value, not percentage points.</p></aside>' % tuple(ch))
ss = load("styles.css")
assert '.dlt' not in ss
save("styles.css", ss.rstrip() + "\n/* v27: percent change next to a table value */\n.tbl .dlt{font-size:20px;font-weight:800;margin-left:8px;white-space:nowrap}\n")

# ------------------------------------------------------------ 6. change counts (ID switches, false positives) as percent
# Author's request: a comparison says "14.1% fewer ID switches", not "174 fewer". Percent = difference / the value of
# the system it is compared with (the baseline; V1 on the V2-vs-V1 note). Bootstrap bounds are divided by the
# baseline's full test-set total (1235) - a fixed rescale of the same interval.
def pc(d, ref): return '%.1f%%' % (d / ref * 100)


TD = {'base': 1235, 'old': 1061, 'v1': 1184, 'v2': 919}
for k, v in TD.items():
    assert re.search(r"id: '%s',[^}]*ids: %d," % (k, v), rj), k
assert re.search(r"id: 'v1',[^}]*fp: 19029,", rj) and re.search(r"id: 'v2',[^}]*fp: 13632,", rj)
assert re.search(r"ids: 558, fn: 270189", rj) and re.search(r"ids: 321, fn: 258376", rj)
assert "idsRed: [51, -114, 219]" in rj and "idsRed: [316, 175, 470]" in rj
b0, a3i = ab_rows[0][4], ab_rows[4][4]
# ablation result (validation)
h = rep(h, '<td class="best">12 fewer</td>', '<td class="best">%s fewer</td>' % pc(b0 - a3i, b0))
h = rep(h, '<b>12 fewer ID switches</b>', '<b>%s fewer ID switches</b>' % pc(b0 - a3i, b0))
h = rep(h, 'and there were 12 fewer ID switches. The biggest', 'and there were %s fewer ID switches. The biggest' % pc(b0 - a3i, b0))
# old AC-MOT on the test set
h = rep(h, '<td class="best">174 fewer</td>', '<td class="best">%s fewer</td>' % pc(TD['base'] - TD['old'], TD['base']))
h = rep(h, 'ID switches from 1235 to 1061,', 'ID switches from 1235 to 1061 (%s fewer),' % pc(TD['base'] - TD['old'], TD['base']))
# V1 on the test set + the identity-switch problem
v1p = pc(TD['base'] - TD['v1'], TD['base'])
h = rep(h, '<td class="best">−51</td>', '<td class="best">−%s</td>' % v1p)
h = rep(h, 'IDF1 plus 8.8, 51 fewer ID switches, and 2.5 FPS faster.', 'IDF1 plus 8.8, %s fewer ID switches, and 2.5 FPS faster.' % v1p)
h = rep(h, 'but it removed <b>only 51 ID switches</b>: 1235 → 1184.', 'but it cut ID switches by <b>only %s</b>: 1235 → 1184.' % v1p)
h = rep(h, 'baseline 1235, V1 1184 — only 51 fewer, while', 'baseline 1235, V1 1184 — only %s fewer, while' % v1p)
# V2 on the test set (compared with V1)
v2p, fpp = pc(TD['v1'] - TD['v2'], TD['v1']), pc(19029 - 13632, 19029)
h = rep(h, 'IDS 1184 → 919 (265 fewer) · FPS +7.04 · about 5,397 fewer false positives',
        'IDS 1184 → 919 (%s fewer) · FPS +7.04 · %s fewer false positives' % (v2p, fpp))
h = rep(h, 'But it has 265 fewer ID switches, is 7 FPS faster, and has about 5,397 fewer false positives.',
        'But it has %s fewer ID switches, is 7 FPS faster, and has %s fewer false positives.' % (v2p, fpp))
# bootstrap on ID switches
B = TD['base']


def pcs(v): return ('%.1f%%' % (v / B * 100)).replace('-', '−')


h = rep(h, '<tr><td>V1</td><td>51</td><td>[−114, 219]</td>', '<tr><td>V1</td><td>%s</td><td>[%s, %s]</td>' % (pcs(51), pcs(-114), pcs(219)))
h = rep(h, '<tr><td>V2</td><td class="best">316</td><td>[175, 470]</td>', '<tr><td>V2</td><td class="best">%s</td><td>[%s, %s]</td>' % (pcs(316), pcs(175), pcs(470)))
h = rep(h, '        <div class="callout warn">We <b>cannot</b> say V1 made a significant ID-switch improvement. V2 did.</div>',
        '        <p class="tiny muted" style="margin:0">Percent of the baseline’s %d ID switches on the test set.</p>\n        <div class="callout warn">We <b>cannot</b> say V1 made a significant ID-switch improvement. V2 did.</div>' % B)
h = rep(h, '<p><b>Say:</b> "For ID switches, V1 removes 51, but the interval goes from minus 114 to 219 — it crosses zero, so it is not significant. V2 removes 316, with an interval from 175 to 470 — significant. This is exactly why V2 was needed."</p>',
        '<p><b>Say:</b> "For ID switches, V1 removes %s of the baseline’s ID switches, but the interval goes from minus %s to %s — it crosses zero, so it is not significant. V2 removes %s, with an interval from %s to %s — significant. This is exactly why V2 was needed."</p><p><b>Note:</b> the percents are the bootstrap values divided by the baseline’s %d ID switches (V1: 51 [−114, 219]; V2: 316 [175, 470] ID switches).</p>'
        % (pcs(51), pcs(114), pcs(219), pcs(316), pcs(175), pcs(470), B))
# UAVDT (compared with its own baseline)
h = rep(h, 'IDS <b>−237</b>.', 'IDS <b>−%s</b>.' % pc(558 - 321, 558))
# bootstrap chart in percent of the baseline (the other count-based forest chart is not shown on any slide)
assert 'data-chart="boot-vis-ids"' not in h
j = load("script.js")
j = rep(j, "'boot-ids2': function (h) { var b = D.testdev.bootstrap;\n      forest(h, { xlabel: 'ID switches removed vs Baseline (positive = fewer)', dec: 0, ml: 90, mr: 170, rows: [\n        { label: 'V1', est: b.v1_vs_base.idsRed[0], lo: b.v1_vs_base.idsRed[1], hi: b.v1_vs_base.idsRed[2], color: COL.v1 },\n        { label: 'V2', est: b.v2_vs_base.idsRed[0], lo: b.v2_vs_base.idsRed[1], hi: b.v2_vs_base.idsRed[2], color: COL.v2 }] }); },",
        "'boot-ids2': function (h) { var b = D.testdev.bootstrap, n = tdRow('base').ids, P = function (v) { return v / n * 100; };\n      forest(h, { xlabel: 'ID switches removed vs Baseline (% of its ' + n + '; positive = fewer)', dec: 1, unit: '%', ml: 90, mr: 170, rows: [\n        { label: 'V1', est: P(b.v1_vs_base.idsRed[0]), lo: P(b.v1_vs_base.idsRed[1]), hi: P(b.v1_vs_base.idsRed[2]), color: COL.v1 },\n        { label: 'V2', est: P(b.v2_vs_base.idsRed[0]), lo: P(b.v2_vs_base.idsRed[1]), hi: P(b.v2_vs_base.idsRed[2]), color: COL.v2 }] }); },")
save("script.js", j)

# ablation table: stage names on one line and no full-name expansion inside it, so the charts above keep their height
i_ab = h.index('data-title="Ablation study"')
t0 = h.index('<table class="tbl" style="font-size:22px">', i_ab)
assert t0 - i_ab < 3000
h = h[:t0] + '<table class="tbl noabbr" style="font-size:22px">' + h[t0 + len('<table class="tbl" style="font-size:22px">'):]
for sid, *_ in ab_rows:
    k = h.index('<td>%s</td>' % sid, t0)
    h = h[:k] + '<td style="white-space:nowrap">%s</td>' % sid + h[k + len('<td>%s</td>' % sid):]

# ------------------------------------------------------------ 7. the two Optuna slides in simple, professional words
def replace_body(h, title_attr, new_body, old_notes, new_notes):
    i = h.index('data-title="%s"' % title_attr)
    e = h.index('</section>', i)
    b0 = h.index('<div class="s-body col">', i)
    b1 = h.index('  <footer class="s-foot">', i)
    assert i < b0 < b1 < e, title_attr
    h = h[:b0] + new_body + h[b1:]
    return rep(h, old_notes, new_notes)


assert h.count('data-title="Why Optuna"') == 1 and h.count('data-title="What Optuna changed in V1"') == 1
h = replace_body(h, 'Why Optuna', '''<div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>Our first design used <b>numbers we picked by hand</b>. <b>Optuna</b> is a search tool that <b>tries many sets of numbers for us</b> and keeps the set that works best on the <b>validation videos</b>.</p></div>
    <div class="flow" style="gap:0">
      <div class="node ad" style="width:240px;font-size:23px">1 · Try<small>pick one set of values</small></div><div class="arr sm"></div>
      <div class="node ad" style="width:240px;font-size:23px">2 · Run<small>AC-MOT on the validation videos</small></div><div class="arr sm"></div>
      <div class="node ad" style="width:240px;font-size:23px">3 · Score<small>read MOTA, ID switches, FPS</small></div><div class="arr sm"></div>
      <div class="node ad" style="width:240px;font-size:23px">4 · Learn<small>next try near the good values</small></div><div class="arr sm"></div>
      <div class="node good" style="width:240px;font-size:23px">Repeat<small>keep the best trial</small></div>
    </div>
    <div class="g2 grow" style="gap:22px">
      <div class="card col" style="border-left:6px solid var(--bad);gap:8px"><h3 class="bad">Before: chosen by hand</h3>
        <ul class="clean x"><li>how much each of the five clues counts (the SCI weights)</li><li>where a scene stops being easy and becomes hard</li><li>the detector settings for each kind of scene</li></ul>
        <p>We could not be sure that these guesses were good.</p></div>
      <div class="card col" style="border-left:6px solid var(--good);gap:8px"><h3 class="good">After: chosen by the results</h3>
        <ul class="clean"><li>the <b>validation videos</b> decide — not our guesses</li><li>it tests <b>many combinations</b> — more than a person can try by hand</li><li>the <b>test set is never used</b>, so the final test stays fair</li></ul></div>
    </div>
    <div class="card flat"><div class="ex-label">The tool</div><p><b>Optuna</b> with the <b>TPE</b> sampler. It is a <b>search method, not an AI model</b>: it trains nothing — it only decides which values to try next, based on the scores so far.</p></div>
  </div>
''', '<p><b>Say:</b> "Our first design had many hand-picked numbers. So we asked whether validation performance could choose them. We used Optuna with TPE, a sequential Bayesian optimizer."</p>',
    '<p><b>Say:</b> "Our first design used numbers that we chose by hand: how much each clue counts, where an easy scene becomes a hard one, and the detector settings for each kind of scene. We could not be sure these guesses were good. Optuna solves this. It is a search tool. It picks one set of values, AC-MOT runs on the validation videos with them, Optuna reads the score, and then it picks the next set close to the values that scored well. After many trials we keep the best one. The test set is never used in this search."</p><p><b>If asked how it chooses:</b> "It uses TPE, the Tree-structured Parzen Estimator (Bergstra et al., 2011): it looks at the trials so far and tries next where good scores are more likely. It is a sequential, Bayesian search."</p>')

h = replace_body(h, 'What Optuna changed in V1', '''<div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>Optuna did <b>not</b> change <b>how we measure the scene</b>. It only chose <b>how AC-MOT reacts</b> to what it measures. Each trial tested <b>one full set</b> of these choices — one complete version of AC-MOT.</p></div>
    <div class="g2 grow" style="gap:22px">
      <div class="card col" style="border-top:6px solid #64748B;gap:6px"><h3>Fixed · how we measure the scene</h3>
        <table class="tbl" style="font-size:24px">
          <tr><td>crowd</td><td style="text-align:left">number of boxes ÷ 30</td></tr>
          <tr><td>tiny objects</td><td style="text-align:left">share of boxes smaller than 32 × 32 px</td></tr>
          <tr><td>busy edges</td><td style="text-align:left">edge density ÷ 0.14</td></tr>
          <tr><td>dark</td><td style="text-align:left">brightness below 80</td></tr>
          <tr><td>blurry</td><td style="text-align:left">sharpness (Laplacian variance) below 180</td></tr>
          <tr><td>smoothing</td><td style="text-align:left">average of the last 7 readings</td></tr>
          <tr><td>how often</td><td style="text-align:left">every 10 frames</td></tr>
        </table></div>
      <div class="card col" style="border-top:6px solid #7C3AED;gap:6px"><h3>Chosen by Optuna · how AC-MOT reacts</h3>
        <table class="tbl" style="font-size:24px">
          <tr><td>SCI weights</td><td style="text-align:left">how much each clue counts: crowd · tiny · edges · dark · blur</td></tr>
          <tr><td>scene limits</td><td style="text-align:left">where SCI turns a scene from easy to medium to hard</td></tr>
          <tr><td>detector settings</td><td style="text-align:left">the confidence and NMS IoU for easy and for hard scenes</td></tr>
        </table>
        <div class="callout mt8">All of these are chosen <b>together</b>. One trial = one full set = <b>one complete AC-MOT</b>, tested on the validation videos.</div></div>
    </div>
  </div>
''', '<p><b>Say:</b> "Be clear about this: Optuna did not touch how the cues are measured. The divisors, thresholds, window and stride stayed fixed. It searched the weights, the regime boundaries and the detector settings — all together."</p>',
    '<p><b>Say:</b> "Be clear about this: Optuna did not change how we measure the scene. The divisors and thresholds of the five clues, the 7-reading average and the 10-frame step all stayed fixed. Optuna chose, all together, how much each clue counts, where a scene becomes medium or hard, and the detector settings for easy and hard scenes. One trial is one complete version of AC-MOT, tested on the validation videos."</p><p><b>If asked for the parameter names:</b> weights w_crowd, w_tiny, w_edge, w_night, w_blur · limits threshold_mid, threshold_high · detector conf_easy, conf_hard, nms_easy, nms_hard.</p>')

# ------------------------------------------------------------ 4. delete the evaluation-protocol slide
ev_s = '<section class="slide" data-sec="5" data-secname="V · Setup &amp; first result" data-title="Evaluation protocol"'
assert h.count(ev_s) == 1 and h.count('How We Score Every System') == 1
x0 = h.index(ev_s)
x1 = h.index('</section>', x0) + len('</section>')
x1 += len(h[x1:]) - len(h[x1:].lstrip('\n'))
assert 'How We Score Every System' in h[x0:x1]
h = h[:x0] + h[x1:]

# ------------------------------------------------------------ outline ranges
tags = slide_tags(h)
assert len(tags) == 94
start = {re.search(r'id="(sec-\d+)"', t).group(1): k for k, t in enumerate(tags, 1) if re.search(r'id="(sec-\d+)"', t)}
od = sorted(start.items(), key=lambda kv: kv[1])
rng = {k: (v, (od[q + 1][1] - 1) if q + 1 < len(od) else len(tags) - 1) for q, (k, v) in enumerate(od)}


def fix_range(m):
    g = m.group(1)
    return f'<button class="ol-row" data-goto="{g}">' + re.sub(r'slides \d+ - \d+', f'slides {rng[g][0]} - {rng[g][1]}', m.group(2))


h, n = re.subn(r'<button class="ol-row" data-goto="(sec-\d+)">(.*?</button>)', fix_range, h)
assert n == 9, n
print('outline', re.findall(r'slides \d+ - \d+', h))
save("index.html", h)
print("ok · slides", len(tags), "· overview at", k_idea + 1)
