"""v9: complete, advanced on-demand explanations (main slides unchanged). Works on a copy of v8."""
import pathlib, re, sys

ROOT = pathlib.Path('/Users/ahmedgouda/Desktop/acmot_interactive_presentation_v9')
IDX, README = ROOT / 'index.html', ROOT / 'README.md'
h = IDX.read_text(encoding='utf-8')

def rep(old, new, label, count=1):
    global h
    n = h.count(old)
    if n != count:
        sys.exit(f'FAILED [{label}]: found {n}')
    h = h.replace(old, new)

def page(sec, title, kicker, h2, body):
    return (f'<section class="xpage" data-sec="{sec}" data-title="{title}">\n'
            f'  <header class="s-head"><div class="kicker">{kicker}</div><h2>{h2}</h2></header>\n'
            f'  <div class="s-body col">\n{body}\n  </div>\n</section>')

MAN = '<span class="origin manual">manually designed</span>'
EMP = '<span class="origin empirical">empirical design constant</span>'
OPT = '<span class="origin optuna">optimization-selected</span>'
ILL = '<span class="origin illus">illustration · made-up numbers</span>'
STD = '<span class="origin empirical">standard definition</span>'
INT = '<span class="origin illus">interpretation, not a measured cause</span>'

# ============================================================== IoU & NMS
iou = [
page(1, 'IoU computed', 'IoU and NMS · 1 of 3 — computing IoU', 'IoU From Box Corners, Step by Step', f'''
    <div class="row grow" style="gap:24px">
      <div class="card col" style="flex:0 0 620px;gap:6px"><div class="ex-label">Two boxes (pixels) {ILL}</div>
        <svg viewBox="0 0 560 360" width="100%" height="330"><g font-family="Inter,Helvetica" font-weight="800">
          <rect x="60" y="60" width="240" height="180" fill="#DCFCE7" stroke="#16A34A" stroke-width="5"/>
          <rect x="156" y="96" width="240" height="180" fill="none" stroke="#DC2626" stroke-width="5"/>
          <rect x="156" y="96" width="144" height="144" fill="#4F46E5" fill-opacity=".35"/>
          <text x="60" y="48" font-size="22" fill="#15803D">real box: (100,100) → (300,250)</text>
          <text x="156" y="310" font-size="22" fill="#B91C1C">detector box: (180,130) → (380,280)</text>
          <text x="228" y="176" font-size="22" fill="#312E81" text-anchor="middle">overlap</text></g></svg></div>
      <div class="col grow" style="gap:10px">
        <table class="tbl" style="font-size:26px">
          <tr><td>1 · area of the real box</td><td class="fcell">200 × 150 = 30,000</td></tr>
          <tr><td>2 · area of the detector box</td><td class="fcell">200 × 150 = 30,000</td></tr>
          <tr><td>3 · overlap width</td><td class="fcell">min(300,380) − max(100,180) = 120</td></tr>
          <tr><td>4 · overlap height</td><td class="fcell">min(250,280) − max(100,130) = 120</td></tr>
          <tr><td>5 · overlap area</td><td class="fcell">120 × 120 = 14,400</td></tr>
          <tr><td>6 · union</td><td class="fcell">30,000 + 30,000 − 14,400 = 45,600</td></tr>
        </table>
        <div class="card sec tc" style="padding:10px"><div class="xeq">IoU = 14,400 ÷ 45,600 ≈ <b>0.32</b></div></div>
        <div class="note">If the overlap width or height is 0 or negative, the boxes do not touch and IoU = 0.</div>
      </div>
    </div>'''),
page(1, 'IoU uses', 'IoU and NMS · 2 of 3 — where IoU is used', 'When Is a Box Correct? Three Uses of IoU', f'''
    <div class="meaning"><div class="tag">The main idea</div><p>The same overlap number is used in <b>three different places</b>, each with its own threshold.</p></div>
    <div class="g3 grow" style="gap:18px">
      <div class="card col" style="gap:8px;border-top:6px solid #16A34A"><h3>1 · Evaluation</h3><p>A detector box counts as a <b>true positive</b> when IoU with a real object is <b>≥ 0.5</b>. Otherwise the box is a false positive and the object may be a false negative.</p><div class="xeq sm">IoU 0.32 → not a match</div></div>
      <div class="card col" style="gap:8px;border-top:6px solid #4F46E5"><h3>2 · Detector NMS</h3><p>Inside one frame, a box that overlaps a <b>higher-score</b> box more than the NMS IoU threshold is <b>deleted</b> as a duplicate.</p><div class="xeq sm">AC-MOT: 0.40 … 0.52</div></div>
      <div class="card col" style="gap:8px;border-top:6px solid #64748B"><h3>3 · Tracker association</h3><p>Between frames, ByteTrack compares predicted track boxes with new boxes using an <b>IoU-based distance</b> (1 − IoU) and its match threshold.</p><div class="xeq sm">match_thresh = 0.86</div></div>
    </div>
    <div class="callout warn">Same measurement, three different jobs: <b>judge</b> a box · <b>remove</b> duplicates · <b>link</b> boxes over time.</div>'''),
page(1, 'NMS algorithm', 'IoU and NMS · 3 of 3 — the NMS algorithm', 'NMS Step by Step', f'''
    <div class="row grow" style="gap:24px">
      <div class="col" style="flex:0 0 640px;gap:10px">
        <div class="ex-label">Four boxes, NMS IoU threshold = 0.45 {ILL}</div>
        <table class="tbl" style="font-size:26px">
          <tr><th style="text-align:left">Box</th><th>Score</th><th style="text-align:left">Overlap with …</th></tr>
          <tr><td>A</td><td>0.92</td><td style="text-align:left">B: 0.70 · C: 0.10 · D: 0.05</td></tr>
          <tr><td>B</td><td>0.85</td><td style="text-align:left">A: 0.70</td></tr>
          <tr><td>C</td><td>0.60</td><td style="text-align:left">D: 0.62</td></tr>
          <tr><td>D</td><td>0.55</td><td style="text-align:left">C: 0.62</td></tr>
        </table>
        <div class="note">Boxes are first sorted by score, highest first.</div>
      </div>
      <div class="col grow" style="gap:8px">
        <div class="card flat" style="padding:10px 16px"><p><b>1.</b> Take the best box <b>A (0.92)</b> → keep it.</p></div>
        <div class="card flat" style="padding:10px 16px"><p><b>2.</b> Delete boxes that overlap A above 0.45 → <b class="bad">B is deleted</b> (0.70). C and D stay.</p></div>
        <div class="card flat" style="padding:10px 16px"><p><b>3.</b> Take the best remaining box <b>C (0.60)</b> → keep it.</p></div>
        <div class="card flat" style="padding:10px 16px"><p><b>4.</b> Delete boxes that overlap C above 0.45 → <b class="bad">D is deleted</b> (0.62).</p></div>
        <div class="card sec tc" style="padding:10px"><div class="xeq">kept: <b>A and C</b> → two objects</div></div>
      </div>
    </div>'''),
]

