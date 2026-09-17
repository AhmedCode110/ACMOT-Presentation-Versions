#!/usr/bin/env python3
"""v12: Outline slide laid out like the Outline slide of the PowerPoint seminar deck
(two columns, Roman numeral, title, subtitle, slide range)."""
import os, re

ROOT = os.path.expanduser("~/Desktop/ACMOT-Presentation-Versions/versions/v12-outline-like-ppt")
P, C = os.path.join(ROOT, "index.html"), os.path.join(ROOT, "styles.css")
h = open(P, encoding="utf-8").read()

# slide ranges computed from the deck itself
main = h[:h.find('<div class="overlay xview"')]
tags = re.findall(r'<section class="slide[^"]*"[^>]*>', main)
start = {re.search(r'id="(sec-\d)"', t).group(1): i for i, t in enumerate(tags, 1) if re.search(r'id="(sec-\d)"', t)}
ends = sorted(start.values())[1:] + [len(tags) + 1]
rng = {k: (v, ends[sorted(start.values()).index(v)] - 1) for k, v in start.items()}

rows = [  # titles and subtitles as in the PowerPoint Outline; VII subtitle follows the current section content
    ("I", "sec-1", "Introduction and Motivation", "Detection, tracking and how we measure them"),
    ("II", "sec-2", "Related Work: Detectors and Trackers", "YOLO, ByteTrack and the benchmarks"),
    ("III", "sec-3", "Problem Formulation and Research Gap", "Why one fixed threshold fails"),
    ("IV", "sec-4", "Proposed Framework: AC-MOT", "Scene score (SCI) and Smart Calibrator"),
    ("V", "sec-5", "Experimental Setup: Dataset and Protocol", "VisDrone and a fair test design"),
    ("VI", "sec-6", "Results and Ablation Study", "Stage 1: A0 to A3, speed and ID switches"),
    ("VII", "sec-7", "Stage 2: Constrained Optimization", "Optuna search, test set, V2 and UAVDT"),
    ("VIII", "sec-8", "Conclusion and Future Work", "What we delivered and what comes next"),
]
cards = "\n".join(
    f'      <button class="ol-row" data-goto="{g}"><span class="n">{n}</span><span class="t"><h3>{t}</h3>'
    f'<p>{s}</p><p class="rg">slides {rng[g][0]} - {rng[g][1]}</p></span></button>'
    for n, g, t, s in rows)

a = h.index('<div class="ol" style="grid-template-columns:repeat(4,1fr)')
b = h.index('    </div>\n  </div>\n  <aside class="notes"><p><b>Say:</b> "The story goes in the order', a)
h = h[:a] + '<div class="ol-ppt">\n' + cards + '\n' + h[b:]
open(P, "w", encoding="utf-8").write(h)

css = """
/* v12: Outline like the PowerPoint deck */
.ol-ppt{display:grid;grid-template-columns:1fr 1fr;grid-auto-flow:column;grid-template-rows:repeat(4,1fr);column-gap:26px;height:100%;
  border-top:2px solid #E2E8F0;border-bottom:2px solid #E2E8F0}
.ol-row{display:flex;align-items:flex-start;gap:0;text-align:left;background:#FAFBFD;border:0;border-bottom:2px solid #E2E8F0;
  padding:18px 10px 14px;cursor:pointer;font-family:var(--font);transition:background .2s}
.ol-row:nth-child(4),.ol-row:nth-child(8){border-bottom:0}
.ol-row:hover{background:#EEF4FB}
.ol-row .n{flex:0 0 106px;font-size:40px;font-weight:700;color:#0B4F8A;line-height:1.1;padding-top:8px}
.ol-row h3{font-size:30px;font-weight:700;color:#0F172A;margin:0 0 6px;line-height:1.2}
.ol-row p{font-size:24px;color:#64748B;margin:0;line-height:1.4}
"""
open(C, "a", encoding="utf-8").write(css)
J = os.path.join(ROOT, "script.js"); j = open(J, encoding="utf-8").read()
assert j.count(".ol-card .n,.node small'") == 1
open(J, "w", encoding="utf-8").write(j.replace(".ol-card .n,.node small'", ".ol-card .n,.ol-ppt,.node small'"))  # keep outline text exactly as in the PPT
print("ok", rng)
