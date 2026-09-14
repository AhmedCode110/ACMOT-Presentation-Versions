"""v7: optional deep explanations for the AC-MOT deck (copy of v6).
Adds a full-screen explanation stage OUTSIDE the main slide sequence, footer buttons on
selected main slides, and the engine/CSS to open, page through and close explanations."""
import pathlib, re, sys

ROOT = pathlib.Path('/Users/ahmedgouda/Desktop/acmot_interactive_presentation_v7')
IDX, JS, CSS, README = ROOT / 'index.html', ROOT / 'script.js', ROOT / 'styles.css', ROOT / 'README.md'

def must_replace(text, old, new, label, count=1):
    n = text.count(old)
    if n != count:
        sys.exit(f'FAILED [{label}]: found {n}x')
    return text.replace(old, new)

def page(sec, title, kicker, h2, body, deck_label=None):
    return (f'<section class="xpage" data-sec="{sec}" data-title="{title}">\n'
            f'  <header class="s-head"><div class="kicker">{kicker}</div><h2>{h2}</h2></header>\n'
            f'  <div class="s-body col">\n{body}\n  </div>\n</section>')

MAN = '<span class="origin manual">manually designed · original controller</span>'
EMP = '<span class="origin empirical">empirical design constant · not chosen by Optuna</span>'
OPT = '<span class="origin optuna">optimization-selected · V1 Trial 24</span>'
ILL = '<span class="origin illus">illustration · made-up numbers</span>'
DOWN = '<div class="xdown">↓</div>'

# =====================================================================================
# 1. CONTROLLER LOGIC (required)
# =====================================================================================
ctrl = []
ctrl.append(page(4, 'Controller part 1', 'Controller logic · Part 1 — confidence', 'SCI Sets a Continuous Confidence Threshold', f'''
    <div class="meaning"><div class="tag">Not just Easy / Medium / Hard</div><p>The controller <b>first calculates a smooth value from SCI</b>: every SCI value gives its own confidence threshold.</p></div>
    <div class="card tc" style="padding:12px 20px"><div class="xeq">confidence = 0.245 − 0.050 × <span class="hl">SCI</span></div><div class="mt8">{MAN}</div></div>
    <div class="g2 grow" style="gap:22px">
      <div class="card col center" style="gap:4px;border-top:6px solid var(--good)"><div class="ex-label">Example 1 · easier scene</div>
        <div class="xeq sm">SCI = <span class="hl">0.20</span></div><div class="xeq sm">0.245 − 0.050 × 0.20</div><div class="xeq">= <b>0.235</b></div><p class="tc">stricter confidence</p></div>
      <div class="card col center" style="gap:4px;border-top:6px solid var(--bad)"><div class="ex-label">Example 2 · harder scene</div>
        <div class="xeq sm">SCI = <span class="hl">0.80</span></div><div class="xeq sm">0.245 − 0.050 × 0.80</div><div class="xeq">= <b>0.205</b></div><p class="tc">lower confidence → less conservative detector</p></div>
    </div>
    <div class="xchain"><span class="pill sec">SCI ↑</span><span>→ harder scene →</span><span class="pill sec">confidence ↓</span><span>→ more detections are allowed to survive</span></div>'''))

ctrl.append(page(4, 'Controller part 2', 'Controller logic · Part 2 — NMS IoU', 'SCI Sets the NMS IoU Threshold', f'''
    <div class="meaning"><div class="tag">What NMS IoU means</div><p>NMS (Non-Maximum Suppression) keeps the best box and <b>deletes other boxes that overlap it more than the NMS IoU threshold</b>.</p></div>
    <div class="row grow" style="gap:22px">
      <div class="col" style="flex:0 0 640px;gap:10px">
        <div class="card tc" style="padding:10px 16px"><div class="xeq">NMS IoU = 0.490 − 0.050 × <span class="hl">SCI</span></div><div class="mt8">{MAN}</div></div>
        <div class="g2" style="gap:14px">
          <div class="card tc" style="padding:10px"><div class="ex-label">SCI = 0.40</div><div class="xeq sm">0.490 − 0.050 × 0.40</div><div class="xeq">= <b>0.470</b></div></div>
          <div class="card tc" style="padding:10px"><div class="ex-label">SCI = 0.80</div><div class="xeq sm">0.490 − 0.050 × 0.80</div><div class="xeq">= <b>0.450</b></div></div>
        </div>
        <div class="callout warn"><b>Detector NMS IoU ≠ tracker match threshold.</b> NMS works inside one frame; the tracker threshold links boxes across frames.</div>
      </div>
      <div class="card col grow" style="gap:8px"><div class="ex-label">Two overlapping boxes on one car <span class="origin illus">illustration</span></div>
        <svg viewBox="0 0 520 250" width="100%" height="230"><g font-family="Inter,Helvetica" font-weight="800">
          <rect x="120" y="120" width="200" height="80" rx="14" fill="#475569"/>
          <rect x="90" y="70" width="220" height="150" fill="none" stroke="#16A34A" stroke-width="6"/>
          <rect x="146" y="94" width="220" height="150" fill="none" stroke="#F59E0B" stroke-width="5" stroke-dasharray="12 7"/>
          <text x="90" y="58" font-size="22" fill="#15803D">box A · score 0.90</text>
          <text x="376" y="150" font-size="22" fill="#B45309">box B · 0.75</text>
          <text x="376" y="182" font-size="22" fill="#0F1B33">overlap IoU ≈ 0.46</text></g></svg>
        <div class="g2" style="gap:12px">
          <div class="card flat" style="padding:10px 14px;border-left:6px solid var(--bad)"><p><b>Threshold 0.45</b> (SCI 0.80)<br>0.46 &gt; 0.45 → box B is <b>deleted</b></p><p class="small muted">lower threshold = more aggressive suppression</p></div>
          <div class="card flat" style="padding:10px 14px;border-left:6px solid var(--good)"><p><b>Threshold 0.49</b> (SCI 0.00)<br>0.46 &lt; 0.49 → both boxes <b>stay</b></p><p class="small muted">higher threshold = more overlapping boxes remain</p></div>
        </div>
      </div>
    </div>'''))

ctrl.append(page(4, 'Controller part 3', 'Controller logic · Part 3 — input size', 'SCI Chooses the Input Resolution', f'''
    <div class="meaning"><div class="tag">Three regions</div><p>The input size <b>steps up</b> when SCI crosses <b>0.35</b> and <b>0.60</b>. {MAN}</p></div>
    <svg viewBox="0 0 1400 170" width="100%" height="170"><g font-family="Inter,Helvetica" font-weight="800">
      <rect x="20" y="40" width="476" height="64" rx="8" fill="#DCFCE7" stroke="#16A34A" stroke-width="3"/>
      <rect x="496" y="40" width="340" height="64" rx="8" fill="#FEF3C7" stroke="#D97706" stroke-width="3"/>
      <rect x="836" y="40" width="544" height="64" rx="8" fill="#FEE2E2" stroke="#DC2626" stroke-width="3"/>
      <text x="258" y="82" font-size="28" fill="#14532D" text-anchor="middle">easier scene · 640</text>
      <text x="666" y="82" font-size="28" fill="#92400E" text-anchor="middle">medium · 736</text>
      <text x="1108" y="82" font-size="28" fill="#7F1D1D" text-anchor="middle">hard / complex · 832</text>
      <g font-size="22" fill="#334155" text-anchor="middle"><text x="30" y="135">0</text><text x="496" y="135">0.35</text><text x="836" y="135">0.60</text><text x="1368" y="135">1</text></g>
      <g fill="#0F1B33"><path d="M292 34 l-10 -16 h20 z"/><path d="M700 34 l-10 -16 h20 z"/><path d="M1040 34 l-10 -16 h20 z"/></g>
      <g font-size="20" fill="#0F1B33" text-anchor="middle"><text x="292" y="14">SCI 0.20</text><text x="700" y="14">SCI 0.50</text><text x="1040" y="14">SCI 0.75</text></g>
      <g font-size="22" fill="#0F1B33" text-anchor="middle"><text x="292" y="162">→ 640</text><text x="700" y="162">→ 736</text><text x="1040" y="162">→ 832</text></g></g></svg>
    <div class="card tc" style="padding:8px 16px"><p class="fcell" style="font-size:27px">SCI ≤ 0.35 → 640 &nbsp;·&nbsp; 0.35 &lt; SCI ≤ 0.60 → 736 &nbsp;·&nbsp; SCI &gt; 0.60 → 832</p></div>
    <div class="g2 grow" style="gap:22px">
      <div class="card" style="border-left:6px solid var(--good)"><h3>Lower resolution (640)</h3><ul class="clean"><li>less computation</li><li>higher potential FPS</li></ul></div>
      <div class="card" style="border-left:6px solid var(--bad)"><h3>Higher resolution (832)</h3><ul class="clean"><li>more image detail</li><li>better chance to keep small objects</li><li>higher computational cost</li></ul></div>
    </div>'''))