# ============================================================== Precision-recall and AP
ap = [
page(1, 'PR table', 'Precision, recall and AP · 1 of 3', 'Building the Precision–Recall Table', f'''
    <div class="meaning"><div class="tag">How it works</div><p>Sort all detections of one class by score. Go down the list and, after each box, recompute <b>precision</b> and <b>recall</b>. {ILL}</p></div>
    <div class="row grow" style="gap:22px">
      <table class="tbl" style="font-size:25px;flex:1.4">
        <tr><th>Rank</th><th>Score</th><th style="text-align:left">Result</th><th>TP so far</th><th>FP so far</th><th>Precision</th><th>Recall</th></tr>
        <tr><td>1</td><td>0.95</td><td style="text-align:left" class="good strong">TP</td><td>1</td><td>0</td><td>1 ÷ 1 = 1.00</td><td>1 ÷ 5 = 0.20</td></tr>
        <tr><td>2</td><td>0.90</td><td style="text-align:left" class="good strong">TP</td><td>2</td><td>0</td><td>2 ÷ 2 = 1.00</td><td>2 ÷ 5 = 0.40</td></tr>
        <tr><td>3</td><td>0.80</td><td style="text-align:left" class="bad strong">FP</td><td>2</td><td>1</td><td>2 ÷ 3 = 0.67</td><td>0.40</td></tr>
        <tr><td>4</td><td>0.70</td><td style="text-align:left" class="good strong">TP</td><td>3</td><td>1</td><td>3 ÷ 4 = 0.75</td><td>3 ÷ 5 = 0.60</td></tr>
        <tr><td>5</td><td>0.60</td><td style="text-align:left" class="bad strong">FP</td><td>3</td><td>2</td><td>3 ÷ 5 = 0.60</td><td>0.60</td></tr>
        <tr><td>6</td><td>0.50</td><td style="text-align:left" class="good strong">TP</td><td>4</td><td>2</td><td>4 ÷ 6 = 0.67</td><td>4 ÷ 5 = 0.80</td></tr>
      </table>
      <div class="col" style="flex:0 0 380px;gap:12px">
        <div class="card sec"><h3>Setup</h3><p><b>5</b> real objects. 6 detections. A detection is TP when IoU ≥ 0.5 with an unmatched real object.</p></div>
        <div class="note">One real object is never found, so recall stops at 0.80.</div>
      </div>
    </div>'''),
page(1, 'AP area', 'Precision, recall and AP · 2 of 3', 'AP = Area Under the Precision–Recall Curve', f'''
    <div class="row grow" style="gap:24px">
      <div class="card" style="flex:0 0 640px;padding:10px 14px">
        <svg viewBox="0 0 600 440" width="100%" height="420"><g font-family="Inter,Helvetica" font-weight="800">
          <line x1="70" y1="380" x2="570" y2="380" stroke="#94A3B8" stroke-width="2"/><line x1="70" y1="380" x2="70" y2="30" stroke="#94A3B8" stroke-width="2"/>
          <path d="M70 60 H270 V140 H370 V167 H470 V380 H70 Z" fill="#DBEAFE"/>
          <path d="M70 60 H270 V140 H370 V167 H470 V380" fill="none" stroke="#2563EB" stroke-width="5"/>
          <g fill="#0F1B33"><circle cx="170" cy="60" r="7"/><circle cx="270" cy="60" r="7"/><circle cx="270" cy="167" r="7"/><circle cx="370" cy="140" r="7"/><circle cx="370" cy="188" r="7"/><circle cx="470" cy="167" r="7"/></g>
          <g font-size="20" fill="#64748B" text-anchor="middle"><text x="70" y="406">0</text><text x="170" y="406">0.2</text><text x="270" y="406">0.4</text><text x="370" y="406">0.6</text><text x="470" y="406">0.8</text><text x="570" y="406">1.0</text></g>
          <g font-size="20" fill="#64748B" text-anchor="end"><text x="60" y="66">1.00</text><text x="60" y="146">0.75</text><text x="60" y="173">0.67</text><text x="60" y="386">0</text></g>
          <text x="320" y="436" font-size="22" fill="#475569" text-anchor="middle">Recall →</text>
          <text x="260" y="290" font-size="40" fill="#1D4ED8" text-anchor="middle">AP</text></g></svg></div>
      <div class="col grow" style="gap:10px">
        <div class="card"><h3>Interpolation</h3><p>At each recall level, use the <b>best precision reached at that recall or higher</b>. This removes the zig-zag.</p></div>
        <table class="tbl" style="font-size:25px">
          <tr><th style="text-align:left">Recall range</th><th>Precision</th><th>Area</th></tr>
          <tr><td>0 → 0.4</td><td>1.00</td><td class="fcell">0.4 × 1.00 = 0.400</td></tr>
          <tr><td>0.4 → 0.6</td><td>0.75</td><td class="fcell">0.2 × 0.75 = 0.150</td></tr>
          <tr><td>0.6 → 0.8</td><td>0.67</td><td class="fcell">0.2 × 0.667 = 0.133</td></tr>
          <tr><td>0.8 → 1.0</td><td>0</td><td class="fcell">never reached = 0</td></tr>
        </table>
        <div class="card sec tc" style="padding:10px"><div class="xeq">AP ≈ 0.400 + 0.150 + 0.133 = <b>0.683</b></div></div>
      </div>
    </div>'''),
page(1, 'mAP and COCO', 'Precision, recall and AP · 3 of 3', 'From AP to mAP — and the COCO Version', f'''
    <div class="g2 grow" style="gap:22px">
      <div class="card col" style="gap:10px;border-top:6px solid #2563EB"><h3>mAP · mean over classes</h3>
        <div class="xeq sm">mAP = (AP<sub>car</sub> + AP<sub>person</sub> + …) ÷ number of classes</div>
        <p>Example: AP 0.90 (car), 0.80 (person) → mAP = <b>0.85</b>.</p></div>
      <div class="card col" style="gap:10px;border-top:6px solid #7C3AED"><h3>COCO mAP (mAP 50–95) {STD}</h3>
        <ul class="clean"><li>AP is computed at <b>10 IoU thresholds</b>: 0.50, 0.55, … 0.95</li><li>each AP uses <b>101 recall points</b></li><li>the final number averages over IoU thresholds <b>and</b> classes</li></ul>
        <p>So a high COCO mAP needs boxes that are <b>both found and tightly placed</b>.</p></div>
    </div>
    <div class="callout">The detector table in this talk (for example YOLOv8n <b>37.3</b>) reports this COCO-style mAP. It judges the <b>detector only</b> — nothing about tracking IDs.</div>'''),
]

