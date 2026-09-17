#!/usr/bin/env python3
"""v24 (from v23), all requested by the author on 2026-09-15:
 1. 'Three clues from the picture': remove the hard-to-read example-value lines;
 2. SCI slide: keep one definition only (the card), remove the second main-idea box;
 3. slightly bigger small text everywhere;
 4. 'Evaluation protocol' rewritten in simple words;
 5. the Initial AC-MOT test-set result is removed; the original ablation study (OLD-A0 … OLD-A3) is shown with
    charts, followed by Baseline (A0) vs Full AC-MOT (A3) and what went up; other mentions of the old result removed;
 6. a chart that shows why V1 Trial 24 was selected (selection rules vs Trial 24);
 7. a slide that explains what a paired bootstrap is, how it is measured and why it was used."""
import os, re

ROOT = os.path.expanduser("~/Desktop/ACMOT-Presentation-Versions/versions/v24-ablation-bootstrap-clarity")


def load(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def save(p, s): open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)


def rep(s, old, new, n=1):
    assert s.count(old) == n, (s.count(old), old[:110])
    return s.replace(old, new)


def span(h, title):
    i = h.index(f'data-title="{title}"')
    a = h.rindex('<section', 0, i)
    return a, h.index('</section>', i) + len('</section>')


h = load("index.html")

# ------------------------------------------------------------ 1. remove example-value lines
a, b = span(h, "Step 1: measure scene complexity")
seg = h[a:b]
for line in ['\n        <p class="small">Calm sky 0.021 → <b>0.15</b> · busy parking lot 0.295 → <b>1</b></p>',
             '\n        <p class="small">Day 110.6 → <b>0</b> · night 40.5 → <b>1</b></p>',
             '\n        <p class="small">Sharp 4,074 → <b>0</b> · blurred 4 → <b>1</b></p>']:
    seg = rep(seg, line, '')
seg = rep(seg, 'Original SCI cue definitions · example values computed on the pictures of the previous slide', 'Original SCI cue definitions')
h = h[:a] + seg + h[b:]

# ------------------------------------------------------------ 4. evaluation protocol, simply
evalp = '''<section class="slide" data-sec="5" data-secname="V · Setup &amp; first result" data-title="Evaluation protocol" data-explain="x-eval#2|Evaluation in Detail">
  <header class="s-head"><div class="kicker">Section V · Protocol</div><h2>How We Score Every System — the Same Way</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>To compare systems <b>fairly</b>, every system is tested on the <b>same videos</b>, with the <b>same rules</b> — and the tracker <b>forgets everything</b> before each new video.</p></div>
    <div class="flow grow" style="align-items:stretch;gap:0">
      <div class="card col" style="flex:1 1 0;min-width:0;gap:6px;border-top:6px solid #2563EB"><div class="tag" style="color:#1D4ED8">Step 1</div><h3>Start fresh</h3><p>Before each video, the tracker <b>forgets all IDs</b>.</p></div>
      <div class="arr sm" style="align-self:center"></div>
      <div class="card col" style="flex:1 1 0;min-width:0;gap:6px;border-top:6px solid #7C3AED"><div class="tag" style="color:#6D28D9">Step 2</div><h3>Clean the answer key</h3><p>Keep only <b>clear labels</b>: the 5 classes, not heavily hidden, not cut off.</p></div>
      <div class="arr sm" style="align-self:center"></div>
      <div class="card col" style="flex:1 1 0;min-width:0;gap:6px;border-top:6px solid #D97706"><div class="tag" style="color:#B45309">Step 3</div><h3>Run and compare</h3><p>Compare every box with the real objects: <b>overlap ≥ 0.5 = found</b>.</p></div>
      <div class="arr sm" style="align-self:center"></div>
      <div class="card col" style="flex:1 1 0;min-width:0;gap:6px;border-top:6px solid #15803D"><div class="tag" style="color:#15803D">Step 4</div><h3>Count and score</h3><p>Count found, false, missed and ID switches → <b>MOTA, HOTA, IDF1, IDS, FPS</b>.</p></div>
    </div>
    <div class="g2" style="gap:20px">
      <div class="card" style="border-left:6px solid #2563EB"><h3>Why start fresh?</h3><p>If the tracker kept its memory, one video could <b>help the next</b> — that would be unfair.</p></div>
      <div class="card" style="border-left:6px solid #15803D"><h3>Why the same rules?</h3><p>Then a better score can only come from <b>the method</b>, not from an easier test.</p></div>
    </div>
  </div>
  <footer class="s-foot"><span class="prov p-hist">Scoring tool: TrackEval, one fixed version · our custom class-agnostic AC-MOT protocol</span></footer>
  <aside class="notes"><p><b>Say:</b> "Every system is scored in the same four steps. First, the tracker starts fresh on each video, so one video cannot help the next. Second, we keep only clear labels. Third, a box counts as found when it overlaps a real object by at least 0.5. Fourth, we count found, false and missed objects and ID switches, and report MOTA, HOTA, IDF1, ID switches and FPS."</p></aside>
</section>'''
a, b = span(h, "Evaluation protocol")
h = h[:a] + evalp + h[b:]

