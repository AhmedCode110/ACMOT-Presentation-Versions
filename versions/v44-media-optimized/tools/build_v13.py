#!/usr/bin/env python3
"""v13: the 'Explain each challenge' pages (slide 7) rewritten in easy English with simple words;
the fast-motion page and the 'fast motion' pill are removed (8 pages, 7 challenges). Same pictures and layout as v10."""
import os

ROOT = os.path.expanduser("~/Desktop/ACMOT-Presentation-Versions/versions/v13-simple-english-challenges")
P = os.path.join(ROOT, "index.html")
h = open(P, encoding="utf-8").read()

F = "assets/figures/"
N = 8


def img(src, lbl):
    return (f'<div class="img zoomable contain grow"><img src="{F}{src}" alt="{lbl}">'
            f'<span class="lbl">{lbl}</span></div>')


def page(i, key, title, pics, what, why, example, later, chip):
    return f'''<section class="xpage" data-sec="1" data-title="Challenge {key}">
  <header class="s-head"><div class="kicker">Tracking challenges · {i} of {N} — {key}</div><h2>{title}</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">What it means</div><p>{what}</p></div>
    <div class="row grow" style="gap:24px">
      <div class="col" style="flex:0 0 700px;gap:10px">{pics}<div class="tc">{chip}</div></div>
      <div class="col grow" style="gap:14px">
        <div class="card" style="border-left:6px solid var(--bad)"><h3>Why it is a problem</h3><ul class="clean">{why}</ul></div>
        <div class="card sec"><h3>Example</h3><p>{example}</p></div>
        <div class="note">{later}</div>
      </div>
    </div>
  </div>
</section>
'''


REAL = '<span class="origin illus">real video picture</span>'
DEMO = '<span class="origin illus">public tracking demo · not our system</span>'
ILL = '<span class="origin illus">drawing made by us</span>'
BLURCHIP = '<span class="origin illus">same picture · we added the blur</span>'

svg_cam = '''<div class="card col center" style="gap:6px;flex:0 0 auto"><div class="ex-label">Drawing · a parked car, the camera moves right</div>
<svg viewBox="0 0 660 190" width="100%">
  <rect x="10" y="20" width="300" height="150" rx="8" fill="#F8FAFC" stroke="#94A3B8" stroke-width="3"/>
  <text x="160" y="185" text-anchor="middle" font-size="20" fill="#475569">frame 1</text>
  <rect x="190" y="75" width="70" height="44" rx="5" fill="#DBEAFE" stroke="#2563EB" stroke-width="4"/>
  <rect x="350" y="20" width="300" height="150" rx="8" fill="#F8FAFC" stroke="#94A3B8" stroke-width="3"/>
  <text x="500" y="185" text-anchor="middle" font-size="20" fill="#475569">frame 2 (camera moved)</text>
  <rect x="380" y="75" width="70" height="44" rx="5" fill="#DBEAFE" stroke="#2563EB" stroke-width="4"/>
  <rect x="530" y="75" width="70" height="44" rx="5" fill="none" stroke="#64748B" stroke-width="3" stroke-dasharray="8 6"/>
  <path d="M525 97 L458 97" stroke="#DC2626" stroke-width="4" marker-end="url(#ah2)"/>
  <defs><marker id="ah2" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#DC2626"/></marker></defs>
</svg></div>'''

pages = []