# ============================================================== HOTA in full (replaces the short HOTA page)
hota = [
page(1, 'Metrics HOTA DetA', 'Tracking metrics · 4 of 6 — HOTA, detection part', 'HOTA, Part 1: Detection Accuracy (DetA)', f'''
    <div class="meaning"><div class="tag">What HOTA measures</div><p>HOTA (Higher Order Tracking Accuracy) combines <b>detection</b> (DetA) and <b>association</b> (AssA). Localization accuracy (LocA) is reported beside it.</p></div>
    <div class="card tc" style="padding:10px 20px"><div class="xeq">at one overlap level α: &nbsp; HOTA<sub>α</sub> = √( DetA<sub>α</sub> × AssA<sub>α</sub> )</div></div>
    <div class="row grow" style="gap:22px">
      <div class="card col" style="flex:0 0 700px;gap:8px;border-top:6px solid #2563EB"><h3>DetA · did we detect the objects?</h3>
        <div class="xeq sm">DetA<sub>α</sub> = TP ÷ ( TP + FN + FP )</div>
        <p>Same small example: A detected in 5 frames + B in 4 frames = <b>9 TP</b>, <b>1 FN</b> (B missed), <b>1 FP</b> (tree).</p>
        <div class="xeq">DetA = 9 ÷ 11 ≈ <b>0.818</b></div></div>
      <div class="col grow" style="gap:12px">
        <div class="card"><h3>Overlap levels α</h3><p>A detection counts as TP at level α only if its overlap is at least α. HOTA repeats the calculation for <b>α = 0.05, 0.10, … 0.95</b> (19 levels) and averages.</p></div>
        <div class="note">{ILL} Here we assume every matched box overlaps well enough at all levels.</div>
      </div>
    </div>'''),
page(1, 'Metrics HOTA AssA', 'Tracking metrics · 5 of 6 — HOTA, association part', 'HOTA, Part 2: Association Accuracy (AssA)', f'''
    <div class="meaning"><div class="tag">How AssA works</div><p>For <b>every true-positive box</b>, ask how well its real ID and its predicted ID stay together over the whole video: <b>A = TPA ÷ (TPA + FNA + FPA)</b>. AssA is the average over all TP boxes.</p></div>
    <table class="tbl" style="font-size:25px">
      <tr><th style="text-align:left">TP boxes</th><th>TPA · same pair</th><th>FNA · real ID elsewhere</th><th>FPA · predicted ID elsewhere</th><th>A per box</th><th>boxes</th></tr>
      <tr><td>A with ID 1</td><td>3</td><td>2 (A as ID 3)</td><td>0</td><td class="strong">3 ÷ 5 = 0.60</td><td>3</td></tr>
      <tr><td>A with ID 3</td><td>2</td><td>3 (A as ID 1)</td><td>0</td><td class="strong">2 ÷ 5 = 0.40</td><td>2</td></tr>
      <tr><td>B with ID 2</td><td>4</td><td>1 (B missed)</td><td>0</td><td class="strong">4 ÷ 5 = 0.80</td><td>4</td></tr>
    </table>
    <div class="g2 grow" style="gap:22px">
      <div class="card sec tc col center" style="gap:4px"><div class="xeq sm">AssA = (3×0.60 + 2×0.40 + 4×0.80) ÷ 9</div><div class="xeq">= 5.8 ÷ 9 ≈ <b>0.644</b></div></div>
      <div class="card sec tc col center" style="gap:4px"><div class="xeq sm">HOTA<sub>α</sub> = √( 0.818 × 0.644 )</div><div class="xeq">≈ <b>0.726</b></div><p class="small">averaged over the 19 α levels (same here by assumption)</p></div>
    </div>'''),
]

# ============================================================== FPS
fps = [
page(1, 'FPS budget', 'Speed · 1 of 2 — FPS', 'FPS and the Real-Time Budget', f'''
    <div class="card tc" style="padding:12px 20px"><div class="xeq">FPS = frames processed ÷ seconds &nbsp; · &nbsp; time per frame = 1000 ms ÷ FPS</div></div>
    <table class="tbl" style="font-size:28px">
      <tr><th style="text-align:left">FPS</th><th>Time per frame</th><th style="text-align:left">Meaning for live video</th></tr>
      <tr><td>50</td><td>20 ms</td><td style="text-align:left" class="good">plenty of spare time</td></tr>
      <tr><td>30</td><td>33 ms</td><td style="text-align:left" class="good">keeps up with a 30 FPS camera</td></tr>
      <tr class="sel"><td>25</td><td>40 ms</td><td style="text-align:left"><b>our real-time rule</b> (hard limit in the search)</td></tr>
      <tr><td>20</td><td>50 ms</td><td style="text-align:left" class="bad">slower than the video — frames pile up</td></tr>
    </table>
    <div class="callout">Every part of the pipeline has to fit inside the time budget of one frame.</div>'''),
page(1, 'FPS where time goes', 'Speed · 2 of 2 — where the time goes', 'Where the Time Goes in AC-MOT', f'''
    <div class="xsteps col grow" style="gap:4px">
      <div class="node fx">every frame · <b>detector</b> (YOLOv8n) — the largest cost; grows with input size (640 → 736 → 832)</div><div class="xdown">+</div>
      <div class="node fx">every frame · <b>tracker</b> (ByteTrack) — prediction and matching</div><div class="xdown">+</div>
      <div class="node ad">every 10th frame · <b>Scene Analyzer</b> on a small gray copy — under 0.2 ms in development timing</div><div class="xdown">=</div>
      <div class="node good">time per frame → FPS</div>
    </div>
    <div class="g2" style="gap:18px">
      <div class="card" style="border-left:6px solid var(--bad)"><h3>Why AC-MOT can be slower</h3><p>Hard scenes can use a <b>bigger input</b>, which gives the detector more pixels to process.</p></div>
      <div class="card" style="border-left:6px solid var(--good)"><h3>Why it can be faster</h3><p>Settings that keep fewer boxes give the detector’s cleanup and the tracker <b>less work</b>.</p></div>
    </div>
    <p class="tc small muted">FPS therefore depends on how many frames fall into each regime in a video.</p>'''),
]

