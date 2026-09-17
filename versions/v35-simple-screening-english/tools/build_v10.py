#!/usr/bin/env python3
"""v10: optional explanation of every tracking challenge on slide 7 (one part per challenge, with a picture)."""
import os

ROOT = os.path.expanduser("~/Desktop/ACMOT-Presentation-Versions/versions/v10-challenges-explained")
P = os.path.join(ROOT, "index.html")
h = open(P, encoding="utf-8").read()

# ---------- 1. button on slide 7 ----------
old = '<section class="slide" data-sec="1" data-secname="I · Introduction" data-title="Challenges of real-time tracking">'
assert h.count(old) == 1
h = h.replace(old, old[:-1] + ' data-explain="x-challenges|Explain each challenge">')

F = "assets/figures/"
N = 9  # total parts


def img(src, lbl, extra=""):
    return (f'<div class="img zoomable contain grow"><img src="{F}{src}" alt="{lbl}">'
            f'<span class="lbl"{extra}>{lbl}</span></div>')


def page(i, key, title, pics, what, why, example, later, chip):
    return f'''<section class="xpage" data-sec="1" data-title="Challenge {key}">
  <header class="s-head"><div class="kicker">Tracking challenges · {i} of {N} — {key}</div><h2>{title}</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">What it means</div><p>{what}</p></div>
    <div class="row grow" style="gap:24px">
      <div class="col" style="flex:0 0 700px;gap:10px">{pics}<div class="tc">{chip}</div></div>
      <div class="col grow" style="gap:14px">
        <div class="card" style="border-left:6px solid var(--bad)"><h3>Why it breaks tracking</h3><ul class="clean">{why}</ul></div>
        <div class="card sec"><h3>Example</h3><p>{example}</p></div>
        <div class="note">{later}</div>
      </div>
    </div>
  </div>
</section>
'''


REAL = '<span class="origin illus">real video frame · picture only, no numbers</span>'
DEMO = '<span class="origin illus">public tracking demo (DeepSORT + YOLOv5) · not our system</span>'
ILL = '<span class="origin illus">illustration · drawn by us</span>'
BLURCHIP = '<span class="origin illus">same picture · blur added on purpose</span>'

# SVG drawings
svg_fast = '''<div class="card col center grow" style="gap:6px"><div class="ex-label">Illustration · a fast car between two frames</div>
<svg viewBox="0 0 660 300" width="100%" style="flex:1;min-height:0">
  <rect x="40" y="110" width="120" height="80" rx="6" fill="#DBEAFE" stroke="#2563EB" stroke-width="5"/>
  <text x="100" y="95" text-anchor="middle" font-size="24" font-weight="800" fill="#1D4ED8">frame t · ID 7</text>
  <rect x="70" y="110" width="120" height="80" rx="6" fill="none" stroke="#64748B" stroke-width="4" stroke-dasharray="10 8"/>
  <text x="130" y="230" text-anchor="middle" font-size="22" fill="#475569">tracker expects it here</text>
  <rect x="480" y="110" width="120" height="80" rx="6" fill="#FEE2E2" stroke="#DC2626" stroke-width="5"/>
  <text x="540" y="95" text-anchor="middle" font-size="24" font-weight="800" fill="#B91C1C">frame t + 1</text>
  <path d="M200 150 L465 150" stroke="#DC2626" stroke-width="5" marker-end="url(#ah)"/>
  <defs><marker id="ah" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#DC2626"/></marker></defs>
  <text x="330" y="280" text-anchor="middle" font-size="26" font-weight="800" fill="#B91C1C">boxes do not overlap → IoU = 0 → new ID</text>
</svg></div>'''

