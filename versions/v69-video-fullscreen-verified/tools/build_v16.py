#!/usr/bin/env python3
"""v16 (from v15):
 - remove Section IX (literature comparison + protocol audit) and its mentions in the conclusion;
 - Related Work: detectors through the ages (timeline, traditional detectors, deep-learning detectors);
 - Section III (problem) rewritten in simple words, three clear slides + baseline;
 - Section IV (AC-MOT) re-ordered as Step 1 measure -> Step 2 score (SCI) -> Step 3 set the detector,
   with a new slide on the three detector settings. All result numbers unchanged."""
import os, re

ROOT = os.path.expanduser("~/Desktop/ACMOT-Presentation-Versions/versions/v16-clear-problem-acmot-detector-history")


def load(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def save(p, s): open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)


def rep(s, old, new, n=1):
    assert s.count(old) == n, (s.count(old), old[:110])
    return s.replace(old, new)


h = load("index.html")
xi = h.index('<div class="overlay xview"')
main, rest = h[:xi], h[xi:]
starts = [m.start() for m in re.finditer(r'<section class="slide[^"]*"[^>]*>', main)]
assert len(starts) == 93, len(starts)
last_end = main.rindex('</section>') + len('</section>')
order, blocks = [], {}
for i, a in enumerate(starts):
    b = starts[i + 1] if i + 1 < len(starts) else last_end
    blk = main[a:b].rstrip() + "\n\n"
    t = re.search(r'data-title="([^"]*)"', blk).group(1)
    assert t not in blocks, t
    order.append(t); blocks[t] = blk
prefix, suffix = main[:starts[0]], main[last_end:]


def head(blk, kicker, h2):
    blk, n = re.subn(r'<div class="kicker">.*?</div><h2>.*?</h2>', f'<div class="kicker">{kicker}</div><h2>{h2}</h2>', blk, count=1, flags=re.S)
    assert n == 1
    return blk


def edit(blk, *pairs):
    for o, n in pairs:
        blk = rep(blk, o, n)
    return blk


def slide(sec, secname, title, kicker, h2, body, notes, foot="", explain=""):
    ex = f' data-explain="{explain}"' if explain else ""
    ft = f'\n  <footer class="s-foot">{foot}</footer>' if foot else ""
    return f'''<section class="slide" data-sec="{sec}" data-secname="{secname}" data-title="{title}"{ex}>
  <header class="s-head"><div class="kicker">{kicker}</div><h2>{h2}</h2></header>
  <div class="s-body col">
{body}
  </div>{ft}
  <aside class="notes">{notes}</aside>
</section>

'''


def meaning(t, tag="The main idea"):
    return f'    <div class="meaning"><div class="tag">{tag}</div><p>{t}</p></div>'


def say(t, extra=""):
    return f'<p><b>Say:</b> "{t}"</p>' + extra


II = (2, "II · Related work")
III = (3, "III · Problem & baseline")
IV = (4, "IV · AC-MOT")