ctrl.append(page(4, 'Controller part 4', 'Controller logic · Part 4 — small fixes', 'The Small Fixes Come After the Main Equations', f'''
    <div class="xchain" style="margin-top:4px"><span class="pill sec">1 · SCI</span><span>→</span><span class="pill sec">confidence</span><span>→</span><span class="pill sec">NMS IoU</span><span>→</span><span class="pill sec">resolution</span><span>→</span><span class="pill warn">2 · then check specific cues</span></div>
    <div class="g3 grow" style="gap:18px">
      <div class="card col" style="gap:8px;border-top:6px solid #4F46E5"><h3>Crowded, tiny or dark</h3><div class="xeq sm">confidence − 0.012</div>
        <p>Difficult objects often get <b>weaker detector scores</b>. A slightly lower line keeps useful detections.</p>
        <div class="card flat tc" style="padding:8px"><div class="ex-label">Example · crowded</div><div class="xeq sm">0.235 − 0.012 = <b>0.223</b></div><p class="small">final confidence before clipping</p></div></div>
      <div class="card col" style="gap:8px;border-top:6px solid #0D9488"><h3>Blurred</h3><div class="xeq sm">NMS IoU − 0.012</div>
        <p>A lower NMS IoU makes overlap suppression <b>slightly more aggressive</b>.</p>
        <div class="card flat tc" style="padding:8px"><div class="ex-label">Example · blur detected</div><div class="xeq sm">0.470 − 0.012 = <b>0.458</b></div></div></div>
      <div class="card col" style="gap:8px;border-top:6px solid #DC2626"><h3>More than half of the boxes are tiny</h3><div class="xeq sm">input size = 832</div>
        <p>This <b>overrides</b> the normal size rule, because small objects need more spatial detail.</p>
        <div class="card flat tc" style="padding:8px"><div class="ex-label">Example</div><p>SCI = 0.45 → normal rule <b>736</b><br>tiny share = 0.60 &gt; 0.50 → <b>832</b></p></div></div>
    </div>
    <div class="tc">{MAN}</div>'''))

ctrl.append(page(4, 'Controller part 5', 'Controller logic · Part 5 — limits', '“The Limits Are Applied Again” = Clamping', f'''
    <div class="meaning"><div class="tag">What it means</div><p>After the small fixes, every value is <b>clamped</b> back into its allowed range. {MAN}</p></div>
    <div class="row grow" style="gap:24px">
      <div class="card col center" style="flex:0 0 560px;gap:4px"><div class="ex-label">Confidence · allowed 0.19 ≤ confidence ≤ 0.28</div>
        <div class="xeq">0.195</div><div class="xdown">↓ <span class="xeq sm">− 0.012 (crowded)</span></div><div class="xeq bad">0.183</div><div class="xdown">↓ <span class="xeq sm">clamp to the minimum</span></div><div class="xeq good"><b>0.190</b></div></div>
      <div class="col grow" style="gap:14px">
        <svg viewBox="0 0 760 150" width="100%" height="150"><g font-family="Inter,Helvetica" font-weight="800">
          <line x1="40" y1="80" x2="720" y2="80" stroke="#94A3B8" stroke-width="4"/>
          <rect x="167" y="58" width="453" height="44" rx="6" fill="#DCFCE7" stroke="#16A34A" stroke-width="3"/>
          <text x="393" y="87" font-size="22" fill="#14532D" text-anchor="middle">allowed 0.19 … 0.28</text>
          <circle cx="129" cy="80" r="12" fill="#DC2626"/><text x="129" y="40" font-size="22" fill="#B91C1C" text-anchor="middle">0.183</text>
          <circle cx="167" cy="80" r="12" fill="#16A34A"/><text x="187" y="138" font-size="22" fill="#15803D" text-anchor="middle">0.190</text>
          <path d="M141 80 h12" stroke="#0F1B33" stroke-width="4"/></g></svg>
        <div class="card" style="border-left:6px solid #0D9488"><h3>NMS IoU · allowed 0.40 ≤ NMS ≤ 0.52</h3><p>Same idea. With SCI between 0 and 1 and the blur fix, NMS stays between <b>0.428</b> and <b>0.490</b> — already inside the limits. Here the clamp is a <b>safety guard</b>.</p></div>
        <div class="callout">Clamping stops a value from leaving the tested, safe range — for example, confidence can never fall below 0.19.</div>
      </div>
    </div>'''))

ctrl.append(page(4, 'Controller complete example', 'Controller logic · Complete example', 'One Frame Through the Whole Controller', f'''
    <div class="xchain"><span class="pill sec">SCI = 0.50</span><span class="pill bad">crowded = yes</span><span class="pill bad">tiny share = 0.60</span><span class="pill bad">blur = yes</span><span class="pill good">dark = no</span><span>{ILL}</span></div>
    <div class="g3 grow" style="gap:18px">
      <div class="card col center" style="gap:4px;border-top:6px solid #4F46E5"><div class="ex-label">Step 1 · confidence</div>
        <div class="xeq sm">0.245 − 0.050 × 0.50</div><div class="xeq">= 0.220</div>{DOWN}<div class="xeq sm">crowded: 0.220 − 0.012</div><div class="xeq">= 0.208</div>{DOWN}<p class="tc">inside 0.19 … 0.28 → <b>0.208</b></p></div>
      <div class="card col center" style="gap:4px;border-top:6px solid #0D9488"><div class="ex-label">Step 2 · NMS IoU</div>
        <div class="xeq sm">0.490 − 0.050 × 0.50</div><div class="xeq">= 0.465</div>{DOWN}<div class="xeq sm">blur: 0.465 − 0.012</div><div class="xeq">= 0.453</div>{DOWN}<p class="tc">inside 0.40 … 0.52 → <b>0.453</b></p></div>
      <div class="card col center" style="gap:4px;border-top:6px solid #DC2626"><div class="ex-label">Step 3 · input size</div>
        <div class="xeq sm">SCI = 0.50</div><div class="xeq">normal: 736</div>{DOWN}<div class="xeq sm">tiny share 0.60 &gt; 0.50</div><div class="xeq">override</div>{DOWN}<p class="tc">→ <b>832</b></p></div>
    </div>
    <div class="card sec row ac jb" style="padding:12px 26px"><span class="strong" style="font-size:28px">Final detector configuration →</span>
      <span class="pills"><span class="pill sec" style="font-size:26px">Confidence = 0.208</span><span class="pill sec" style="font-size:26px">NMS IoU = 0.453</span><span class="pill sec" style="font-size:26px">Input size = 832</span></span></div>
    <p class="tc small muted">The crowded correction is applied once (crowded, tiny or dark share one −0.012 fix).</p>'''))

# =====================================================================================
# 2. SCI CUES
# =====================================================================================
cues = []
cues.append(page(4, 'Cue crowd', 'SCI cues · 1 of 5 — crowd', 'Crowd: How Many Objects Are There?', f'''
    <div class="card tc" style="padding:12px 20px"><div class="xeq">Crowd = min( <span class="hl">tracked boxes in the previous frame</span> ÷ 30 , 1 )</div><div class="mt8">{EMP}</div></div>
    <div class="row grow" style="gap:24px">
      <table class="tbl" style="font-size:28px;flex:0 0 620px">
        <tr><th style="text-align:left">Boxes</th><th style="text-align:left">Calculation</th><th>Crowd</th></tr>
        <tr><td>3</td><td style="text-align:left" class="fcell">3 ÷ 30</td><td class="strong">0.10</td></tr>
        <tr><td>15</td><td style="text-align:left" class="fcell">15 ÷ 30</td><td class="strong">0.50</td></tr>
        <tr><td>30</td><td style="text-align:left" class="fcell">30 ÷ 30</td><td class="strong">1.00</td></tr>
        <tr><td>45</td><td style="text-align:left" class="fcell">45 ÷ 30 = 1.5 → min(1.5, 1)</td><td class="strong bad">still 1.00</td></tr>
      </table>
      <div class="col grow" style="gap:14px">
        <div class="card sec"><h3>Why min(…, 1)?</h3><ul class="clean"><li>keeps the cue between <b>0 and 1</b>, like the other cues</li><li>30 or more objects already counts as <b>fully crowded</b></li><li>stops one very crowded frame from making SCI grow without limit</li></ul></div>
        <div class="note">30 is a <b>normalization ceiling chosen by design</b>, not a universal value.</div>
      </div>
    </div>'''))