svg_cam = '''<div class="card col center" style="gap:6px;flex:0 0 auto"><div class="ex-label">Illustration · a parked car, camera moves right</div>
<svg viewBox="0 0 660 190" width="100%">
  <rect x="10" y="20" width="300" height="150" rx="8" fill="#F8FAFC" stroke="#94A3B8" stroke-width="3"/>
  <text x="160" y="185" text-anchor="middle" font-size="20" fill="#475569">frame t</text>
  <rect x="190" y="75" width="70" height="44" rx="5" fill="#DBEAFE" stroke="#2563EB" stroke-width="4"/>
  <rect x="350" y="20" width="300" height="150" rx="8" fill="#F8FAFC" stroke="#94A3B8" stroke-width="3"/>
  <text x="500" y="185" text-anchor="middle" font-size="20" fill="#475569">frame t + 1 (camera moved)</text>
  <rect x="380" y="75" width="70" height="44" rx="5" fill="#DBEAFE" stroke="#2563EB" stroke-width="4"/>
  <rect x="530" y="75" width="70" height="44" rx="5" fill="none" stroke="#64748B" stroke-width="3" stroke-dasharray="8 6"/>
  <path d="M525 97 L458 97" stroke="#DC2626" stroke-width="4" marker-end="url(#ah2)"/>
  <defs><marker id="ah2" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#DC2626"/></marker></defs>
</svg></div>'''

pages = []

# ---------- part 1: overview ----------
items = [
    ("image3.png", "Occlusion", "an object is hidden"),
    ("generated/small_hard.jpg", "Small objects", "only a few pixels"),
    ("image9.png", "Crowds", "many objects close together"),
    ("image28.jpeg", "Camera motion", "the camera itself moves"),
    ("image21.jpeg", "Low light", "dark, noisy frames"),
    ("generated/blur_blurred.jpg", "Motion blur", "smeared object edges"),
    (None, "Fast motion", "big jump between frames"),
    ("image29.jpeg", "Look-alike objects", "objects that look the same"),
]
cards = []
for src, name, line in items:
    pic = (f'<div class="img" style="flex:0 0 150px;height:150px"><img src="{F}{src}" alt="{name}"></div>' if src else
           '<div class="img contain center" style="flex:0 0 150px;height:150px;display:flex;align-items:center;justify-content:center">'
           '<svg viewBox="0 0 220 120" width="80%"><rect x="10" y="40" width="50" height="40" fill="#DBEAFE" stroke="#2563EB" stroke-width="4"/>'
           '<rect x="160" y="40" width="50" height="40" fill="#FEE2E2" stroke="#DC2626" stroke-width="4"/>'
           '<path d="M68 60 L150 60" stroke="#DC2626" stroke-width="4"/></svg></div>')
    cards.append(f'<div class="card col" style="gap:6px;padding:10px 12px">{pic}<h3 style="margin:0">{name}</h3><p class="small muted" style="margin:0">{line}</p></div>')
pages.append(f'''<section class="xpage" data-sec="1" data-title="Challenges overview">
  <header class="s-head"><div class="kicker">Tracking challenges · 1 of {N} — overview</div><h2>Eight Things That Make Tracking Hard</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>Each challenge makes the detector <b>miss</b> objects or the tracker <b>mix up</b> identities.</p></div>
    <div class="g4" style="gap:14px">{"".join(cards)}</div>
  </div>
</section>
''')

pages.append(page(2, "occlusion", "Occlusion: The Object Is Hidden",
    img("image3.png", "Before occlusion · person id 1") + img("image4.png", "After occlusion · same person, id 8"),
    "Something (a car, a tree, another person) <b>covers the object</b> for a few frames.",
    "<li>the detector cannot see it → <b>no box</b> (a miss)</li><li>the tracker must <b>guess</b> where it went</li><li>when it comes back it may get a <b>new ID</b> (an identity switch)</li>",
    "In the pictures, a person walks behind the white car. Before: <b>id 1</b>. After: the same person is <b>id 8</b> — one identity switch.",
    "Trackers keep a lost track alive for a few frames (the <b>track buffer</b>) to survive short occlusions.",
    DEMO))

pages.append(page(3, "small objects", "Small Objects: Only a Few Pixels",
    img("generated/small_hard.jpg", "Cars seen from high up"),
    "The object is <b>far away</b>, so it covers only a tiny area of the image.",
    "<li>few pixels → little detail → <b>low confidence</b> or no box</li><li>a box shift of 2–3 pixels already changes the overlap a lot</li><li>very common in <b>drone</b> video</li>",
    "The COCO dataset calls an object <b>small</b> when it is under <b>32 × 32 pixels</b>. Many cars in this picture are about that size.",
    "Later in this talk, one clue measures the <b>share of tiny boxes</b> in the frame.",
    REAL))

