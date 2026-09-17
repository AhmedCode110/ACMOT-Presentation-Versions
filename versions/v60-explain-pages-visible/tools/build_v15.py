#!/usr/bin/env python3
"""v15: rebuild the deck from Section III on, following the author's full research story (2026-09-14):
baseline -> initial (heuristic) AC-MOT -> why these weights -> Optuna/TPE V1 -> V1 test -> ID-switch problem ->
V2 multi-objective (Pareto) -> V2 test -> V1 or V2 -> paired bootstrap -> UAVDT zero tuning ->
literature comparison -> protocol audit -> official VisDrone protocol -> van class -> two kinds of results ->
correction freeze -> story in one line -> proven vs open -> conclusion.
Numbers exactly as supplied by the author in that story."""
import os, re

ROOT = os.path.expanduser("~/Desktop/ACMOT-Presentation-Versions/versions/v15-full-research-story")


def load(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def save(p, s): open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)


def rep(s, old, new, n=1):
    assert s.count(old) == n, (s.count(old), old[:100])
    return s.replace(old, new)


h = load("index.html")
xi = h.index('<div class="overlay xview"')
main, rest = h[:xi], h[xi:]
starts = [m.start() for m in re.finditer(r'<section class="slide[^"]*"[^>]*>', main)]
assert len(starts) == 75, len(starts)
last_end = main.rindex('</section>') + len('</section>')
blocks = {}
for i in range(29, 75):
    a = starts[i]; b = starts[i + 1] if i + 1 < 75 else last_end
    blk = main[a:b].rstrip() + "\n\n"
    title = re.search(r'data-title="([^"]*)"', blk).group(1)
    blocks[title] = blk
prefix, suffix = main[:starts[29]], main[last_end:]

# ------------------------------------------------------------------ sections
SEC = {  # roman: (data-sec colour, secname, divider id)
    "III": (3, "III · Problem & baseline", "sec-3"),
    "IV": (4, "IV · AC-MOT", "sec-4"),
    "V": (5, "V · Setup & first result", "sec-5"),
    "VI": (7, "VI · V1 optimization", "sec-6"),
    "VII": (6, "VII · V2 multi-objective", "sec-7"),
    "VIII": (8, "VIII · Statistics & UAVDT", "sec-8"),
    "IX": (3, "IX · Protocol audit", "sec-9"),
    "X": (9, "X · Conclusion", "sec-10"),
}


def use(title, roman, *edits):
    blk = blocks.pop(title)
    d, name, _ = SEC[roman]
    blk = re.sub(r'data-sec="\d+" data-secname="[^"]*"', f'data-sec="{d}" data-secname="{name}"', blk, count=1)
    blk = re.sub(r'(<div class="kicker">)Section [IVX]+', r'\g<1>Section ' + roman, blk, count=1)
    for old, new in edits:
        blk = rep(blk, old, new)
    return blk


def divider(roman, img, h1, p, say):
    d, name, sid = SEC[roman]
    return f'''<section class="slide divider" id="{sid}" data-sec="{d}" data-secname="{name}" data-title="Section {roman}">
  <div class="dv-bg"><img src="assets/figures/{img}" alt=""></div>
  <div class="dv-text"><div class="dv-num">{roman}</div><div class="dv-kicker">Section {roman}</div>
    <h1>{h1}</h1>
    <p>{p}</p></div>
  <aside class="notes"><p><b>Say:</b> "{say}"</p></aside>
</section>

'''


def slide(roman, title, kicker, h2, body, notes, foot="", explain=""):
    d, name, _ = SEC[roman]
    ex = f' data-explain="{explain}"' if explain else ""
    ft = f'\n  <footer class="s-foot">{foot}</footer>' if foot else ""
    return f'''<section class="slide" data-sec="{d}" data-secname="{name}" data-title="{title}"{ex}>
  <header class="s-head"><div class="kicker">Section {roman} · {kicker}</div><h2>{h2}</h2></header>
  <div class="s-body col">
{body}
  </div>{ft}
  <aside class="notes">{notes}</aside>
</section>

'''


def meaning(t, tag="The main idea"):
    return f'    <div class="meaning"><div class="tag">{tag}</div><p>{t}</p></div>'


def charts(*ids):
    out = []
    for i, c in enumerate(ids):
        st = 'flex:1.6;padding:10px 14px' if i == 0 and len(ids) > 1 else 'padding:10px 14px'
        cls = 'card' if i == 0 and len(ids) > 1 else 'card grow'
        out.append(f'<div class="{cls}" style="{st}"><div class="chart zoomable" data-chart="{c}"></div></div>')
    return '    <div class="row grow" style="gap:16px">' + "".join(out) + '</div>'


TEST = '<span class="prov p-test">Test set · VisDrone2019-MOT test-dev · 17 sequences · our custom AC-MOT protocol</span>'
VAL = '<span class="prov p-val">Validation · VisDrone2019-MOT-val · 7 sequences · our custom AC-MOT protocol</span>'
EXT = '<span class="prov p-ext">External test · UAVDT · 20 sequences / 16,592 frames · frozen systems, zero tuning</span>'
HDR = '<tr><th style="text-align:left">System</th><th>MOTA ↑</th><th>HOTA ↑</th><th>IDF1 ↑</th><th>IDS ↓</th><th>FPS ↑</th></tr>'


def say(*ps):
    return "".join(f"<p><b>{k}:</b> \"{v}\"</p>" if k == "Say" else f"<p><b>{k}:</b> {v}</p>" for k, v in ps)


S = []

# ================================================================== III · Problem & baseline
S.append(divider("III", "image9.png", "The Problem and Our Starting Point",
                 "Drone scenes change from easy to hard — but a normal pipeline keeps one fixed detector setting. First, a baseline to measure against.",
                 "First the problem, then the simple system we start from."))
S.append(use("One fixed threshold", "III"))
S.append(use("The main question", "III"))
S.append(slide("III", "The baseline", "Starting point", "Before Adding Anything: A Baseline", "\n".join([
    meaning("First we need a <b>simple, fast starting system</b>. Every later gain is measured <b>against it</b>."),
    '''    <div class="flow" style="gap:0">
      <div class="node io" style="width:160px">Frame</div><div class="arr"></div>
      <div class="node fx" style="width:250px">Detector<small>YOLOv8n</small></div><div class="arr"></div>
      <div class="node fx" style="width:250px">Tracker<small>ByteTrack</small></div><div class="arr"></div>
      <div class="node good" style="width:160px">Tracks</div>
    </div>''',
    '''    <div class="g5" style="gap:14px">
      <div class="kpi"><div class="l">MOTA</div><div class="v">19.729</div></div>
      <div class="kpi"><div class="l">HOTA</div><div class="v">28.430</div></div>
      <div class="kpi"><div class="l">IDF1</div><div class="v">32.724</div></div>
      <div class="kpi"><div class="l">IDS</div><div class="v">1235</div></div>
      <div class="kpi"><div class="l">FPS</div><div class="v">36.53</div></div>
    </div>''',
    '''    <div class="g2 grow" style="gap:22px">
      <div class="card sec"><h3>Why this pipeline?</h3><ul class="clean"><li><b>fast</b> — real-time on drone video</li><li><b>modular</b> — detector and tracker are separate parts</li><li>anything we add around them can be <b>measured</b></li></ul></div>
      <div class="callout warn">This is <b>not</b> ByteTrack’s global score. It means: YOLOv8n + ByteTrack, <b>with our settings and our test protocol</b>, gives 19.729 MOTA.</div>
    </div>''']),
    say(("Say", "Before adding anything, we need a baseline: YOLOv8n for detection and ByteTrack for tracking. It is fast and modular, so any part we add can be measured. On our test videos it gives 19.729 MOTA."),
        ("Careful", "This is not ByteTrack's worldwide number — it is YOLOv8n plus ByteTrack under our settings and our protocol.")),
    foot=TEST.replace("our custom AC-MOT protocol", "our custom evaluation protocol"), explain="x-bytetrack|ByteTrack in Detail"))