# ============================================================== Detector benchmark
bench = [
page(2, 'Benchmark columns', 'Detector benchmark · reading the table', 'How to Read the Detector Benchmark', f'''
    <table class="tbl" style="font-size:27px">
      <tr><th style="text-align:left">Column</th><th style="text-align:left">What it means</th><th style="text-align:left">Example · YOLOv8n</th></tr>
      <tr><td class="strong">mAP</td><td style="text-align:left">COCO mAP 50–95 on COCO val2017 — accuracy of the boxes</td><td style="text-align:left">37.3</td></tr>
      <tr><td class="strong">Speed</td><td style="text-align:left">milliseconds for one image</td><td style="text-align:left">3.2 ms</td></tr>
      <tr><td class="strong">FPS</td><td style="text-align:left">1000 ÷ milliseconds — detector alone</td><td style="text-align:left">1000 ÷ 3.2 ≈ 312</td></tr>
      <tr><td class="strong">Size</td><td style="text-align:left">number of learned parameters (millions)</td><td style="text-align:left">3.2 M</td></tr>
    </table>
    <div class="g2 grow" style="gap:20px">
      <div class="card sec"><h3>Same test conditions</h3><ul class="clean"><li>T4 GPU</li><li>TensorRT with FP16 (16-bit numbers, faster)</li><li>640 × 640 input, batch size 1</li></ul></div>
      <div class="card"><h3>Why it matters here</h3><p>Only rows measured under the <b>same conditions</b> can be compared. The detector-only FPS is much higher than the full tracking system, which also runs the tracker and scene analysis.</p></div>
    </div>
    <div class="tc"><span class="origin empirical">published values · IEEE ICMISI 2026 survey</span></div>'''),
]

# ============================================================== ByteTrack in depth
bt = [
page(2, 'ByteTrack predict', 'ByteTrack in depth · 1 of 4 — prediction', 'Step 1: Predict Where Each Track Moved', f'''
    <div class="meaning"><div class="tag">Kalman filter, simply</div><p>Each track remembers its box and its <b>velocity</b>. Before looking at the new frame, a <b>Kalman filter</b> predicts where the box should be now.</p></div>
    <div class="row grow" style="gap:24px">
      <div class="card" style="flex:0 0 700px;padding:10px 14px">
        <svg viewBox="0 0 640 300" width="100%" height="290"><g font-family="Inter,Helvetica" font-weight="800">
          <rect x="40" y="110" width="110" height="80" fill="none" stroke="#94A3B8" stroke-width="4" stroke-dasharray="8 6"/><text x="40" y="96" font-size="20" fill="#64748B">frame t−2</text>
          <rect x="190" y="100" width="110" height="80" fill="none" stroke="#64748B" stroke-width="4" stroke-dasharray="8 6"/><text x="190" y="86" font-size="20" fill="#475569">frame t−1</text>
          <rect x="340" y="90" width="110" height="80" fill="#EEF2FF" stroke="#4F46E5" stroke-width="5"/><text x="340" y="76" font-size="20" fill="#3730A3">predicted for t</text>
          <rect x="352" y="100" width="110" height="80" fill="none" stroke="#16A34A" stroke-width="5"/><text x="352" y="215" font-size="20" fill="#15803D">new detection at t</text>
          <path d="M150 150 H186 M300 140 H336" stroke="#0F1B33" stroke-width="4"/></g></svg></div>
      <div class="col grow" style="gap:12px">
        <div class="card"><h3>What is predicted</h3><p>Box centre, aspect ratio and height, plus how fast each one changes (a constant-velocity model).</p></div>
        <div class="card"><h3>Why it helps</h3><p>Comparing the new detection with the <b>predicted</b> box, not the old one, gives a much better overlap when objects move.</p></div>
      </div>
    </div>'''),
page(2, 'ByteTrack two rounds', 'ByteTrack in depth · 2 of 4 — matching', 'Step 2: Two Rounds of Matching', '''
    <div class="card tc" style="padding:10px 20px"><div class="xeq">distance = 1 − IoU(predicted track box, detection) &nbsp;→ optimal one-to-one assignment</div></div>
    <div class="g2 grow" style="gap:22px">
      <div class="card col" style="gap:8px;border-top:6px solid #16A34A"><h3>Round 1 · high-score detections</h3>
        <p>Detections with score ≥ <b>track_high_thresh</b> are matched to <b>all</b> tracks first.</p>
        <p>A pair is accepted only if its distance is inside the <b>match threshold</b>.</p>
        <div class="card flat" style="padding:8px 12px"><p>Result: most tracks get their box. Some tracks stay unmatched.</p></div></div>
      <div class="card col" style="gap:8px;border-top:6px solid #F59E0B"><h3>Round 2 · low-score detections</h3>
        <p>Detections with score between <b>track_low_thresh</b> and <b>track_high_thresh</b> are matched to the tracks <b>still unmatched</b>.</p>
        <p>These weak boxes are often <b>half-hidden or blurred</b> objects — this round keeps their IDs alive.</p>
        <div class="card flat" style="padding:8px 12px"><p>Weak boxes that match no track are thrown away (they never start new tracks).</p></div></div>
    </div>
    <div class="note">Detail: in the Ultralytics ByteTrack implementation the distance can also be combined with the detection score; the idea stays the same.</div>'''),
page(2, 'ByteTrack lifecycle', 'ByteTrack in depth · 3 of 4 — track life', 'Step 3: Starting, Keeping and Ending Tracks', '''
    <div class="flow grow" style="align-items:stretch;gap:0">
      <div class="card col" style="width:330px;gap:6px;border-top:6px solid #16A34A"><h3>New</h3><p>An unmatched <b>high-score</b> detection with score ≥ <b>new_track_thresh</b> starts a new track with a new ID.</p></div><div class="arr" style="align-self:center"></div>
      <div class="card col" style="width:330px;gap:6px;border-top:6px solid #2563EB"><h3>Tracked</h3><p>Matched in a frame → the box and velocity are updated and the ID continues.</p></div><div class="arr" style="align-self:center"></div>
      <div class="card col" style="width:330px;gap:6px;border-top:6px solid #F59E0B"><h3>Lost</h3><p>Not matched → kept in memory and still predicted, so it can be <b>re-found with the same ID</b>.</p></div><div class="arr" style="align-self:center"></div>
      <div class="card col" style="width:330px;gap:6px;border-top:6px solid #DC2626"><h3>Removed</h3><p>Lost for longer than about <b>track_buffer</b> frames (scaled to the video frame rate) → deleted.</p></div>
    </div>
    <div class="callout">A <b>longer track_buffer</b> lets a hidden object come back with its old ID, but keeps dead tracks around longer.</div>'''),
page(2, 'ByteTrack settings', 'ByteTrack in depth · 4 of 4 — our settings', 'Every ByteTrack Setting We Use', '''
    <table class="tbl" style="font-size:25px">
      <tr><th style="text-align:left">Setting</th><th style="text-align:left">What it controls</th><th>Default</th><th>Tuned (AC-MOT)</th></tr>
      <tr><td class="strong">track_high_thresh</td><td style="text-align:left">minimum score for round 1 (high-score detections)</td><td>0.25</td><td class="best">0.18</td></tr>
      <tr><td class="strong">track_low_thresh</td><td style="text-align:left">lowest score still used in round 2</td><td>0.10</td><td class="best">0.04</td></tr>
      <tr><td class="strong">new_track_thresh</td><td style="text-align:left">minimum score to start a new track</td><td>0.25</td><td class="best">0.20</td></tr>
      <tr><td class="strong">track_buffer</td><td style="text-align:left">how long a lost track is kept (frames)</td><td>30</td><td class="best">45</td></tr>
      <tr><td class="strong">match_thresh</td><td style="text-align:left">how far apart a track and a box may be and still match</td><td>0.80</td><td class="best">0.86</td></tr>
    </table>
    <div class="g2 grow" style="gap:20px">
      <div class="card sec"><h3>Direction of the tuning</h3><ul class="clean"><li>lower score limits → weaker boxes still help tracks</li><li>longer buffer → hidden objects keep their ID longer</li><li>larger match threshold → matches with less overlap are accepted</li></ul></div>
      <div class="card"><h3>Status</h3><p>Tuned once, then <b>frozen</b>. AC-MOT never changes these per frame — it only changes the <b>detector</b> settings.</p><div class="mt8"><span class="origin manual">tuned once · then frozen</span></div></div>
    </div>'''),
]

