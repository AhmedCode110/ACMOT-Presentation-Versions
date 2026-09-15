#!/usr/bin/env python3
"""v26 (from v25): a V1 trials curve like the V2 Pareto chart, drawn from the real V1 Optuna study
(assets/data/source/EMPIRICAL_OPTUNA_TRIALS.csv, copied from the author's Downloads on 2026-09-15).
Every completed trial is plotted as MOTA vs ID switches on validation; the IDS <= 271 rule is drawn as a line;
the best trade-off line (non-dominated trials) is drawn; Trial 24 is highlighted."""
import csv, os, re

ROOT = os.path.expanduser("~/Desktop/ACMOT-Presentation-Versions/versions/v26-v1-trials-curve")


def load(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def save(p, s): open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)


def rep(s, old, new, n=1):
    assert s.count(old) == n, (s.count(old), old[:110])
    return s.replace(old, new)


# ------------------------------------------------------------ data from the study export
rows = list(csv.DictReader(open(os.path.join(ROOT, "assets/data/source/EMPIRICAL_OPTUNA_TRIALS.csv"), encoding="utf-8")))
done = [r for r in rows if r["state"] == "COMPLETE"]
unfinished = [int(r["number"]) for r in rows if r["state"] != "COMPLETE"]
trials = [[int(r["number"]), round(float(r["user_attrs_MOTA"]) * 100, 3), int(float(r["user_attrs_IDS"])),
           round(float(r["user_attrs_FPS"]), 2), r["user_attrs_feasible"] == "True"] for r in done]
n_done, n_feas = len(trials), sum(1 for t in trials if t[4])
min_fps = min(t[3] for t in trials)
best = max(trials, key=lambda t: t[1])
assert n_done == 50 and unfinished == [33] and best[0] == 24 and best[4], (n_done, unfinished, best)
assert all(t[3] >= 25 for t in trials) and all((t[2] <= 271) == t[4] for t in trials)

r = load("assets/data/results.js")
assert "window.ACMOT.v1trials" not in r
js_rows = ",\n    ".join("[%d, %.3f, %d, %.2f, %s]" % (t[0], t[1], t[2], t[3], "true" if t[4] else "false") for t in trials)
r = r.rstrip() + f"""

/* V1 Optuna study on validation (VisDrone2019-MOT-val): every COMPLETED trial.
   Source: EMPIRICAL_OPTUNA_TRIALS.csv from defensible_acmot_3workers (copy in assets/data/source/).
   [trial, MOTA %, IDS, FPS, feasible (FPS gate and IDS <= Old-A3 271)] · trial {unfinished[0]} never finished. */
window.ACMOT.v1trials = {{
  completed: {n_done}, feasible: {n_feas}, unfinished: {unfinished},
  rows: [
    {js_rows}
  ]
}};
"""
save("assets/data/results.js", r)

# ------------------------------------------------------------ chart: scatter gets an optional vertical rule line
j = load("script.js")
j = rep(j, "    if (o.better) {\n      var g = E('g', { 'class': 'cann' }, s);",
        "    if (o.vline) {\n"
        "      E('line', { x1: X(o.vline.x), x2: X(o.vline.x), y1: m.t, y2: m.t + ih, 'class': 'cref' }, s);\n"
        "      T(s, X(o.vline.x) + 8, m.t + ih - 10, o.vline.label, 'creft');\n"
        "    }\n"
        "    if (o.better) {\n      var g = E('g', { 'class': 'cann' }, s);")
j = rep(j, "    'pub-mota': function (h) {", """    /* v26: every completed V1 Optuna trial on validation */
    'v1-trials': function (h) {
      var t = D.v1trials.rows, front = [], best = -1;
      t.slice().sort(function (a, b) { return a[2] - b[2] || b[1] - a[1]; }).forEach(function (p) { if (p[1] > best) { front.push([p[2], p[1]]); best = p[1]; } });
      var pts = t.map(function (p) {
        var o = { x: p[2], y: p[1], color: p[4] ? '#A78BFA' : '#CBD5E1', r: 7 };
        if (p[0] === 24) { o.color = COL.v1; o.r = 10; o.ring = true; o.label = 'T24 · selected\\nhighest MOTA · IDS 270'; o.strong = true; o.dx = -26; o.dy = 112; o.anchor = 'end'; }
        return o;
      });
      scatter(h, { xmin: 100, xmax: 360, ymin: 10, ymax: 25, xlabel: 'ID switches on validation  (lower is better →  left)', ylabel: 'MOTA on validation (%)',
        points: pts, front: front, vline: { x: 271, label: 'rule: IDS ≤ 271' }, better: '↖ better: more MOTA, fewer ID switches' });
    },
    'pub-mota': function (h) {""")