# ============================================================ Related work: detectors through the ages
ages = slide(*II, "Detectors through the ages", "Section II · Detectors through the ages", "Object Detectors Through the Ages", "\n".join([
    meaning("Object detection moved from <b>rules made by people</b> to <b>deep learning</b> — and from <b>slow and careful</b> to <b>fast and accurate</b>."),
    '''    <div class="flow grow noabbr" style="align-items:stretch;gap:0">
      <div class="card col" style="width:350px;gap:8px;border-top:6px solid #64748B"><div class="tag" style="color:#475569">2001 – 2012 · Traditional</div>
        <p>Features <b>made by people</b> + a simple classifier.</p><div class="pills"><span class="pill">Viola–Jones 2001</span><span class="pill">HOG + SVM 2005</span><span class="pill">DPM 2008</span></div></div>
      <div class="arr sm" style="align-self:center"></div>
      <div class="card col" style="width:350px;gap:8px;border-top:6px solid #2563EB"><div class="tag" style="color:#1D4ED8">2014 – 2015 · Two-stage</div>
        <p><b>Deep learning</b>: first find possible regions, then check each one.</p><div class="pills"><span class="pill">R-CNN 2014</span><span class="pill">Fast R-CNN 2015</span><span class="pill">Faster R-CNN 2015</span></div></div>
      <div class="arr sm" style="align-self:center"></div>
      <div class="card col" style="width:350px;gap:8px;border-top:6px solid #4F46E5;box-shadow:0 0 0 3px #E0E7FF,var(--shadow)"><div class="tag" style="color:#4338CA">2016 → today · One-stage · our family</div>
        <p><b>Deep learning</b>: one look gives boxes and classes together.</p><div class="pills"><span class="pill">YOLO 2016</span><span class="pill">SSD 2016</span><span class="pill">YOLOv3 2018</span><span class="pill">YOLOv8 2023</span><span class="pill">YOLO12 2025</span></div></div>
      <div class="arr sm" style="align-self:center"></div>
      <div class="card col" style="width:350px;gap:8px;border-top:6px solid #0D9488"><div class="tag" style="color:#0F766E">2020 → today · Transformers</div>
        <p><b>Deep learning</b> with attention: looks at the whole image together.</p><div class="pills"><span class="pill">DETR 2020</span><span class="pill">RT-DETR</span><span class="pill">RF-DETR 2025</span></div></div>
    </div>''',
    '''    <div class="g2" style="gap:22px">
      <div class="card flat"><h3>Traditional</h3><p>Hand-made features · runs on a CPU · <b>weak</b> with small, crowded or unusual objects.</p></div>
      <div class="card flat"><h3>Deep learning</h3><p>Features <b>learned</b> from many labelled images · needs a GPU · <b>much stronger</b> in hard scenes.</p></div>
    </div>''']),
    say("Detection started with hand-made features: Viola–Jones, HOG and DPM. Deep learning came with R-CNN and Faster R-CNN, which were accurate but slow. YOLO made detection one fast look, and transformers like DETR and RF-DETR look at the whole image."),
    foot='<span class="prov p-pub">Years of the original publications</span>')

trad = slide(*II, "Traditional detectors", "Section II · Detectors through the ages", "Before Deep Learning: Traditional Detectors", "\n".join([
    meaning("These detectors used <b>features designed by people</b>, not learned features. They could run <b>on a CPU</b>, but they were <b>weak in hard scenes</b>."),
    '''    <table class="tbl" style="font-size:25px">
      <tr><th>Year</th><th style="text-align:left">Detector</th><th style="text-align:left">How it works</th><th style="text-align:left">Good at</th><th style="text-align:left">Weak at</th></tr>
      <tr><td>2001</td><td style="text-align:left" class="strong">Viola–Jones</td><td style="text-align:left">slides a window and checks simple light/dark patterns with many quick tests</td><td style="text-align:left" class="good">very fast faces</td><td style="text-align:left" class="bad">mostly one object type</td></tr>
      <tr><td>2005</td><td style="text-align:left" class="strong">HOG + SVM</td><td style="text-align:left">describes shape by edge directions (HOG); an SVM says object or not</td><td style="text-align:left" class="good">people with clear shapes</td><td style="text-align:left" class="bad">hidden and small objects</td></tr>
      <tr><td>2008</td><td style="text-align:left" class="strong">DPM</td><td style="text-align:left">a whole-object template plus movable part templates</td><td style="text-align:left" class="good">objects that change pose</td><td style="text-align:left" class="bad">slow and complex</td></tr>
    </table>''',
    '''    <div class="g2 grow" style="gap:22px">
      <div class="card" style="border-left:6px solid #64748B"><h3>Type</h3><p><b>Traditional computer vision</b>: hand-made features + a classic classifier. <b>No deep learning.</b></p></div>
      <div class="card" style="border-left:6px solid var(--bad)"><h3>Why they were replaced</h3><p>After 2012, deep learning <b>learned better features</b> and became far more accurate.</p></div>
    </div>''',
    '    <div class="note">Our survey benchmark has <b>no comparable scores</b> for these methods, so no numbers are shown.</div>']),
    say("Viola–Jones checked simple light and dark patterns and was very fast for faces. HOG with an SVM described shapes with edge directions. DPM added movable parts. All were hand-made features, not deep learning, and they struggled with small or hidden objects."),
    foot='<span class="prov p-pub">Method descriptions from the original papers · no scores shown</span>')

