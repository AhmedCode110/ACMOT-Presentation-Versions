#!/usr/bin/env python3
"""v18 (from v17): richer 'idea' slide for AC-MOT (every pipeline block explains what happens, what it outputs
and where it is detailed), and no 'NEW' tags on any slide."""
import os, re

ROOT = os.path.expanduser("~/Desktop/ACMOT-Presentation-Versions/versions/v18-rich-acmot-idea-no-new-tags")
P = os.path.join(ROOT, "index.html")
h = open(P, encoding="utf-8").read()

main = h[:h.index('<div class="overlay xview"')]
titles = re.findall(r'<section class="slide[^"]*"[^>]*data-title="([^"]*)"', main)
num = {t: i + 1 for i, t in enumerate(titles)}
r1 = (num["Three clues on real pictures"], num["Step 1: measure scene complexity"])
r2 = (num["The pipeline for each frame"], num["SCI from frame to score"])
r3 = (num["The three detector settings"], num["Smart Calibrator exact settings"])


def card(tag, color, title, lines, out, where="", width=1.0, frag=True):
    li = "".join(f"<li style=\"margin:3px 0\">{x}</li>" for x in lines)
    wh = f'<p class="muted" style="margin-top:auto;font-size:19px;font-weight:700">{where}</p>' if where else ""
    return (f'<div class="card col{" frag" if frag else ""}" style="flex:{width} 1 0;min-width:0;padding:12px 14px;gap:8px;border-top:6px solid {color}">'
            f'<div class="tag" style="color:{color};font-size:17px">{tag}</div><h3 style="font-size:27px;margin:0">{title}</h3>'
            f'<ul class="clean" style="font-size:22px;line-height:1.3;margin:0">{li}</ul>'
            f'<div><span class="pill" style="font-size:20px;white-space:normal">→ {out}</span></div>{wh}</div>')


arr = '<div class="arr sm frag" style="align-self:center"></div>'
flow = '<div class="node io frag" style="flex:0 0 96px;align-self:center;font-size:22px;padding:10px 6px">Frame<small>new picture</small></div>' + arr + arr.join([
    card("Step 1 · Measure", "#2563EB", "Scene Analyzer",
         ["asks <b>5 questions</b>: many objects? tiny? busy? dark? blurry?", "uses the <b>last boxes</b> and a <b>small gray copy</b>"],
         "5 clue values", f"details: slides {r1[0]}–{r1[1]}"),
    card("Step 2 · Score", "#7C3AED", "SCI",
         ["<b>mixes</b> the 5 clues with weights", "one number: <b>0 = easy · 1 = hard</b>", "averaged over 7 readings, every 10 frames"],
         "one score, e.g. 0.63", f"details: slides {r2[0]}–{r2[1]}"),
    card("Step 3 · Set", "#D97706", "Smart Calibrator",
         ["turns SCI into <b>3 detector settings</b>", "hard → lower confidence, stronger copy removal, bigger input", "easy → strict, small and fast"],
         "confidence · NMS IoU · input size", f"details: slides {r3[0]}–{r3[1]}"),
    card("Unchanged", "#475569", "Detector · YOLOv8n",
         ["<b>finds the boxes</b> with these settings", "same model, <b>no retraining</b>"], "boxes", width=0.8),
    card("Unchanged", "#475569", "Tracker · ByteTrack",
         ["<b>links boxes</b> over time and keeps the IDs", "its own settings stay <b>fixed</b>"], "tracks with IDs", width=0.8),
])

idea = f'''<section class="slide" data-sec="4" data-secname="IV · AC-MOT" data-title="What we add">
  <header class="s-head"><div class="kicker">Section IV · The idea</div><h2>The Idea: Measure the Scene, Then Set the Detector</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>AC-MOT adds <b>three small steps before the detector</b>. For every frame it <b>measures</b> how hard the scene is, turns that into <b>one score</b>, and <b>sets the detector</b> for it — like a driver who goes <b>slowly in fog</b> and <b>faster on an empty road</b>.</p></div>
    <div class="flow grow noabbr" style="align-items:stretch;gap:0;flex-wrap:nowrap">{flow}</div>
    <div class="note frag" style="font-size:22px">↺ <b>Loop:</b> the boxes of this frame are reused in <b>Step 1 for the next frame</b> (for the crowd and tiny clues).</div>
    <div class="callout frag" style="font-size:24px"><b>Example:</b> a crowded, tiny, dark frame → high clue values → <b>SCI = 0.63</b> → lower confidence and a bigger input (832) → the detector can keep <b>weak, tiny objects</b>.</div>
  </div>
  <aside class="notes"><p><b>How to present:</b> press → to reveal the blocks one by one.</p><p><b>Say:</b> "AC-MOT is not a new detector and not a new tracker. Before the detector, it adds three small steps. Step one, the Scene Analyzer, asks five questions about the frame: are there many objects, are they tiny, is the background busy, is it dark, is it blurry? Step two mixes the five answers into one score, SCI, from 0 for easy to 1 for hard. Step three, the Smart Calibrator, turns that score into three detector settings. Then YOLOv8n finds the boxes with these settings and ByteTrack links them over time. The boxes are reused in step one for the next frame. The next slides explain each step in detail."</p></aside>
</section>

'''

a = h.index('data-title="What we add"'); a = h.rindex('<section class="slide', 0, a)
b = h.index('</section>', a) + len('</section>\n\n')
h = h[:a] + idea + h[b:]

h, n = re.subn(r'\s*<span class="newtag">NEW</span>', '', h)
print("removed NEW tags:", n)
assert 'class="newtag"' not in h and 'class="adapt"' not in h and ">NEW<" not in h
open(P, "w", encoding="utf-8").write(h)
print("ok", r1, r2, r3)