# ================================================================== IV · AC-MOT (unchanged design slides)
S.append(divider("IV", "image22.png", "AC-MOT: The First Adaptive Design",
                 "Not a new detector and not a new tracker — a small control layer that reads scene difficulty and changes the detector’s settings.",
                 "Now our idea: AC-MOT. This first version used hand-picked weights."))
for t in ["What we add", "The pipeline for each frame", "SCI from frame to score", "Step 1: measure scene complexity",
          "Three clues on real pictures", "Initial SCI", "SCI example 0.63", "One frame becomes one setting",
          "Step 2: use SCI to choose settings", "Smart Calibrator exact settings", "Confidence threshold",
          "Implementation of the calibrator"]:
    S.append(use(t, "IV"))

# ================================================================== V · Setup & first result
S.append(divider("V", "image26.jpeg", "Experimental Setup and the First Result",
                 "VisDrone2019-MOT, the scoring rules — and the first answer: did the hand-designed AC-MOT help?",
                 "How we test, and the first result."))
for t in ["Choosing the test domain", "The VisDrone2019-MOT benchmark", "Object classes evaluated",
          "Ground-truth filtering rules", "Evaluation protocol"]:
    S.append(use(t, "V"))
S.append(slide("V", "Initial AC-MOT result", "First result", "Did the Idea Work? Initial AC-MOT vs Baseline", "\n".join([
    meaning("<b>Yes.</b> The first, hand-designed AC-MOT already <b>beat the baseline</b> on the same test videos."),
    charts("init-quality", "init-ids", "init-fps"),
    f'''    <table class="tbl" style="font-size:25px">
      {HDR}
      <tr><td>Baseline</td><td>19.729</td><td>28.430</td><td>32.724</td><td>1235</td><td>36.53</td></tr>
      <tr class="sel"><td>Initial AC-MOT</td><td class="best">23.236</td><td class="best">32.698</td><td class="best">39.516</td><td class="best">1061</td><td class="best">41.96</td></tr>
    </table>''',
    '''    <div class="pills" style="justify-content:center"><span class="pill good">MOTA 19.729 → 23.236 · +3.51 pp</span><span class="pill good">IDF1 32.724 → 39.516</span><span class="pill good">IDS 1235 → 1061</span></div>''']),
    say(("Say", "The first AC-MOT, with hand-picked weights, already worked: MOTA went from 19.729 to 23.236 — about 3.5 points — IDF1 went up, and ID switches went down from 1235 to 1061."),
        ("Note", "pp = percentage points.")),
    foot=TEST))
S.append(use("Same frames, different control", "V"))

# ================================================================== VI · V1
S.append(divider("VI", "image15.jpeg", "V1: Letting Validation Data Choose",
                 "The idea worked — but were the hand-picked weights the best? Optuna with TPE searched on validation data only.",
                 "The first scientific question: why these weights?"))
S.append(slide("VI", "Why these weights", "The first scientific question", "Why Crowd = 0.30? Why Edge = 0.20?", "\n".join([
    meaning("The five cues have a reason. The <b>exact weights did not</b> — we chose them <b>by hand</b>."),
    '''    <div class="row grow" style="gap:24px">
      <table class="tbl" style="font-size:27px;flex:0 0 640px">
        <tr><th style="text-align:left">Cue</th><th>Hand-set weight</th><th>Proof it is the best?</th></tr>
        <tr><td>Crowd</td><td>0.30</td><td class="bad strong">?</td></tr>
        <tr><td>Tiny objects</td><td>0.30</td><td class="bad strong">?</td></tr>
        <tr><td>Edge complexity</td><td>0.20</td><td class="bad strong">?</td></tr>
        <tr><td>Low light</td><td>0.10</td><td class="bad strong">?</td></tr>
        <tr><td>Blur</td><td>0.05</td><td class="bad strong">?</td></tr>
      </table>
      <div class="col grow" style="gap:16px">
        <div class="card" style="border-left:6px solid var(--good)"><h3>Has a scientific reason</h3><p>The <b>five cues</b>: crowd, tiny objects, edges, low light and blur.</p></div>
        <div class="card" style="border-left:6px solid var(--bad)"><h3>Chosen by hand</h3><p>The <b>exact weights</b> 0.30 / 0.30 / 0.20 / 0.10 / 0.05.</p></div>
      </div>
    </div>''',
    '    <div class="callout">So: instead of choosing the weights by hand, <b>let optimization choose them from validation data</b>.</div>']),
    say(("Say", "A supervisor can ask: why is crowd 0.30 and edge 0.20? What is the proof these are the best weights? The five cues have a scientific reason, but the exact weights were handcrafted. So we let optimization choose them from validation data.")),
    foot='<span class="prov p-hist">Initial heuristic weights · manually designed</span>'))
S.append(use("Why Optuna", "VI"))
S.append(use("What Optuna changed in V1", "VI"))
S.append(use("One Optuna trial", "VI"))
S.append(use("Step 4 result: Trial 24", "VI",
             ('<div class="v">23.0381</div>', '<div class="v">23.038</div>'),
             ('<div class="v">36.1102</div>', '<div class="v">36.110</div>'),
             ('<div class="v">40.7578</div>', '<div class="v">40.758</div>'),
             ('<div class="v">37.1686</div>', '<div class="v">37.17</div>'),
             ('<li>FPS must be at least 25</li><li>IDS must not exceed 271 — the original full AC-MOT (OLD-A3)</li><li>among the trials that pass, take the highest MOTA</li>',
              '<li>FPS must stay acceptable (at least 25)</li><li>IDS must not exceed the reference: <b>271</b> (Old-A3, the initial full AC-MOT on validation)</li><li>then take the <b>highest MOTA</b></li><li><b>50 trials</b> · TPE sampler</li>')))
S.append(use("Quick question: what did the search learn", "VI"))
S.append(use("V1 Trial 24 weights", "VI",
             ('<td>0.12949277455301997</td>', '<td>0.129</td>'),
             ('<td>0.22174766876599927</td>', '<td>0.222</td>'),
             ('<td class="best">0.43371337893805056</td>', '<td class="best">0.434</td>'),
             ('<td>0.05355765312756694</td>', '<td>0.054</td>'),
             ('<td>0.16148852461536325</td>', '<td>0.161</td>'),
             ('      </table>\n    </div>\n  </div>\n  <footer',
              '      </table>\n    </div>\n    <div class="callout">The optimizer says: <b>edge complexity matters much more</b> than we assumed by hand (0.20 → 0.434).</div>\n  </div>\n  <footer')))
S.append(use("V1 Trial 24 regimes", "VI"))
S.append(use("Validation builds it, test judges it", "VI",
             ("Ablation, validation and test-set numbers", "Validation and test-set numbers")))