deep = slide(*II, "Deep learning detectors", "Section II · Detectors through the ages", "Deep Learning Detectors: From Careful to Fast", "\n".join([
    meaning("Deep learning <b>learns the features itself</b>. Two-stage models were accurate but slow; one-stage and new transformer models are <b>fast enough for live video</b>."),
    '''    <table class="tbl" style="font-size:22px">
      <tr><th>Year</th><th style="text-align:left">Detector</th><th style="text-align:left">Family</th><th style="text-align:left">How it works</th><th>mAP</th><th>Time</th><th style="text-align:left">Strong / weak</th></tr>
      <tr><td>2014</td><td style="text-align:left" class="strong">R-CNN</td><td style="text-align:left">two-stage</td><td style="text-align:left">proposes regions, runs a CNN on each one</td><td>—</td><td>—</td><td style="text-align:left"><span class="good">+ big accuracy jump</span> · <span class="bad">− very slow</span></td></tr>
      <tr><td>2015</td><td style="text-align:left" class="strong">Faster R-CNN</td><td style="text-align:left">two-stage</td><td style="text-align:left">one network proposes and checks regions</td><td>37.0</td><td>172 ms</td><td style="text-align:left"><span class="good">+ accurate</span> · <span class="bad">− too slow for live video</span></td></tr>
      <tr><td>2016</td><td style="text-align:left" class="strong">YOLO</td><td style="text-align:left">one-stage</td><td style="text-align:left">one look: a grid predicts boxes and classes</td><td>—</td><td>—</td><td style="text-align:left"><span class="good">+ very fast</span> · <span class="bad">− weak on small objects</span></td></tr>
      <tr><td>2018</td><td style="text-align:left" class="strong">YOLOv3</td><td style="text-align:left">one-stage</td><td style="text-align:left">predicts at three sizes</td><td>31.0</td><td>28.6 ms</td><td style="text-align:left"><span class="good">+ real-time</span> · <span class="bad">− lower accuracy</span></td></tr>
      <tr><td>2020</td><td style="text-align:left" class="strong">DETR R101</td><td style="text-align:left">transformer</td><td style="text-align:left">attention over the whole image</td><td>42.9</td><td>145 ms</td><td style="text-align:left"><span class="good">+ simple design</span> · <span class="bad">− very slow</span></td></tr>
      <tr class="sel"><td>2023</td><td style="text-align:left" class="strong">YOLOv8n</td><td style="text-align:left">one-stage</td><td style="text-align:left">small YOLO without anchor boxes</td><td>37.3</td><td>3.2 ms</td><td style="text-align:left"><span class="good">+ tiny and fast</span> · <span class="bad">− less accurate than big models</span></td></tr>
      <tr><td>2025</td><td style="text-align:left" class="strong">YOLO12m</td><td style="text-align:left">one-stage</td><td style="text-align:left">YOLO with attention blocks</td><td>52.5</td><td>4.86 ms</td><td style="text-align:left"><span class="good">+ real-time accuracy leader</span> · <span class="bad">− bigger (20.2M)</span></td></tr>
      <tr><td>2025</td><td style="text-align:left" class="strong">RF-DETR-S</td><td style="text-align:left">transformer</td><td style="text-align:left">a real-time DETR</td><td class="best">52.9</td><td>3.5 ms</td><td style="text-align:left"><span class="good">+ best published trade-off</span> · <span class="bad">− bigger (32.1M)</span></td></tr>
    </table>''',
    '    <div class="callout">Best in our table: <b>RF-DETR-S</b> (52.9 mAP at 3.5 ms). Our choice: <b>YOLOv8n</b> — tiny, fast and easy to control.</div>']),
    say("Deep learning learns the features. R-CNN and Faster R-CNN were accurate but slow — Faster R-CNN needs 172 milliseconds. YOLO made it one fast look. DETR brought transformers but was slow. Today RF-DETR-S has the best trade-off in our table, and we use YOLOv8n because it is tiny, fast and easy to control."),
    foot='<span class="prov p-pub">mAP and time: published values in our IEEE ICMISI 2026 survey (COCO val2017 · T4 · TensorRT FP16 · 640 × 640) · — = not in our benchmark</span>')