cues.append(page(4, 'Cue tiny', 'SCI cues · 2 of 5 — tiny objects', 'Tiny: What Share of the Boxes Is Small?', f'''
    <div class="card tc" style="padding:12px 20px"><div class="xeq">Tiny = <span class="hl">boxes smaller than 32 × 32</span> ÷ all boxes</div><div class="mt8">{EMP} <span class="origin illus">32² follows the COCO small-object size</span></div></div>
    <div class="row grow" style="gap:24px">
      <div class="card col center" style="flex:0 0 700px;gap:10px"><div class="ex-label">Example · 10 boxes</div>
        <svg viewBox="0 0 640 150" width="100%" height="150"><g>
          <rect x="10" y="30" width="96" height="96" fill="#DBEAFE" stroke="#2563EB" stroke-width="4"/><rect x="126" y="40" width="80" height="80" fill="#DBEAFE" stroke="#2563EB" stroke-width="4"/>
          <rect x="226" y="50" width="70" height="70" fill="#DBEAFE" stroke="#2563EB" stroke-width="4"/><rect x="316" y="40" width="84" height="84" fill="#DBEAFE" stroke="#2563EB" stroke-width="4"/>
          <rect x="420" y="46" width="76" height="76" fill="#DBEAFE" stroke="#2563EB" stroke-width="4"/><rect x="516" y="36" width="90" height="90" fill="#DBEAFE" stroke="#2563EB" stroke-width="4"/>
          <g fill="#FEF3C7" stroke="#D97706" stroke-width="4"><rect x="140" y="130" width="18" height="18"/><rect x="250" y="130" width="16" height="16"/><rect x="440" y="130" width="18" height="18"/><rect x="560" y="130" width="16" height="16"/></g></g></svg>
        <p class="tc">6 normal boxes and <b>4 tiny boxes</b> (orange)</p>
        <div class="xeq">Tiny = 4 ÷ 10 = <b>0.40</b></div></div>
      <div class="col grow" style="gap:14px">
        <div class="card sec"><h3>Why it matters</h3><p>Tiny objects get <b>weak scores</b> and are easy to lose, so a high Tiny value warns that the scene is hard.</p></div>
        <div class="note">If there are no boxes, Tiny = 0.</div>
      </div>
    </div>'''))

cues.append(page(4, 'Cue edge', 'SCI cues · 3 of 5 — edges', 'Edge: How Busy Is the Background?', f'''
    <div class="xchain"><span class="pill sec">frame</span><span>→</span><span class="pill sec">grayscale</span><span>→</span><span class="pill sec">Canny edge map</span><span>→</span><span class="pill sec">edge density = share of edge pixels</span><span>→</span><span class="pill warn">÷ 0.14, max 1</span></div>
    <div class="card tc" style="padding:12px 20px"><div class="xeq">Edge = min( <span class="hl">edge density</span> ÷ 0.14 , 1 )</div><div class="mt8">{EMP}</div></div>
    <div class="row grow" style="gap:24px">
      <table class="tbl" style="font-size:28px;flex:0 0 620px">
        <tr><th style="text-align:left">Edge density</th><th style="text-align:left">Calculation</th><th>Edge</th></tr>
        <tr><td>0.035</td><td style="text-align:left" class="fcell">0.035 ÷ 0.14</td><td class="strong">0.25</td></tr>
        <tr><td>0.07</td><td style="text-align:left" class="fcell">0.07 ÷ 0.14</td><td class="strong">0.50</td></tr>
        <tr><td>0.14</td><td style="text-align:left" class="fcell">0.14 ÷ 0.14</td><td class="strong">1.00</td></tr>
        <tr><td>0.21</td><td style="text-align:left" class="fcell">1.5 → min(1.5, 1)</td><td class="strong bad">1.00</td></tr>
      </table>
      <div class="col grow" style="gap:14px">
        <div class="card sec"><h3>Meaning</h3><p>Many edges = roads, roofs, trees and markings. A busy background makes <b>ghost boxes</b> and hides real objects.</p></div>
        <div class="note">Density 0.14 or more already counts as a <b>very busy</b> frame (Edge = 1).</div>
      </div>
    </div>'''))

cues.append(page(4, 'Cue night', 'SCI cues · 4 of 5 — low light', 'Night: Is the Frame Dark?', f'''
    <div class="card tc" style="padding:12px 20px"><div class="xeq">Night = 1 if <span class="hl">mean grayscale</span> &lt; 80, otherwise 0</div><div class="mt8">{EMP}</div></div>
    <svg viewBox="0 0 1400 150" width="100%" height="150"><defs><linearGradient id="gray" x1="0" x2="1"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#fff"/></linearGradient></defs>
      <g font-family="Inter,Helvetica" font-weight="800">
      <rect x="20" y="40" width="1360" height="56" fill="url(#gray)" stroke="#94A3B8" stroke-width="2"/>
      <line x1="447" y1="26" x2="447" y2="110" stroke="#DC2626" stroke-width="6"/><text x="447" y="18" font-size="24" fill="#B91C1C" text-anchor="middle">80</text>
      <g font-size="22" fill="#334155" text-anchor="middle"><text x="30" y="135">0 = black</text><text x="1340" y="135">255 = white</text></g>
      <path d="M340 110 l-10 18 h20 z" fill="#0F1B33"/><text x="340" y="146" font-size="22" fill="#0F1B33" text-anchor="middle">60</text>
      <path d="M660 110 l-10 18 h20 z" fill="#0F1B33"/><text x="660" y="146" font-size="22" fill="#0F1B33" text-anchor="middle">120</text></g></svg>
    <div class="g2 grow" style="gap:22px">
      <div class="card col center" style="border-top:6px solid #0F1B33"><div class="ex-label">Example · night street</div><div class="xeq">mean gray = 60</div><div class="xeq sm">60 &lt; 80</div><div class="xeq">Night = <b>1</b></div></div>
      <div class="card col center" style="border-top:6px solid #F59E0B"><div class="ex-label">Example · daytime road</div><div class="xeq">mean gray = 120</div><div class="xeq sm">120 ≥ 80</div><div class="xeq">Night = <b>0</b></div></div>
    </div>'''))

cues.append(page(4, 'Cue blur', 'SCI cues · 5 of 5 — blur', 'Blur: Is the Frame Sharp?', f'''
    <div class="card tc" style="padding:12px 20px"><div class="xeq">Blur = 1 if <span class="hl">variance of the Laplacian</span> &lt; 180, otherwise 0</div><div class="mt8">{EMP}</div></div>
    <div class="row grow" style="gap:24px">
      <div class="card col" style="flex:0 0 640px;gap:10px"><h3>Variance of the Laplacian, simply</h3>
        <div class="xchain" style="justify-content:flex-start"><span class="pill sec">Laplacian</span><span>= finds sudden brightness changes (sharp edges)</span></div>
        <ul class="clean"><li><b>Sharp image</b> → many strong changes → <b>high</b> variance</li><li><b>Blurred image</b> → changes are smoothed out → <b>low</b> variance</li></ul></div>
      <div class="col grow" style="gap:14px">
        <div class="card col center" style="border-top:6px solid var(--bad)"><div class="ex-label">Example · shaking camera</div><div class="xeq">variance = 90 &lt; 180 → Blur = <b>1</b></div></div>
        <div class="card col center" style="border-top:6px solid var(--good)"><div class="ex-label">Example · steady camera</div><div class="xeq">variance = 350 ≥ 180 → Blur = <b>0</b></div></div>
      </div>
    </div>'''))