# ------------------------------------------------------------ 5. ablation study instead of the Initial AC-MOT result
FOOT_ABL = '<span class="prov p-val">Ablation study · original AC-MOT components · VisDrone2019-MOT-val · same split as the V1 search</span>'
ablation = f'''<section class="slide" data-sec="5" data-secname="V · Setup &amp; first result" data-title="Ablation study" data-explain="x-ablation|Ablation in Detail">
  <header class="s-head"><div class="kicker">Section V · Ablation study</div><h2>Ablation Study: What Each Part of AC-MOT Adds</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>We switch on AC-MOT <b>one part at a time</b> on the same videos, so every change in the score can be traced to <b>that part</b>.</p></div>
    <div class="row grow" style="gap:16px"><div class="card" style="flex:1.6;padding:10px 14px"><div class="chart zoomable" data-chart="oab-quality"></div></div><div class="card grow" style="padding:10px 14px"><div class="chart zoomable" data-chart="oab-ids"></div></div><div class="card grow" style="padding:10px 14px"><div class="chart zoomable" data-chart="oab-fps"></div></div></div>
    <table class="tbl" style="font-size:22px">
      <tr><th style="text-align:left">Stage</th><th style="text-align:left">Configuration</th><th>MOTA ↑</th><th>HOTA ↑</th><th>IDF1 ↑</th><th>IDS ↓</th><th>FPS ↑</th></tr>
      <tr><td>OLD-A0</td><td style="text-align:left">Baseline Default</td><td>17.633%</td><td>29.837%</td><td>30.892%</td><td>283</td><td>44.09</td></tr>
      <tr><td>OLD-A1</td><td style="text-align:left">Tuned ByteTrack</td><td>17.802%</td><td>30.864%</td><td>32.854%</td><td>217</td><td class="best">44.51</td></tr>
      <tr><td>OLD-A2</td><td style="text-align:left">Adaptive Confidence + NMS</td><td>17.636%</td><td>31.384%</td><td>33.727%</td><td class="best">210</td><td>40.65</td></tr>
      <tr><td>OLD-A2R</td><td style="text-align:left">Adaptive Resolution Only</td><td class="best">18.425%</td><td>32.446%</td><td>35.669%</td><td>241</td><td>39.56</td></tr>
      <tr class="sel"><td>OLD-A3</td><td style="text-align:left">Full AC-MOT</td><td>18.165%</td><td class="best">33.064%</td><td class="best">36.296%</td><td>271</td><td>37.96</td></tr>
    </table>
  </div>
  <footer class="s-foot">{FOOT_ABL}</footer>
  <aside class="notes"><p><b>Say:</b> "This is the ablation study of the original AC-MOT. A0 is the baseline. A1 tunes ByteTrack. A2 adds adaptive confidence and NMS. A2R uses only the adaptive resolution. A3 is the full AC-MOT. Green marks the best value in each column — four different stages win the five metrics."</p></aside>
</section>

<section class="slide" data-sec="5" data-secname="V · Setup &amp; first result" data-title="Ablation result" data-explain="x-ablation#2|Ablation in Detail">
  <header class="s-head"><div class="kicker">Section V · Ablation result</div><h2>Baseline vs Full AC-MOT: What Went Up</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>The full AC-MOT improved <b>all three quality scores</b> over the baseline — most of all <b>IDF1</b> (+5.404) and <b>HOTA</b> (+3.227) — at the cost of some <b>speed</b>.</p></div>
    <div class="row grow" style="gap:20px">
      <div class="card grow" style="padding:10px 14px"><div class="chart zoomable" data-chart="oab-a0a3"></div></div>
      <div class="col" style="flex:0 0 640px;gap:12px">
        <table class="tbl" style="font-size:24px">
          <tr><th style="text-align:left">Metric</th><th>OLD-A0 · Baseline</th><th>OLD-A3 · Full AC-MOT</th><th>Change</th></tr>
          <tr><td>MOTA ↑</td><td>17.633%</td><td>18.165%</td><td class="best">+0.532</td></tr>
          <tr><td>HOTA ↑</td><td>29.837%</td><td>33.064%</td><td class="best">+3.227</td></tr>
          <tr><td>IDF1 ↑</td><td>30.892%</td><td>36.296%</td><td class="best">+5.404</td></tr>
          <tr><td>IDS ↓</td><td>283</td><td>271</td><td class="best">12 fewer</td></tr>
          <tr><td>FPS ↑</td><td>44.09</td><td>37.96</td><td class="bad strong">−6.13</td></tr>
        </table>
        <div class="card" style="border-left:6px solid var(--good);padding:10px 18px"><h3 style="margin:0 0 4px;font-size:26px">What went up</h3><p style="font-size:23px">Keeping the <b>same identity</b> (IDF1, HOTA) improved the most; MOTA rose a little and there were <b>12 fewer ID switches</b>.</p></div>
        <div class="card" style="border-left:6px solid var(--bad);padding:10px 18px"><h3 style="margin:0 0 4px;font-size:26px">The cost</h3><p style="font-size:23px">Speed dropped from <b>44.09 to 37.96 FPS</b> — still above the 25 FPS real-time line.</p></div>
      </div>
    </div>
  </div>
  <footer class="s-foot">{FOOT_ABL}</footer>
  <aside class="notes"><p><b>Say:</b> "Comparing the baseline with the full AC-MOT: MOTA went up by 0.532, HOTA by 3.227 and IDF1 by 5.404, and there were 12 fewer ID switches. The biggest gain is in keeping identities. The cost is speed: 44.09 down to 37.96 FPS, which is still real time."</p></aside>
</section>'''
a, b = span(h, "Initial AC-MOT result")
h = h[:a] + ablation + h[b:]

