#!/usr/bin/env python3
"""v29 (from v28), requested by the author on 2026-09-15:
'Cross-Dataset Evidence: UAVDT' table - next to every V1 and V2 value, the change against the UAVDT Baseline in percent
of the Baseline value (green = better, red = worse; fewer IDS is better). A legend line under the table and a notes
sentence. Values are checked against results.js -> uavdt."""
import os, re

ROOT = os.path.expanduser("~/Desktop/ACMOT-Presentation-Versions/versions/v29-uavdt-percent-change")


def load(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def save(p, s): open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)


h = load("index.html")
rj = load("assets/data/results.js")
assert '.tbl .dlt' in load("styles.css")
n_slides = len(re.findall(r'<section class="slide[^"]*"[^>]*>', h[:h.index('<div class="overlay xview"')]))
outline_before = re.findall(r'slides \d+ - \d+', h)

rows = {'Baseline': (13.841, 24.085, 27.887, 558, 65.015), 'V1': (17.399, 28.390, 34.453, 321, 58.353), 'V2': (16.118, 26.930, 32.014, 308, 61.462)}
ids = {'Baseline': 'base', 'V1': 'v1', 'V2': 'v2'}
uv = rj[rj.index('uavdt'):]
for name, v in rows.items():
    pat = r"id: '%s',\s*name: '[^']*',\s*mota: %.3f, hota: %.3f, idf1: %.3f, ids: %d, fn: \d+, fp: \d+, fps: %.3f" % ((ids[name],) + v)
    assert re.search(pat, uv), name
better_up = [True, True, True, False, True]
fmt = ['%.3f', '%.3f', '%.3f', '%d', '%.3f']
base = rows['Baseline']


def pct(v, b):
    x = (v - b) / b * 100
    return (('%+.2f%%' if abs(x) < 0.1 else '%+.1f%%') % x).replace('-', '−'), x


i = h.index('data-title="UAVDT with zero tuning"')
e = h.index('</section>', i)
t0 = h.index('<table class="tbl" style="font-size:24px">', i)
t1 = h.index('</table>', t0)
assert t0 < e and t1 < e
tbl = h[t0:t1]
summary = {}
for name in ('V1', 'V2'):
    rs = tbl.index('<td>%s</td>' % name)
    re_ = tbl.index('</tr>', rs)
    row = tbl[rs:re_]
    summary[name] = []
    for k in range(5):
        txt, x = pct(rows[name][k], base[k])
        summary[name].append(abs(x))
        span = '<span class="dlt %s">%s</span>' % ('good' if (x > 0) == better_up[k] else 'bad', txt)
        cell = re.compile(r'(<td(?: class="best")?>)%s(</td>)' % re.escape(fmt[k] % rows[name][k]))
        assert len(cell.findall(row)) == 1, (name, k)
        row = cell.sub(lambda m, f=fmt[k] % rows[name][k], sp=span: m.group(1) + f + sp + m.group(2), row)
    tbl = tbl[:rs] + row + tbl[re_:]
h = h[:t0] + tbl + h[t1:]
t1 = h.index('</table>', t0) + len('</table>')
h = h[:t1] + '\n    <p class="tiny muted" style="margin:0">Small numbers = change compared with the <b>Baseline on UAVDT</b>, in percent of its value · <b class="good">green = better</b> · <b class="bad">red = worse</b></p>' + h[t1:]

e = h.index('</section>', i)
a_end = h.rindex('</aside>', i, e)
s1, s2 = summary['V1'], summary['V2']
h = h[:a_end] + ('<p><b>Then:</b> "The small numbers show the change against the baseline in percent of its value. V1 raises MOTA by %.1f%%, HOTA by %.1f%% and IDF1 by %.1f%%, has %.1f%% fewer ID switches and runs %.1f%% slower. V2 raises MOTA by %.1f%%, HOTA by %.1f%% and IDF1 by %.1f%%, has %.1f%% fewer ID switches and runs %.1f%% slower."</p>' % tuple(s1 + s2)) + h[a_end:]

assert len(re.findall(r'<section class="slide[^"]*"[^>]*>', h[:h.index('<div class="overlay xview"')])) == n_slides == 94
assert re.findall(r'slides \d+ - \d+', h) == outline_before
save("index.html", h)
print("ok · V1", ["%.2f" % x for x in s1], "· V2", ["%.2f" % x for x in s2])