# =====================================================================================
# 3. SCI CALCULATION
# =====================================================================================
sci = []
sci.append(page(4, 'SCI weighted example', 'SCI calculation · 1 of 2', 'From Five Cues to One SCI Value', f'''
    <div class="xchain"><span class="pill sec">Crowd</span><span class="pill sec">Tiny</span><span class="pill sec">Edge</span><span class="pill sec">Night</span><span class="pill sec">Blur</span><span>→ × weight → add →</span><span class="pill warn">SCI</span><span>{ILL}</span></div>
    <table class="tbl" style="font-size:27px">
      <tr><th style="text-align:left">Cue</th><th style="text-align:left">What was measured</th><th>Cue value</th><th>Initial weight</th><th>Contribution</th></tr>
      <tr><td>Crowd</td><td style="text-align:left">15 boxes → 15 ÷ 30</td><td>0.50</td><td>× 0.30</td><td class="strong">0.15</td></tr>
      <tr><td>Tiny</td><td style="text-align:left">6 of 15 boxes are tiny</td><td>0.40</td><td>× 0.30</td><td class="strong">0.12</td></tr>
      <tr><td>Edge</td><td style="text-align:left">density 0.07 → 0.07 ÷ 0.14</td><td>0.50</td><td>× 0.20</td><td class="strong">0.10</td></tr>
      <tr><td>Night</td><td style="text-align:left">mean gray 60 &lt; 80</td><td>1</td><td>× 0.10</td><td class="strong">0.10</td></tr>
      <tr><td>Blur</td><td style="text-align:left">variance 350 ≥ 180</td><td>0</td><td>× 0.05</td><td class="strong">0.00</td></tr>
    </table>
    <div class="card sec tc" style="padding:12px 20px"><div class="xeq">SCI = 0.15 + 0.12 + 0.10 + 0.10 + 0.00 = <span class="hl"><b>0.47</b></span></div>
      <div class="mt8"><span class="origin manual">weights manually designed · initial SCI</span> <span class="origin empirical">cue limits: empirical design constants</span></div></div>'''))

sci.append(page(4, 'SCI stabilise', 'SCI calculation · 2 of 2', 'Then SCI Is Clipped, Smoothed and Updated Every 10 Frames', f'''
    <div class="g3 grow" style="gap:20px">
      <div class="card col" style="gap:10px;border-top:6px solid #4F46E5"><h3>1 · Clip to [0, 1]</h3><p>If the weighted sum leaves 0 … 1, it is cut back into the range.</p><div class="xeq sm">0.47 → stays <b>0.47</b></div></div>
      <div class="card col" style="gap:10px;border-top:6px solid #7C3AED"><h3>2 · Smooth · window = 7</h3><p>SCI = the mean of the last 7 readings, so one odd frame changes little.</p>
        <p class="fcell" style="font-size:24px">0.40, 0.42, 0.45, 0.47, 0.46, 0.48, 0.51</p><div class="xeq sm">3.19 ÷ 7 = <b>0.456</b></div></div>
      <div class="card col" style="gap:10px;border-top:6px solid #0D9488"><h3>3 · Analyse every 10 frames</h3><p>The scene changes over seconds, not single frames. The last SCI is reused in between.</p><div class="xeq sm">30 FPS → 3 analyses per second</div></div>
    </div>
    <div class="tc"><span class="origin empirical">window 7 and stride 10: fixed design constants · not chosen by Optuna</span> {ILL}</div>'''))

# =====================================================================================
# 4. OPTUNA V1
# =====================================================================================
opt = []
opt.append(page(7, 'Optuna what a trial contains', 'Optuna V1 · 1 of 3', 'Optuna Proposes a Complete Configuration', f'''
    <div class="g2" style="gap:18px">
      <div class="card" style="border-left:6px solid var(--bad)"><h3 class="bad">Optuna does not…</h3><ul class="clean x"><li>calculate SCI itself</li><li>train a neural network — it is not an AI model</li><li>try values on a fixed grid or blindly at random</li></ul></div>
      <div class="card" style="border-left:6px solid var(--good)"><h3 class="good">Optuna does…</h3><ul class="clean v"><li>propose <b>one complete parameter set</b> per trial</li><li>read the trial’s validation result</li><li>use earlier results to propose the next set (TPE)</li></ul></div>
    </div>
    <table class="tbl grow" style="font-size:25px">
      <tr><th style="text-align:left">Each trial contains</th><th style="text-align:left">Parameters</th><th style="text-align:left">Selected in V1 Trial 24</th></tr>
      <tr><td>SCI weights</td><td style="text-align:left">w_crowd · w_tiny · w_edge · w_night · w_blur</td><td style="text-align:left" class="fcell">0.1295 · 0.2217 · 0.4337 · 0.0536 · 0.1615</td></tr>
      <tr><td>regime boundaries</td><td style="text-align:left">threshold_mid · threshold_high</td><td style="text-align:left" class="fcell">0.13535 · 0.28729</td></tr>
      <tr><td>detector parameters</td><td style="text-align:left">conf_easy · conf_hard · nms_easy · nms_hard</td><td style="text-align:left" class="fcell">0.30 · 0.40 · 0.35 · 0.35</td></tr>
    </table>
    <div class="tc">{OPT} <span class="origin illus">weights rounded here; exact values on the main slides</span></div>'''))

opt.append(page(7, 'Optuna one trial loop', 'Optuna V1 · 2 of 3', 'One Trial, Step by Step', '''
    <div class="row grow" style="gap:30px">
      <div class="xsteps col" style="flex:0 0 700px">
        <div class="node ad">configuration proposed by Optuna</div><div class="xdown">↓</div>
        <div class="node">validation run</div><div class="xdown">↓</div>
        <div class="node">SCI calculated for each analysed frame</div><div class="xdown">↓</div>
        <div class="node">Easy / Medium / Hard decision</div><div class="xdown">↓</div>
        <div class="node">detector settings for that regime</div><div class="xdown">↓</div>
        <div class="node">detection + tracking</div><div class="xdown">↓</div>
        <div class="node good">MOTA · HOTA · IDF1 · IDS · FPS</div><div class="xdown">↓</div>
        <div class="node ad">trial result → next TPE proposal</div>
      </div>
      <div class="col grow" style="gap:16px">
        <div class="card sec"><h3>V1 rules for a valid result</h3><ul class="clean"><li>FPS ≥ 25</li><li>IDS ≤ 271 (original full AC-MOT)</li><li>best = highest MOTA among valid trials</li></ul></div>
        <div class="callout">The whole pipeline runs <b>for every trial</b> — 50 trials in V1, on validation videos only.</div>
      </div>
    </div>'''))

opt.append(page(7, 'Optuna how TPE learns', 'Optuna V1 · 3 of 3', 'How Later Trials Use Earlier Trials (TPE)', '''
    <div class="meaning"><div class="tag">The main idea</div><p>TPE (Tree-structured Parzen Estimator) is a <b>sequential Bayesian method</b>: every finished trial changes where the next trial is likely to look.</p></div>
    <div class="flow grow" style="align-items:stretch;gap:0">
      <div class="card col" style="width:420px;gap:8px"><div class="ex-label">1 · early trials</div><p>The first trials explore the allowed ranges.</p></div><div class="arr" style="align-self:center"></div>
      <div class="card col" style="width:440px;gap:8px"><div class="ex-label">2 · split the history</div><p>TPE separates earlier trials into a <b>better group</b> and <b>the rest</b>.</p></div><div class="arr" style="align-self:center"></div>
      <div class="card col" style="width:440px;gap:8px"><div class="ex-label">3 · propose</div><p>New values are proposed <b>more often where the better trials were</b>, while still exploring.</p></div>
    </div>
    <div class="g2" style="gap:18px">
      <div class="callout warn">Not a grid search and not pure random search: <b>trial 30 is influenced by trials 1–29</b>.</div>
      <div class="callout">A fixed random seed (42) makes the V1 search <b>repeatable</b>.</div>
    </div>'''))