S.append(slide("VI", "V1 on the test set", "Test set", "V1 on the Test Set: The Strongest Quality Result", "\n".join([
    meaning("After freezing V1, we tested it <b>once</b>. It gave our <b>biggest quality gain</b> over the baseline."),
    charts("v1b-quality", "v1b-ids", "v1b-fps"),
    f'''    <table class="tbl" style="font-size:25px">
      {HDR}
      <tr><td>Baseline</td><td>19.729</td><td>28.430</td><td>32.724</td><td>1235</td><td>36.53</td></tr>
      <tr class="sel"><td>V1</td><td>26.948</td><td>33.835</td><td>41.546</td><td>1184</td><td>38.98</td></tr>
      <tr><td class="strong">V1 − Baseline</td><td class="best">+7.220 pp</td><td class="best">+5.405</td><td class="best">+8.822</td><td class="best">−51</td><td class="best">+2.46</td></tr>
    </table>''']),
    say(("Say", "After freezing V1 we ran it once on the test set. Against the baseline: MOTA plus 7.22 points, HOTA plus 5.4, IDF1 plus 8.8, 51 fewer ID switches, and 2.5 FPS faster. This is our most important quality result.")),
    foot=TEST, explain="x-v1v2|V1 vs V2 Explained"))
S.append(slide("VI", "The identity-switch problem", "What V1 did not solve", "Where Is the Problem? ID Switches", "\n".join([
    meaning("V1 has the best quality, but the <b>initial AC-MOT had fewer ID switches</b>: 1061 &lt; 1184."),
    '''    <div class="row grow" style="gap:22px">
      <div class="card" style="flex:0 0 620px;padding:10px 14px"><div class="chart zoomable" data-chart="v1t-ids"></div></div>
      <div class="col grow" style="gap:14px">
        <table class="tbl" style="font-size:26px">
          <tr><th style="text-align:left">In the V1 search</th><th style="text-align:left">Role</th></tr>
          <tr><td>MOTA</td><td style="text-align:left" class="good strong">goal — as high as possible</td></tr>
          <tr><td>IDS</td><td style="text-align:left" class="warn strong">rule — only stay ≤ 271</td></tr>
          <tr><td>FPS</td><td style="text-align:left" class="warn strong">rule — only stay acceptable</td></tr>
        </table>
        <div class="callout warn">IDS was a <b>constraint</b>, not an <b>objective</b>. Optuna only needed IDS to <b>pass the rule</b> — not to make it as low as possible.</div>
      </div>
    </div>''',
    '    <div class="note">So identity stability did <b>not</b> improve as much as tracking quality. This is the second research question.</div>']),
    say(("Say", "Look at ID switches: baseline 1235, initial AC-MOT 1061, V1 1184. V1 is much better in quality, but the initial version had fewer ID switches. The reason: in V1, IDS was only a rule to pass, not a goal to minimize.")),
    foot=TEST))

# ================================================================== VII · V2
S.append(divider("VII", "image28.jpeg", "V2: Two Goals at Once",
                 "Maximize MOTA and minimize ID switches together — and find the trade-off between them.",
                 "So we changed the question: two goals at the same time."))
S.append(use("Stage 3: why V2", "VII"))
S.append(slide("VII", "Trade-off in simple words", "Multi-objective idea", "Two Goals: What Is a Trade-off?", "\n".join([
    meaning("With two goals, one setting can be better in one goal and <b>worse in the other</b>. Neither one wins everything."),
    '''    <div class="g2 grow" style="gap:24px">
      <div class="card" style="border-top:6px solid #7C3AED"><div class="tag" style="color:#7C3AED">Trial A</div>
        <table class="tbl mt8" style="font-size:30px"><tr><td>MOTA</td><td class="good strong">high</td></tr><tr><td>ID switches</td><td class="bad strong">high</td></tr></table></div>
      <div class="card" style="border-top:6px solid #0D9488"><div class="tag" style="color:#0D9488">Trial B</div>
        <table class="tbl mt8" style="font-size:30px"><tr><td>MOTA</td><td class="bad strong">lower</td></tr><tr><td>ID switches</td><td class="good strong">very low</td></tr></table></div>
    </div>''',
    '    <div class="callout">This is a <b>trade-off</b>. All the best trade-off points together form the <b>Pareto front</b>.</div>']),
    say(("Say", "Very simply: trial A has high MOTA but many ID switches. Trial B has lower MOTA but very few ID switches. Neither is better in everything — that is a trade-off, and the best trade-off points form the Pareto front.")),
    foot='<span class="prov p-illus">Illustration · no numbers</span>', explain="x-pareto|Multi-Objective Search"))
S.append(use("V2 Pareto front", "VII",
             ('Section VII · Stage 3 <span class="newtag">NEW</span>', 'Section VII · Pareto front'),
             ('V1 T24 and old A3 shown as references', 'V1 Trial 24 and the initial AC-MOT (Old-A3) shown as references')))
S.append(slide("VII", "V2 search and selection", "Validation search", "V2 Search: 49 Trials, One Balanced Pick", "\n".join([
    meaning("The V2 search ran on <b>validation only</b>. <b>49 of 50</b> planned trials finished, and a <b>fixed balanced rule</b> picked Trial 22."),
    '''    <div class="g3" style="gap:18px">
      <div class="kpi"><div class="l">Planned</div><div class="v">50</div><div class="s">trials</div></div>
      <div class="kpi hi"><div class="l">Completed</div><div class="v">49</div><div class="s">Trial 0 → Trial 48</div></div>
      <div class="kpi hi"><div class="l">Selected</div><div class="v">Trial 22</div><div class="s">balanced selection</div></div>
    </div>''',
    '''    <div class="g2 grow" style="gap:22px">
      <div class="card sec"><h3>V2 goals</h3><ul class="clean"><li><b>maximize</b> MOTA</li><li><b>minimize</b> IDS</li><li>FPS must stay at least 25</li></ul></div>
      <div class="card sec"><h3>Balanced selection</h3><p class="lead" style="font-size:32px"><b>50%</b> MOTA + <b>50%</b> IDS quality</p><p class="mt8">Applied to the Pareto solutions → <b>Trial 22</b>.</p></div>
    </div>''',
    '    <div class="note"><b>Always say it correctly:</b> 50 trials were planned; <b>49 completed</b>.</div>']),
    say(("Say", "V2 was planned for 50 trials; 49 finished, trial 0 to trial 48. From the Pareto solutions, a balanced rule — half MOTA, half ID-switch quality — selected Trial 22.")),
    foot='<span class="prov p-val">Validation · V2 Pareto study · 49 completed trials</span>', explain="x-pareto#2|Pareto Front Explained"))
S.append(slide("VII", "V2 validation result", "Validation result", "V1 vs V2 on Validation", "\n".join([
    meaning("Now the two versions have <b>different characters</b>: <b>V1 = quality-oriented</b> · <b>V2 = identity + speed-oriented</b>."),
    charts("val-quality", "val-ids", "val-fps"),
    f'''    <table class="tbl" style="font-size:25px">
      {HDR}
      <tr><td>V1 · Trial 24</td><td class="best">23.038</td><td class="best">36.110</td><td class="best">40.758</td><td>270</td><td>37.17</td></tr>
      <tr><td>V2 · Trial 22</td><td>19.330</td><td>31.651</td><td>34.226</td><td class="best">168</td><td class="best">51.41</td></tr>
    </table>''']),
    say(("Say", "On validation, V1 keeps the higher MOTA, HOTA and IDF1. V2 has far fewer ID switches, 168 instead of 270, and is much faster. So V1 is quality-oriented and V2 is identity and speed oriented.")),
    foot=VAL))
