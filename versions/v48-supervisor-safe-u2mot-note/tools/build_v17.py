#!/usr/bin/env python3
"""v17 (from v16):
 - Section IV Step 1: the cue pictures come first; the old five-cue table becomes two simple slides
   (clues from the boxes: crowd, tiny · clues from the picture: edges, night, blur) with plain explanations of
   Canny edge density, mean brightness and the variance of the Laplacian;
 - 'The Three Detector Settings We Change': too high / too low for each setting, with an example object."""
import os, re

ROOT = os.path.expanduser("~/Desktop/ACMOT-Presentation-Versions/versions/v17-simple-cues-and-setting-examples")
P = os.path.join(ROOT, "index.html")
h = open(P, encoding="utf-8").read()


def block(title):
    a = h.index(f'data-title="{title}"')
    a = h.rindex('<section class="slide', 0, a)
    b = h.index('</section>', a) + len('</section>\n\n')
    return a, b


S1 = "Section IV · Step 1 of 3 — Measure"
SEC = 'data-sec="4" data-secname="IV · AC-MOT"'

boxes = f'''<section class="slide" {SEC} data-title="Clues from the boxes" data-explain="x-cues|Explain Each Cue">
  <header class="s-head"><div class="kicker">{S1}</div><h2>Step 1: Two Clues From the Detector’s Boxes</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>Two clues use the <b>boxes found in the previous frame</b>: <b>how many</b> objects are there, and <b>how small</b> are they?</p></div>
    <div class="g2 grow" style="gap:24px">
      <div class="card col" style="border-top:6px solid #2563EB;gap:10px"><div class="tag" style="color:#1D4ED8">Crowd · how many objects?</div>
        <div class="xchain" style="justify-content:flex-start;font-size:24px"><span class="pill">count the boxes</span>→<span class="pill">÷ 30</span>→<span class="pill">stop at 1</span></div>
        <table class="tbl" style="font-size:25px"><tr><th style="text-align:left">Boxes</th><th style="text-align:left">Crowd</th></tr>
          <tr><td>3</td><td style="text-align:left">3 ÷ 30 = <b>0.10</b></td></tr><tr><td>15</td><td style="text-align:left">15 ÷ 30 = <b>0.50</b></td></tr>
          <tr><td>30</td><td style="text-align:left">30 ÷ 30 = <b>1.00</b></td></tr><tr><td>45</td><td style="text-align:left">more than 30 → still <b>1.00</b></td></tr></table>
        <p class="small">30 or more objects already counts as <b>fully crowded</b>.</p></div>
      <div class="card col" style="border-top:6px solid #F59E0B;gap:10px"><div class="tag" style="color:#B45309">Tiny · are the objects very small?</div>
        <div class="xchain" style="justify-content:flex-start;font-size:24px"><span class="pill">look at every box</span>→<span class="pill">count boxes under 32 × 32 px</span>→<span class="pill">÷ all boxes</span></div>
        <table class="tbl" style="font-size:25px"><tr><th style="text-align:left">Boxes</th><th style="text-align:left">Tiny</th></tr>
          <tr><td>10 boxes, 2 tiny</td><td style="text-align:left">2 ÷ 10 = <b>0.2</b></td></tr><tr><td>10 boxes, 7 tiny</td><td style="text-align:left">7 ÷ 10 = <b>0.7</b></td></tr></table>
        <p class="small"><b>32 × 32 pixels</b> is how the COCO dataset defines a <b>small object</b>.</p></div>
    </div>
    <div class="note">Both clues give a number from <b>0</b> (easy) to <b>1</b> (hard).</div>
  </div>
  <footer class="s-foot"><span class="prov p-illus">Box counts are examples · 30 = our design constant · 32 × 32 = COCO small-object size</span></footer>
  <aside class="notes"><p><b>Say:</b> "The first two clues come from the boxes of the previous frame. Crowd counts the boxes and divides by 30 — 30 or more is fully crowded. Tiny is the share of boxes smaller than 32 by 32 pixels, the COCO size for a small object."</p><p><b>If asked “why 30?”:</b> "It is a design constant: it turns the count into a number between 0 and 1. Optuna did not change it."</p></aside>
</section>

'''