# other mentions of the old test-set result
h = rep(h, 'Three frozen systems, run once: Baseline, Initial AC-MOT and New AC-MOT (Trial 24).',
        'Frozen systems, run once: the Baseline and V1 (Trial 24) — and later V2.')
a, b = span(h, "The identity-switch problem")
seg = h[a:b]
seg = rep(seg, '<p>V1 has the best quality, but the <b>initial AC-MOT had fewer ID switches</b>: 1061 &lt; 1184.</p>',
          '<p>V1 has the best quality, but it removed <b>only 51 ID switches</b>: 1235 → 1184.</p>')
seg = rep(seg, 'data-chart="v1t-ids"', 'data-chart="v1b-ids"')
seg = rep(seg, '"Look at ID switches: baseline 1235, initial AC-MOT 1061, V1 1184. V1 is much better in quality, but the initial version had fewer ID switches. The reason: in V1, IDS was only a rule to pass, not a goal to minimize."',
          '"Look at ID switches: baseline 1235, V1 1184 — only 51 fewer, while quality jumped a lot. The reason: in V1, IDS was only a rule to pass, not a goal to minimize."')
h = h[:a] + seg + h[b:]
h = rep(h, 'Heuristic AC-MOT<small>23.236 MOTA</small>', 'Heuristic AC-MOT<small>ablation: IDF1 +5.404 · HOTA +3.227</small>')
h = rep(h, "the problem and the baseline, the first heuristic design, V1, V2, and finally the statistics and UAVDT.",
        "the problem and the baseline, the first heuristic design and its ablation, V1, V2, and finally the statistics and UAVDT.")