S.append(slide("VII", "V2 on the test set", "Test set", "V2 on the Test Set", "\n".join([
    meaning("V2 is <b>not better than V1</b>. It is a <b>different point</b> on the trade-off."),
    charts("td3-quality", "td3-ids", "td3-fps"),
    f'''    <table class="tbl" style="font-size:24px">
      {HDR}
      <tr><td>Baseline</td><td>19.729</td><td>28.430</td><td>32.724</td><td>1235</td><td>36.53</td></tr>
      <tr><td>V1</td><td class="best">26.948</td><td class="best">33.835</td><td class="best">41.546</td><td>1184</td><td>38.98</td></tr>
      <tr><td>V2</td><td>23.792</td><td>31.218</td><td>37.870</td><td class="best">919</td><td class="best">46.02</td></tr>
    </table>''',
    '''    <div class="g2" style="gap:18px">
      <div class="note" style="border-left-color:var(--bad)"><b>V2 lost vs V1:</b> MOTA −3.157 pp · HOTA −2.617 · IDF1 −3.676</div>
      <div class="note" style="border-left-color:var(--good)"><b>V2 gained vs V1:</b> IDS 1184 → 919 (265 fewer) · FPS +7.04 · about 5,397 fewer false positives</div>
    </div>''']),
    say(("Say", "On the test set, V2 loses about 3 MOTA points against V1, and some HOTA and IDF1. But it has 265 fewer ID switches, is 7 FPS faster, and has about 5,397 fewer false positives. So we do not say V2 is better — they are two points on a trade-off.")),
    foot=TEST, explain="x-v1v2|V1 vs V2 Explained"))
S.append(slide("VII", "V1 or V2", "Which version?", "So Which One Is Better — V1 or V2?", "\n".join([
    meaning("There is <b>no absolute best</b>. The right version depends on <b>the priority</b>."),
    '''    <div class="g2 grow" style="gap:26px">
      <div class="card col center" style="border-top:8px solid #7C3AED;gap:10px"><div class="tag" style="color:#7C3AED">If the priority is</div>
        <p class="lead tc">the <b>highest tracking quality</b></p><div class="big" style="font-size:64px;color:#7C3AED">→ V1</div></div>
      <div class="card col center" style="border-top:8px solid #0D9488;gap:10px"><div class="tag" style="color:#0D9488">If the priority is</div>
        <p class="lead tc"><b>fewer ID switches</b>, <b>fewer false positives</b> and <b>higher speed</b></p><div class="big" style="font-size:64px;color:#0D9488">→ V2</div></div>
    </div>''',
    '    <div class="callout">Showing this trade-off clearly is itself a <b>scientific result</b> of the thesis.</div>']),
    say(("Say", "If you ask me which version is best: there is no absolute best. For the highest tracking quality, choose V1. For fewer ID switches, fewer false positives and higher speed, choose V2.")),
    foot=TEST))

# ================================================================== VIII · Statistics & UAVDT
S.append(divider("VIII", "image20.jpeg", "Is the Gain Real?",
                 "A paired bootstrap on the test videos, then a zero-tuning test on a completely different dataset: UAVDT.",
                 "Are these gains real, or luck?"))
S.append(slide("VIII", "Paired bootstrap", "Statistical validation", "Paired Bootstrap: Is the V1 Gain Real?", "\n".join([
    meaning("Maybe a few easy videos made the gain look big? We <b>resampled the test videos 5,000 times</b>. The V1 quality gains stay <b>clearly above zero</b>."),
    '''    <div class="xchain"><span class="pill sec">pick test videos at random, with repeats</span>→<span class="pill sec">compute V1 − Baseline</span>→<span class="pill sec">repeat 5,000 times</span>→<span class="pill sec">middle 95% = confidence interval (CI)</span></div>''',
    '''    <div class="row grow" style="gap:20px">
      <div class="card grow" style="padding:10px 14px"><div class="chart zoomable" data-chart="boot-v1q"></div></div>
      <div class="col" style="flex:0 0 560px;gap:14px">
        <table class="tbl" style="font-size:25px">
          <tr><th style="text-align:left">V1 − Baseline</th><th>Gain</th><th>95% CI</th></tr>
          <tr><td>MOTA</td><td class="best">+7.2195</td><td>[5.4362, 9.2934]</td></tr>
          <tr><td>HOTA</td><td class="best">+5.4051</td><td>[4.1273, 6.9022]</td></tr>
          <tr><td>IDF1</td><td class="best">+8.8220</td><td>[6.9005, 11.0537]</td></tr>
        </table>
        <div class="callout">All three intervals are <b>above zero</b> → the quality gain is <b>statistically strong</b>.</div>
      </div>
    </div>''']),
    say(("Say", "To check that the gain is not caused by a few easy sequences, we used a paired bootstrap with 5,000 resamples. For V1 against the baseline, MOTA plus 7.2 with a 95 percent interval from 5.4 to 9.3; HOTA and IDF1 are also clearly above zero.")),
    foot='<span class="prov p-test">Test set · paired bootstrap · 5,000 resamples of the 17 sequences</span>'))
S.append(slide("VIII", "Bootstrap on ID switches", "Statistical validation", "ID Switches: V1 Not Significant, V2 Significant", "\n".join([
    meaning("For V1, the ID-switch interval <b>crosses zero</b> — we cannot claim a real improvement. For V2 it does not. <b>This is exactly why V2 was needed.</b>"),
    '''    <div class="row grow" style="gap:20px">
      <div class="card grow" style="padding:10px 14px"><div class="chart zoomable" data-chart="boot-ids2"></div></div>
      <div class="col" style="flex:0 0 600px;gap:14px">
        <table class="tbl" style="font-size:25px">
          <tr><th style="text-align:left">vs Baseline</th><th>IDS removed</th><th>95% CI</th><th>Real?</th></tr>
          <tr><td>V1</td><td>51</td><td>[−114, 219]</td><td class="bad strong">no</td></tr>
          <tr><td>V2</td><td class="best">316</td><td>[175, 470]</td><td class="good strong">yes</td></tr>
        </table>
        <div class="callout warn">We <b>cannot</b> say V1 made a significant ID-switch improvement. V2 did.</div>
      </div>
    </div>''']),
    say(("Say", "For ID switches, V1 removes 51, but the interval goes from minus 114 to 219 — it crosses zero, so it is not significant. V2 removes 316, with an interval from 175 to 470 — significant. This is exactly why V2 was needed.")),
    foot='<span class="prov p-test">Test set · paired bootstrap · 5,000 resamples</span>'))
S.append(slide("VIII", "Zero-tuning question", "Generalization", "Did It Only Work Because We Tuned on VisDrone?", "\n".join([
    meaning("To check, we <b>froze V1 and V2</b> and ran them on a <b>completely different dataset: UAVDT</b>."),
    '''    <div class="flow" style="gap:0">
      <div class="node good" style="width:260px">Frozen V1 and V2<small>chosen on VisDrone validation</small></div><div class="arr"></div>
      <div class="node io" style="width:260px">UAVDT<small>20 sequences · 16,592 frames</small></div><div class="arr"></div>
      <div class="node hot" style="width:260px">Score once<small>same protocol</small></div>
    </div>''',
    '''    <div class="g2 grow" style="gap:22px">
      <div class="card" style="border-left:6px solid var(--bad)"><h3>What we did NOT do</h3><ul class="clean"><li>no training</li><li>no Optuna</li><li>no retuning</li><li>no recalibration</li></ul></div>
      <div class="card" style="border-left:6px solid var(--good)"><h3>What this tests</h3><p class="lead" style="font-size:32px"><b>Zero-tuning external generalization</b></p><p class="mt8">Does the gain survive on data the system has never seen?</p></div>
    </div>''']),
    say(("Say", "Maybe AC-MOT only worked because we optimized on VisDrone. So we froze V1 and V2 and sent them to a completely different dataset, UAVDT — no training, no Optuna, no retuning, no recalibration.")),
    foot=EXT))