save("script.js", j)

# ------------------------------------------------------------ slide after the V1 validation selection
h = load("index.html")
assert 'data-title="V1 trials curve"' not in h
slide = f'''<section class="slide" data-sec="7" data-secname="VI · V1 optimization" data-title="V1 trials curve">
  <header class="s-head"><div class="kicker">Section VI · V1 search on validation</div><h2>All V1 Trials: The Trade-off Curve</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>Each dot is <b>one V1 trial</b> on the validation videos. Dots <b>right of the red line</b> broke the ID-switch rule. <b>Trial 24</b> has the highest MOTA — of the allowed trials and of <b>all {n_done}</b>.</p></div>
    <div class="row grow" style="gap:20px">
      <div class="card col grow" style="padding:12px 16px;gap:6px">
        <div class="chart zoomable grow" data-chart="v1-trials"></div>
        <div class="pills" style="justify-content:center"><span class="pill"><b style="color:#A78BFA">●</b> allowed (IDS ≤ 271)</span><span class="pill"><b style="color:#94A3B8">●</b> broke the IDS rule</span><span class="pill"><b style="color:#7C3AED">◉</b> Trial 24</span><span class="pill">— best trade-off line</span></div>
      </div>
      <div class="col" style="flex:0 0 400px;gap:12px">
        <div class="kpi"><div class="l">Completed trials</div><div class="v">{n_done}</div><div class="s">trial {unfinished[0]} did not finish</div></div>
        <div class="kpi hi"><div class="l">Allowed by the rules</div><div class="v">{n_feas}</div><div class="s">{n_done - n_feas} broke IDS ≤ 271</div></div>
        <div class="kpi"><div class="l">Speed rule</div><div class="v">all ≥ 25</div><div class="s">slowest trial: {min_fps:.2f} FPS</div></div>
        <div class="callout"><b>Trial 24:</b> MOTA 23.038 · IDS 270 · FPS 37.17</div>
      </div>
    </div>
  </div>
  <footer class="s-foot"><span class="prov p-val">Validation · VisDrone2019-MOT-val · V1 Optuna study · {n_done} completed trials · EMPIRICAL_OPTUNA_TRIALS.csv</span></footer>
  <aside class="notes"><p><b>Say:</b> "This is every trial of the V1 search on the validation videos. Up means more MOTA, left means fewer ID switches. The red line is the rule: at most 271 ID switches. {n_feas} of the {n_done} completed trials were allowed; {n_done - n_feas} broke the ID-switch rule, and every trial was fast enough — the slowest ran at {min_fps:.1f} FPS. Trial 24, the ringed dot, has the highest MOTA of all the trials, 23.038, with 270 ID switches, so it was selected."</p><p><b>Note:</b> the dashed line joins the trials that no other trial beats on both MOTA and ID switches. Trial {unfinished[0]} started but never finished, so it is not shown.</p></aside>
</section>

'''
i = h.index('data-title="Step 4 result: Trial 24"')
b = h.index('</section>', i) + len('</section>')
b = b + len(h[b:]) - len(h[b:].lstrip('\n'))
h = h[:b] + slide + h[b:]
h = rep(h, '<p><b>If asked for all 50 trials:</b> "The frozen configuration records the rule and the selected trial; the full list of trial scores is in the Optuna study log."</p>',
        '<p><b>If asked for all 50 trials:</b> "They are on the previous slide — every completed trial, with the rule line and Trial 24."</p>')

mm = h[:h.index('<div class="overlay xview"')]
tags = re.findall(r'<section class="slide[^"]*"[^>]*>', mm)
start = {re.search(r'id="(sec-\d+)"', t).group(1): k for k, t in enumerate(tags, 1) if re.search(r'id="(sec-\d+)"', t)}
od = sorted(start.items(), key=lambda kv: kv[1])
rng = {k: (v, (od[q + 1][1] - 1) if q + 1 < len(od) else len(tags) - 1) for q, (k, v) in enumerate(od)}


def fix_range(m):
    g = m.group(1)
    return f'<button class="ol-row" data-goto="{g}">' + re.sub(r'slides \d+ - \d+', f'slides {rng[g][0]} - {rng[g][1]}', m.group(2))


h, n = re.subn(r'<button class="ol-row" data-goto="(sec-\d+)">(.*?</button>)', fix_range, h)
assert n == 9, n
save("index.html", h)
print("ok · completed", n_done, "feasible", n_feas, "unfinished", unfinished, "min fps", min_fps, "· slides", len(tags))