# ============================================================ Section III: the problem, simply
p1 = slide(*III, "One fixed threshold", "Section III · The problem", "One Drone Video, Very Different Frames", "\n".join([
    meaning("In the <b>same drone video</b>, some frames are <b>easy</b> and some are <b>hard</b>."),
    '''    <div class="g2 grow" style="gap:24px">
      <div class="card col" style="border-top:6px solid var(--good);gap:10px"><h3 class="good">Easy frame</h3>
        <div class="row grow" style="gap:18px"><div class="img zoomable" style="flex:0 0 360px"><img src="assets/figures/image1.png" alt="Easy frame"></div>
          <ul class="clean"><li><b>few</b> objects</li><li><b>big</b> objects</li><li><b>good</b> light</li><li><b>sharp</b> picture</li></ul></div></div>
      <div class="card col" style="border-top:6px solid var(--bad);gap:10px"><h3 class="bad">Hard frame</h3>
        <div class="row grow" style="gap:18px"><div class="img zoomable" style="flex:0 0 360px"><img src="assets/figures/image20.jpeg" alt="Hard frame"></div>
          <ul class="clean"><li><b>many</b> objects</li><li><b>tiny</b> objects</li><li><b>busy</b> background</li><li><b>dark</b> or <b>blurry</b></li></ul></div></div>
    </div>''',
    '    <div class="callout">As the drone flies, the scene can change from <b>easy</b> to <b>hard</b> and back again.</div>']),
    say("Look at two frames from drone video. The left one is easy: few, big objects in good light. The right one is hard: many tiny objects, a busy background, and poor light. And one flight can move between the two."))

p2 = slide(*III, "Same settings for every frame", "Section III · The problem", "The Problem: The Detector Never Changes Its Settings", "\n".join([
    meaning("A normal detector uses the <b>same settings for every frame</b> — easy or hard."),
    '''    <div class="flow" style="gap:0;align-items:stretch">
      <div class="img" style="width:330px;height:190px"><img src="assets/figures/image1.png" alt=""><span class="lbl" style="color:#15803D">easy</span></div><div class="arr" style="align-self:center"></div>
      <div class="img" style="width:330px;height:190px"><img src="assets/figures/image20.jpeg" alt=""><span class="lbl" style="color:#B91C1C">hard</span></div><div class="arr" style="align-self:center"></div>
      <div class="img" style="width:330px;height:190px"><img src="assets/figures/image21.jpeg" alt=""><span class="lbl" style="color:#B91C1C">hard · dark</span></div><div class="arr" style="align-self:center"></div>
      <div class="img" style="width:330px;height:190px"><img src="assets/figures/image26.jpeg" alt=""><span class="lbl" style="color:#15803D">easy</span></div>
    </div>''',
    '''    <div class="card flat tc" style="padding:12px 20px;border:2px dashed #94A3B8"><span class="strong" style="font-size:28px">same settings for all frames →</span> <span class="pills" style="display:inline-flex;margin-left:12px"><span class="pill">same confidence threshold</span><span class="pill">same NMS IoU</span><span class="pill">same input size</span></span></div>''',
    '''    <div class="g2 grow" style="gap:22px">
      <div class="card" style="border-left:6px solid var(--bad)"><h3 class="bad">On a hard frame</h3><p>Settings that are too strict <b>miss weak and tiny objects</b>.</p></div>
      <div class="card" style="border-left:6px solid var(--warn)"><h3 style="color:#B45309">On an easy frame</h3><p>Extra effort, like a bigger input image, only <b>costs time</b>.</p></div>
    </div>''',
    '    <div class="callout warn">One fixed setting <b>cannot be right for every frame</b>.</div>']),
    say("The frames change, but the detector settings do not: the same confidence threshold, the same NMS IoU and the same input size for every frame. On a hard frame, strict settings miss weak and tiny objects. On an easy frame, extra effort only costs time."),
    foot='<span class="prov p-illus">Example frames · no numbers</span>')