S.append(use("UAVDT with zero tuning", "VIII",
             ('<p>On a <b>different drone dataset</b>, both V1 and V2 beat the baseline. <b>V1</b> gives stronger tracking quality; <b>V2</b> gives fewer ID switches and better speed than V1. This supports transfer — <b>not a state-of-the-art claim</b>.</p>',
              '<p>The improvement <b>transferred to UAVDT without tuning</b>. V1 vs Baseline: MOTA <b>+3.558</b> · HOTA <b>+4.305</b> · IDF1 <b>+6.565</b> · IDS <b>−237</b>. The bootstrap confirmed these main gains are <b>significant</b>.</p>'),
             ('Section VIII · Cross-dataset', 'Section VIII · UAVDT result')))

# ================================================================== IX · Literature & protocol audit
S.append(divider("IX", "image25.jpeg", "Comparing With Published Work: A Protocol Audit",
                 "A fair comparison with papers made us check our evaluator — and we found an important difference.",
                 "The supervisor asked for a comparison with published work. This led to an important check."))
S.append(slide("IX", "Published comparison", "Literature", "First Look: V1 vs Published ByteTrack", "\n".join([
    meaning("We looked for papers on the <b>same test split</b> (VisDrone2019-MOT test-dev). <b>At first sight</b>, V1 looked better than published ByteTrack."),
    charts("lit-quality", "lit-ids"),
    '''    <table class="tbl" style="font-size:25px">
      <tr><th style="text-align:left">Result</th><th>MOTA ↑</th><th>IDF1 ↑</th><th>IDS ↓</th></tr>
      <tr><td>ByteTrack · reported in DroneMOT (ICRA 2024)</td><td>25.1</td><td>40.8</td><td>1590</td></tr>
      <tr><td>V1 · our old custom protocol</td><td>26.948</td><td>41.546</td><td>1184</td></tr>
      <tr><td class="strong">Difference — only at first sight <span class="warn">(not yet comparable)</span></td><td>+1.848</td><td>+0.746</td><td>406 fewer</td></tr>
    </table>''',
    ]),
    say(("Say", "DroneMOT, at ICRA 2024, reports ByteTrack on VisDrone test-dev: MOTA 25.1, IDF1 40.8, 1590 ID switches. Our V1 number was 26.948 MOTA. At first sight that is better — but we had to check the evaluation first.")),
    foot='<span class="prov p-pub">Published · DroneMOT, ICRA 2024 · ByteTrack row</span><span class="prov p-test">V1 · our custom AC-MOT protocol</span>'))
S.append(slide("IX", "Protocol audit", "Protocol audit", "We Checked Our Evaluator: Not the Official Protocol", "\n".join([
    meaning("Our 26.948 is <b>correct for our controlled comparison</b>, but it was <b>not computed with the official VisDrone protocol</b> — so it cannot stand next to the published 25.1."),
    '''    <table class="tbl" style="font-size:25px">
      <tr><th style="text-align:left">Rule</th><th style="text-align:left">Our old AC-MOT protocol</th><th style="text-align:left">Official VisDrone protocol</th></tr>
      <tr><td>Classes</td><td style="text-align:left">1, 4, 5, 6, 9</td><td style="text-align:left">1, 4, 5, 6, 9</td></tr>
      <tr><td>Matching</td><td style="text-align:left" class="bad strong">class-agnostic — after picking the 5 classes, any class could match</td><td style="text-align:left" class="good strong">class-aware — car ↔ car, bus ↔ bus …</td></tr>
      <tr><td>Extra filters</td><td style="text-align:left">score = 1, occlusion &lt; 2, truncation &lt; 2</td><td style="text-align:left">only what the official toolkit itself asks for</td></tr>
      <tr><td>Ignore regions</td><td style="text-align:left" class="bad strong">not applied the official way</td><td style="text-align:left" class="good strong">special ignore handling (class 0 and class 11)</td></tr>
    </table>''',
    '    <div class="callout">Not a disaster: finding this <b>before</b> the paper is an important research step.</div>']),
    say(("Say", "We went back to our evaluator. It used classes 1, 4, 5, 6 and 9 with score 1, occlusion below 2 and truncation below 2, and it was class-agnostic. It also did not apply the official ignore-region processing. So 26.948 is valid for our controlled comparison, but it is not an official VisDrone number.")),
    foot='<span class="prov p-hist">Protocol audit of our own evaluator</span>', explain="x-eval|Our Evaluation in Detail"))
S.append(slide("IX", "Official protocol", "Official VisDrone protocol", "The Official VisDrone Evaluation", "\n".join([
    meaning("The official protocol <b>matches boxes only inside the same class</b> and <b>does not count</b> predictions inside ignore regions as normal false positives."),
    '''    <div class="g3 grow" style="gap:20px">
      <div class="card sec"><h3>Data and classes</h3><p>VisDrone2019-MOT-test-dev</p>
        <div class="pills mt8"><span class="pill">1 pedestrian</span><span class="pill">4 car</span><span class="pill">5 van</span><span class="pill">6 truck</span><span class="pill">9 bus</span></div>
        <p class="mt8">A match needs <b>IoU ≥ 0.5</b>.</p></div>
      <div class="card sec col" style="gap:8px"><h3>Class-aware matching</h3>
        <svg viewBox="0 0 420 200" width="100%" style="flex:1;min-height:0"><g font-family="Inter,Helvetica" font-weight="800" font-size="22">
          <rect x="20" y="30" width="110" height="60" fill="#DCFCE7" stroke="#16A34A" stroke-width="4"/><text x="75" y="22" text-anchor="middle" fill="#15803D">GT car</text>
          <rect x="30" y="38" width="110" height="60" fill="none" stroke="#DC2626" stroke-width="4"/><text x="200" y="72" fill="#15803D">car ↔ car ✓</text>
          <rect x="20" y="126" width="110" height="60" fill="#DCFCE7" stroke="#16A34A" stroke-width="4"/><text x="75" y="120" text-anchor="middle" fill="#15803D">GT van</text>
          <rect x="30" y="134" width="110" height="60" fill="none" stroke="#DC2626" stroke-width="4"/><text x="200" y="168" fill="#B91C1C">car ↔ van ✗</text>
        </g></svg><div class="tc"><span class="origin illus">drawing · no numbers</span></div></div>
      <div class="card sec"><h3>Ignore regions</h3><ul class="clean"><li><b>class 0</b> = ignored region</li><li><b>class 11</b> = others</li><li>a prediction that falls enough inside them is <b>not counted as a normal FP</b></li></ul></div>
    </div>''',
    '    <div class="note">We will <b>not</b> use our custom occlusion &lt; 2 and truncation &lt; 2 filters unless the official toolkit itself asks for them.</div>']),
    say(("Say", "The official protocol uses test-dev with the five classes pedestrian, car, van, truck and bus. Matching is class-aware: a car can only match a car. IoU is 0.5. Classes 0 and 11 are ignore regions: predictions that fall enough inside them are not counted as normal false positives.")),
    foot='<span class="prov p-pub">Official VisDrone MOT evaluation rules (as reviewed)</span>'))
