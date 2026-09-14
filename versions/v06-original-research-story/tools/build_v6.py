"""Rebuild the AC-MOT v6 deck: original AC-MOT research story, chronological.
Reads/writes ~/Desktop/acmot_interactive_presentation_v6/index.html (a copy of v5)."""
import re, pathlib, sys

P = pathlib.Path('/Users/ahmedgouda/Desktop/acmot_interactive_presentation_v6/index.html')
html = P.read_text(encoding='utf-8')
START_TAG = '<main class="stage" id="stage">'
s0 = html.index(START_TAG) + len(START_TAG)
s1 = html.index('</main>')
head, body, tail = html[:s0], html[s0:s1], html[s1:]

sections = re.findall(r'<section class="slide[^"]*"[^>]*>.*?</section>', body, flags=re.S)
def title_of(sec):
    return re.search(r'data-title="([^"]*)"', sec).group(1)
order = [(title_of(s), s) for s in sections]
titles = [t for t, _ in order]
assert len(titles) == len(set(titles)), 'duplicate titles'
print('v5 slides:', len(order))

# ------------------------------------------------------------------ small patches on kept slides
patched = {t: s for t, s in order}
def patch(title, old, new, count=1):
    s = patched[title]
    n = s.count(old)
    if n != count:
        sys.exit(f'PATCH FAILED on "{title}": found {n}x: {old[:70]}')
    patched[title] = s.replace(old, new)

patch('ID switches on MOT17',
      'ByteTrack is not the lowest-IDS tracker. We chose it for balance. Cutting ID switches is a goal of this work: tuning alone cuts them from <b data-bind="devAblation.rows.0.ids">2508</b> to <b data-bind="devAblation.rows.1.ids">2148</b> in our ablation.',
      'ByteTrack is not the lowest-IDS tracker. We chose it for balance, and reducing its ID switches became one goal of this work.')
patch('ID switches on MOT17', '<span class="prov p-dev">Our IDS numbers: development ablation</span>', '')
patch('Implementation of the calibrator',
      '<div class="callout good">This is why AC-MOT stays real-time: <b data-bind="devAblation.rows.3.fps" data-dec="2">28.86</b> FPS against <b data-bind="devAblation.rows.0.fps" data-dec="2">30.81</b> for the baseline in the development ablation.</div>',
      '<div class="callout good">Analysing a small gray copy only every 10 frames keeps the extra cost very low.</div>')
patch('Implementation of the calibrator',
      '<span class="prov p-dev">FPS: development ablation · smoothing chart: illustrative readings</span>',
      '<span class="prov p-illus">Smoothing chart: illustrative readings · timing from development runs</span>')
patch('Evaluation protocol',
      '<div class="note"><b>Update:</b> the early ablation used a quick HOTA estimate (HOTA*). All final results use the official TrackEval tool, pinned to one exact version.</div>',
      '<div class="note">All results are computed with <b>TrackEval</b>, pinned to one exact version, with the same rules for every system.</div>')
patch('Validation builds it, test judges it',
      '<p>Sweeps, temporal grid, 50 Optuna trials. Every setting is chosen and frozen here.</p>',
      '<p>All 50 V1 Optuna trials run here. Every setting is chosen and frozen here.</p>')
patch('Validation builds it, test judges it',
      '<h3>What we do not mix</h3><p>Stage 1 numbers (A0–A3) use an older evaluator, so we never compare them directly with these.</p>',
      '<h3>What we do not mix</h3><p>Ablation, validation and test-set numbers come from different runs, so they are never put in one table.</p>')
patch('Same frames, different control', '>A0 vs A3 · uav0000249<', '>Clip 1 · uav0000249<')
patch('Same frames, different control', '>A0 vs A3 · uav0000188 (tiny objects)<', '>Clip 2 · uav0000188 (tiny objects)<')
patch('Same frames, different control', '>Baseline vs Full AC-MOT · uav0000249 <span class="newtag">NEW</span><', '>Clip 3 · uav0000249 · final system<')
patch('Same frames, different control', 'data-secname="VI · Results"', 'data-secname="VI · Ablation"')
for t in ('Next step: U2MOT', 'U2MOT reproduction status'):
    patch(t, 'data-sec="9" data-secname="VIII · Conclusion"', 'data-sec="8" data-secname="VIII · Transfer"')
    patch(t, 'Section VIII · Next step', 'Section VIII · Transfer')
patch('Directions for future work', 'data-secname="VIII · Conclusion"', 'data-secname="IX · Conclusion"')
patch('Directions for future work', 'Section VIII · Future work', 'Section IX · Future work')

# ------------------------------------------------------------------ new / rewritten slides
N = {}

N['Outline'] = r'''<section class="slide" data-sec="0" data-secname="Title" data-title="Outline">
  <header class="s-head"><div class="kicker">Presentation structure</div><h2>Outline</h2></header>
  <div class="s-body">
    <div class="ol" style="grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,1fr);gap:14px">
      <button class="ol-card" data-sec="1" data-goto="sec-1"><span class="n">I</span><span><h3>Introduction and Metrics</h3><p>Detection, tracking and how we score them</p></span></button>
      <button class="ol-card" data-sec="2" data-goto="sec-2"><span class="n">II</span><span><h3>Related Work</h3><p>Detectors, trackers and datasets</p></span></button>
      <button class="ol-card" data-sec="3" data-goto="sec-3"><span class="n">III</span><span><h3>The Problem</h3><p>Scenes change, detector settings do not</p></span></button>
      <button class="ol-card" data-sec="4" data-goto="sec-4"><span class="n">IV</span><span><h3>An Adaptive Control Layer</h3><p>Scene cues, SCI and the controller</p></span></button>
      <button class="ol-card" data-sec="5" data-goto="sec-5"><span class="n">V</span><span><h3>Experimental Setup</h3><p>Data and scoring rules</p></span></button>
      <button class="ol-card" data-sec="6" data-goto="sec-6"><span class="n">VI</span><span><h3>Original Ablation</h3><p>What each component changes</p></span></button>
      <button class="ol-card" data-sec="7" data-goto="sec-7"><span class="n">VII</span><span><h3>Optimization and Results</h3><p>Optuna V1, test set, V2 and UAVDT</p></span></button>
      <button class="ol-card" data-sec="8" data-goto="sec-8"><span class="n">VIII</span><span><h3>Transfer</h3><p>A published strong MOT pipeline</p></span></button>
      <button class="ol-card" data-sec="9" data-goto="sec-9"><span class="n">IX</span><span><h3>Contributions and Conclusion</h3><p>What the work delivers</p></span></button>
    </div>
  </div>
  <aside class="notes"><p><b>Say:</b> "The story goes in the order the work happened: the problem, the first heuristic design, the ablation, the optimization, the test results and a second dataset."</p><p><b>Tip:</b> click a card to jump to that part.</p></aside>
</section>'''