picture = f'''<section class="slide" {SEC} data-title="Step 1: measure scene complexity" data-explain="x-cues|Explain Each Cue">
  <header class="s-head"><div class="kicker">{S1}</div><h2>Step 1: Three Clues From the Picture Itself</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>Three clues look at a <b>small gray copy of the frame</b> and ask: is it <b>busy</b>, <b>dark</b> or <b>blurry</b>?</p></div>
    <div class="g3 grow" style="gap:18px">
      <div class="card col" style="border-top:6px solid #7C3AED;gap:8px"><div class="tag" style="color:#6D28D9">Edges · is it busy?</div>
        <p><b>Canny</b> is a standard method that <b>draws the edges</b> of a picture: the places where brightness <b>changes sharply</b>, like object borders and road lines.</p>
        <p><b>Edge density</b> = edge pixels ÷ all pixels.</p>
        <div class="note" style="font-size:22px">Edges = edge density ÷ 0.14, at most 1<br>→ <b>14%</b> edge pixels already counts as <b>fully busy</b>.</div>
        <p class="small">Calm sky 0.021 → <b>0.15</b> · busy parking lot 0.295 → <b>1</b></p></div>
      <div class="card col" style="border-top:6px solid #0F766E;gap:8px"><div class="tag" style="color:#0F766E">Night · is it dark?</div>
        <p>Every pixel has a <b>brightness</b> from <b>0</b> (black) to <b>255</b> (white).</p>
        <p>We take the <b>average brightness</b> of the whole picture.</p>
        <div class="note" style="font-size:22px">Night = <b>1</b> if the average is below <b>80</b>, otherwise 0.</div>
        <p class="small">Day 110.6 → <b>0</b> · night 40.5 → <b>1</b></p></div>
      <div class="card col" style="border-top:6px solid #E11D48;gap:8px"><div class="tag" style="color:#BE123C">Blur · is it blurry?</div>
        <p>The <b>Laplacian</b> is a filter that gives a <b>big answer at sharp details</b> and a small answer on smooth areas.</p>
        <p>Its <b>variance</b> (spread) is <b>big for a sharp picture</b> and <b>small for a blurry one</b>.</p>
        <div class="note" style="font-size:22px">Blur = <b>1</b> if the variance is below <b>180</b>, otherwise 0.</div>
        <p class="small">Sharp 4,074 → <b>0</b> · blurred 4 → <b>1</b></p></div>
    </div>
    <div class="callout warn" style="font-size:23px"><b>30, 32 × 32, 0.14, 80 and 180</b> are fixed design constants (only 32 × 32 comes from COCO). <b>Optuna did not change them.</b></div>
    <div class="cap">Canny, IEEE TPAMI 1986 · variance of the Laplacian: Pech-Pacheco et al., ICPR 2000 · small object: Lin et al., “Microsoft COCO,” ECCV 2014</div>
  </div>
  <footer class="s-foot"><span class="prov p-hist">Original SCI cue definitions · example values computed on the pictures of the previous slide</span></footer>
  <aside class="notes"><p><b>Say:</b> "Three clues look at the picture. Edges: Canny marks every place where brightness changes sharply; edge density is the share of edge pixels, and 14 percent already counts as fully busy. Night: the average brightness from 0 to 255 — below 80 means dark. Blur: the Laplacian reacts to sharp details; if its variance is below 180, the picture is blurry."</p>
    <p><b>If asked about 0.14, 80 and 180:</b> "Canny edges, mean brightness and the variance of the Laplacian are standard measurements. The exact limits are empirical design constants, and they stayed fixed — Optuna did not tune them."</p></aside>
</section>

'''