items = [
    ("image3.png", "Occlusion", "something hides the object"),
    ("generated/small_hard.jpg", "Small objects", "the object looks very small"),
    ("image9.png", "Crowds", "many objects close together"),
    ("image28.jpeg", "Camera motion", "the camera is moving"),
    ("image21.jpeg", "Low light", "the picture is dark"),
    ("generated/blur_blurred.jpg", "Motion blur", "the picture is not sharp"),
    ("image29.jpeg", "Look-alike objects", "objects look the same"),
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
  <header class="s-head"><div class="kicker">Tracking challenges · 1 of {N} — overview</div><h2>Seven Things That Make Tracking Hard</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>Each problem makes the detector <b>miss</b> objects, or makes the tracker <b>mix up</b> their IDs.</p></div>
    <div class="g4" style="gap:14px">{"".join(cards)}</div>
  </div>
</section>
''')

pages.append(page(2, "occlusion", "Occlusion: The Object Is Hidden",
    img("image3.png", "Before · the person is ID 1") + img("image4.png", "After · the same person is ID 8"),
    "Something <b>hides the object</b> for a short time — for example a car, a tree or another person.",
    "<li>the detector cannot see it, so there is <b>no box</b></li><li>the tracker must <b>guess</b> where it is</li><li>when it comes back, it may get a <b>new ID</b></li>",
    "A person walks behind the white car. Before: <b>ID 1</b>. After: the same person gets <b>ID 8</b>. This is one ID switch.",
    "Trackers remember a lost object for a few frames, so a short hide is often OK.",
    DEMO))

pages.append(page(3, "small objects", "Small Objects: Too Few Pixels",
    img("generated/small_hard.jpg", "Cars seen from high up"),
    "The object is <b>far from the camera</b>, so it looks <b>very small</b> in the picture.",
    "<li>few pixels means few details, so the detector is <b>not sure</b> or <b>misses it</b></li><li>a tiny move of the box changes the match a lot</li><li>this happens a lot in <b>drone</b> videos</li>",
    "The COCO dataset calls an object <b>small</b> if it is less than <b>32 × 32 pixels</b>. Many cars here are about that size.",
    "Later, one clue counts how many boxes are tiny.",
    REAL))

pages.append(page(4, "crowds", "Crowds: Many Objects Close Together",
    img("image9.png", "A crowded place · boxes cover each other"),
    "Many objects are <b>very close to each other</b>.",
    "<li>boxes <b>cover each other</b>, so a correct box can be deleted</li><li>people hide each other again and again</li><li>the tracker can <b>swap</b> the IDs of two people</li>",
    "Here many boxes cover each other. When two people walk past each other, their IDs can <b>swap</b>.",
    "Later, one clue counts how crowded the scene is.",
    REAL))

pages.append(page(5, "camera motion", "Camera Motion: The Camera Moves",
    img("image28.jpeg", "The camera is on a flying drone") + svg_cam,
    "The <b>camera moves</b> (for example on a drone), so <b>everything in the picture moves</b> — even things that stand still.",
    "<li>the tracker guesses the next place from the old movement</li><li>camera movement makes this guess <b>wrong</b></li><li>the object is lost and gets a <b>new ID</b></li>",
    "A car is parked. The drone turns right, so in the picture the car <b>moves left</b>.",
    "Drone videos, like VisDrone, have a lot of camera movement.",
    ILL))

pages.append(page(6, "low light", "Low Light: The Picture Is Dark",
    img("image21.jpeg", "A night picture") + img("generated/gray_night.jpg", "Gray version · very dark"),
    "At <b>night</b> or in shadow, the picture is <b>dark</b>, so things are hard to see.",
    "<li>objects mix with the dark background, so they are <b>missed</b></li><li>noise in the picture can make <b>wrong boxes</b></li><li>colours are lost, so people look more alike</li>",
    "In the night picture, people in dark clothes are hard to see on the dark ground.",
    "Later, one clue checks if the picture is dark.",
    REAL))

pages.append(page(7, "motion blur", "Motion Blur: The Picture Is Not Sharp",
    img("generated/blur_sharp.jpg", "Sharp") + img("generated/blur_blurred.jpg", "Blurry"),
    "When the object or the camera <b>moves fast</b>, the picture becomes <b>blurry</b>, like a shaky photo.",
    "<li>the detector cannot see the shape well, so it is <b>not sure</b> or <b>misses</b> the object</li><li>boxes are placed <b>less exactly</b></li><li>it often comes together with fast movement</li>",
    "Both pictures are the same. We made the lower one blurry on purpose. The small details are gone.",
    "Later, one clue checks if the picture is blurry.",
    BLURCHIP))

pages.append(page(8, "look-alike objects", "Look-Alike Objects: They Look the Same",
    img("image29.jpeg", "Many white cars from above"),
    "Some objects look <b>almost the same</b> — same colour and same shape.",
    "<li>the tracker cannot tell them apart by how they look</li><li>when they come close, their IDs can <b>swap</b></li><li>from high up, small objects look even more alike</li>",
    "This road has many <b>white cars</b>. When two white cars pass each other, their IDs can swap.",
    "ID switches (IDS) and IDF1 show this kind of mistake.",
    REAL))

a = h.index('<div class="xdeck" id="x-challenges"')
b = h.index('<div class="xdeck" id="x-controller"')
assert a < b
h = h[:a] + '<div class="xdeck" id="x-challenges" data-label="Tracking challenges">\n' + "".join(pages) + '</div>\n' + h[b:]
pill = '<span class="pill">fast motion</span>'
assert h.count(pill) == 1
h = h.replace(pill, "")
open(P, "w", encoding="utf-8").write(h)
print("ok", h.count('class="xpage"'), "explanation pages")