# =====================================================================================
# 5. V1 SCI RANGES
# =====================================================================================
reg = []
reg.append(page(7, 'Regimes are parameters', 'V1 SCI ranges · 1 of 2', 'The Easy / Medium / Hard Boundaries Were Optimized', f'''
    <div class="meaning"><div class="tag">The main idea</div><p>threshold_mid and threshold_high were <b>optimization parameters</b>, searched together with the weights — <b>not chosen by hand after looking at SCI values</b>. {OPT}</p></div>
    <svg viewBox="0 0 1400 112" width="100%" height="112"><g font-family="Inter,Helvetica" font-weight="800">
      <rect x="20" y="14" width="184" height="50" rx="6" fill="#DCFCE7" stroke="#16A34A" stroke-width="3"/>
      <rect x="204" y="14" width="207" height="50" rx="6" fill="#FEF3C7" stroke="#D97706" stroke-width="3"/>
      <rect x="411" y="14" width="969" height="50" rx="6" fill="#FEE2E2" stroke="#DC2626" stroke-width="3"/>
      <text x="112" y="48" font-size="26" fill="#14532D" text-anchor="middle">Easy</text><text x="307" y="48" font-size="26" fill="#92400E" text-anchor="middle">Medium</text><text x="895" y="48" font-size="26" fill="#7F1D1D" text-anchor="middle">Hard</text>
      <g font-size="22" fill="#334155" text-anchor="middle"><text x="30" y="98">0</text><text x="204" y="98">0.13535</text><text x="411" y="98">0.28729</text><text x="1368" y="98">1</text></g></g></svg>
    <table class="tbl grow" style="font-size:27px">
      <tr><th style="text-align:left">Parameter</th><th style="text-align:left">Selected value (Trial 24)</th><th style="text-align:left">Regime rule</th></tr>
      <tr><td>threshold_mid</td><td style="text-align:left" class="fcell">0.13534938199219218</td><td style="text-align:left"><b class="good">Easy</b>: SCI &lt; 0.13535</td></tr>
      <tr><td>threshold_high</td><td style="text-align:left" class="fcell">0.28728676236279177</td><td style="text-align:left"><b class="warn">Medium</b>: 0.13535 ≤ SCI &lt; 0.28729</td></tr>
      <tr><td></td><td></td><td style="text-align:left"><b class="bad">Hard</b>: SCI ≥ 0.28729</td></tr>
    </table>'''))

reg.append(page(7, 'Weights move a frame', 'V1 SCI ranges · 2 of 2', 'Changing the Weights Can Move the Same Frame', f'''
    <div class="card flat row ac jb" style="padding:10px 22px"><span class="strong">One frame (one reading, before smoothing):</span><span class="pills"><span class="pill">Crowd 0.10</span><span class="pill">Tiny 0</span><span class="pill">Edge 0.50</span><span class="pill">Night 0</span><span class="pill">Blur 0</span></span></div>
    <div class="g2 grow" style="gap:22px">
      <div class="card col" style="gap:8px;border-top:6px solid #94A3B8"><h3>Initial hand-designed weights</h3>
        <div class="xeq sm">0.30 × 0.10 + 0.20 × 0.50</div><div class="xeq">SCI = <b>0.130</b></div>
        <p>0.130 &lt; 0.13535 → <b class="good">Easy</b></p><div><span class="origin manual">manually designed weights</span></div></div>
      <div class="card col" style="gap:8px;border-top:6px solid #7C3AED"><h3>V1 Trial 24 weights</h3>
        <div class="xeq sm">0.1295 × 0.10 + 0.4337 × 0.50</div><div class="xeq">SCI ≈ <b>0.230</b></div>
        <p>0.13535 ≤ 0.230 &lt; 0.28729 → <b class="warn">Medium</b></p><div>{OPT}</div></div>
    </div>
    <div class="callout">Same frame, same cues — different weights give a <b>different SCI</b>, so the frame can land in a <b>different regime</b> and get <b>different detector settings</b>. That is why weights and boundaries were searched together.</div>
    <p class="tc small muted">Illustration: both weight sets are compared against the V1 boundaries only to show the effect.</p>'''))

# =====================================================================================
# 6. NMS vs TRACKER MATCH
# =====================================================================================
nmsm = [page(4, 'NMS vs tracker match', 'Detector vs tracker', 'Detector NMS IoU ≠ Tracker Match Threshold', '''
    <div class="meaning"><div class="tag">Two different operations</div><p><b>NMS</b> cleans duplicate boxes <b>inside one frame</b>. The <b>tracker match threshold</b> links boxes <b>across frames</b> to existing tracks.</p></div>
    <div class="g2 grow" style="gap:22px">
      <div class="card col" style="gap:8px;border-top:6px solid #4F46E5"><h3>Detector NMS IoU · frame t only</h3>
        <svg viewBox="0 0 560 210" width="100%" height="200"><g font-family="Inter,Helvetica" font-weight="800">
          <rect x="150" y="90" width="200" height="80" rx="14" fill="#475569"/>
          <rect x="120" y="50" width="240" height="140" fill="none" stroke="#16A34A" stroke-width="6"/>
          <rect x="140" y="64" width="240" height="140" fill="none" stroke="#DC2626" stroke-width="4" stroke-dasharray="12 7"/>
          <text x="120" y="38" font-size="22" fill="#15803D">kept (0.90)</text><text x="392" y="140" font-size="22" fill="#B91C1C">deleted duplicate</text></g></svg>
        <p>Removes <b>duplicate detector boxes</b> on the same object. Controlled by AC-MOT (0.40 … 0.52).</p></div>
      <div class="card col" style="gap:8px;border-top:6px solid #64748B"><h3>Tracker match threshold · frame t−1 → t</h3>
        <svg viewBox="0 0 560 210" width="100%" height="200"><g font-family="Inter,Helvetica" font-weight="800">
          <rect x="60" y="60" width="160" height="110" fill="none" stroke="#94A3B8" stroke-width="5" stroke-dasharray="10 7"/><text x="60" y="48" font-size="22" fill="#64748B">track ID 7 (t−1)</text>
          <rect x="300" y="70" width="160" height="110" fill="none" stroke="#2563EB" stroke-width="6"/><text x="300" y="205" font-size="22" fill="#1D4ED8">new detection (t)</text>
          <path d="M226 115 C255 105 270 110 294 120" fill="none" stroke="#0F1B33" stroke-width="4"/><path d="M294 120 l-16 -2 l8 -12 z" fill="#0F1B33"/>
          <text x="248" y="92" font-size="22" fill="#0F1B33" text-anchor="middle">link?</text></g></svg>
        <p>Decides whether a new box <b>belongs to an existing track</b>. ByteTrack setting <b>match_thresh = 0.86</b>, tuned once and frozen — <b>not</b> changed by AC-MOT.</p></div>
    </div>''')]

# =====================================================================================
# 7. METRICS (practical)
# =====================================================================================
GRID = '''<svg viewBox="0 0 1280 250" width="100%" height="236"><g font-family="Inter,Helvetica" font-weight="800" text-anchor="middle">
      <g font-size="22" fill="#64748B"><text x="310" y="26">frame 1</text><text x="510" y="26">frame 2</text><text x="710" y="26">frame 3</text><text x="910" y="26">frame 4</text><text x="1110" y="26">frame 5</text></g>
      <g font-size="24" fill="#0F1B33" text-anchor="end"><text x="200" y="85">Person A</text><text x="200" y="160">Person B</text><text x="200" y="232">Tree</text></g>
      <g stroke-width="3"><rect x="220" y="50" width="180" height="56" rx="10" fill="#DCFCE7" stroke="#16A34A"/><rect x="420" y="50" width="180" height="56" rx="10" fill="#DCFCE7" stroke="#16A34A"/><rect x="620" y="50" width="180" height="56" rx="10" fill="#DCFCE7" stroke="#16A34A"/><rect x="820" y="50" width="180" height="56" rx="10" fill="#FEE2E2" stroke="#DC2626"/><rect x="1020" y="50" width="180" height="56" rx="10" fill="#FEE2E2" stroke="#DC2626"/>
        <rect x="220" y="124" width="180" height="56" rx="10" fill="#DBEAFE" stroke="#2563EB"/><rect x="420" y="124" width="180" height="56" rx="10" fill="#DBEAFE" stroke="#2563EB"/><rect x="620" y="124" width="180" height="56" rx="10" fill="#F8FAFC" stroke="#94A3B8" stroke-dasharray="8 6"/><rect x="820" y="124" width="180" height="56" rx="10" fill="#DBEAFE" stroke="#2563EB"/><rect x="1020" y="124" width="180" height="56" rx="10" fill="#DBEAFE" stroke="#2563EB"/>
        <rect x="820" y="196" width="180" height="50" rx="10" fill="#FEF3C7" stroke="#D97706"/></g>
      <g font-size="26"><text x="310" y="87" fill="#14532D">ID 1</text><text x="510" y="87" fill="#14532D">ID 1</text><text x="710" y="87" fill="#14532D">ID 1</text><text x="910" y="87" fill="#7F1D1D">ID 3</text><text x="1110" y="87" fill="#7F1D1D">ID 3</text>
        <text x="310" y="161" fill="#1E3A8A">ID 2</text><text x="510" y="161" fill="#1E3A8A">ID 2</text><text x="710" y="161" fill="#64748B">missed</text><text x="910" y="161" fill="#1E3A8A">ID 2</text><text x="1110" y="161" fill="#1E3A8A">ID 2</text>
        <text x="910" y="230" fill="#92400E">false box</text></g></g></svg>'''