N['Section III'] = r'''<section class="slide divider" id="sec-3" data-sec="3" data-secname="III · Problem" data-title="Section III">
  <div class="dv-bg"><img src="assets/figures/image9.png" alt=""></div>
  <div class="dv-text"><div class="dv-num">III</div><div class="dv-kicker">Section III</div>
    <h1>The Problem: Not Every Frame Is Equally Hard</h1>
    <p>Aerial scenes keep changing, but a normal tracking pipeline uses one fixed detector configuration for every frame.</p></div>
  <aside class="notes"><p><b>Say:</b> "Now the problem that started this work."</p></aside>
</section>'''

N['One fixed threshold'] = r'''<section class="slide" data-sec="3" data-secname="III · Problem" data-title="One fixed threshold">
  <header class="s-head"><div class="kicker">Section III · The problem</div><h2>Aerial Scenes Are Not Equally Difficult</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>In the same drone video some frames are <b>easy</b> and some are <b>hard</b> — yet a normal tracking-by-detection pipeline uses <b>one fixed detector configuration</b> for all of them.</p></div>
    <div class="g2 grow" style="gap:22px">
      <div class="card col" style="border-top:6px solid var(--good);gap:10px"><h3 class="good">Easy frames</h3>
        <div class="row grow" style="gap:18px"><div class="img zoomable" style="flex:0 0 330px"><img src="assets/figures/image1.png" alt="Easy frame"></div>
          <ul class="clean v"><li><b>sparse</b> — few objects</li><li><b>clear</b> background</li><li><b>well illuminated</b></li><li><b>larger</b> objects</li></ul></div></div>
      <div class="card col" style="border-top:6px solid var(--bad);gap:10px"><h3 class="bad">Hard frames</h3>
        <div class="row grow" style="gap:18px"><div class="img zoomable" style="flex:0 0 330px"><img src="assets/figures/image20.jpeg" alt="Hard frame"></div>
          <ul class="clean x"><li><b>crowded</b></li><li><b>tiny</b> objects</li><li>high <b>edge complexity</b></li><li><b>low light</b></li><li><b>blurred</b></li></ul></div></div>
    </div>
    <div class="card flat row ac jb" style="padding:12px 22px"><span class="strong">A normal pipeline gives every frame the same settings →</span><span class="pills"><span class="pill">one confidence threshold</span><span class="pill">one NMS IoU</span><span class="pill">one input size</span></span></div>
  </div>
  <aside class="notes"><p><b>Say:</b> "Some frames are sparse, clear, bright, with larger objects. Others are crowded, tiny, busy, dark or blurred. Yet the detector runs with exactly the same settings on all of them."</p></aside>
</section>'''

N['The main question'] = r'''<section class="slide" data-sec="3" data-secname="III · Problem" data-title="The main question">
  <header class="s-head"><div class="kicker">Section III · Research question</div><h2>The Main Question</h2></header>
  <div class="s-body col center" style="gap:34px">
    <div class="card sec" style="padding:36px 52px;max-width:1320px"><div class="tag">Our question</div>
      <p class="lead mt16" style="font-size:48px;line-height:1.25;color:var(--ink)">“Why should the detector use the <b>same operating point</b> when <b>scene difficulty changes</b> over time?”</p></div>
    <p class="tc" style="font-size:28px;color:var(--ink2);max-width:1200px">The detector’s <b>operating point</b> = its settings, such as the confidence threshold, the NMS IoU and the input size.</p>
  </div>
  <aside class="notes"><p><b>Say:</b> "This is the question behind the thesis: when the scene becomes harder or easier, why should the detector stay at the same operating point?"</p></aside>
</section>'''

N['Section IV'] = r'''<section class="slide divider" id="sec-4" data-sec="4" data-secname="IV · AC-MOT" data-title="Section IV">
  <div class="dv-bg"><img src="assets/figures/image22.png" alt=""></div>
  <div class="dv-text"><div class="dv-num">IV</div><div class="dv-kicker">Section IV</div>
    <h1>AC-MOT: An Adaptive Control Layer</h1>
    <p>Not a new detector and not a new tracker — a small control layer that reads scene difficulty and changes the detector’s settings.</p></div>
  <aside class="notes"><p><b>Say:</b> "Now our answer: AC-MOT."</p></aside>
</section>'''

N['What we add'] = r'''<section class="slide" data-sec="4" data-secname="IV · AC-MOT" data-title="What we add">
  <header class="s-head"><div class="kicker">Section IV · The proposed framework</div><h2>AC-MOT: A Control Layer, Not a New Detector or Tracker</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>AC-MOT <b>reads how hard each scene is</b> and <b>adapts the detector-side parameters</b> to match. The detector and the tracker themselves stay <b>unchanged</b>.</p></div>
    <div class="flow" style="flex-wrap:nowrap">
      <div class="node io frag" style="width:140px">Frame</div><div class="arr sm frag"></div>
      <div class="node ad frag" style="width:190px">Scene Analyzer<small>5 cheap cues</small><span class="adapt">NEW</span></div><div class="arr sm frag"></div>
      <div class="node ad frag" style="width:170px">SCI<small>difficulty 0 → 1</small><span class="adapt">NEW</span></div><div class="arr sm frag"></div>
      <div class="node ad frag" style="width:210px">Adaptive Controller<small>chooses settings</small><span class="adapt">NEW</span></div><div class="arr sm frag"></div>
      <div class="node fx frag" style="width:170px">Detector<small>YOLOv8n · unchanged</small></div><div class="arr sm frag"></div>
      <div class="node fx frag" style="width:170px">Tracker<small>ByteTrack · unchanged</small></div><div class="arr sm frag"></div>
      <div class="node good frag" style="width:130px">Tracks</div>
    </div>
    <div class="g3 grow" style="gap:20px">
      <div class="card" style="border-left:6px solid #4F46E5"><h3>What is new</h3><p>The Scene Analyzer, the Scene Complexity Index and the Adaptive Controller.</p></div>
      <div class="card" style="border-left:6px solid #64748B"><h3>What stays the same</h3><p>The detector weights and the tracker. No retraining.</p></div>
      <div class="card" style="border-left:6px solid var(--good)"><h3>What adapts per scene</h3><p>Detector-side parameters, such as the confidence threshold, the NMS IoU and the input size.</p></div>
    </div>
  </div>
  <aside class="notes"><p><b>How to present:</b> press → to reveal the pipeline step by step.</p><p><b>Say:</b> "AC-MOT is not a detector and not a tracker. It is a control layer: the Scene Analyzer measures the frame, the SCI summarises how hard it is, and the controller chooses the detector settings."</p></aside>
</section>'''