# ============================================================== Evaluation in depth
ev = [
page(5, 'Eval filtering', 'Evaluation in depth · 1 of 3 — ground truth', 'Step 1: Which Real Objects Are Counted', '''
    <table class="tbl" style="font-size:26px">
      <tr><th style="text-align:left">Rule</th><th style="text-align:left">Kept</th><th style="text-align:left">Removed · example</th></tr>
      <tr><td class="strong">class</td><td style="text-align:left">pedestrian, car, van, truck, bus (IDs 1, 4, 5, 6, 9)</td><td style="text-align:left">a bicycle at 100 m</td></tr>
      <tr><td class="strong">occlusion</td><td style="text-align:left">0 (visible) or 1 (slightly hidden)</td><td style="text-align:left">2–3: a person behind a bus</td></tr>
      <tr><td class="strong">truncation</td><td style="text-align:left">0 or 1 (a small part outside the image)</td><td style="text-align:left">2–3: a car mostly outside the frame</td></tr>
      <tr><td class="strong">annotation score</td><td style="text-align:left">1</td><td style="text-align:left">0 = an “ignore” region</td></tr>
    </table>
    <div class="g2 grow" style="gap:20px">
      <div class="card sec"><h3>Class-agnostic</h3><p>All kept classes are <b>merged into one class</b>: a van detected as “car” still counts as found.</p></div>
      <div class="card"><h3>Same for every system</h3><p>The filter is applied once to the ground truth and used by every system, so comparisons stay fair.</p></div>
    </div>'''),
page(5, 'Eval matching', 'Evaluation in depth · 2 of 3 — matching', 'Step 2: Matching Boxes in Every Frame', f'''
    <div class="xsteps col grow" style="gap:4px">
      <div class="node">for each frame: compute IoU between every tracker box and every real object</div><div class="xdown">↓</div>
      <div class="node">pairs with IoU ≥ 0.5 may match · one real object ↔ at most one tracker box</div><div class="xdown">↓</div>
      <div class="node">matched pairs → <b>TP</b> · unmatched tracker boxes → <b>FP</b> · unmatched real objects → <b>FN</b></div><div class="xdown">↓</div>
      <div class="node">if a real object is now matched to a <b>different track ID</b> than before → <b>IDS + 1</b></div><div class="xdown">↓</div>
      <div class="node good">add up over all frames and all sequences → MOTA, IDF1, HOTA</div>
    </div>
    <div class="note">TrackEval prefers to keep the previous frame’s match when it is still valid, so an ID is not switched just because another pairing is slightly better. IDF1 and HOTA use their own global matching (previous explanation).</div>'''),
page(5, 'Eval reset totals', 'Evaluation in depth · 3 of 3 — reset and totals', 'Step 3: Reset, Run, Add Up', '''
    <div class="g3 grow" style="gap:18px">
      <div class="card col" style="gap:8px;border-top:6px solid #4F46E5"><h3>1 · Reset per video</h3><p>The tracker starts with <b>no tracks and ID 1</b>. Without a reset, tracks from one video could match objects in the next.</p></div>
      <div class="card col" style="gap:8px;border-top:6px solid #0D9488"><h3>2 · Run and time</h3><p>The system processes every frame. FPS = frames processed ÷ processing time, on the same GPU for every system.</p></div>
      <div class="card col" style="gap:8px;border-top:6px solid #16A34A"><h3>3 · One total</h3><p>TrackEval (pinned to one exact version) combines all sequences into <b>one</b> MOTA, IDF1, HOTA and IDS per system.</p></div>
    </div>
    <div class="callout warn">These scores follow <b>our AC-MOT protocol</b> (class-agnostic, filtered ground truth). They are fair between our systems but are <b>not</b> official leaderboard results.</div>'''),
]