met = []
met.append(page(1, 'Metrics example', 'Tracking metrics · 1 of 5 — the example', 'One Small Tracking Example', f'''
    <div class="card" style="padding:8px 18px">{GRID}</div>
    <div class="g4 grow" style="gap:14px">
      <div class="kpi"><div class="l">real appearances (GT)</div><div class="v">10</div><div class="s">2 people × 5 frames</div></div>
      <div class="kpi"><div class="l">missed (FN)</div><div class="v bad">1</div><div class="s">B in frame 3</div></div>
      <div class="kpi"><div class="l">false box (FP)</div><div class="v bad">1</div><div class="s">tree in frame 4</div></div>
      <div class="kpi"><div class="l">ID switch (IDS)</div><div class="v warn">1</div><div class="s">A: ID 1 → ID 3</div></div>
    </div>
    <div class="tc">{ILL}</div>'''))

met.append(page(1, 'Metrics MOTA', 'Tracking metrics · 2 of 5 — MOTA', 'MOTA: Overall Tracking Errors', f'''
    <div class="meaning"><div class="tag">What it measures</div><p>MOTA (Multiple Object Tracking Accuracy) counts <b>all tracking errors together</b> — misses, false boxes and ID switches — against the number of real objects.</p></div>
    <div class="card tc" style="padding:12px 20px"><div class="xeq">MOTA = 1 − ( FN + FP + IDS ) ÷ GT</div></div>
    <div class="row grow ac" style="gap:24px">
      <div class="card col center grow" style="gap:4px"><div class="ex-label">Our example</div><div class="xeq">1 − ( <span class="hl">1</span> + <span class="hl">1</span> + <span class="hl">1</span> ) ÷ 10</div><div class="xdown">↓</div><div class="xeq">= 1 − 0.30 = <b>0.70</b></div></div>
      <div class="card col" style="flex:0 0 560px;gap:8px"><h3>Practical reading</h3><ul class="clean"><li>higher is better; 1.00 = no errors</li><li>one number for everything</li><li class="bad">it cannot tell <b>which</b> error happened</li></ul></div>
    </div>'''))

met.append(page(1, 'Metrics IDF1', 'Tracking metrics · 3 of 5 — IDF1', 'IDF1: Identity Consistency', f'''
    <div class="meaning"><div class="tag">What it measures</div><p>IDF1 (Identity F1 score) checks <b>how much of the time each person keeps the right ID</b>. Each real person is matched to its best predicted ID over the whole video.</p></div>
    <div class="card tc" style="padding:10px 20px"><div class="xeq">IDF1 = 2·IDTP ÷ ( 2·IDTP + IDFP + IDFN )</div></div>
    <div class="g3 grow" style="gap:16px">
      <div class="card col" style="gap:6px"><div class="ex-label">IDTP · correct-ID boxes</div><p>A ↔ ID 1 in 3 frames<br>B ↔ ID 2 in 4 frames</p><div class="xeq">IDTP = <b>7</b></div></div>
      <div class="card col" style="gap:6px"><div class="ex-label">IDFP · predicted boxes not matched</div><p>10 predicted boxes − 7<br>(ID 3 twice, the false box)</p><div class="xeq">IDFP = <b>3</b></div></div>
      <div class="card col" style="gap:6px"><div class="ex-label">IDFN · real boxes not matched</div><p>10 real appearances − 7<br>(A as ID 3 twice, B missed)</p><div class="xeq">IDFN = <b>3</b></div></div>
    </div>
    <div class="card sec tc" style="padding:10px 20px"><div class="xeq">IDF1 = 14 ÷ ( 14 + 3 + 3 ) = <b>0.70</b></div></div>'''))

met.append(page(1, 'Metrics HOTA', 'Tracking metrics · 4 of 5 — HOTA', 'HOTA: Balanced Detection and Association', f'''
    <div class="meaning"><div class="tag">What it measures</div><p>HOTA (Higher Order Tracking Accuracy) balances two questions: <b>did we detect the objects?</b> (DetA) and <b>did we keep them linked correctly?</b> (AssA).</p></div>
    <div class="card tc" style="padding:12px 20px"><div class="xeq">HOTA = √( DetA × AssA )</div></div>
    <div class="g2 grow" style="gap:22px">
      <div class="card col" style="gap:8px;border-top:6px solid #2563EB"><h3>DetA · detection</h3><div class="xeq sm">DetA = TP ÷ ( TP + FN + FP )</div><p>Example: 9 detected appearances, 1 missed, 1 false box</p><div class="xeq">9 ÷ 11 ≈ <b>0.82</b></div></div>
      <div class="card col" style="gap:8px;border-top:6px solid #7C3AED"><h3>AssA · association</h3><p>Person A is split into <b>two IDs</b> (1 and 3), so A’s association is only partly correct → AssA goes down.</p><p>If either DetA or AssA is low, HOTA is low.</p></div>
    </div>
    <p class="tc small muted">The official HOTA averages over many overlap levels; this page shows the idea, not the full calculation.</p>'''))

met.append(page(1, 'Metrics IDS', 'Tracking metrics · 5 of 5 — IDS', 'IDS: Counting Identity Switches', f'''
    <div class="meaning"><div class="tag">What it measures</div><p>IDS (identity switches) = <b>how many times a real object suddenly gets a different ID</b>. Lower is better.</p></div>
    <div class="g2 grow" style="gap:22px">
      <div class="card col" style="gap:8px;border-top:6px solid var(--bad)"><h3>Person A → 1 switch</h3><div class="xchain" style="justify-content:flex-start"><span class="pill good">ID 1</span><span class="pill good">ID 1</span><span class="pill good">ID 1</span><span>→</span><span class="pill bad">ID 3</span><span class="pill bad">ID 3</span></div><p>The ID changes once, at frame 4 → <b>IDS = 1</b>.</p></div>
      <div class="card col" style="gap:8px;border-top:6px solid var(--good)"><h3>Person B → 0 switches</h3><div class="xchain" style="justify-content:flex-start"><span class="pill sec">ID 2</span><span class="pill sec">ID 2</span><span class="pill">missed</span><span class="pill sec">ID 2</span><span class="pill sec">ID 2</span></div><p>B is missed once (that is an <b>FN</b>), but comes back with the <b>same ID</b> → no switch.</p></div>
    </div>
    <div class="callout"><b>In this example:</b> MOTA 0.70 (all errors) · IDF1 0.70 (identity) · IDS 1 (switch count) — each metric looks at a different part of the same tracking result.</div>'''))

# =====================================================================================
# 8. V1 vs V2 (frozen metrics bound from results.js)
# =====================================================================================
def row(label, path, dec, better_v1):
    b = lambda sys_: f'<td class="{"best" if (sys_ == "v1") == better_v1 else ""}" data-bind="{path.format(sys_)}"{" data-dec=%s" % dec if dec is not None else ""}>…</td>'
    return f'<tr><td>{label}</td>{b("v1")}{b("v2")}<td style="text-align:left" class="strong">{"V1" if better_v1 else "V2"}</td></tr>'

def cmp_table(prefix, v1i, v2i):
    p = lambda k: prefix + '{}' + '.' + k
    rows = ''
    for label, key, dec, v1better in (('MOTA ↑', 'mota', 3, True), ('HOTA ↑', 'hota', 3, True), ('IDF1 ↑', 'idf1', 3, True), ('IDS ↓', 'ids', None, False), ('FPS ↑', 'fps', 3, False)):
        cell = lambda idx, good: f'<td class="{"best" if good else ""}" data-bind="{prefix}{idx}.{key}"' + (f' data-dec="{dec}"' if dec is not None else '') + '>…</td>'
        rows += f'<tr><td>{label}</td>{cell(v1i, v1better)}{cell(v2i, not v1better)}<td style="text-align:left" class="strong">{"V1" if v1better else "V2"}</td></tr>'
    return ('<table class="tbl" style="font-size:30px"><tr><th style="text-align:left">Metric</th><th>V1</th><th>V2</th><th style="text-align:left">Better here</th></tr>' + rows + '</table>')