N['Step 1: measure scene complexity'] = r'''<section class="slide" data-sec="4" data-secname="IV · AC-MOT" data-title="Step 1: measure scene complexity">
  <header class="s-head"><div class="kicker">Section IV · Scene Analyzer</div><h2>The Five SCI Cues</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>The Scene Analyzer measures <b>five cheap cues</b>. Three are <b>continuous</b> (0 → 1) and two are <b>binary</b> (0 or 1).</p></div>
    <table class="tbl" style="font-size:24px">
      <tr><th style="text-align:left">Cue</th><th style="text-align:left">Type</th><th style="text-align:left">Definition</th><th style="text-align:left">Built on</th></tr>
      <tr><td class="strong">Crowd density</td><td style="text-align:left">continuous</td><td style="text-align:left" class="fcell">Crowd = min(previous tracked boxes ÷ 30, 1)</td><td style="text-align:left">box count from the previous frame</td></tr>
      <tr><td class="strong">Tiny-object proportion</td><td style="text-align:left">continuous</td><td style="text-align:left" class="fcell">Tiny = tracked boxes smaller than 32×32 ÷ all tracked boxes</td><td style="text-align:left">COCO small-object size [1]</td></tr>
      <tr><td class="strong">Edge complexity</td><td style="text-align:left">continuous</td><td style="text-align:left" class="fcell">Edge = min(edge density ÷ 0.14, 1)</td><td style="text-align:left">grayscale image + Canny edges [2]</td></tr>
      <tr><td class="strong">Low light</td><td style="text-align:left">binary</td><td style="text-align:left" class="fcell">Night = 1 if mean grayscale &lt; 80, else 0</td><td style="text-align:left">mean grayscale brightness</td></tr>
      <tr><td class="strong">Blur</td><td style="text-align:left">binary</td><td style="text-align:left" class="fcell">Blur = 1 if Laplacian variance &lt; 180, else 0</td><td style="text-align:left">variance of the Laplacian [3]</td></tr>
    </table>
    <div class="callout warn"><b>30, 32×32, 0.14, 80 and 180 are empirical design constants.</b> They define the cues and were fixed by design — <b>Optuna did not choose them</b>.</div>
    <div class="cap">[1] Lin et al., “Microsoft COCO,” ECCV 2014 (detection evaluation: small = area &lt; 32²) · [2] J. Canny, IEEE TPAMI 1986 · [3] Pech-Pacheco et al., ICPR 2000</div>
  </div>
  <footer class="s-foot"><span class="prov p-hist">Original SCI cue definitions · kept fixed in every later study</span></footer>
  <aside class="notes"><p><b>Say:</b> "Crowd, Tiny and Edge are continuous between 0 and 1; Night and Blur are simple on/off flags."</p>
    <p><b>If asked “why 30?”:</b> "It is an empirical normalisation ceiling: it turns the object count into a value between 0 and 1, and 30 or more objects already counts as fully crowded. It is a design constant, not a universal threshold."</p>
    <p><b>If asked about 32×32:</b> "It follows the COCO definition of a small object."</p>
    <p><b>If asked about 0.14, 80 and 180:</b> "Canny edges, mean brightness and the variance of the Laplacian are standard measurements. The exact limits are empirical design constants, and they stayed fixed — Optuna did not tune them."</p></aside>
</section>'''

N['Initial SCI'] = r'''<section class="slide" data-sec="4" data-secname="IV · AC-MOT" data-title="Initial SCI">
  <header class="s-head"><div class="kicker">Section IV · First heuristic design</div><h2>The Initial SCI: Hand-Designed Weights</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>The first AC-MOT design mixed the five cues with <b>hand-picked weights</b> into one number, the SCI, and then kept that number <b>stable over time</b>.</p></div>
    <div class="card tc" style="padding:14px 20px"><div class="formula" style="font-size:38px">SCI = 0.30·Crowd + 0.30·Tiny + 0.20·Edge + 0.10·Night + 0.05·Blur</div></div>
    <div class="row grow" style="gap:24px">
      <table class="tbl" style="font-size:26px;flex:0 0 460px">
        <tr><th style="text-align:left">Cue</th><th>Initial weight</th></tr>
        <tr><td>Crowd</td><td class="strong">0.30</td></tr>
        <tr><td>Tiny</td><td class="strong">0.30</td></tr>
        <tr><td>Edge</td><td class="strong">0.20</td></tr>
        <tr><td>Night</td><td class="strong">0.10</td></tr>
        <tr><td>Blur</td><td class="strong">0.05</td></tr>
      </table>
      <div class="col grow" style="gap:14px"><div class="ex-label">Then, to keep SCI stable</div>
        <div class="flow" style="justify-content:flex-start">
          <div class="node ad" style="width:220px">Clip<small>to [0, 1]</small></div><div class="arr"></div>
          <div class="node ad" style="width:260px">Smooth<small>window = 7 readings</small></div><div class="arr"></div>
          <div class="node ad" style="width:260px">Analyse<small>every 10 frames</small></div>
        </div>
        <div class="callout"><b>This was the first heuristic AC-MOT design.</b> The weights were chosen by hand — they even add up to 0.95, not 1.</div>
      </div>
    </div>
  </div>
  <footer class="s-foot"><span class="prov p-hist">Initial heuristic SCI · window 7 · analysis every 10 frames</span></footer>
  <aside class="notes"><p><b>Say:</b> "The first version simply weighted the cues: crowd and tiny most, then edges, then night and blur. The result is clipped to 0–1, averaged over the last 7 readings, and computed every 10 frames."</p><p><b>If asked why these weights:</b> "They were initial heuristic weights — which is exactly why we later optimised the controller on validation data."</p></aside>
</section>'''

N['Fair and attributable design'] = r'''<section class="slide" data-sec="5" data-secname="V · Setup" data-title="Fair and attributable design">
  <header class="s-head"><div class="kicker">Section V · Protocol</div><h2>A Fair Ablation Design</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>Each ablation stage switches on a <b>different part</b> of AC-MOT while keeping the <b>same detector</b> — so every score change can be traced to that part.</p></div>
    <div class="g5 grow" style="gap:14px">
      <div class="card" style="border-top:6px solid #94A3B8"><h3>OLD-A0</h3><p>Baseline</p></div>
      <div class="card" style="border-top:6px solid #60A5FA"><h3>OLD-A1</h3><p>Tuned ByteTrack</p></div>
      <div class="card" style="border-top:6px solid #818CF8"><h3>OLD-A2</h3><p>Adaptive confidence + NMS</p></div>
      <div class="card" style="border-top:6px solid #F59E0B"><h3>OLD-A2R</h3><p>Adaptive resolution only</p></div>
      <div class="card" style="border-top:6px solid #4F46E5"><h3>OLD-A3</h3><p>Full AC-MOT</p></div>
    </div>
    <div class="callout good">All stages use the <b>same YOLOv8n detector</b>, with no retraining. The ablation is a <b>separate study</b> from the final test-set comparison.</div>
  </div>
  <aside class="notes"><p><b>Say:</b> "We built AC-MOT in stages and measured each one: tuned tracking, adaptive confidence and NMS, adaptive resolution alone, and the full system."</p></aside>
</section>'''

N['Section VI'] = r'''<section class="slide divider" id="sec-6" data-sec="6" data-secname="VI · Ablation" data-title="Section VI">
  <div class="dv-bg"><img src="assets/figures/image26.jpeg" alt=""></div>
  <div class="dv-text"><div class="dv-num">VI</div><div class="dv-kicker">Section VI</div>
    <h1>The Original Ablation Study</h1>
    <p>Which part of the first AC-MOT design improves which part of tracking? This study is separate from the final test-set comparison.</p></div>
  <aside class="notes"><p><b>Say:</b> "First, the component ablation of the original AC-MOT."</p></aside>
</section>'''