p3 = slide(*III, "The main question", "Section III · Research question", "The Main Question", "\n".join([
    '''    <div class="card sec tc" style="padding:30px 48px"><div class="tag">Our question</div>
      <p class="lead mt8" style="font-size:50px;line-height:1.22;color:var(--ink)">If the scene keeps changing, <b>why do the detector settings stay the same?</b></p></div>''',
    '''    <div class="g3 grow" style="gap:20px">
      <div class="card"><h3>Confidence threshold</h3><p>How <b>sure</b> the detector must be to keep a box.</p></div>
      <div class="card"><h3>NMS IoU</h3><p>How much two boxes may <b>overlap</b> before one is removed as a copy.</p></div>
      <div class="card"><h3>Input size</h3><p>How <b>big</b> the image is when the detector looks at it.</p></div>
    </div>''',
    '    <div class="callout good">Our idea: let these settings <b>follow the scene</b> — automatically, for every frame, <b>without retraining</b> the detector.</div>']),
    say("So our question is simple: if the scene keeps changing, why do the detector settings stay the same? The settings are three: the confidence threshold — how sure the detector must be; the NMS IoU — how much boxes may overlap; and the input size. Our idea is to let them follow the scene."))

# ============================================================ Section IV: AC-MOT, step by step
S1, S2, S3 = "Section IV · Step 1 of 3 — Measure", "Section IV · Step 2 of 3 — Score", "Section IV · Step 3 of 3 — Set the detector"

idea = slide(*IV, "What we add", "Section IV · The idea", "The Idea: Measure the Scene, Then Set the Detector", "\n".join([
    meaning("AC-MOT works like a good driver: <b>slow and careful in fog</b>, <b>fast on an empty road</b>. It checks how hard each frame is, then <b>adjusts the detector</b> to match."),
    '''    <div class="flow" style="flex-wrap:nowrap">
      <div class="node io frag" style="width:130px">Frame</div><div class="arr sm frag"></div>
      <div class="node ad frag" style="width:220px">Step 1 · Measure<small>five simple clues</small><span class="adapt">NEW</span></div><div class="arr sm frag"></div>
      <div class="node ad frag" style="width:220px">Step 2 · Score<small>SCI: 0 easy … 1 hard</small><span class="adapt">NEW</span></div><div class="arr sm frag"></div>
      <div class="node ad frag" style="width:230px">Step 3 · Set<small>Smart Calibrator</small><span class="adapt">NEW</span></div><div class="arr sm frag"></div>
      <div class="node fx frag" style="width:190px">Detector<small>YOLOv8n · unchanged</small></div><div class="arr sm frag"></div>
      <div class="node fx frag" style="width:190px">Tracker<small>ByteTrack · unchanged</small></div><div class="arr sm frag"></div>
      <div class="node good frag" style="width:120px">Tracks</div>
    </div>''',
    '''    <div class="g3 grow" style="gap:20px">
      <div class="card" style="border-left:6px solid #4F46E5"><h3>What is new</h3><p>Three small steps <b>before</b> the detector: measure, score, set.</p></div>
      <div class="card" style="border-left:6px solid #64748B"><h3>What stays the same</h3><p>The detector and the tracker. <b>No retraining.</b></p></div>
      <div class="card" style="border-left:6px solid var(--good)"><h3>What changes per frame</h3><p>Only the detector settings: confidence, NMS IoU and input size.</p></div>
    </div>''']),
    '<p><b>How to present:</b> press → to reveal the pipeline step by step.</p>' +
    say("AC-MOT is not a new detector and not a new tracker. It adds three small steps before the detector: step one measures five simple clues, step two turns them into one difficulty score called SCI, and step three sets the detector for that difficulty. The detector and tracker stay the same."))