h = rep(h, '<p>VisDrone, protocol and the initial AC-MOT</p>', '<p>VisDrone, protocol and the ablation study</p>')

# ------------------------------------------------------------ 6. why Trial 24
why24 = '''<section class="slide" data-sec="7" data-secname="VI · V1 optimization" data-title="Why Trial 24">
  <header class="s-head"><div class="kicker">Section VI · V1 selection</div><h2>Why Trial 24? The Selection Rules on a Chart</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>A trial could only win if it was <b>fast enough</b> and did <b>not add ID switches</b>. Among the trials that passed both rules, <b>Trial 24 had the highest MOTA</b>.</p></div>
    <div class="row grow" style="gap:16px">
      <div class="card col grow" style="padding:10px 14px;gap:4px"><div class="tag">Rule 1 · FPS must stay at least 25</div><div class="chart zoomable grow" data-chart="v1-rule-fps"></div><p class="tc good strong" style="font-size:22px;margin:0">✓ 37.17 FPS</p></div>
      <div class="card col grow" style="padding:10px 14px;gap:4px"><div class="tag">Rule 2 · IDS must not exceed Old-A3 (271)</div><div class="chart zoomable grow" data-chart="v1-rule-ids"></div><p class="tc good strong" style="font-size:22px;margin:0">✓ 270 ≤ 271</p></div>
      <div class="card col grow" style="padding:10px 14px;gap:4px"><div class="tag">Then · the highest MOTA wins</div><div class="chart zoomable grow" data-chart="v1-rule-mota"></div><p class="tc good strong" style="font-size:22px;margin:0">✓ 23.038 vs 18.165</p></div>
    </div>
    <div class="note">If two trials had the same MOTA, the tie would go to fewer ID switches, then higher HOTA, IDF1 and FPS. Everything was decided on <b>validation</b> — the test set was never used.</div>
  </div>
  <footer class="s-foot"><span class="prov p-val">Validation · VisDrone2019-MOT-val · 50 trials · rule and values from the frozen V1 configuration</span></footer>
  <aside class="notes"><p><b>Say:</b> "Why Trial 24? The rules were fixed before the search. Rule one: FPS must stay at least 25 — Trial 24 runs at 37.17. Rule two: ID switches must not exceed the original full AC-MOT, 271 — Trial 24 has 270. Among the trials that passed both rules, Trial 24 had the highest MOTA, 23.038, compared with 18.165 for the original AC-MOT on the same validation videos."</p><p><b>If asked for all 50 trials:</b> "The frozen configuration records the rule and the selected trial; the full list of trial scores is in the Optuna study log."</p></aside>
</section>'''
a, b = span(h, "Step 4 result: Trial 24")
h = h[:b] + "\n\n" + why24 + h[b:]

# ------------------------------------------------------------ 7. what is a paired bootstrap
bars = []
heights = [6, 14, 26, 44, 66, 90, 112, 124, 118, 98, 74, 50, 30, 16, 7]
x0, bw = 60, 34
for k, hh in enumerate(heights):
    x = x0 + k * (bw + 4)
    inside = 2 <= k <= 12
    bars.append(f'<rect x="{x}" y="{200 - hh}" width="{bw}" height="{hh}" rx="3" fill="{"#7C3AED" if inside else "#CBD5E1"}"/>')