v12 = []
v12.append(page(7, 'V1 vs V2 test', 'V1 vs V2 · 1 of 3 — test set', 'V1 vs V2 on the Test Set', f'''
    <div class="meaning"><div class="tag">The main idea</div><p><b>V1</b> wins the <b>quality</b> metrics; <b>V2</b> wins <b>identity switches and speed</b>. Neither wins everything.</p></div>
    {cmp_table('testdev.rows.', 2, 3)}
    <div class="tc"><span class="origin optuna">frozen systems</span> <span class="prov p-test">Test set · VisDrone2019-MOT test-dev · 17 sequences</span></div>'''))

v12.append(page(7, 'V1 vs V2 UAVDT', 'V1 vs V2 · 2 of 3 — UAVDT', 'The Same Pattern on UAVDT', f'''
    <div class="meaning"><div class="tag">The main idea</div><p>On a different drone dataset the trade-off <b>repeats</b>: V1 has higher quality, V2 has fewer ID switches and more speed than V1.</p></div>
    {cmp_table('uavdt.rows.', 1, 2)}
    <div class="tc"><span class="origin optuna">frozen systems · no tuning</span> <span class="prov p-ext">Cross-dataset test · UAVDT · separate evaluation</span></div>'''))

v12.append(page(7, 'V1 vs V2 choose', 'V1 vs V2 · 3 of 3 — how to choose', 'Two Operating Points, Not a Winner and a Loser', '''
    <div class="g2 grow" style="gap:24px">
      <div class="card col" style="gap:10px;border-top:8px solid #7C3AED"><h3 style="color:#6D28D9;font-size:34px">V1 · quality-oriented</h3>
        <ul class="clean"><li>highest MOTA, HOTA, IDF1</li><li>more ID switches than V2</li><li>pick it when <b>finding and tracking as much as possible</b> matters most</li></ul></div>
      <div class="card col" style="gap:10px;border-top:8px solid #0D9488"><h3 style="color:#0F766E;font-size:34px">V2 · identity / efficiency</h3>
        <ul class="clean"><li>fewest ID switches, fastest</li><li>lower quality metrics than V1</li><li>pick it when <b>stable IDs and speed</b> matter most</li></ul></div>
    </div>
    <div class="xchain"><span class="pill sec" style="font-size:26px">V1 = one objective + rules</span><span>vs</span><span class="pill sec" style="font-size:26px">V2 = maximize MOTA and minimize IDS, with an FPS constraint</span></div>
    <div class="callout warn"><b>V2 is not universally better than V1</b> — and V1 is not best on every metric. They are different points on the quality / identity / efficiency trade-off.</div>'''))

DECKS = [
    ('x-controller', 'Controller logic', ctrl),
    ('x-cues', 'SCI cues', cues),
    ('x-sci', 'SCI calculation', sci),
    ('x-optuna', 'Optuna V1', opt),
    ('x-regimes', 'V1 SCI ranges', reg),
    ('x-nms', 'NMS vs tracker match', nmsm),
    ('x-metrics', 'Tracking metrics', met),
    ('x-v1v2', 'V1 vs V2', v12),
]
xview = ['<!-- ============ v7: OPTIONAL DETAILED EXPLANATIONS (outside the main slide sequence) ============ -->',
         '<div class="overlay xview" id="xview" aria-label="Detailed explanation">', '<div class="xstage" id="xstage">']
for did, label, pages in DECKS:
    xview.append(f'<div class="xdeck" id="{did}" data-label="{label}">')
    xview.extend(pages)
    xview.append('</div>')
xview += ['</div>', '</div>']
XVIEW = '\n'.join(xview)
total_pages = sum(len(p) for _, _, p in DECKS)

# ------------------------------------------------------------------ buttons on main slides
BUTTONS = {
    'How we evaluate tracking': 'x-metrics|Explain the Metrics',
    'MOTA': 'x-metrics#2|Explain MOTA',
    'Identity switches': 'x-metrics#5|Explain IDS',
    'IDF1': 'x-metrics#3|Explain IDF1',
    'HOTA and FPS': 'x-metrics#4|Explain HOTA',
    'The pipeline for each frame': 'x-sci|How Is SCI Calculated?',
    'SCI from frame to score': 'x-sci|How Is SCI Calculated?',
    'Step 1: measure scene complexity': 'x-cues|Explain Each Cue',
    'Initial SCI': 'x-sci|Worked SCI Example',
    'SCI example 0.63': 'x-sci|Worked SCI Example',
    'One frame becomes one setting': 'x-controller|Explain Controller Logic',
    'Step 2: use SCI to choose settings': 'x-controller|Explain Controller Logic;x-nms|NMS vs Tracker Match',
    'Smart Calibrator exact settings': 'x-nms|NMS vs Tracker Match;x-controller|Explain Controller Logic',
    'Implementation of the calibrator': 'x-sci#2|Clip, Smooth, Stride',
    'Why Optuna': 'x-optuna|How Does Optuna Work?',
    'What Optuna changed in V1': 'x-optuna|How Does Optuna Work?',
    'One Optuna trial': 'x-optuna#2|Trial Step by Step',
    'V1 Trial 24 weights': 'x-regimes#2|How Weights Move a Frame',
    'V1 Trial 24 regimes': 'x-regimes|Why These SCI Ranges?',
    'Final test-set comparison': 'x-v1v2|V1 vs V2 Explained',
    'Reading the test-set result': 'x-v1v2|V1 vs V2 Explained',
    'Stage 3: why V2': 'x-v1v2#3|V1 vs V2 Explained',
    'UAVDT with zero tuning': 'x-v1v2#2|V1 vs V2 on UAVDT',
}

html = IDX.read_text(encoding='utf-8')
for title, spec in BUTTONS.items():
    pat = re.compile(r'(<section class="slide[^"]*"[^>]*data-title="' + re.escape(title) + r'")')
    html, n = pat.subn(r'\1 data-explain="' + spec.replace('\\', '') + '"', html)
    if n != 1:
        sys.exit(f'button target not found once: {title} ({n})')
html = must_replace(html, '</main>\n</div>', '</main>\n</div>\n' + XVIEW, 'xview insert')
html = must_replace(html, 'Tracking (v6)</title>', 'Tracking (v7)</title>', 'title')
IDX.write_text(html, encoding='utf-8')

# ------------------------------------------------------------------ engine
js = JS.read_text(encoding='utf-8')
js = must_replace(js,
    "    var n = document.createElement('span'); n.className = 'num'; n.textContent = (i + 1) + ' / ' + N;",
    "    (s.getAttribute('data-explain') || '').split(';').forEach(function (item) {\n"
    "      if (!item) return;\n"
    "      var p = item.split('|'), b = document.createElement('button');\n"
    "      b.type = 'button'; b.className = 'xbtn'; b.setAttribute('data-x', p[0]);\n"
    "      b.title = 'Open a detailed explanation (Esc returns to this slide)';\n"
    "      b.innerHTML = '<span class=\"xi\">?</span>' + p[1];\n"
    "      f.appendChild(b);\n"
    "    });\n"
    "    var n = document.createElement('span'); n.className = 'num'; n.textContent = (i + 1) + ' / ' + N;",
    'footer buttons')
js = must_replace(js,
    "    if (e.target.closest('.ex-btn')) { openExplain(); return; }",
    "    var xb = e.target.closest('.xbtn');\n"
    "    if (xb) { var xt = xb.getAttribute('data-x').split('#'); openX(xt[0], xt[1] ? +xt[1] - 1 : 0); return; }\n"
    "    if (e.target.closest('.ex-btn')) { openExplain(); return; }",
    'stage click')