N['Original ablation table'] = r'''<section class="slide" data-sec="6" data-secname="VI · Ablation" data-title="Original ablation table">
  <header class="s-head"><div class="kicker">Section VI · Ablation study</div><h2>Original AC-MOT Ablation</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>Different adaptive parts improve <b>different aspects</b> of tracking. <b>No single stage is best on every metric.</b></p></div>
    <table class="tbl" style="font-size:27px">
      <tr><th style="text-align:left">Stage</th><th style="text-align:left">Description</th><th>MOTA ↑</th><th>HOTA ↑</th><th>IDF1 ↑</th><th>IDS ↓</th><th>FPS ↑</th></tr>
      <tr><td>OLD-A0</td><td style="text-align:left">Baseline</td><td>17.633</td><td>29.837</td><td>30.892</td><td>283</td><td>44.09</td></tr>
      <tr><td>OLD-A1</td><td style="text-align:left">Tuned ByteTrack</td><td>17.802</td><td>30.864</td><td>32.854</td><td>217</td><td class="best">44.51</td></tr>
      <tr><td>OLD-A2</td><td style="text-align:left">Adaptive Confidence + NMS</td><td>17.636</td><td>31.384</td><td>33.727</td><td class="best">210</td><td>40.65</td></tr>
      <tr><td>OLD-A2R</td><td style="text-align:left">Adaptive Resolution Only</td><td class="best">18.425</td><td>32.446</td><td>35.669</td><td>241</td><td>39.56</td></tr>
      <tr class="sel"><td>OLD-A3</td><td style="text-align:left">Full AC-MOT</td><td>18.165</td><td class="best">33.064</td><td class="best">36.296</td><td>271</td><td>37.96</td></tr>
    </table>
    <div class="note">Green = best value in each column. All stages use the same detector.</div>
  </div>
  <footer class="s-foot"><span class="prov p-dev">Ablation study · original AC-MOT components · not the final test set</span></footer>
  <aside class="notes"><p><b>Say:</b> "Here is the original ablation. Read it column by column: the best MOTA, the best HOTA and IDF1, and the fewest ID switches come from different stages."</p><p><b>Do not say</b> that the full system wins every metric — it does not.</p></aside>
</section>'''

N['What each component changed'] = r'''<section class="slide" data-sec="6" data-secname="VI · Ablation" data-title="What each component changed">
  <header class="s-head"><div class="kicker">Section VI · Ablation study</div><h2>What Each Component Changed</h2></header>
  <div class="s-body col">
    <div class="row grow" style="gap:18px">
      <div class="card" style="flex:1.6;padding:10px 14px"><div class="chart zoomable" data-chart="oab-quality"></div></div>
      <div class="card grow" style="padding:10px 14px"><div class="chart zoomable" data-chart="oab-ids"></div></div>
    </div>
    <div class="g4" style="gap:14px">
      <div class="card" style="border-left:6px solid #60A5FA"><h3>A1 · tuned tracker</h3><p>Better association: HOTA and IDF1 up, IDS 283 → 217.</p></div>
      <div class="card" style="border-left:6px solid #818CF8"><h3>A2 · confidence + NMS</h3><p><b>Lowest IDS</b> in the ablation: 210.</p></div>
      <div class="card" style="border-left:6px solid #F59E0B"><h3>A2R · resolution only</h3><p><b>Highest MOTA</b>: 18.425.</p></div>
      <div class="card" style="border-left:6px solid #4F46E5"><h3>A3 · full AC-MOT</h3><p><b>Highest HOTA and IDF1</b> — not the best MOTA or IDS.</p></div>
    </div>
  </div>
  <footer class="s-foot"><span class="prov p-dev">Ablation study · original AC-MOT components · not the final test set</span></footer>
  <aside class="notes"><p><b>Say:</b> "Tuning the tracker improves association and cuts ID switches. Adaptive confidence and NMS gives the fewest ID switches. Adaptive resolution alone gives the highest MOTA. The full system gives the highest HOTA and IDF1. Each part helps a different aspect."</p></aside>
</section>'''

N['Section VII'] = r'''<section class="slide divider" id="sec-7" data-sec="7" data-secname="VII · Optimization" data-title="Section VII">
  <div class="dv-bg"><img src="assets/figures/image23.jpeg" alt=""></div>
  <div class="dv-text"><div class="dv-num">VII</div><div class="dv-kicker">Section VII</div>
    <h1>Optimizing AC-MOT With Validation Data</h1>
    <p>From hand-picked values to a validation-driven search: Optuna V1, the test-set comparison, the V2 trade-off and UAVDT.</p></div>
  <aside class="notes"><p><b>Say:</b> "The first design worked, but many of its values were chosen by hand. Next, we let validation data choose them."</p></aside>
</section>'''

N['Why Optuna'] = r'''<section class="slide" data-sec="7" data-secname="VII · Optimization" data-title="Why Optuna">
  <header class="s-head"><div class="kicker">Section VII · Motivation</div><h2>Why Optuna Was Introduced</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>The initial SCI and controller were full of <b>manually selected values</b>. We wanted <b>validation performance</b> — not our guesses — to choose them.</p></div>
    <div class="g2 grow" style="gap:22px">
      <div class="card col" style="border-left:6px solid var(--bad);gap:8px"><h3 class="bad">Chosen by hand in the first design</h3>
        <ul class="clean x"><li>the five SCI weights</li><li>the SCI limits between easy and hard scenes</li><li>the detector settings for each kind of scene</li></ul></div>
      <div class="card col" style="border-left:6px solid var(--good);gap:8px"><h3 class="good">The new question</h3>
        <p class="lead" style="font-size:30px">“Can the relationship between <b>scene complexity</b> and <b>detector settings</b> be optimized from <b>validation performance</b> instead of being fully hand-designed?”</p></div>
    </div>
    <div class="card flat"><div class="ex-label">The tool</div><p><b>Optuna</b> with the <b>TPE</b> sampler: a <b>sequential, Bayesian hyperparameter optimization</b> method. It is <b>not an AI model</b> and trains nothing — it proposes settings, reads the score, and proposes better settings next.</p></div>
  </div>
  <footer class="s-foot"><span class="prov p-pub">Optuna (Akiba et al., KDD 2019) · TPE (Bergstra et al., NIPS 2011)</span></footer>
  <aside class="notes"><p><b>Say:</b> "Our first design had many hand-picked numbers. So we asked whether validation performance could choose them. We used Optuna with TPE, a sequential Bayesian optimizer."</p><p><b>If asked “is Optuna AI?”:</b> "No. It is a search method; it trains no model."</p></aside>
</section>'''