settings = f'''<section class="slide" {SEC} data-title="The three detector settings" data-explain="x-controller|Explain Controller Logic">
  <header class="s-head"><div class="kicker">Section IV · Step 3 of 3 — Set the detector</div><h2>Step 3: The Three Detector Settings We Change</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>Each setting has a job — and <b>both too high and too low cause a problem</b> for the objects.</p></div>
    <div class="g3 grow" style="gap:18px">
      <div class="card col" style="border-top:6px solid #4F46E5;gap:8px"><h3>Confidence threshold</h3><p>How <b>sure</b> must the detector be to keep a box?</p>
        <table class="tbl" style="font-size:22px"><tr><td class="strong bad">too high</td><td style="text-align:left">weak but <b>real</b> objects are <b>missed</b></td></tr><tr><td class="strong bad">too low</td><td style="text-align:left"><b>false boxes</b> on shadows and noise</td></tr></table>
        <div class="note" style="font-size:21px"><b>Example:</b> a tiny car scores 0.4. Threshold 0.5 → the car is <b>missed</b>. Threshold 0.2 → the car is kept, but a shadow scoring 0.25 is kept too.</div></div>
      <div class="card col" style="border-top:6px solid #0D9488;gap:8px"><h3>NMS IoU</h3><p>When are two overlapping boxes <b>the same object</b>?</p>
        <table class="tbl" style="font-size:22px"><tr><td class="strong bad">too high</td><td style="text-align:left"><b>copies stay</b> — one car counted twice</td></tr><tr><td class="strong bad">too low</td><td style="text-align:left">close <b>real</b> objects are <b>deleted</b></td></tr></table>
        <div class="note" style="font-size:21px"><b>Example:</b> two boxes on one car overlap 0.6. Limit 0.45 → the copy is removed. Limit 0.7 → both stay. Two people standing close (overlap 0.5) with limit 0.45 → one <b>real person is deleted</b>.</div></div>
      <div class="card col" style="border-top:6px solid #D97706;gap:8px"><h3>Input size</h3><p>How <b>big</b> is the image the detector sees?</p>
        <table class="tbl" style="font-size:22px"><tr><td class="strong bad">too small</td><td style="text-align:left">tiny objects <b>vanish</b></td></tr><tr><td class="strong bad">too big</td><td style="text-align:left">every frame is <b>slower</b></td></tr></table>
        <div class="note" style="font-size:21px"><b>Example:</b> a person only a few pixels wide. Small input (640) → the person can <b>disappear</b>. Big input (832) → still visible, but the frame takes <b>more time</b>.</div></div>
    </div>
    <div class="g2" style="gap:20px">
      <div class="note" style="border-left-color:var(--bad)"><b>Hard frame →</b> lower confidence · stronger copy removal · bigger input</div>
      <div class="note" style="border-left-color:var(--good)"><b>Easy frame →</b> stay strict, small and fast</div>
    </div>
  </div>
  <footer class="s-foot"><span class="prov p-illus">Examples are illustrations · sizes 640 / 832 from the original Smart Calibrator</span></footer>
  <aside class="notes"><p><b>Say:</b> "Every setting can go wrong in both directions. Confidence too high misses a weak real car; too low keeps shadows as false boxes. NMS IoU too high keeps duplicate boxes on one car; too low deletes a real person standing next to another. Input size too small makes tiny people disappear; too big makes every frame slower. That is why the best value depends on the scene."</p></aside>
</section>

'''

# replace the settings slide
a, b = block("The three detector settings")
h = h[:a] + settings + h[b:]
# remove the old five-cue table slide
a, b = block("Step 1: measure scene complexity")
h = h[:a] + h[b:]
# pictures first, then the two new clue slides right after the pictures slide
a, b = block("Three clues on real pictures")
pics = h[a:b]
pics = re.sub(r'<div class="kicker">.*?</div><h2>.*?</h2>',
              f'<div class="kicker">{S1}</div><h2>Step 1: First, See the Clues in Real Pictures</h2>', pics, count=1, flags=re.S)
h = h[:a] + pics + boxes + picture + h[b:]

main = h[:h.index('<div class="overlay xview"')]
titles = re.findall(r'<section class="slide[^"]*"[^>]*data-title="([^"]*)"', main)
i = titles.index("What we add")
assert titles[i + 1:i + 5] == ["Three clues on real pictures", "Clues from the boxes", "Step 1: measure scene complexity", "The pipeline for each frame"], titles[i:i + 6]

# outline ranges shift by one from Section IV on
tags = re.findall(r'<section class="slide[^"]*"[^>]*>', main)
start = {re.search(r'id="(sec-\d+)"', t).group(1): k for k, t in enumerate(tags, 1) if re.search(r'id="(sec-\d+)"', t)}
od = sorted(start.items(), key=lambda kv: kv[1])
rng = {k: (v, (od[j + 1][1] - 1) if j + 1 < len(od) else len(tags) - 1) for j, (k, v) in enumerate(od)}


def fix_range(m):
    g = m.group(1)
    return f'<button class="ol-row" data-goto="{g}">' + re.sub(r'slides \d+ - \d+', f'slides {rng[g][0]} - {rng[g][1]}', m.group(2))


h, n = re.subn(r'<button class="ol-row" data-goto="(sec-\d+)">(.*?</button>)', fix_range, h)
assert n == 9, n
open(P, "w", encoding="utf-8").write(h)

m = open(os.path.join(ROOT, "assets/data/meaning.js"), encoding="utf-8").read()
old = "t: 'The clues are <b>simple image measurements you can see</b>: a busy scene has more edges, a night image is darker, and a blurred image has less sharp detail.' }"
assert m.count(old) == 1
m = m.replace(old, "t: 'Before any formula, just <b>look</b>: a busy scene has <b>many edges</b>, a night picture is <b>darker</b>, and a blurred picture has <b>no sharp details</b>.' }")
open(os.path.join(ROOT, "assets/data/meaning.js"), "w", encoding="utf-8").write(m)
print("ok · slides:", len(tags), rng)