ENGINE = r'''
  /* ------------------------------------------------ v7: optional detailed explanations
     Pages live in #xstage, outside the main slide list: they never appear in Next / Previous,
     do not change slide numbers, and closing returns to the slide that opened them. */
  var xview = document.getElementById('xview'), xstage = document.getElementById('xstage');
  var xdeck = null, xpages = [], xi = 0, xFrom = -1;
  function fitX() {
    if (!xstage) return;
    var s = Math.min(window.innerWidth / W, window.innerHeight / H);
    xstage.style.transform = 'translate(-50%,-50%) scale(' + s + ')';
  }
  window.addEventListener('resize', fitX);
  if (xstage) {
    $$('.xdeck', xstage).forEach(function (d) {
      var pages = $$('.xpage', d), label = d.getAttribute('data-label') || 'Detailed explanation';
      pages.forEach(function (p, i) {
        p.classList.add('slide');
        var bar = document.createElement('div'); bar.className = 'xnav';
        bar.innerHTML = '<button class="xback" type="button">← Back to main slide <span class="xfrom"></span></button>' +
          '<span class="xtag">Detailed explanation · ' + label + '</span>' +
          '<span class="xpager"><button class="xprev" type="button" aria-label="Previous part">‹</button>' +
          '<span class="xcount">' + (i + 1) + ' / ' + pages.length + '</span>' +
          '<button class="xnext" type="button" aria-label="Next part">›</button></span>';
        p.appendChild(bar);
      });
    });
    bindAll(xstage);
  }
  function xShow(i) {
    if (!xpages.length) return;
    xi = Math.max(0, Math.min(xpages.length - 1, i));
    xpages.forEach(function (p, j) { p.classList.toggle('active', j === xi); p.classList.toggle('past', j < xi); });
    $$('.xprev', xdeck).forEach(function (b) { b.disabled = xi === 0; });
    $$('.xnext', xdeck).forEach(function (b) { b.disabled = xi === xpages.length - 1; });
  }
  function openX(id, pageIndex) {
    var d = document.getElementById(id);
    if (!d || !xview) return;
    closeOverlays();
    if (xdeck) xdeck.classList.remove('open');
    xdeck = d; xpages = $$('.xpage', d); xFrom = cur;
    $$('.xfrom', d).forEach(function (e) { e.textContent = '(slide ' + (cur + 1) + ')'; });
    $$('video', slides[cur]).forEach(function (v) { v.pause(); });
    d.classList.add('open'); xview.classList.add('open'); fitX(); xShow(pageIndex || 0);
  }
  function closeX() {
    if (!xview || !xview.classList.contains('open')) return false;
    xview.classList.remove('open');
    if (xdeck) xdeck.classList.remove('open');
    xpages.forEach(function (p) { p.classList.remove('active', 'past'); });
    xdeck = null; xpages = [];
    if (xFrom > -1 && xFrom !== cur) go(xFrom);
    return true;
  }
  window.ACMOT_X = { open: openX, close: closeX, show: function (i) { xShow(i); } };
  if (xview) xview.addEventListener('click', function (e) {
    if (e.target.closest('.xback') || e.target === xview) closeX();
    else if (e.target.closest('.xprev')) xShow(xi - 1);
    else if (e.target.closest('.xnext')) xShow(xi + 1);
  });
  document.addEventListener('keydown', function (e) {
    if (!xview || !xview.classList.contains('open')) return;
    var k = e.key;
    if (k === 'f' || k === 'F') return;
    e.stopImmediatePropagation();
    if (k === 'Escape' || k === 'Backspace') { e.preventDefault(); closeX(); }
    else if (k === 'ArrowRight' || k === 'PageDown' || k === ' ' || k === 'ArrowDown') { e.preventDefault(); xShow(xi + 1); }
    else if (k === 'ArrowLeft' || k === 'PageUp' || k === 'ArrowUp') { e.preventDefault(); xShow(xi - 1); }
  }, true);

  /* ------------------------------------------------ v3: fit each slide body above its strip */'''
js = must_replace(js, "\n  /* ------------------------------------------------ v3: fit each slide body above its strip */", ENGINE, 'engine insert')
JS.write_text(js, encoding='utf-8')

# ------------------------------------------------------------------ styles
CSS_ADD = r'''

/* ================= v7: optional detailed explanations ================= */
.s-foot .xbtn{margin-left:auto;flex:0 0 auto;display:inline-flex;align-items:center;gap:9px;border:2px solid var(--sec);background:#fff;color:var(--sec);
  font-weight:850;font-size:19px;border-radius:999px;padding:4px 16px 4px 5px;cursor:pointer;line-height:1.2;box-shadow:var(--shadow-sm);transition:background .15s,transform .15s;white-space:nowrap}
.s-foot .xbtn ~ .xbtn{margin-left:0}
.s-foot .xbtn ~ .num{margin-left:14px}
.s-foot .xbtn:hover{background:var(--sec-t);transform:translateY(-1px)}
.s-foot .xbtn .xi{display:grid;place-items:center;width:28px;height:28px;border-radius:50%;background:var(--sec);color:#fff;font-size:18px;font-weight:900}
.xview{background:rgba(15,27,51,.62);z-index:85}
.xview.open{animation:xfade .28s ease}
@keyframes xfade{from{opacity:0}to{opacity:1}}
.xstage{position:absolute;left:50%;top:50%;width:1600px;height:900px;transform-origin:center center;background:#fff;overflow:hidden;border-radius:6px;box-shadow:0 30px 80px -20px rgba(0,0,0,.55)}
.xdeck{display:none}.xdeck.open{display:block}
.xpage .s-head{top:84px}
.xpage .s-body{top:214px;bottom:28px}
.xnav{position:absolute;left:60px;right:60px;top:18px;display:flex;align-items:center;gap:16px;z-index:5}
.xback{font-family:inherit;font-size:22px;font-weight:850;color:#fff;background:var(--sec);border:0;border-radius:999px;padding:10px 22px;cursor:pointer;box-shadow:var(--shadow-sm)}
.xback:hover{filter:brightness(1.08)}
.xback .xfrom{font-weight:650;opacity:.85}
.xtag{font-size:17px;font-weight:850;letter-spacing:.1em;text-transform:uppercase;color:var(--sec);background:var(--sec-t);padding:6px 14px;border-radius:999px}
.xpager{margin-left:auto;display:flex;align-items:center;gap:10px}
.xpager button{width:50px;height:50px;border-radius:50%;border:2px solid var(--line2);background:#fff;font-size:32px;line-height:1;cursor:pointer;color:var(--ink);font-family:inherit}
.xpager button:disabled{opacity:.3;cursor:default}
.xcount{font-size:22px;font-weight:800;color:var(--ink2);min-width:74px;text-align:center}
.xeq{font-family:var(--math);font-size:38px;line-height:1.25;color:var(--ink)}
.xeq.sm{font-size:30px}
.xeq.good{color:var(--good)}.xeq.bad{color:var(--bad)}
.hl{background:#FEF08A;border-radius:6px;padding:0 6px}
.xdown{font-size:32px;line-height:1;color:var(--muted);text-align:center;font-weight:800}
.xchain{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:10px 12px;font-size:26px;font-weight:700;color:var(--ink2)}
.xsteps{align-items:stretch;gap:2px}.xsteps .node{font-size:24px;padding:8px 14px}
.origin{display:inline-block;font-size:17px;font-weight:850;letter-spacing:.03em;padding:3px 12px;border-radius:999px;vertical-align:middle;margin:2px 4px;font-family:var(--font)}
.origin.manual{background:#FEF3C7;color:#92400E}.origin.empirical{background:#E0E7FF;color:#3730A3}
.origin.optuna{background:#DCFCE7;color:#166534}.origin.illus{background:#F1F5F9;color:#475569}
@media print{.s-foot .xbtn,.xview{display:none!important}}
'''
CSS.write_text(CSS.read_text(encoding='utf-8') + CSS_ADD, encoding='utf-8')

# ------------------------------------------------------------------ README
rd = README.read_text(encoding='utf-8')
README.write_text('''# AC-MOT — Interactive Master's Presentation (v7: optional detailed explanations)

## Version 7

v7 is a copy of v6 (earlier versions unchanged). The 78 main slides and their order are the same.
Difficult topics now have **optional** detailed explanations that open only when you click a footer
button such as “Explain Controller Logic”. They live outside the slide sequence (Next / Previous and
slide numbers are unaffected). Inside an explanation: ‹ › or the arrow keys change the part;
**← Back to main slide**, **Esc** or **Backspace** returns to the exact slide that opened it.
Every page labels where numbers come from: manually designed · empirical design constant ·
optimization-selected (V1 Trial 24) · illustration. Build script: `build_v7.py` (session scratchpad).

''' + rd, encoding='utf-8')

print('decks:', len(DECKS), 'explanation pages:', total_pages)
print('buttons on main slides:', len(BUTTONS))