N['What Optuna changed in V1'] = r'''<section class="slide" data-sec="7" data-secname="VII · Optimization" data-title="What Optuna changed in V1">
  <header class="s-head"><div class="kicker">Section VII · V1 search space</div><h2>What Optuna Changed in V1 — and What It Did Not</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>The <b>cue definitions stayed fixed</b>. Optuna jointly searched the <b>controller configuration</b> — so <b>each trial was one complete AC-MOT configuration</b>.</p></div>
    <div class="g2 grow" style="gap:22px">
      <div class="card col" style="border-top:6px solid #64748B;gap:6px"><h3>Fixed — not changed by Optuna</h3>
        <table class="tbl" style="font-size:24px">
          <tr><td>crowd divisor</td><td>30</td></tr>
          <tr><td>tiny threshold</td><td>32 × 32</td></tr>
          <tr><td>edge normalization divisor</td><td>0.14</td></tr>
          <tr><td>low-light threshold</td><td>80</td></tr>
          <tr><td>blur threshold</td><td>180</td></tr>
          <tr><td>smoothing window</td><td>7</td></tr>
          <tr><td>analysis stride</td><td>10</td></tr>
        </table></div>
      <div class="card col" style="border-top:6px solid #7C3AED;gap:6px"><h3>Searched jointly by Optuna</h3>
        <table class="tbl" style="font-size:24px">
          <tr><td>SCI weights</td><td style="text-align:left">w_crowd · w_tiny · w_edge · w_night · w_blur</td></tr>
          <tr><td>SCI regime boundaries</td><td style="text-align:left">threshold_mid · threshold_high</td></tr>
          <tr><td>detector operating settings</td><td style="text-align:left">confidence settings · NMS IoU settings</td></tr>
        </table>
        <div class="callout mt8">One trial = one full set of these values = <b>one complete AC-MOT configuration</b>.</div></div>
    </div>
  </div>
  <footer class="s-foot"><span class="prov p-val">V1 study design · validation only</span></footer>
  <aside class="notes"><p><b>Say:</b> "Be clear about this: Optuna did not touch how the cues are measured. The divisors, thresholds, window and stride stayed fixed. It searched the weights, the regime boundaries and the detector settings — all together."</p></aside>
</section>'''

N['One Optuna trial'] = r'''<section class="slide" data-sec="7" data-secname="VII · Optimization" data-title="One Optuna trial">
  <header class="s-head"><div class="kicker">Section VII · How the search works</div><h2>What Happens in One Optuna Trial</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>One trial = <b>run the complete pipeline</b> on the validation videos with one configuration, then <b>score it</b>. TPE uses earlier trials to steer later trials toward <b>more promising regions</b>.</p></div>
    <div class="flow frag" style="flex-wrap:nowrap">
      <div class="node ad" style="width:230px">1 · Optuna proposes<small>parameters</small></div><div class="arr sm"></div>
      <div class="node" style="width:250px">2 · Run the complete<small>validation pipeline</small></div><div class="arr sm"></div>
      <div class="node" style="width:260px">3 · Compute SCI<small>for every analysed frame</small></div><div class="arr sm"></div>
      <div class="node" style="width:260px">4 · Classify the frame<small>Easy / Medium / Hard</small></div>
    </div>
    <div class="flow frag" style="flex-wrap:nowrap">
      <div class="node ad" style="width:270px">8 · Return the result<small>Optuna proposes the next one</small></div><div class="arr sm" style="transform:scaleX(-1)"></div>
      <div class="node" style="width:270px">7 · Evaluate<small>MOTA · HOTA · IDF1 · IDS · FPS</small></div><div class="arr sm" style="transform:scaleX(-1)"></div>
      <div class="node" style="width:220px">6 · Detect and track</div><div class="arr sm" style="transform:scaleX(-1)"></div>
      <div class="node" style="width:260px">5 · Apply that regime’s<small>detector parameters</small></div>
    </div>
    <div class="card flat frag"><div class="ex-label">The link is indirect</div>
      <div class="flow mt8" style="flex-wrap:wrap;row-gap:8px">
        <span class="pill sec">SCI weights</span><div class="arr sm"></div><span class="pill sec">SCI values</span><div class="arr sm"></div><span class="pill sec">Easy / Medium / Hard</span><div class="arr sm"></div><span class="pill sec">detector parameters</span><div class="arr sm"></div><span class="pill sec">detections</span><div class="arr sm"></div><span class="pill sec">tracking</span><div class="arr sm"></div><span class="pill good">final metrics</span>
      </div>
      <p class="mt8">Optuna never learns a rule like “SCI = X means MOTA = Y”. It only sees which complete configuration scored better.</p></div>
  </div>
  <footer class="s-foot"><span class="prov p-illus">Illustration of one V1 trial</span></footer>
  <aside class="notes"><p><b>How to present:</b> press → to show the loop, then the indirect chain.</p><p><b>Say:</b> "Optuna proposes one configuration. We run the whole validation pipeline with it: SCI for every analysed frame, easy, medium or hard, the matching detector settings, detection, tracking, and the metrics. The score goes back to Optuna, and TPE uses it to choose the next configuration."</p></aside>
</section>'''

N['V1 Trial 24 weights'] = r'''<section class="slide" data-sec="7" data-secname="VII · Optimization" data-title="V1 Trial 24 weights">
  <header class="s-head"><div class="kicker">Section VII · V1 selected configuration</div><h2>V1 Trial 24: The Selected SCI Weights</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>The selected V1 configuration trusts <b>edge complexity most</b> and <b>low light least</b> — very different from the initial hand-designed weights.</p></div>
    <div class="row grow" style="gap:20px">
      <div class="card grow" style="padding:10px 14px"><div class="chart zoomable" data-chart="weights-v1"></div></div>
      <table class="tbl" style="font-size:24px;flex:0 0 640px">
        <tr><th style="text-align:left">Cue</th><th>Initial</th><th>V1 Trial 24</th></tr>
        <tr><td>Crowd</td><td>0.30</td><td>0.12949277455301997</td></tr>
        <tr><td>Tiny</td><td>0.30</td><td>0.22174766876599927</td></tr>
        <tr><td>Edge</td><td>0.20</td><td class="best">0.43371337893805056</td></tr>
        <tr><td>Night</td><td>0.10</td><td>0.05355765312756694</td></tr>
        <tr><td>Blur</td><td>0.05</td><td>0.16148852461536325</td></tr>
      </table>
    </div>
  </div>
  <footer class="s-foot"><span class="prov p-hist">Initial heuristic weights</span><span class="prov p-val">V1 Trial 24 · selected on validation</span></footer>
  <aside class="notes"><p><b>Say:</b> "These are the exact weights of the selected configuration. Edges became the strongest cue, night the weakest."</p></aside>
</section>'''