cue_table = '''<table class="tbl" style="font-size:24px">
      <tr><th style="text-align:left">Clue</th><th style="text-align:left">Question it answers</th><th style="text-align:left">How we measure it</th><th style="text-align:left">Value</th></tr>
      <tr><td class="strong">Crowd</td><td style="text-align:left">How many objects?</td><td style="text-align:left" class="fcell">boxes in the previous frame ÷ 30, at most 1</td><td style="text-align:left">0 → 1</td></tr>
      <tr><td class="strong">Tiny</td><td style="text-align:left">Are the objects tiny?</td><td style="text-align:left" class="fcell">share of boxes smaller than 32 × 32 pixels [1]</td><td style="text-align:left">0 → 1</td></tr>
      <tr><td class="strong">Edges</td><td style="text-align:left">Is the background busy?</td><td style="text-align:left" class="fcell">Canny edge density [2] ÷ 0.14, at most 1</td><td style="text-align:left">0 → 1</td></tr>
      <tr><td class="strong">Night</td><td style="text-align:left">Is it dark?</td><td style="text-align:left" class="fcell">1 if the mean brightness is below 80</td><td style="text-align:left">0 or 1</td></tr>
      <tr><td class="strong">Blur</td><td style="text-align:left">Is it blurry?</td><td style="text-align:left" class="fcell">1 if the Laplacian variance [3] is below 180</td><td style="text-align:left">0 or 1</td></tr>
    </table>'''

iv = []
iv.append(idea)
b = head(blocks["Step 1: measure scene complexity"], S1, "Step 1: Measure Five Simple Clues")
b = edit(b, ('<p>The Scene Analyzer measures <b>five cheap cues</b>. Three are <b>continuous</b> (0 → 1) and two are <b>binary</b> (0 or 1).</p>',
             '<p>The Scene Analyzer asks <b>five simple questions</b> about each frame. Three answers are a number from 0 to 1; two are just <b>yes (1) or no (0)</b>.</p>'))
b, n = re.subn(r'<table class="tbl" style="font-size:24px">.*?</table>', cue_table, b, count=1, flags=re.S); assert n == 1
iv.append(b)
iv.append(head(blocks["Three clues on real pictures"], S1, "Step 1: Three Clues on Real Pictures"))
iv.append(head(blocks["The pipeline for each frame"], S2, "Step 2: One Difficulty Score — the SCI"))
iv.append(head(blocks["Initial SCI"], S2, "Step 2: How the Five Clues Become SCI"))
iv.append(head(blocks["SCI example 0.63"], S2, "Step 2: Example — SCI = 0.63"))
iv.append(head(blocks["Implementation of the calibrator"], S2, "Step 2: Keeping SCI Stable and Cheap"))
iv.append(head(blocks["SCI from frame to score"], "Section IV · Steps 1 and 2 together", "From a Frame to SCI — All Steps Together"))
iv.append(slide(*IV, "The three detector settings", S3, "Step 3: The Three Detector Settings We Change", "\n".join([
    meaning("The Smart Calibrator changes only <b>three detector settings</b>. Each one has a <b>simple job</b>."),
    '''    <div class="g3 grow" style="gap:20px">
      <div class="card col" style="border-top:6px solid #4F46E5;gap:8px"><h3>Confidence threshold</h3><p>How <b>sure</b> must the detector be to keep a box?</p>
        <table class="tbl" style="font-size:22px"><tr><td class="strong">lower</td><td style="text-align:left">keeps weak, tiny objects · more false boxes possible</td></tr><tr><td class="strong">higher</td><td style="text-align:left">cleaner · misses weak objects</td></tr></table></div>
      <div class="card col" style="border-top:6px solid #0D9488;gap:8px"><h3>NMS IoU</h3><p>When are two overlapping boxes <b>the same object</b>?</p>
        <table class="tbl" style="font-size:22px"><tr><td class="strong">lower</td><td style="text-align:left">removes more overlapping boxes · fewer copies</td></tr><tr><td class="strong">higher</td><td style="text-align:left">keeps more overlapping boxes</td></tr></table></div>
      <div class="card col" style="border-top:6px solid #D97706;gap:8px"><h3>Input size</h3><p>How <b>big</b> is the image the detector sees?</p>
        <table class="tbl" style="font-size:22px"><tr><td class="strong">bigger</td><td style="text-align:left">more pixels for tiny objects · slower</td></tr><tr><td class="strong">smaller</td><td style="text-align:left">faster · fewer details</td></tr></table></div>
    </div>''',
    '''    <div class="g2" style="gap:20px">
      <div class="note" style="border-left-color:var(--bad)"><b>Hard frame →</b> lower confidence · stronger copy removal · bigger input</div>
      <div class="note" style="border-left-color:var(--good)"><b>Easy frame →</b> stay strict, small and fast</div>
    </div>''']),
    say("Step three changes only three settings. Confidence: how sure the detector must be to keep a box. NMS IoU: when two overlapping boxes count as the same object. Input size: how big the image is. On a hard frame we lower confidence, remove copies more strongly, and use a bigger input. Easy frames stay strict and fast."),
    foot='<span class="prov p-hist">Original hand-set Smart Calibrator · directions only</span>', explain="x-controller|Explain Controller Logic"))