S.append(slide("IX", "The van problem", "Detector classes", "A Real Challenge: COCO Has No “Van” Class", "\n".join([
    meaning("Our detector is <b>YOLOv8n pretrained on COCO</b>. It can output person, car, truck and bus — but <b>COCO has no van</b>."),
    '''    <div class="row grow" style="gap:24px">
      <table class="tbl" style="font-size:28px;flex:0 0 700px">
        <tr><th style="text-align:left">COCO class (detector)</th><th style="text-align:center"></th><th style="text-align:left">VisDrone class (official)</th></tr>
        <tr><td>person</td><td style="text-align:center">→</td><td style="text-align:left">pedestrian</td></tr>
        <tr><td>car</td><td style="text-align:center">→</td><td style="text-align:left">car</td></tr>
        <tr><td>truck</td><td style="text-align:center">→</td><td style="text-align:left">truck</td></tr>
        <tr><td>bus</td><td style="text-align:center">→</td><td style="text-align:left">bus</td></tr>
        <tr><td class="bad strong">no matching COCO class</td><td style="text-align:center">✗</td><td style="text-align:left" class="bad strong">van</td></tr>
      </table>
      <div class="col grow" style="gap:16px">
        <div class="card" style="border-left:6px solid var(--bad)"><h3>We will not say car = van</h3><p>That would be <b>scientifically wrong</b>.</p></div>
        <div class="card" style="border-left:6px solid var(--warn)"><h3>So vans are a real challenge</h3><p>The van ground truth will be a <b>real challenge</b> for our system in class-aware scoring.</p></div>
      </div>
    </div>''']),
    say(("Say", "There is one more issue. Our detector is YOLOv8n pretrained on COCO. COCO person maps to pedestrian, car to car, truck to truck and bus to bus — but there is no van in COCO. We will not pretend a car is a van, so vans will be a real challenge.")),
    foot='<span class="prov p-hist">Class mapping · COCO-pretrained YOLOv8n → VisDrone</span>'))
S.append(slide("IX", "Two kinds of results", "Where we stand", "Two Kinds of Results — Two Different Questions", "\n".join([
    meaning("The controlled results <b>stay valid</b>. Only the comparison with papers needs an <b>official re-evaluation</b>."),
    '''    <div class="g2 grow" style="gap:22px">
      <div class="card col" style="border-top:8px solid var(--good);gap:8px"><div class="tag" style="color:#15803D">A · Controlled AC-MOT results</div>
        <h3>Did AC-MOT improve my baseline?</h3>
        <div class="pills"><span class="pill">Baseline 19.729</span><span class="pill">V1 26.948</span><span class="pill">V2 23.792</span></div>
        <p><b>Answer: yes</b> — the same protocol for every system.</p>
        <p>Keep them: they are the <b>main evidence</b> of the contribution.</p></div>
      <div class="card col" style="border-top:8px solid var(--warn);gap:8px"><div class="tag" style="color:#B45309">B · Official literature comparison</div>
        <h3>Does AC-MOT beat published methods?</h3>
        <ul class="clean" style="font-size:23px"><li>same <b>frozen</b> systems and outputs</li><li>no retraining · no parameter changes · no Optuna · no reselection</li><li>change <b>only the evaluation protocol</b> → official</li><li>report official MOTA, IDF1, IDS, FP, FN</li><li>then: ByteTrack published vs V1 official vs V2 official</li></ul>
        <div><span class="prov p-pend">Status · not done yet</span></div></div>
    </div>''']),
    say(("Say", "We now have two kinds of results. A: the controlled AC-MOT results — they prove AC-MOT improved the baseline under one protocol, and we keep them. B: the comparison with papers — it needs an official-aligned re-evaluation of the same frozen systems, changing only the evaluation protocol.")),
    foot='<span class="prov p-test">A · custom AC-MOT protocol</span><span class="prov p-pend">B · official re-evaluation pending</span>'))
S.append(slide("IX", "Correction freeze", "Research integrity", "Why We Made a New Freeze", "\n".join([
    meaning("We did <b>not erase</b> the mistake. <b>We documented the correction.</b>"),
    '''    <div class="flow" style="gap:0">
      <div class="node fx" style="width:360px">Old freeze<small>results with our custom research protocol · kept</small></div><div class="arr"></div>
      <div class="node hot" style="width:380px">Correction freeze<small>from now on, comparison with papers must be official-aligned</small></div><div class="arr"></div>
      <div class="node io" style="width:340px">Next<small>official VisDrone re-evaluation → fair comparison</small></div>
    </div>''',
    '''    <div class="g2 grow" style="gap:22px">
      <div class="card" style="border-left:6px solid var(--bad)"><h3>We did not</h3><ul class="clean"><li>go back and change history</li><li>delete the old results</li></ul></div>
      <div class="card" style="border-left:6px solid var(--good)"><h3>We did</h3><ul class="clean"><li>keep the old freeze as it is</li><li>document the protocol difference</li><li>fix the rule for every future comparison</li></ul></div>
    </div>''',
    '    <div class="callout">Documenting a correction is a <b>stronger research practice</b> than silently changing numbers.</div>']),
    say(("Say", "We did not go back and rewrite history. The old freeze stays and says: these results used the custom research protocol. A new correction freeze says: from here on, comparison with published work must be official-aligned.")),
    foot='<span class="prov p-hist">Freeze records · old freeze kept · correction freeze added</span>'))

# ================================================================== X · Conclusion
S.append(divider("X", "image29.jpeg", "Conclusion and Future Work",
                 "The whole story in one line, what is proven, and what comes next.",
                 "To finish: the whole story in one line."))


def chain(nodes):
    parts = []
    for i, (cls, txt, sm) in enumerate(nodes):
        if i: parts.append('<div class="arr sm"></div>')
        parts.append(f'<div class="node {cls}" style="width:262px;font-size:21px;padding:9px 10px">{txt}<small>{sm}</small></div>')
    return '    <div class="flow" style="gap:0">' + "".join(parts) + '</div>'


S.append(slide("X", "The story in one line", "Summary", "The Whole Story in One Line", "\n".join([
    chain([("fx", "Baseline", "YOLOv8n + ByteTrack · 19.729 MOTA"), ("ad", "Heuristic AC-MOT", "23.236 MOTA"),
           ("bad", "Problem", "hand-picked SCI weights"), ("ad", "Optuna + TPE", "validation only"),
           ("good", "V1", "26.948 MOTA · 41.546 IDF1")]),
    '    <div class="tc strong muted" style="font-size:26px;line-height:1">↓</div>',
    chain([("bad", "Problem", "weak IDS improvement"), ("ad", "Multi-objective", "MOTA ↑ / IDS ↓ · Pareto"),
           ("good", "V2", "23.792 MOTA · 919 IDS · 46.02 FPS"), ("good", "Bootstrap", "quality gains significant"),
           ("good", "UAVDT", "zero tuning · gain transfers")]),
    '    <div class="tc strong muted" style="font-size:26px;line-height:1">↓</div>',
    chain([("fx", "Literature comparison", "DroneMOT · ByteTrack"), ("bad", "Protocol audit", "old evaluation not official"),
           ("hot", "Correction freeze", "documented, not erased"), ("io", "NEXT", "official VisDrone re-evaluation"),
           ("io", "Then", "fair comparison with papers")]),
    '    <div class="callout tc">Every step answered <b>one question</b> — and opened the next one.</div>']),
    say(("Say", "The whole story: a baseline at 19.7 MOTA; heuristic AC-MOT at 23.2; the weights were hand-picked, so Optuna built V1 at 26.9; V1's ID switches did not improve enough, so a multi-objective search built V2 with 919 ID switches and 46 FPS; the bootstrap and UAVDT confirmed the gains; comparing with papers led to a protocol audit and a correction freeze; next is the official VisDrone re-evaluation.")),
    foot=""))
S.append(use("Main contributions", "X",
             ('Demonstrated <b>performance trade-offs</b> on the original test set and in the cross-dataset UAVDT evaluation.',
              'A measured <b>quality vs identity / speed trade-off</b> (V1 vs V2), checked with a <b>paired bootstrap</b> and a <b>zero-tuning UAVDT</b> test.')))