N['V1 Trial 24 regimes'] = r'''<section class="slide" data-sec="7" data-secname="VII · Optimization" data-title="V1 Trial 24 regimes">
  <header class="s-head"><div class="kicker">Section VII · V1 selected configuration</div><h2>V1 Trial 24: Easy, Medium and Hard Scenes</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>The SCI ranges were <b>not set by hand after looking at SCI values</b>. They <b>emerged from the joint Optuna optimization</b>, together with the detector parameters.</p></div>
    <svg viewBox="0 0 1400 112" width="100%" height="112"><g font-family="Inter,Helvetica" font-weight="800">
      <rect x="20" y="14" width="184" height="50" rx="6" fill="#DCFCE7" stroke="#16A34A" stroke-width="3"/>
      <rect x="204" y="14" width="207" height="50" rx="6" fill="#FEF3C7" stroke="#D97706" stroke-width="3"/>
      <rect x="411" y="14" width="969" height="50" rx="6" fill="#FEE2E2" stroke="#DC2626" stroke-width="3"/>
      <text x="112" y="48" font-size="26" fill="#14532D" text-anchor="middle">Easy</text>
      <text x="307" y="48" font-size="26" fill="#92400E" text-anchor="middle">Medium</text>
      <text x="895" y="48" font-size="26" fill="#7F1D1D" text-anchor="middle">Hard</text>
      <g font-size="22" fill="#334155" text-anchor="middle"><text x="30" y="98">0</text><text x="204" y="98">0.13535</text><text x="411" y="98">0.28729</text><text x="1368" y="98">1</text></g>
      <text x="895" y="98" font-size="22" fill="#64748B" text-anchor="middle">SCI →</text></g></svg>
    <div class="g2 grow" style="gap:22px">
      <table class="tbl" style="font-size:24px">
        <tr><th style="text-align:left">Regime</th><th style="text-align:left">SCI range</th></tr>
        <tr><td class="good strong">Easy</td><td style="text-align:left">SCI &lt; 0.13535</td></tr>
        <tr><td class="warn strong">Medium</td><td style="text-align:left">0.13535 ≤ SCI &lt; 0.28729</td></tr>
        <tr><td class="bad strong">Hard</td><td style="text-align:left">SCI ≥ 0.28729</td></tr>
        <tr><td class="muted">threshold_mid</td><td style="text-align:left">0.13534938199219218</td></tr>
        <tr><td class="muted">threshold_high</td><td style="text-align:left">0.28728676236279177</td></tr>
      </table>
      <table class="tbl" style="font-size:24px">
        <tr><th style="text-align:left">Detector parameter</th><th>Value</th></tr>
        <tr><td>conf_easy</td><td>0.30</td></tr>
        <tr><td>conf_hard</td><td>0.40</td></tr>
        <tr><td>nms_easy</td><td>0.35</td></tr>
        <tr><td>nms_hard</td><td>0.35</td></tr>
      </table>
    </div>
  </div>
  <footer class="s-foot"><span class="prov p-val">V1 Trial 24 · selected on validation</span></footer>
  <aside class="notes"><p><b>Say:</b> "The boundaries between easy, medium and hard were searched together with the weights and detector settings. We did not draw them by hand after looking at SCI values."</p></aside>
</section>'''

N['Step 4 result: Trial 24'] = r'''<section class="slide" data-sec="7" data-secname="VII · Optimization" data-title="Step 4 result: Trial 24">
  <header class="s-head"><div class="kicker">Section VII · Validation result</div><h2>V1 Selection on the Validation Set</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p><b>Trial 24</b> was selected by the V1 <b>validation-selection rules</b>, and then frozen before the test-set run.</p></div>
    <div class="g5" style="gap:14px">
      <div class="kpi"><div class="l">MOTA</div><div class="v">23.0381</div></div>
      <div class="kpi"><div class="l">HOTA</div><div class="v">36.1102</div></div>
      <div class="kpi"><div class="l">IDF1</div><div class="v">40.7578</div></div>
      <div class="kpi hi"><div class="l">IDS</div><div class="v">270</div></div>
      <div class="kpi hi"><div class="l">FPS</div><div class="v">37.1686</div></div>
    </div>
    <div class="g2 grow" style="gap:22px">
      <div class="card sec"><h3>V1 selection rules</h3><ul class="clean"><li>FPS must be at least 25</li><li>IDS must not exceed 271 — the original full AC-MOT (OLD-A3)</li><li>among the trials that pass, take the highest MOTA</li></ul></div>
      <div class="card"><h3>Validation, not test</h3><p>These numbers come from the <b>validation split</b> used for selection. The test-set comparison follows on the next slides.</p></div>
    </div>
  </div>
  <footer class="s-foot"><span class="prov p-val">Validation result · VisDrone2019-MOT-val · 7 sequences · V1 Trial 24</span></footer>
  <aside class="notes"><p><b>Say:</b> "On the validation set, Trial 24 passed both rules and had the highest MOTA among the trials that passed, so it was selected and frozen."</p></aside>
</section>'''

N['Final test-set comparison'] = r'''<section class="slide" data-sec="7" data-secname="VII · Optimization" data-title="Final test-set comparison">
  <header class="s-head"><div class="kicker">Section VII · Test set</div><h2>Final Test-Set Comparison</h2></header>
  <div class="s-body col">
    <div class="row grow" style="gap:16px">
      <div class="card" style="flex:1.6;padding:10px 14px"><div class="chart zoomable" data-chart="td4-quality"></div></div>
      <div class="card grow" style="padding:10px 14px"><div class="chart zoomable" data-chart="td-ids"></div></div>
      <div class="card grow" style="padding:10px 14px"><div class="chart zoomable" data-chart="td-fps"></div></div>
    </div>
    <table class="tbl" style="font-size:25px">
      <tr><th style="text-align:left">System</th><th>MOTA ↑</th><th>HOTA ↑</th><th>IDF1 ↑</th><th>IDS ↓</th><th>FPS ↑</th></tr>
      <tr><td>Baseline</td><td>19.729</td><td>28.430</td><td>32.724</td><td>1235</td><td>36.528</td></tr>
      <tr><td>Old AC-MOT</td><td>23.236</td><td>32.698</td><td>39.516</td><td>1061</td><td>41.957</td></tr>
      <tr class="sel"><td>V1</td><td class="best">26.948</td><td class="best">33.835</td><td class="best">41.546</td><td>1184</td><td>38.985</td></tr>
      <tr><td>V2</td><td>23.792</td><td>31.218</td><td>37.870</td><td class="best">919</td><td class="best">46.024</td></tr>
    </table>
  </div>
  <footer class="s-foot"><span class="prov p-test">Test set · VisDrone2019-MOT test-dev · 17 sequences · same detector, tracker and GPU</span></footer>
  <aside class="notes"><p><b>Say:</b> "This is the historical test-set comparison of the four systems. Green marks the best value in each column — note that it is not always the same system."</p></aside>
</section>'''