# ============================================================== Ablation in depth
ab = [
page(6, 'Ablation stages', 'Ablation in depth · 1 of 3 — the stages', 'What Each Ablation Stage Switches On', '''
    <table class="tbl" style="font-size:27px">
      <tr><th style="text-align:left">Stage</th><th style="text-align:left">What is switched on</th><th style="text-align:left">What it can change</th></tr>
      <tr><td class="strong">OLD-A0</td><td style="text-align:left">baseline: default settings</td><td style="text-align:left">reference point</td></tr>
      <tr><td class="strong">OLD-A1</td><td style="text-align:left">tuned ByteTrack settings</td><td style="text-align:left">association: how tracks and boxes are linked</td></tr>
      <tr><td class="strong">OLD-A2</td><td style="text-align:left">adaptive confidence + NMS (from SCI)</td><td style="text-align:left">which boxes reach the tracker</td></tr>
      <tr><td class="strong">OLD-A2R</td><td style="text-align:left">adaptive resolution only</td><td style="text-align:left">how much image detail the detector sees</td></tr>
      <tr><td class="strong">OLD-A3</td><td style="text-align:left">full AC-MOT</td><td style="text-align:left">all adaptive parts together</td></tr>
    </table>
    <div class="callout good">Every stage uses the <b>same YOLOv8n detector</b> without retraining. Only the listed part changes.</div>'''),
page(6, 'Ablation per metric', 'Ablation in depth · 2 of 3 — metric by metric', 'Reading the Ablation Metric by Metric', '''
    <table class="tbl" style="font-size:27px">
      <tr><th style="text-align:left">Metric</th><th style="text-align:left">Best stage</th><th>Value</th><th style="text-align:left">Baseline (A0)</th></tr>
      <tr><td>MOTA ↑</td><td style="text-align:left" class="strong">OLD-A2R · adaptive resolution only</td><td class="best">18.425</td><td style="text-align:left">17.633</td></tr>
      <tr><td>HOTA ↑</td><td style="text-align:left" class="strong">OLD-A3 · full AC-MOT</td><td class="best">33.064</td><td style="text-align:left">29.837</td></tr>
      <tr><td>IDF1 ↑</td><td style="text-align:left" class="strong">OLD-A3 · full AC-MOT</td><td class="best">36.296</td><td style="text-align:left">30.892</td></tr>
      <tr><td>IDS ↓</td><td style="text-align:left" class="strong">OLD-A2 · adaptive confidence + NMS</td><td class="best">210</td><td style="text-align:left">283</td></tr>
      <tr><td>FPS ↑</td><td style="text-align:left" class="strong">OLD-A1 · tuned ByteTrack</td><td class="best">44.51</td><td style="text-align:left">44.09</td></tr>
    </table>
    <div class="callout">Four different stages win the five metrics. That is why the result is read <b>metric by metric</b>, not as one overall winner.</div>
    <div class="tc"><span class="prov p-dev">Ablation study · original AC-MOT components · not the final test set</span></div>'''),
page(6, 'Ablation trade-offs', 'Ablation in depth · 3 of 3 — trade-offs', 'Why No Stage Wins Everything', f'''
    <div class="g2 grow" style="gap:20px">
      <div class="card col" style="gap:8px;border-top:6px solid #F59E0B"><h3>Resolution helps detection…</h3><p><b>Measured:</b> A2R has the highest MOTA (18.425), but more IDS (241) than A2 (210) and lower FPS (39.56).</p><p><b>Likely reason:</b> more pixels help find small objects, but more small objects close together give more chances to mix up IDs, and bigger inputs cost time.</p></div>
      <div class="card col" style="gap:8px;border-top:6px solid #4F46E5"><h3>The full system helps identity quality…</h3><p><b>Measured:</b> A3 has the highest HOTA (33.064) and IDF1 (36.296), but IDS 271 and the lowest FPS (37.96).</p><p><b>Likely reason:</b> combining all adaptive parts keeps identities consistent for longer, while the extra processing lowers speed.</p></div>
    </div>
    <div class="tc">{INT}</div>
    <div class="callout warn">Measured values are from the table; the “likely reasons” are our interpretation. The ablation did not isolate these causes separately.</div>'''),
]

# ============================================================== V2 multi-objective
PARETO_PTS = [(16,627.3,65.0),(17,589.1,65.6),(20,575.5,66.8),(5,561.8,68.2),(4,501.8,69.9),(26,422.7,80.8),(42,384.5,111.6),(34,370.9,129.0),
              (22,245.5,140.1),(10,223.6,154.5),(3,190.9,179.5),(43,174.5,216.7),(32,158.2,217.5),(45,155.5,230.4),(28,106.4,231.2),(44,100.9,301.7),(8,98.2,307.1)]
dots = ''.join(f'<circle cx="{x}" cy="{y}" r="{9 if t in (16,22,8) else 6}" fill="{"#0D9488" if t==22 else ("#14B8A6" if t in (16,8) else "#5EEAD4")}" stroke="#fff" stroke-width="2"/>' for t, x, y in PARETO_PTS)
line = 'M' + ' L'.join(f'{x} {y}' for t, x, y in sorted(PARETO_PTS, key=lambda p: p[1]))
PARETO_SVG = f'''<svg viewBox="0 0 700 390" width="100%" height="380"><g font-family="Inter,Helvetica" font-weight="800">
          <line x1="60" y1="340" x2="680" y2="340" stroke="#94A3B8" stroke-width="2"/><line x1="60" y1="340" x2="60" y2="30" stroke="#94A3B8" stroke-width="2"/>
          <path d="{line}" fill="none" stroke="#0D9488" stroke-width="2.5" stroke-dasharray="6 5"/>{dots}
          <text x="627" y="48" font-size="18" fill="#0F766E" text-anchor="middle">T16</text><text x="258" y="128" font-size="20" fill="#0F766E">T22</text><text x="112" y="322" font-size="18" fill="#0F766E">T8</text>
          <g font-size="17" fill="#64748B" text-anchor="middle"><text x="60" y="362">100</text><text x="333" y="362">200</text><text x="605" y="362">300</text></g>
          <g font-size="17" fill="#64748B" text-anchor="end"><text x="52" y="345">10</text><text x="52" y="195">17</text><text x="52" y="45">24</text></g>
          <text x="370" y="386" font-size="19" fill="#475569" text-anchor="middle">ID switches on validation (lower is better ←)</text>
          <text x="20" y="190" font-size="19" fill="#475569" text-anchor="middle" transform="rotate(-90 20 190)">MOTA % (higher ↑)</text></g></svg>'''