S.append(slide("X", "Proven and open", "Key message", "What Is Proven — and What Is Still Open", "\n".join([
    meaning("The research did <b>not collapse</b> because of the official evaluation. <b>Three results are solid</b>; one question is still open."),
    '''    <div class="g3" style="gap:18px">
      <div class="card" style="border-top:6px solid var(--good)"><div class="tag" style="color:#15803D">Proven 1 · controlled result</div><p class="mt8">Adding AC-MOT to the <b>same detector and tracker</b> clearly improved MOTA, HOTA and IDF1.</p></div>
      <div class="card" style="border-top:6px solid var(--good)"><div class="tag" style="color:#15803D">Proven 2 · trade-off</div><p class="mt8">Moving from a constrained single goal to <b>multi-objective</b> revealed a real quality vs identity / speed trade-off.</p></div>
      <div class="card" style="border-top:6px solid var(--good)"><div class="tag" style="color:#15803D">Proven 3 · transfer</div><p class="mt8">The improvement <b>transferred to UAVDT</b> with zero tuning.</p></div>
    </div>''',
    '    <div class="card" style="border-left:8px solid var(--warn)"><div class="tag" style="color:#B45309">Still open</div><p class="mt8">Do the new <b>official</b> numbers put AC-MOT above ByteTrack or other published methods on the official VisDrone benchmark? → needs the <b>official re-run</b>.</p></div>',
    '    <div class="callout">26.948 is <b>not wrong</b>. It answers “Did AC-MOT improve my baseline?” — <b>yes</b>. It does not yet answer “Did AC-MOT beat published ByteTrack on the official benchmark?”</div>']),
    say(("Say", "The most important point: 26.948 is not wrong. It answers the question 'did AC-MOT improve my baseline?' — yes. It is not yet the answer to 'did AC-MOT beat published ByteTrack on the official VisDrone benchmark?' That needs the official re-run.")),
    foot=""))
S.append(use("Conclusion: what AC-MOT delivers", "X",
             ('<table class="tbl" style="font-size:30px">', '<table class="tbl" style="font-size:27px">'),
             ('<td style="text-align:left">supports cross-dataset transfer</td></tr>',
              '<td style="text-align:left">supports cross-dataset transfer</td></tr>\n      <tr><td class="strong" style="color:#B45309">Official VisDrone</td><td style="text-align:center">→</td><td style="text-align:left">re-evaluation needed before comparing with papers</td></tr>')))
S.append(use("Directions for future work", "X",
             ('  <div class="s-body col">\n    <div class="g2 grow" style="gap:20px">',
              '  <div class="s-body col">\n    <div class="callout warn"><b>Next step first:</b> official-aligned VisDrone re-evaluation of the frozen V1 and V2 — then a fair comparison with published papers.</div>\n    <div class="g2 grow" style="gap:20px">')))
S.append(use("Thank you", "X",
             ('data-sec="9" data-secname="X · Conclusion"', 'data-sec="0" data-secname="Questions"')))

# removed from the main story (still available in older versions)
dropped = sorted(blocks)
assert set(dropped) == {"Section III", "Section IV", "Section V", "Section VI", "Section VII", "Section VIII",
                        "Fair and attributable design", "Original ablation table", "What each component changed",
                        "Final test-set comparison", "Reading the test-set result"}, dropped

main = prefix + "".join(S).rstrip() + "\n" + suffix
h = main + rest

# ------------------------------------------------------------------ renames everywhere
h = h.replace("Old AC-MOT", "Initial AC-MOT")

# ------------------------------------------------------------------ outline (PowerPoint style, 10 sections)
mm = h[:h.index('<div class="overlay xview"')]
tags = re.findall(r'<section class="slide[^"]*"[^>]*>', mm)
start = {re.search(r'id="(sec-\d+)"', t).group(1): i for i, t in enumerate(tags, 1) if re.search(r'id="(sec-\d+)"', t)}
order = sorted(start.items(), key=lambda kv: kv[1])
rng = {k: (v, (order[j + 1][1] - 1) if j + 1 < len(order) else len(tags)) for j, (k, v) in enumerate(order)}
rows = [("I", "sec-1", "Introduction and Motivation", "Detection, tracking and how we measure them"),
        ("II", "sec-2", "Related Work: Detectors and Trackers", "YOLO, ByteTrack and the benchmarks"),
        ("III", "sec-3", "Problem and Baseline", "Why one fixed setting is not enough"),
        ("IV", "sec-4", "Proposed Framework: AC-MOT", "Scene score (SCI) and Smart Calibrator"),
        ("V", "sec-5", "Experimental Setup and First Result", "VisDrone, protocol and the initial AC-MOT"),
        ("VI", "sec-6", "V1: Validation-Driven Optimization", "Optuna, Trial 24 and the test result"),
        ("VII", "sec-7", "V2: Multi-Objective Optimization", "Pareto search and the V1 / V2 trade-off"),
        ("VIII", "sec-8", "Statistical and External Validation", "Paired bootstrap and UAVDT with zero tuning"),
        ("IX", "sec-9", "Literature Comparison and Protocol Audit", "Official VisDrone protocol and the next step"),
        ("X", "sec-10", "Conclusion and Future Work", "What is proven and what comes next")]
last = len(tags) - 1  # the Thank-you slide is not part of section X's range label
rng["sec-10"] = (rng["sec-10"][0], last)
cards = "\n".join(
    f'      <button class="ol-row" data-goto="{g}"><span class="n">{n}</span><span class="t"><h3>{t}</h3>'
    f'<p>{s}</p><p class="rg">slides {rng[g][0]} - {rng[g][1]}</p></span></button>' for n, g, t, s in rows)
a = h.index('<div class="ol-ppt">'); b = h.index('    </div>\n  </div>\n  <aside class="notes"><p><b>Say:</b> "The story goes in the order', a)
h = h[:a] + '<div class="ol-ppt">\n' + cards + '\n' + h[b:]
h = rep(h, 'the problem, the first heuristic design, the ablation, the optimization, the test results and a second dataset.',
        'the problem and the baseline, the first heuristic design, V1, V2, the statistics and UAVDT, and finally the protocol audit.')
save("index.html", h)

# ------------------------------------------------------------------ styles: outline with 5 rows per column
c = load("styles.css")
c = rep(c, "grid-template-rows:repeat(4,1fr)", "grid-template-rows:repeat(5,1fr)")
c = rep(c, ".ol-row:nth-child(4),.ol-row:nth-child(8){border-bottom:0}", ".ol-row:nth-child(5),.ol-row:nth-child(10){border-bottom:0}")
c = rep(c, ".ol-row{display:flex;align-items:flex-start;gap:0;text-align:left;background:#FAFBFD;border:0;border-bottom:2px solid #E2E8F0;\n  padding:18px 10px 14px;",
        ".ol-row{display:flex;align-items:flex-start;gap:0;text-align:left;background:#FAFBFD;border:0;border-bottom:2px solid #E2E8F0;\n  padding:10px 10px 8px;")
c = rep(c, ".ol-row h3{font-size:30px;font-weight:700;color:#0F172A;margin:0 0 6px;line-height:1.2}", ".ol-row h3{font-size:28px;font-weight:700;color:#0F172A;margin:0 0 3px;line-height:1.15}")
c = rep(c, ".ol-row p{font-size:24px;color:#64748B;margin:0;line-height:1.4}", ".ol-row p{font-size:22px;color:#64748B;margin:0;line-height:1.3}")
c = rep(c, ".ol-row .n{flex:0 0 106px;font-size:40px;font-weight:700;color:#0B4F8A;line-height:1.1;padding-top:8px}", ".ol-row .n{flex:0 0 106px;font-size:38px;font-weight:700;color:#0B4F8A;line-height:1.1;padding-top:4px}")
save("styles.css", c)