pages.append(page(4, "crowds", "Crowds: Many Objects Close Together",
    img("image9.png", "Crowded scene · boxes overlap"),
    "Many objects stand or move <b>close to each other</b>.",
    "<li>boxes <b>overlap</b> → the cleanup step can delete a correct box</li><li>people hide each other → many short occlusions</li><li>the tracker has <b>many similar candidates</b> to match → more identity switches</li>",
    "In the picture, several boxes cover each other. If two people cross, their IDs can easily be <b>swapped</b>.",
    "Later in this talk, one clue measures <b>how crowded</b> the scene is (number of tracked boxes).",
    REAL))

pages.append(page(5, "camera motion", "Camera Motion: The Camera Itself Moves",
    img("image28.jpeg", "The camera is on a moving drone") + svg_cam,
    "The <b>camera moves</b> (drone, car, hand-held), so the whole picture shifts — even objects that stand still.",
    "<li>the tracker predicts positions from past motion; camera motion breaks that prediction</li><li>predicted box and new box <b>stop overlapping</b></li><li>result: lost tracks and <b>new IDs</b></li>",
    "A parked car does not move, but when the drone turns right the car <b>jumps left</b> in the image.",
    "Drone video (like VisDrone) has a lot of camera motion.",
    ILL))

pages.append(page(6, "low light", "Low Light: Dark, Noisy Frames",
    img("image21.jpeg", "Night scene") + img("generated/gray_night.jpg", "Same idea in gray · very dark"),
    "At <b>night</b> or in shadow the image is dark and has little contrast.",
    "<li>objects blend into the background → <b>missed boxes</b></li><li>camera noise creates <b>false boxes</b></li><li>colours disappear → people look more alike</li>",
    "In the night picture, people in dark clothes are hard to separate from the dark ground.",
    "Later in this talk, one clue checks if the frame is <b>dark</b> (mean gray level).",
    REAL))

pages.append(page(7, "motion blur", "Motion Blur: Smeared Edges",
    img("generated/blur_sharp.jpg", "Sharp") + img("generated/blur_blurred.jpg", "Blurred"),
    "The object or the camera moves <b>during</b> the exposure, so edges are <b>smeared</b>.",
    "<li>the detector loses the shape → <b>lower confidence</b> or a miss</li><li>boxes become <b>less precise</b></li><li>often happens together with fast motion and camera shake</li>",
    "The two pictures are the same frame; the lower one was blurred on purpose. Fine details disappear.",
    "Later in this talk, one clue checks for <b>blur</b> (variance of the Laplacian, a published sharpness measure).",
    BLURCHIP))

pages.append(page(8, "fast motion", "Fast Motion: A Big Jump Between Frames",
    svg_fast,
    "The object moves <b>very far</b> between two frames.",
    "<li>the tracker matches boxes that <b>overlap</b> with the prediction</li><li>a big jump → <b>no overlap</b> → no match</li><li>the old track is lost and a <b>new ID</b> starts</li>",
    "A car at ID 7 jumps far to the right. The new box does not touch the expected box, so IoU (Intersection over Union) = 0 and it gets a new ID.",
    "Low frame rate makes this worse: fewer frames per second means bigger jumps.",
    ILL))

pages.append(page(9, "look-alike objects", "Look-Alike Objects: Hard to Tell Apart",
    img("image29.jpeg", "Many white cars from above"),
    "Several objects look <b>almost the same</b> (same colour, same shape).",
    "<li>appearance cannot tell them apart</li><li>when they come close, the tracker may <b>swap</b> their IDs</li><li>from high up, small similar objects are even harder</li>",
    "On this road there are many <b>white cars</b>. If two white cars pass each other, their IDs can be exchanged.",
    "Identity switches (IDS) and IDF1 are the metrics that show this kind of error.",
    REAL))

deck = '<div class="xdeck" id="x-challenges" data-label="Tracking challenges">\n' + "".join(pages) + '</div>\n'
anchor = '<div class="xdeck" id="x-controller"'
assert h.count(anchor) == 1
h = h.replace(anchor, deck + anchor)
open(P, "w", encoding="utf-8").write(h)
print("ok", h.count('class="xpage"'), "pages")