N['Reading the test-set result'] = r'''<section class="slide" data-sec="7" data-secname="VII · Optimization" data-title="Reading the test-set result">
  <header class="s-head"><div class="kicker">Section VII · Test set</div><h2>Reading the Test-Set Result</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p><b>V1 = quality-oriented</b> configuration. <b>V2 = identity- and speed-oriented</b> trade-off. Neither is best on every metric.</p></div>
    <div class="g3 grow" style="gap:20px">
      <div class="card" style="border-top:6px solid #0EA5E9"><h3>Baseline → Old AC-MOT</h3><ul class="clean v"><li>clear gain in tracking quality</li><li>lower IDS: 1235 → 1061</li><li>higher FPS in this historical comparison</li></ul></div>
      <div class="card" style="border-top:6px solid #7C3AED"><h3>Old AC-MOT → V1</h3><ul class="clean"><li><b>highest</b> MOTA, HOTA and IDF1</li><li>but IDS <b>increases</b>: 1061 → 1184</li></ul></div>
      <div class="card" style="border-top:6px solid #0D9488"><h3>V2</h3><ul class="clean"><li>lower quality metrics than V1</li><li><b>lowest IDS</b>: 919</li><li><b>highest FPS</b>: 46.024</li></ul></div>
    </div>
    <div class="callout warn">V1 is <b>not</b> the best system on every metric: it gives up some identity stability for higher tracking quality.</div>
  </div>
  <footer class="s-foot"><span class="prov p-test">Test set · VisDrone2019-MOT test-dev · 17 sequences</span></footer>
  <aside class="notes"><p><b>Say:</b> "Old AC-MOT already beat the baseline. V1 pushed quality to the highest level, but with more ID switches than Old AC-MOT. V2 gives the fewest ID switches and the highest speed, with lower quality than V1."</p></aside>
</section>'''

N['Stage 3: why V2'] = r'''<section class="slide" data-sec="7" data-secname="VII · Optimization" data-title="Stage 3: why V2">
  <header class="s-head"><div class="kicker">Section VII · V2</div><h2>Why V2 Was Created</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>V1 improved quality strongly, but <b>identity switches were not minimized</b>. So a <b>second optimization direction</b> was investigated.</p></div>
    <div class="g2 grow" style="gap:24px">
      <div class="card" style="border-top:6px solid #7C3AED"><div class="tag" style="color:#7C3AED">V1 · one objective with rules</div><p class="lead mt8" style="font-size:30px">Highest MOTA, while FPS ≥ 25 and IDS ≤ 271.</p></div>
      <div class="card" style="border-top:6px solid #0D9488"><div class="tag" style="color:#0D9488">V2 · multi-objective</div><ul class="clean mt8"><li><b>maximize</b> MOTA</li><li><b>minimize</b> IDS</li><li>with an <b>FPS constraint</b></li></ul></div>
    </div>
    <div class="callout">V2 was <b>not meant to replace V1</b> everywhere. It is <b>another operating point</b> on the quality / identity / efficiency trade-off.</div>
  </div>
  <footer class="s-foot"><span class="prov p-val">V2 study design · validation only</span></footer>
  <aside class="notes"><p><b>Say:</b> "V1 chased MOTA under rules. V2 asked for two goals at once — more MOTA and fewer ID switches — while staying fast enough."</p><p><b>Honest:</b> 50 trials were planned; 49 finished.</p></aside>
</section>'''

N['UAVDT with zero tuning'] = r'''<section class="slide" data-sec="7" data-secname="VII · Optimization" data-title="UAVDT with zero tuning">
  <header class="s-head"><div class="kicker">Section VII · Cross-dataset</div><h2>Cross-Dataset Evidence: UAVDT</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>On a <b>different drone dataset</b>, both V1 and V2 improve over the baseline — support that the <b>adaptive-control idea transfers</b>.</p></div>
    <div class="row grow" style="gap:16px">
      <div class="card" style="flex:1.6;padding:10px 14px"><div class="chart zoomable" data-chart="uav-quality"></div></div>
      <div class="card grow" style="padding:10px 14px"><div class="chart zoomable" data-chart="uav-ids"></div></div>
      <div class="card grow" style="padding:10px 14px"><div class="chart zoomable" data-chart="uav-fps"></div></div>
    </div>
    <div class="row" style="gap:18px">
      <table class="tbl" style="font-size:24px;flex:1.4">
        <tr><th style="text-align:left">System</th><th>MOTA ↑</th><th>HOTA ↑</th><th>IDF1 ↑</th><th>IDS ↓</th><th>FPS ↑</th></tr>
        <tr><td>Baseline</td><td>13.841</td><td>24.085</td><td>27.887</td><td>558</td><td class="best">65.015</td></tr>
        <tr class="sel"><td>V1</td><td class="best">17.399</td><td class="best">28.390</td><td class="best">34.453</td><td>321</td><td>58.353</td></tr>
        <tr><td>V2</td><td>16.118</td><td>26.930</td><td>32.014</td><td class="best">308</td><td>61.462</td></tr>
      </table>
      <div class="col" style="flex:1;gap:8px">
        <div class="card flat" style="padding:10px 16px"><p><b>V1:</b> stronger tracking quality.</p><p><b>V2:</b> fewer ID switches and better speed than V1.</p></div>
        <div class="note">Cross-dataset support only — <b>not a state-of-the-art claim</b>.</div>
      </div>
    </div>
  </div>
  <footer class="s-foot"><span class="prov p-ext">Cross-dataset test · UAVDT · 20 sequences / 16,592 frames · frozen systems, no tuning</span></footer>
  <aside class="notes"><p><b>Say:</b> "We ran the frozen systems on UAVDT without changing anything. Both beat the baseline on quality and ID switches. V1 is stronger on quality; V2 has fewer ID switches and is faster than V1."</p><p><b>Careful:</b> this is cross-dataset support, not a state-of-the-art claim.</p></aside>
</section>'''

N['Section VIII'] = r'''<section class="slide divider" id="sec-8" data-sec="8" data-secname="VIII · Transfer" data-title="Section VIII">
  <div class="dv-bg"><img src="assets/figures/image28.jpeg" alt=""></div>
  <div class="dv-text"><div class="dv-num">VIII</div><div class="dv-kicker">Section VIII</div>
    <h1>Transfer to a Published Strong MOT Pipeline</h1>
    <p>A short, separate study after the original AC-MOT story: can the same control idea be added to a much heavier published tracker?</p></div>
  <aside class="notes"><p><b>Say:</b> "The original story is complete. This short part is a separate transfer experiment."</p></aside>
</section>'''

N['Section IX'] = r'''<section class="slide divider" id="sec-9" data-sec="9" data-secname="IX · Conclusion" data-title="Section IX">
  <div class="dv-bg"><img src="assets/figures/image29.jpeg" alt=""></div>
  <div class="dv-text"><div class="dv-num">IX</div><div class="dv-kicker">Section IX</div>
    <h1>Contributions and Conclusion</h1>
    <p>What AC-MOT adds, and what the results show.</p></div>
  <aside class="notes"><p><b>Say:</b> "To finish."</p></aside>
</section>'''