# ------------------------------------------------------------------ data
r = load("assets/data/results.js")
r = rep(r, "name: 'Old AC-MOT',  mota: 23.236", "name: 'Initial AC-MOT', mota: 23.236")
r = rep(r, "v1_vs_base: { mota: [7.22, 5.44, 9.29], hota: [5.41, 4.13, 6.90], idf1: [8.82, 6.90, 11.05], idsRed: [51, -114, 219] },",
        "v1_vs_base: { mota: [7.2195, 5.4362, 9.2934], hota: [5.4051, 4.1273, 6.9022], idf1: [8.8220, 6.9005, 11.0537], idsRed: [51, -114, 219] },")
r = rep(r, "window.ACMOT.published = {\n",
        "window.ACMOT.published = {\n  /* DroneMOT (ICRA 2024) reports ByteTrack on VisDrone2019-MOT test-dev — as supplied by the author */\n"
        "  droneMOTByteTrack: { mota: 25.1, idf1: 40.8, ids: 1590 },\n")
save("assets/data/results.js", r)

j = load("script.js")
j = rep(j, ".replace('Old AC-MOT', 'Old\\nAC-MOT')", ".replace('Initial AC-MOT', 'Initial\\nAC-MOT')")
j = rep(j, "label: 'Old A3 reference'", "label: 'Initial AC-MOT (Old-A3) reference'")
new_charts = r"""    /* v15: charts for the full research story */
    'init-quality': function (h) { grouped(h, { groups: ['MOTA', 'HOTA', 'IDF1'], better: 'higher', dec: 1, ylabel: 'percent',
      series: ['base', 'old'].map(tdRow).map(function (x) { return { name: x.name, color: COL[x.id], values: [x.mota, x.hota, x.idf1] }; }) }); },
    'init-ids': function (h) { sysBars(h, ['base', 'old'].map(tdRow), 'ids', 'lower', 0, null, 'ID switches'); },
    'init-fps': function (h) { sysBars(h, ['base', 'old'].map(tdRow), 'fps', 'higher', 1, REF25, 'FPS'); },
    'v1b-quality': function (h) { grouped(h, { groups: ['MOTA', 'HOTA', 'IDF1'], better: 'higher', dec: 1, ylabel: 'percent',
      series: ['base', 'v1'].map(tdRow).map(function (x) { return { name: x.name, color: COL[x.id], values: [x.mota, x.hota, x.idf1] }; }) }); },
    'v1b-ids': function (h) { sysBars(h, ['base', 'v1'].map(tdRow), 'ids', 'lower', 0, null, 'ID switches'); },
    'v1b-fps': function (h) { sysBars(h, ['base', 'v1'].map(tdRow), 'fps', 'higher', 1, REF25, 'FPS'); },
    'td3-quality': function (h) { grouped(h, { groups: ['MOTA', 'HOTA', 'IDF1'], better: 'higher', dec: 1, ylabel: 'percent',
      series: ['base', 'v1', 'v2'].map(tdRow).map(function (x) { return { name: x.name, color: COL[x.id], values: [x.mota, x.hota, x.idf1] }; }) }); },
    'td3-ids': function (h) { sysBars(h, ['base', 'v1', 'v2'].map(tdRow), 'ids', 'lower', 0, null, 'ID switches'); },
    'td3-fps': function (h) { sysBars(h, ['base', 'v1', 'v2'].map(tdRow), 'fps', 'higher', 1, REF25, 'FPS'); },
    'val-quality': function (h) { var a = D.v1.val, b = D.v2.val;
      grouped(h, { groups: ['MOTA', 'HOTA', 'IDF1'], better: 'higher', dec: 1, ylabel: 'percent',
        series: [{ name: 'V1 Trial 24', color: COL.v1, values: [a.mota, a.hota, a.idf1] }, { name: 'V2 Trial 22', color: COL.v2, values: [b.mota, b.hota, b.idf1] }] }); },
    'val-ids': function (h) { bars(h, { labels: ['V1\nTrial 24', 'V2\nTrial 22'], values: [D.v1.val.ids, D.v2.val.ids], colors: [COL.v1, COL.v2], better: 'lower', dec: 0, ylabel: 'ID switches', mb: 76, bw: 84 }); },
    'val-fps': function (h) { bars(h, { labels: ['V1\nTrial 24', 'V2\nTrial 22'], values: [D.v1.val.fps, D.v2.val.fps], colors: [COL.v1, COL.v2], better: 'higher', dec: 1, ref: REF25, ylabel: 'FPS', mb: 76, bw: 84 }); },
    'boot-v1q': function (h) { var b = D.testdev.bootstrap.v1_vs_base;
      forest(h, { xlabel: 'V1 − Baseline (points) · 95% confidence interval', dec: 2, ml: 110, mr: 180, rows: [
        { label: 'MOTA', est: b.mota[0], lo: b.mota[1], hi: b.mota[2], color: COL.v1 },
        { label: 'HOTA', est: b.hota[0], lo: b.hota[1], hi: b.hota[2], color: COL.v1 },
        { label: 'IDF1', est: b.idf1[0], lo: b.idf1[1], hi: b.idf1[2], color: COL.v1 }] }); },
    'boot-ids2': function (h) { var b = D.testdev.bootstrap;
      forest(h, { xlabel: 'ID switches removed vs Baseline (positive = fewer)', dec: 0, ml: 90, mr: 170, rows: [
        { label: 'V1', est: b.v1_vs_base.idsRed[0], lo: b.v1_vs_base.idsRed[1], hi: b.v1_vs_base.idsRed[2], color: COL.v1 },
        { label: 'V2', est: b.v2_vs_base.idsRed[0], lo: b.v2_vs_base.idsRed[1], hi: b.v2_vs_base.idsRed[2], color: COL.v2 }] }); },
    'lit-quality': function (h) { var p = D.published.droneMOTByteTrack, v = tdRow('v1');
      grouped(h, { groups: ['MOTA', 'IDF1'], better: 'higher', dec: 1, ylabel: 'percent', bw: 90,
        series: [{ name: 'ByteTrack (DroneMOT)', color: '#F59E0B', values: [p.mota, p.idf1] }, { name: 'V1 (old custom protocol)', color: COL.v1, values: [v.mota, v.idf1] }] }); },
    'lit-ids': function (h) { var p = D.published.droneMOTByteTrack, v = tdRow('v1');
      bars(h, { labels: ['ByteTrack\n(DroneMOT)', 'V1\n(old protocol)'], values: [p.ids, v.ids], colors: ['#F59E0B', COL.v1], better: 'lower', dec: 0, ylabel: 'ID switches', mb: 76, bw: 84 }); },
"""
j = rep(j, "    'pub-mota': function (h) {", new_charts + "    'pub-mota': function (h) {")
j = rep(j, "#u2setup,.ol-card .n,.ol-ppt,.node small'", "#u2setup,.ol-card .n,.ol-ppt,.tbl th,.node small'")  # no full names inside table headers
save("script.js", j)

m = load("assets/data/meaning.js")
m = rep(m, "t: 'Every next step targets a <b>weakness we measured</b>: camera motion, a smarter input size, better appearance matching, and other detectors.' }",
        "t: 'First the <b>official VisDrone re-evaluation</b>; then every next step targets a <b>weakness we measured</b>: camera motion, input size, appearance matching and other detectors.' }")
save("assets/data/meaning.js", m)

print("ok · main slides:", len(tags), "· dropped:", dropped)
print({k: v for k, v in rng.items()})