par = [
page(7, 'Pareto two goals', 'V2 multi-objective search · 1 of 3', 'Searching for Two Goals at Once', f'''
    <div class="g3" style="gap:18px">
      <div class="card tc" style="border-top:6px solid #16A34A"><div class="ex-label">goal 1</div><div class="xeq">maximize MOTA</div></div>
      <div class="card tc" style="border-top:6px solid #DC2626"><div class="ex-label">goal 2</div><div class="xeq">minimize IDS</div></div>
      <div class="card tc" style="border-top:6px solid #64748B"><div class="ex-label">constraint</div><div class="xeq">FPS ≥ 25</div></div>
    </div>
    <div class="g2 grow" style="gap:22px">
      <div class="card col" style="gap:8px"><h3>What changes from V1</h3><ul class="clean"><li>V1: one score (MOTA) + rules (FPS ≥ 25, IDS ≤ 271)</li><li>V2: <b>two scores</b> kept separate — no single “best” number</li><li>same search space, same TPE sampler and seed, validation videos only</li></ul></div>
      <div class="card col" style="gap:8px"><h3>What one trial gives</h3><p>Each trial runs the full validation pipeline and returns <b>a pair</b>: (MOTA, IDS). Trials that break the FPS limit are not acceptable.</p><p class="small muted">50 trials were planned; <b>49</b> completed.</p></div>
    </div>
    <div class="tc"><span class="prov p-val">V2 study design · validation only</span></div>'''),
page(7, 'Pareto dominance', 'V2 multi-objective search · 2 of 3', 'Dominance and the Pareto Front', f'''
    <div class="row grow" style="gap:22px">
      <div class="col" style="flex:0 0 640px;gap:10px">
        <div class="card sec"><h3>Dominance</h3><p>Trial X <b>dominates</b> trial Y if X is at least as good on <b>both</b> goals and better on at least one.</p></div>
        <table class="tbl" style="font-size:24px">
          <tr><th style="text-align:left">Toy trial</th><th>MOTA</th><th>IDS</th><th style="text-align:left">On the front?</th></tr>
          <tr><td>A</td><td>22</td><td>300</td><td style="text-align:left" class="good">yes — best MOTA</td></tr>
          <tr><td>B</td><td>20</td><td>200</td><td style="text-align:left" class="good">yes — better IDS than A</td></tr>
          <tr><td>C</td><td>19</td><td>250</td><td style="text-align:left" class="bad">no — B is better on both</td></tr>
        </table>
        <div class="note">{ILL} for the toy table · the chart shows the real V2 front.</div>
      </div>
      <div class="card grow" style="padding:8px 12px"><div class="ex-label">Real V2 Pareto points (validation)</div>{PARETO_SVG}</div>
    </div>'''),
page(7, 'Pareto choose T22', 'V2 multi-objective search · 3 of 3', 'Why Trial 22 Was Selected', f'''
    <div class="meaning"><div class="tag">The main idea</div><p>A front has <b>many</b> good trials, so a <b>selection rule fixed in advance</b> picks one: give <b>equal weight to both goals</b>. That rule selected <b>Trial 22</b>.</p></div>
    <table class="tbl" style="font-size:26px">
      <tr><th style="text-align:left">Front point (validation)</th><th>MOTA</th><th>IDS</th><th style="text-align:left">Character</th></tr>
      <tr><td>Trial 16</td><td data-bind="v2.pareto.0.1" data-dec="2">…</td><td data-bind="v2.pareto.0.2">…</td><td style="text-align:left">highest MOTA, many IDS</td></tr>
      <tr class="sel"><td>Trial 22 · selected</td><td data-bind="v2.val.mota" data-dec="2">…</td><td data-bind="v2.val.ids">…</td><td style="text-align:left"><b>balanced</b></td></tr>
      <tr><td>Trial 8</td><td data-bind="v2.pareto.16.1" data-dec="2">…</td><td data-bind="v2.pareto.16.2">…</td><td style="text-align:left">fewest IDS, low MOTA</td></tr>
    </table>
    <div class="g2 grow" style="gap:20px">
      <div class="card"><h3>Then frozen and tested</h3><p>Trial 22 was frozen and run on the test set: MOTA <b data-bind="testdev.rows.3.mota" data-dec="3">…</b>, IDS <b data-bind="testdev.rows.3.ids">…</b>, FPS <b data-bind="testdev.rows.3.fps" data-dec="3">…</b>.</p></div>
      <div class="card"><h3>Read it correctly</h3><p>V2 is a <b>different operating point</b>, not a replacement for V1 — see the V1 vs V2 explanation.</p></div>
    </div>
    <div class="tc">{OPT} <span class="prov p-val">Validation · V2 study</span> <span class="prov p-test">Test set · after selection</span></div>'''),
]

# ============================================================== SCI: frame preparation (appended to x-sci)
sci_prep = page(4, 'SCI frame preparation', 'SCI calculation · 3 of 3', 'Preparing the Frame and Where Each Cue Gets Its Data', f'''
    <div class="xchain"><span class="pill sec">frame 1920 × 1080</span><span>→ shrink to 25% →</span><span class="pill sec">480 × 270</span><span>→ grayscale →</span><span class="pill warn">small gray copy</span></div>
    <div class="g2 grow" style="gap:22px">
      <div class="card col" style="gap:8px;border-top:6px solid #7C3AED"><h3>From the small gray copy</h3><ul class="clean"><li><b>Edge</b>: Canny edge density</li><li><b>Night</b>: mean gray level</li><li><b>Blur</b>: variance of the Laplacian</li></ul><p>25% width × 25% height = <b>16× fewer pixels</b>, so these three cues are very cheap.</p></div>
      <div class="card col" style="gap:8px;border-top:6px solid #2563EB"><h3>From the previous frame’s tracked boxes</h3><ul class="clean"><li><b>Crowd</b>: how many boxes</li><li><b>Tiny</b>: how many are smaller than 32 × 32</li></ul><p>No ground truth is used — only the system’s own output, so SCI works on live video.</p></div>
    </div>
    <div class="callout">Box sizes for Tiny are measured on the <b>tracked boxes</b>, not on the shrunken gray copy.</div>
    <div class="tc">{EMP} <span class="origin empirical">25% scale · design choice</span></div>''')

# ============================================================== assemble
def deck(did, label, pages):
    return f'<div class="xdeck" id="{did}" data-label="{label}">\n' + '\n'.join(pages) + '\n</div>'