iv.append(head(blocks["Confidence threshold"], S3, "Step 3: The Confidence Threshold in Detail"))
iv.append(head(blocks["One frame becomes one setting"], S3, "Step 3: From SCI to Detector Settings"))
iv.append(head(blocks["Step 2: use SCI to choose settings"], S3, "Step 3: The Exact Rules"))
iv.append(head(blocks["Smart Calibrator exact settings"], S3, "Step 3: What Changes and What Never Changes"))

# ============================================================ assemble
new = []
for t in order:
    blk = blocks[t]
    sec = re.search(r'data-secname="([^"]*)"', blk).group(1)
    if sec.startswith("IX · Protocol audit"):
        continue  # Section IX removed
    if t == "Detector families":
        new += [ages, trad, deep]
    if t == "One fixed threshold":
        new += [p1, p2]; continue
    if t == "The main question":
        new.append(p3); continue
    if t == "Section IV":
        blk = edit(blk, ('<h1>AC-MOT: The First Adaptive Design</h1>', '<h1>AC-MOT: Our Idea, Step by Step</h1>'),
                   ('<p>Not a new detector and not a new tracker — a small control layer that reads scene difficulty and changes the detector’s settings.</p>',
                    '<p>Measure how hard the frame is, turn it into one score, then set the detector to match.</p>'))
        new.append(blk); new += iv; continue
    if t in ("What we add", "Step 1: measure scene complexity", "Three clues on real pictures", "The pipeline for each frame",
             "Initial SCI", "SCI example 0.63", "Implementation of the calibrator", "SCI from frame to score",
             "Confidence threshold", "One frame becomes one setting", "Step 2: use SCI to choose settings",
             "Smart Calibrator exact settings", "Proven and open"):
        continue
    if sec == "X · Conclusion":
        blk = blk.replace('data-secname="X · Conclusion"', 'data-secname="IX · Conclusion"')
        blk = re.sub(r'(<div class="kicker">)Section X\b', r'\1Section IX', blk)
    if t == "Section X":
        blk = edit(blk, ('id="sec-10"', 'id="sec-9"'), ('data-title="Section X"', 'data-title="Section IX"'),
                   ('<div class="dv-num">X</div><div class="dv-kicker">Section X</div>', '<div class="dv-num">IX</div><div class="dv-kicker">Section IX</div>'),
                   ('<p>The whole story in one line, what is proven, and what comes next.</p>', '<p>The whole story in one line, the contributions, and what comes next.</p>'))
    if t == "The story in one line":
        arrow = '    <div class="tc strong muted" style="font-size:26px;line-height:1">↓</div>\n'
        i2 = blk.index(arrow, blk.index(arrow) + 1)
        j2 = blk.index('\n', i2 + len(arrow)) + 1
        blk = blk[:i2] + blk[j2:]
        blk = edit(blk, ("; the bootstrap and UAVDT confirmed the gains; comparing with papers led to a protocol audit and a correction freeze; next is the official VisDrone re-evaluation.",
                         "; and the bootstrap and the zero-tuning UAVDT test confirmed the gains."))
        assert "Protocol audit" not in blk
    if t == "Conclusion: what AC-MOT delivers":
        blk = edit(blk, ('\n      <tr><td class="strong" style="color:#B45309">Official VisDrone</td><td style="text-align:center">→</td><td style="text-align:left">re-evaluation needed before comparing with papers</td></tr>', ''),
                   ('<table class="tbl" style="font-size:27px">', '<table class="tbl" style="font-size:30px">'))
    if t == "Directions for future work":
        blk = edit(blk, ('    <div class="callout warn"><b>Next step first:</b> official-aligned VisDrone re-evaluation of the frozen V1 and V2 — then a fair comparison with published papers.</div>\n', ''))
    new.append(blk)