svg = ('<svg viewBox="0 0 660 260" width="100%" style="flex:1;min-height:0"><g font-family="Inter,Helvetica" font-weight="800">'
       '<line x1="30" y1="200" x2="640" y2="200" stroke="#94A3B8" stroke-width="3"/>'
       '<line x1="30" y1="40" x2="30" y2="206" stroke="#DC2626" stroke-width="4" stroke-dasharray="8 6"/>'
       '<text x="30" y="30" text-anchor="middle" font-size="20" fill="#B91C1C">0</text>'
       + "".join(bars) +
       '<line x1="134" y1="215" x2="518" y2="215" stroke="#7C3AED" stroke-width="4"/>'
       '<text x="326" y="240" text-anchor="middle" font-size="22" fill="#6D28D9">middle 95% = confidence interval</text>'
       '<text x="96" y="252" text-anchor="middle" font-size="17" fill="#64748B">lowest 2.5%</text>'
       '<text x="590" y="252" text-anchor="middle" font-size="17" fill="#64748B">highest 2.5%</text>'
       '<text x="400" y="60" text-anchor="middle" font-size="20" fill="#334155">5,000 differences (V1 − Baseline)</text>'
       '</g></svg>')
boot_explain = f'''<section class="slide" data-sec="8" data-secname="VIII · Statistics &amp; UAVDT" data-title="What is a paired bootstrap">
  <header class="s-head"><div class="kicker">Section VIII · Statistical validation</div><h2>What Is a Paired Bootstrap — and Why We Used It</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>A bootstrap checks whether a gain is <b>real</b> or just <b>luck with the test videos we happened to have</b>.</p></div>
    <div class="row grow" style="gap:20px">
      <div class="col" style="flex:0 0 470px;gap:12px">
        <div class="card" style="border-left:6px solid var(--bad)"><h3>Why?</h3><p>The test set has only <b>17 videos</b>. If a few of them are easy, the gain could look <b>bigger than it really is</b>.</p></div>
        <div class="card" style="border-left:6px solid var(--good)"><h3>How to read it</h3><p>Interval <b>fully above 0</b> → the gain is real.<br>Interval <b>crosses 0</b> → we cannot claim a gain.</p></div>
      </div>
      <div class="card col grow" style="gap:8px"><h3>How it is measured</h3>
        <table class="tbl" style="font-size:22px">
          <tr><td class="strong">1</td><td style="text-align:left"><b>Pick 17 videos at random</b> from the 17 test videos — the same video may be picked twice.</td></tr>
          <tr><td class="strong">2</td><td style="text-align:left">On <b>these same videos</b>, score V1 and the Baseline and take the <b>difference</b>. Same videos for both = <b>paired</b>.</td></tr>
          <tr><td class="strong">3</td><td style="text-align:left"><b>Repeat 5,000 times</b> → 5,000 differences.</td></tr>
          <tr><td class="strong">4</td><td style="text-align:left">Cut off the lowest and highest 2.5% → the <b>middle 95%</b> is the confidence interval.</td></tr>
        </table>
        {svg}
        <div class="tc"><span class="origin illus">drawing · shape only, no real numbers</span></div>
      </div>
    </div>
  </div>
  <footer class="s-foot"><span class="prov p-test">Test set · 17 sequences · 5,000 paired resamples</span></footer>
  <aside class="notes"><p><b>Say:</b> "A bootstrap asks: is the gain real, or were we lucky with these 17 test videos? We pick 17 videos at random, where the same video can be picked twice. On exactly those videos we score V1 and the baseline and take the difference — that is why it is called paired. We repeat this 5,000 times, sort the 5,000 differences and keep the middle 95 percent. If that whole interval is above zero, the gain is real. If it crosses zero, we cannot claim a gain."</p></aside>
</section>'''
a, b = span(h, "Paired bootstrap")
h = h[:a] + boot_explain + "\n\n" + h[a:]