NEW_DECKS = '\n'.join([deck('x-iou', 'IoU and NMS', iou), deck('x-ap', 'Precision, recall and AP', ap), deck('x-fps', 'Speed', fps),
                       deck('x-bench', 'Detector benchmark', bench), deck('x-bytetrack', 'ByteTrack in depth', bt),
                       deck('x-eval', 'Evaluation in depth', ev), deck('x-ablation', 'Ablation in depth', ab),
                       deck('x-pareto', 'V2 multi-objective search', par)])

# replace short HOTA page with the full two-page version, renumber metric kickers
m = re.search(r'<section class="xpage" data-sec="1" data-title="Metrics HOTA">.*?</section>', h, re.S)
if not m: sys.exit('HOTA page not found')
h = h[:m.start()] + '\n'.join(hota) + h[m.end():]
for i, t in ((1, 'the example'), (2, 'MOTA'), (3, 'IDF1')):
    rep(f'Tracking metrics · {i} of 5 — {t}', f'Tracking metrics · {i} of 6 — {t}', f'metrics kicker {i}')
rep('Tracking metrics · 5 of 5 — IDS', 'Tracking metrics · 6 of 6 — IDS', 'metrics kicker IDS')

# append frame-preparation page to x-sci, renumber its kickers
m = re.search(r'(<section class="xpage" data-sec="4" data-title="SCI stabilise">.*?</section>)', h, re.S)
if not m: sys.exit('SCI stabilise not found')
h = h[:m.end()] + '\n' + sci_prep + h[m.end():]
rep('SCI calculation · 1 of 2', 'SCI calculation · 1 of 3', 'sci k1')
rep('SCI calculation · 2 of 2', 'SCI calculation · 2 of 3', 'sci k2')

# insert new decks at the end of the explanation stage
anchor = '</div>\n</div>\n<script src="assets/data/results.js"></script>'
rep(anchor, NEW_DECKS + '\n' + anchor, 'deck insert')

# buttons: add or extend data-explain on main slides
def add_btn(title, spec):
    global h
    pat = re.compile(r'(<section class="slide[^"]*"[^>]*?data-title="' + re.escape(title) + r'")( data-explain="([^"]*)")?')
    mm = list(pat.finditer(h))
    if len(mm) != 1: sys.exit(f'slide not found once: {title}')
    mo = mm[0]
    new = mo.group(1) + ' data-explain="' + ((mo.group(3) + ';') if mo.group(3) else '') + spec + '"'
    h = h[:mo.start()] + new + h[mo.end():]

rep('data-title="Identity switches" data-explain="x-metrics#5|Explain IDS"', 'data-title="Identity switches" data-explain="x-metrics#6|Explain IDS"', 'IDS button index')
for title, spec in [
    ('IoU vs NMS', 'x-iou|IoU and NMS Step by Step'),
    ('TP, FP, FN and TN', 'x-iou#2|When Is a Box Correct?'),
    ('Precision and recall', 'x-ap|Precision–Recall in Detail'),
    ('AP and mAP', 'x-ap#2|How AP Is Computed'),
    ('HOTA and FPS', 'x-fps|Explain FPS'),
    ('Detector benchmark comparison', 'x-bench|Reading the Benchmark'),
    ('Why YOLOv8n', 'x-bench|Reading the Benchmark'),
    ('Evolution of trackers', 'x-bytetrack|How ByteTrack Works'),
    ('ByteTrack baseline', 'x-bytetrack|How ByteTrack Works'),
    ('Smart Calibrator exact settings', 'x-bytetrack#4|Tracker Settings'),
    ('SCI from frame to score', 'x-sci#3|Frame Preparation'),
    ('Object classes evaluated', 'x-eval|Evaluation in Detail'),
    ('Ground-truth filtering rules', 'x-eval|Evaluation in Detail'),
    ('Evaluation protocol', 'x-eval#2|Evaluation in Detail'),
    ('Fair and attributable design', 'x-ablation|Ablation in Detail'),
    ('Original ablation table', 'x-ablation#2|Ablation in Detail'),
    ('What each component changed', 'x-ablation#3|Why No Single Winner?'),
    ('Stage 3: why V2', 'x-pareto|Multi-Objective Search'),
    ('V2 Pareto front', 'x-pareto#2|Pareto Front Explained'),
    ('Confidence threshold', 'x-controller|Explain Controller Logic'),
]:
    add_btn(title, spec)

rep('Tracking (v8)</title>', 'Tracking (v9)</title>', 'title')
IDX.write_text(h, encoding='utf-8')

# every explanation opens on its first page (user request)
JS = ROOT / 'script.js'
js = JS.read_text(encoding='utf-8')
old = "    if (xb) { var xt = xb.getAttribute('data-x').split('#'); openX(xt[0], xt[1] ? +xt[1] - 1 : 0); return; }"
if js.count(old) != 1: sys.exit('FAILED: openX call not found')
js = js.replace(old, "    if (xb) { openX(xb.getAttribute('data-x').split('#')[0], 0); return; }  /* always start at part 1 */")
JS.write_text(js, encoding='utf-8')

README.write_text('''# AC-MOT — Interactive Master's Presentation (v9: complete advanced explanations)

## Version 9

v9 is a copy of v8 (earlier versions unchanged). Main slides are unchanged (75). The optional explanation
system now covers every advanced topic: IoU computation and NMS algorithm, precision–recall and AP/mAP
(COCO), full HOTA (DetA + AssA worked example), FPS budget, detector benchmark columns, ByteTrack in depth
(Kalman prediction, two-round matching, track life cycle, every setting), evaluation in depth, the ablation
metric by metric, and the V2 multi-objective (Pareto) search — in addition to the v7 controller, SCI,
Optuna, V1 ranges, NMS-vs-tracker, metrics and V1-vs-V2 explanations. Build script: `build_v9.py`.

''' + README.read_text(encoding='utf-8'), encoding='utf-8')

decks = re.findall(r'<div class="xdeck" id="([^"]+)"', h)
pages = len(re.findall(r'<section class="xpage"', h))
btn_slides = len(re.findall(r'<section class="slide[^>]*data-explain=', h))
btns = sum(len(x.split(';')) for x in re.findall(r'data-explain="([^"]*)"', h))
print('main slides:', len(re.findall(r'<section class="slide', h)), '| decks:', len(decks), '| explanation pages:', pages, '| slides with buttons:', btn_slides, '| buttons:', btns)