main = prefix + "".join(new).rstrip() + "\n" + suffix
h = main + rest

# ------------------------------------------------------------ outline: 9 sections
mm = h[:h.index('<div class="overlay xview"')]
tags = re.findall(r'<section class="slide[^"]*"[^>]*>', mm)
start = {re.search(r'id="(sec-\d+)"', t).group(1): i for i, t in enumerate(tags, 1) if re.search(r'id="(sec-\d+)"', t)}
od = sorted(start.items(), key=lambda kv: kv[1])
rng = {k: (v, (od[j + 1][1] - 1) if j + 1 < len(od) else len(tags) - 1) for j, (k, v) in enumerate(od)}
rows = [("I", "sec-1", "Introduction and Motivation", "Detection, tracking and how we measure them"),
        ("II", "sec-2", "Related Work: Detectors and Trackers", "Detectors through the ages, trackers and benchmarks"),
        ("III", "sec-3", "Problem and Baseline", "Easy and hard frames, one fixed setting"),
        ("IV", "sec-4", "Proposed Framework: AC-MOT", "Measure the scene, score it, set the detector"),
        ("V", "sec-5", "Experimental Setup and First Result", "VisDrone, protocol and the initial AC-MOT"),
        ("VI", "sec-6", "V1: Validation-Driven Optimization", "Optuna, Trial 24 and the test result"),
        ("VII", "sec-7", "V2: Multi-Objective Optimization", "Pareto search and the V1 / V2 trade-off"),
        ("VIII", "sec-8", "Statistical and External Validation", "Paired bootstrap and UAVDT with zero tuning"),
        ("IX", "sec-9", "Conclusion and Future Work", "What we delivered and what comes next")]
cards = "\n".join(
    f'      <button class="ol-row" data-goto="{g}"><span class="n">{n}</span><span class="t"><h3>{t}</h3>'
    f'<p>{s}</p><p class="rg">slides {rng[g][0]} - {rng[g][1]}</p></span></button>' for n, g, t, s in rows)
a = h.index('<div class="ol-ppt">'); b = h.index('    </div>\n  </div>\n  <aside class="notes"><p><b>Say:</b> "The story goes in the order', a)
h = h[:a] + '<div class="ol-ppt">\n' + cards + '\n' + h[b:]
h = rep(h, 'the problem and the baseline, the first heuristic design, V1, V2, the statistics and UAVDT, and finally the protocol audit.',
        'the problem and the baseline, the first heuristic design, V1, V2, and finally the statistics and UAVDT.')
assert "Protocol audit" not in h[:h.index('<div class="overlay xview"')]
save("index.html", h)

c = load("styles.css")
c = rep(c, ".ol-row:nth-child(5),.ol-row:nth-child(10){border-bottom:0}", ".ol-row:nth-child(5),.ol-row:nth-child(9){border-bottom:0}")
save("styles.css", c)

j = load("script.js")
j = rep(j, "#u2setup,.ol-card .n,.ol-ppt,.tbl th,.node small'", "#u2setup,.ol-card .n,.ol-ppt,.tbl th,.noabbr,.node small'")  # no full names inside the timeline tags
save("script.js", j)

m = load("assets/data/meaning.js")
m = rep(m, "t: 'First the <b>official VisDrone re-evaluation</b>; then every next step targets a <b>weakness we measured</b>: camera motion, input size, appearance matching and other detectors.' }",
        "t: 'Every next step targets a <b>weakness we measured</b>: camera motion, a smarter input size, better appearance matching, and other detectors.' }")
save("assets/data/meaning.js", m)
print("ok · main slides:", len(tags), rng)