N['Main contributions'] = r'''<section class="slide" data-sec="9" data-secname="IX · Conclusion" data-title="Main contributions">
  <header class="s-head"><div class="kicker">Section IX · Contributions</div><h2>Main Contributions</h2></header>
  <div class="s-body col">
    <div class="g2 grow" style="gap:22px">
      <div class="card row ac" style="gap:22px;border-left:8px solid #2563EB"><div class="big" style="font-size:72px;color:#2563EB">1</div><p class="lead" style="font-size:32px">A lightweight <b>Scene Complexity Index</b> built from <b>five low-cost cues</b>.</p></div>
      <div class="card row ac" style="gap:22px;border-left:8px solid #4F46E5"><div class="big" style="font-size:72px;color:#4F46E5">2</div><p class="lead" style="font-size:32px"><b>Adaptive detector-side control</b> according to scene difficulty.</p></div>
      <div class="card row ac" style="gap:22px;border-left:8px solid #7C3AED"><div class="big" style="font-size:72px;color:#7C3AED">3</div><p class="lead" style="font-size:32px"><b>Validation-driven joint optimization</b> of SCI weights, regime boundaries and detector operating parameters.</p></div>
      <div class="card row ac" style="gap:22px;border-left:8px solid #0D9488"><div class="big" style="font-size:72px;color:#0D9488">4</div><p class="lead" style="font-size:32px">Demonstrated <b>performance trade-offs</b> on the original test set and in the cross-dataset UAVDT evaluation.</p></div>
    </div>
  </div>
  <aside class="notes"><p><b>Say:</b> "Four contributions: the SCI, the adaptive control, the validation-driven joint optimization, and the measured trade-offs on the test set and on UAVDT."</p></aside>
</section>'''

N['Conclusion: what AC-MOT delivers'] = r'''<section class="slide" data-sec="9" data-secname="IX · Conclusion" data-title="Conclusion: what AC-MOT delivers">
  <header class="s-head"><div class="kicker">Section IX · Conclusion</div><h2>Conclusion</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">In one sentence</div><p>“AC-MOT does <b>not replace</b> the detector or tracker. It adds a <b>scene-aware control layer</b> that changes the detector operating point according to scene complexity.”</p></div>
    <table class="tbl" style="font-size:30px">
      <tr><td class="strong">Fixed detector settings</td><td style="text-align:center">→</td><td style="text-align:left">ignore temporal scene variation</td></tr>
      <tr><td class="strong">SCI</td><td style="text-align:center">→</td><td style="text-align:left">estimates scene complexity</td></tr>
      <tr><td class="strong">Adaptive controller</td><td style="text-align:center">→</td><td style="text-align:left">selects detector operating parameters</td></tr>
      <tr><td class="strong" style="color:#7C3AED">V1</td><td style="text-align:center">→</td><td style="text-align:left">prioritizes tracking quality</td></tr>
      <tr><td class="strong" style="color:#0D9488">V2</td><td style="text-align:center">→</td><td style="text-align:left">prioritizes identity and efficiency trade-offs</td></tr>
      <tr><td class="strong" style="color:#0891B2">UAVDT</td><td style="text-align:center">→</td><td style="text-align:left">supports cross-dataset transfer</td></tr>
    </table>
  </div>
  <aside class="notes"><p><b>Say:</b> "AC-MOT does not replace the detector or the tracker. It adds a scene-aware control layer. Fixed settings ignore how scenes change; SCI estimates the difficulty; the controller picks the detector settings; V1 favours quality, V2 favours identity and speed, and UAVDT supports transfer."</p></aside>
</section>'''

# ------------------------------------------------------------------ assemble in story order
DELETE = {
    'Research question and contributions', 'SCI formulas', 'Two protocols',
    'Ablation A0 to A3', 'Accuracy improves at every step', 'Where the MOTA gain comes from',
    'Recall explains the MOTA gain', 'The identity-switch trade-off', 'Accuracy at real-time speed',
    'Baseline A0 versus AC-MOT A3', 'Final live run: baseline vs Full AC-MOT', 'Choosing the winner among finalists',
    'Quick question: higher MOTA', 'Accuracy up, ID switches back', 'Why one score can fool us',
    'The new plan: a search with rules', 'What is Optuna', 'Step 1: sweeps shrink the search',
    'Step 2: how often to look, how much to smooth', 'Step 3: learn what a hard scene looks like',
    'Optuna-based optimization', 'What the search learned', 'Final test on test-dev', 'What Stage 2 adds',
    'V2 Trial 22', 'All systems on test-dev', 'Are the differences real', 'Results across both datasets',
    'What we focused on and why',
}
REPLACE = {'Outline', 'Section III', 'One fixed threshold', 'Section IV', 'What we add',
           'Step 1: measure scene complexity', 'Fair and attributable design', 'Section VI', 'Section VII',
           'Step 4 result: Trial 24', 'Stage 3: why V2', 'UAVDT with zero tuning', 'Section VIII',
           'Conclusion: what AC-MOT delivers'}
INSERT_AFTER = {
    'One fixed threshold': ['The main question'],
    'Three clues on real pictures': ['Initial SCI'],
    'Section VI': ['Original ablation table', 'What each component changed'],
    'Section VII': ['Why Optuna', 'What Optuna changed in V1', 'One Optuna trial'],
    'Quick question: what did the search learn': ['V1 Trial 24 weights', 'V1 Trial 24 regimes'],
    'Validation builds it, test judges it': ['Final test-set comparison', 'Reading the test-set result'],
    'U2MOT reproduction status': ['Section IX', 'Main contributions'],
}
for t in DELETE | REPLACE | set(INSERT_AFTER):
    if t not in patched:
        sys.exit(f'unknown title: {t}')

out = []
for t, _ in order:
    if t in DELETE:
        continue
    out.append(N[t] if t in REPLACE else patched[t])
    for extra in INSERT_AFTER.get(t, []):
        out.append(N[extra])

# story-order sanity: move the three test/V2/UAVDT slides already follow; verify key order
final_titles = [title_of(s) for s in out]
must = ['One fixed threshold', 'The main question', 'What we add', 'Step 1: measure scene complexity', 'Initial SCI',
        'Section VI', 'Original ablation table', 'What each component changed', 'Section VII', 'Why Optuna',
        'What Optuna changed in V1', 'One Optuna trial', 'V1 Trial 24 weights', 'V1 Trial 24 regimes',
        'Step 4 result: Trial 24', 'Final test-set comparison', 'Reading the test-set result', 'Stage 3: why V2',
        'UAVDT with zero tuning', 'Section VIII', 'Next step: U2MOT', 'Section IX', 'Main contributions',
        'Conclusion: what AC-MOT delivers', 'Thank you']
pos = [final_titles.index(m) for m in must]
assert pos == sorted(pos), 'story order broken'
assert len(final_titles) == len(set(final_titles)), 'duplicate after build'
bad = [t for t, s in zip(final_titles, out) if re.search(r'devAblation|devDerived|historical\.', s)]
assert not bad, f'old experiment bindings left in: {bad}'

new_body = '\n\n' + '\n\n'.join(out) + '\n\n'
P.write_text(head + new_body + tail, encoding='utf-8')
print('v6 slides:', len(out))
for i, t in enumerate(final_titles, 1):
    print(f'{i:3d}  {t}')
