#!/usr/bin/env python3
"""v14: move the 'Benchmark datasets' slide before 'Published MOTA on MOT17', so MOT17 is introduced
before its results are shown."""
import os, re

P = os.path.expanduser("~/Desktop/ACMOT-Presentation-Versions/versions/v14-datasets-before-mot17-results/index.html")
h = open(P, encoding="utf-8").read()


def block(title):
    a = h.index(f'<section class="slide" data-sec="2" data-secname="II · Related work" data-title="{title}">')
    b = h.index('</section>', a) + len('</section>\n\n')
    return a, b


a, b = block("Benchmark datasets")
ds = h[a:b]
h = h[:a] + h[b:]
old = 'Later we also test on UAVDT, without any tuning."'
assert ds.count(old) == 1
ds = ds.replace(old, 'Later we also test on UAVDT, without any tuning. MOT17 is the street benchmark — the next slide shows published results on it."')
a, _ = block("Published MOTA on MOT17")
h = h[:a] + ds + h[a:]
open(P, "w", encoding="utf-8").write(h)
main = h[:h.find('<div class="overlay xview"')]
print("ok", [t for t in re.findall(r'<section class="slide[^"]*"[^>]*data-title="([^"]*)"', main)][23:29])