# ------------------------------------------------------------ 8. Section I divider: the tracking video of the Thank-you slide
a, b = span(h, "Section I")
seg = h[a:b]
tv = re.search(r'<video[^>]*>(</video>)?', h[slice(*span(h, "Thank you"))]).group(0)
seg = re.sub(r'<div class="dv-bg">.*?</div>', '<div class="dv-bg">' + (tv if tv.endswith("</video>") else tv + "</video>") + '</div>', seg, count=1, flags=re.S)
h = h[:a] + seg + h[b:]

# ------------------------------------------------------------ outline ranges
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
save("index.html", h)

# ------------------------------------------------------------ 2. one SCI definition only
m = load("assets/data/meaning.js")
m, n = re.subn(r"  'The pipeline for each frame': \{[^}]*\},\n", "", m)
assert n == 1, n
save("assets/data/meaning.js", m)

# ------------------------------------------------------------ charts
j = load("script.js")
j = rep(j, "    'pub-mota': function (h) {", """    /* v24: ablation A0 vs A3, and why V1 Trial 24 was selected */
    'oab-a0a3': function (h) { var r = D.oldAblation.rows, a0 = r[0], a3 = r[r.length - 1];
      grouped(h, { groups: ['MOTA', 'HOTA', 'IDF1'], better: 'higher', dec: 1, ylabel: 'percent', max: 40, bw: 90,
        series: [{ name: 'OLD-A0 · Baseline', color: '#94A3B8', values: [a0.mota, a0.hota, a0.idf1] }, { name: 'OLD-A3 · Full AC-MOT', color: '#4F46E5', values: [a3.mota, a3.hota, a3.idf1] }] }); },
    'v1-rule-fps': function (h) { bars(h, { labels: ['Trial 24'], values: [D.v1.val.fps], colors: [COL.v1], better: 'higher', dec: 2, ref: { v: 25, label: 'rule: at least 25 FPS' }, ylabel: 'FPS', max: 50, bw: 120 }); },
    'v1-rule-ids': function (h) { bars(h, { labels: ['Old-A3\\nlimit', 'Trial 24'], values: [D.v1.oldA3val.ids, D.v1.val.ids], colors: ['#94A3B8', COL.v1], better: 'lower', dec: 0, ylabel: 'ID switches', max: 320, bw: 100, mb: 76 }); },
    'v1-rule-mota': function (h) { bars(h, { labels: ['Old-A3\\nreference', 'Trial 24'], values: [D.v1.oldA3val.mota, D.v1.val.mota], colors: ['#94A3B8', COL.v1], better: 'higher', dec: 3, ylabel: 'MOTA (%)', max: 30, bw: 100, mb: 76 }); },
    'pub-mota': function (h) {""")
save("script.js", j)

# ------------------------------------------------------------ 3. slightly bigger small text
c = load("styles.css")
assert "v24: slightly bigger small text" not in c
c += """
/* v24: slightly bigger small text (author request) */
.small{font-size:26px}.tiny{font-size:22px}.cap{font-size:21px}
.s-foot{font-size:20px}.ex-label{font-size:20px}
.card .tag,.meaning .tag{font-size:20px}
.kpi .l{font-size:20px}.kpi .s{font-size:20px}
.node small{font-size:20px}
.tbl th{font-size:20px}
.pill{font-size:22px}
.ctick{font-size:20px}.caxis{font-size:21px}.clabel{font-size:22px}.clegend{font-size:21px}
.cval.sm{font-size:20px}.cptl{font-size:20px}.cptl.strong{font-size:21px}
"""
save("styles.css", c)
# 9. previous / next buttons beside the Outline button: applied to script.js and styles.css right after this build (see VERSION_HISTORY v24)
print("ok · slides:", len(tags), rng)
