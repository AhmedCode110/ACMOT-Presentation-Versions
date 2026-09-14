# AC-MOT — Interactive Master's Presentation (v6: the original AC-MOT research story)

## Version 6

v6 is a copy of v5 (all earlier versions are kept unchanged). It tells the original AC-MOT story in
chronological order, 78 slides:

1. Introduction and metrics · related work (unchanged background)
2. **The problem** — aerial frames are not equally hard; one fixed detector configuration; the main question
3. **AC-MOT as an adaptive control layer** — Frame → Scene Analyzer → SCI → Adaptive Controller → Detector → Tracker → Tracks
4. **The five SCI cues** (continuous vs binary; 30, 32×32, 0.14, 80, 180 are empirical design constants, not chosen by Optuna)
5. **Initial SCI** — hand-designed weights 0.30/0.30/0.20/0.10/0.05, clip, window 7, every 10 frames
6. **Original ablation** (OLD-A0 … OLD-A3, incl. A2R) — separate from the test set (`results.js → oldAblation`)
7. **Why Optuna** → what Optuna changed in V1 (and what it did not) → one Optuna trial → V1 Trial 24 exact weights, regimes and detector parameters → V1 validation selection
8. **Final test-set comparison** (Baseline, Old AC-MOT, V1, V2) and how to read it; why V2; Pareto front
9. **UAVDT** cross-dataset evidence (table + charts, no mixed-dataset table)
10. Separate **Transfer** section (U2MOT, metrics still shown as pending)
11. **Contributions** and **Conclusion**

Removed from v5 so that experiments are never mixed: the older development ablation slides (35.85 … MOTA),
the historical finalist run (TRK_MATCH_090), the official-protocol slide, the sweep / temporal-grid /
cue-calibration slides, the combined two-dataset table, the V2 detail, dashboard and bootstrap slides.
Rebuild script: `build_v6.py` (session scratchpad) — slide HTML for the new story lives there.

# AC-MOT — Interactive Master's Presentation (v5: big "main idea" on every slide)

## Version 5

v5 is a copy of v4 (v2, v3 and v4 are kept unchanged). The style of the metric slides is now used on
every content slide: a big **"The main idea / What it means"** box at the top, in easy words, with the
details and examples below it. The texts live in **`assets/data/meaning.js`** (keyed by `data-title`;
`r: 1` means the box replaces the slide's old one-line summary). The small bottom strip of v3/v4 is
removed. Slide 8 spells out every abbreviation in full. AC-MOT is still not named before Section IV.
No algorithm / pseudo-code boxes are shown: ByteTrack matching and the evaluation protocol are plain
step tables, SCI and calibrator formulas are tables, and the two all-code slides
(SceneAnalyzer.analyze, SmartCalibrator.params) were removed, so the deck has 94 slides. Slide 37 states
where every SCI number comes from (published method vs our own starting value) with references.

# AC-MOT — Interactive Master's Presentation (v4: abbreviations spelled out)

## Version 4

v4 is a copy of v3 (v2 and v3 are kept unchanged). Two changes:

* **Abbreviations spelled out.** The first time an abbreviation appears on a slide, its full name is
  written next to it, e.g. “IDS (identity switches)”. The glossary is the `ABBR` list near the top of
  `script.js`. It is applied to sentences first, never inside titles, formulas, code or charts, and is
  skipped when the slide already spells the full name.
* **Slide 9 (IoU vs NMS) rewritten with tables:** IoU 0 / 0.5 / 1 with small drawings, the
  poor/good/excellent picture explained (0.40 / 0.73 / 0.93), and NMS as a step-by-step table.

# AC-MOT — Interactive Master's Presentation (v3: explanation built into every slide)

## Version 3

v3 is a copy of v2 (v2 is kept unchanged in `../acmot_interactive_presentation_v2/`). Every content,
section and quick-question slide now carries its own **“In simple words + Example”** strip at the
bottom — real slide text, no pop-up. The texts live in **`assets/data/explain_inline.js`**
(`[kind, simple, example]`, keyed by the slide's `data-title`; thesis numbers are bound from
`results.js` with `B('path')`; the tag shows *made-up numbers*, *real thesis numbers* or *published
numbers*). The title and Thank-you slides stay clean. On load, the engine fits each slide body into
the space above its strip (`data-fit` on each slide shows the scale used; never below 0.72).
The E-key pop-up of v2 is removed in v3.

# AC-MOT — Interactive Master's Presentation (v2: original seminar content + new results)

## Version 2

`index.html` is the new 85-slide version. It keeps the light theme, animations,
keyboard controls, charts, speaker notes, overview, tooltips, tabs, lightbox,
and video support.

The first 47 slides restore the content and order of `b9_claude.key` in simpler
English. The remaining slides keep the verified experiment story and add the
real V1, V2, UAVDT, and U2MOT material. Simulated Trial 37 results are not used.

The original project in `../acmot_interactive_presentation/` was not replaced.

**AC-MOT: Adaptive Control for Real-Time Multi-Object Tracking**
Ahmed Gouda Ismail · Military Technical College · Computers Engineering and Artificial Intelligence Department · Cairo, Egypt

A self-contained HTML/CSS/JavaScript presentation (85 slides, light theme, 16:9). It follows the
same section order as the seminar deck `b9_claude.key`, extended with the frozen V1/V2/UAVDT
results and the ongoing U2MOT cross-pipeline study. No internet connection or libraries are needed.

---

## How to open

Double-click **`index.html`** — it opens in any modern browser (Chrome, Edge, Safari, Firefox).

Or from a terminal:

```bash
open ~/Desktop/acmot_interactive_presentation_v2/index.html
```

Tip: Chrome or Edge give the smoothest video playback. Press **F** for full screen before presenting.

## Controls

| Key / action | What it does |
|---|---|
| `→` `Space` `PgDn` `↓` | Next step (reveals the next part of a flowchart), then next slide |
| `←` `PgUp` `↑` `Backspace` | Previous step / previous slide |
| `Home` / `End` | First / last slide |
| `F` | Full-screen presentation mode |
| `O` | Slide navigator (overview by section) — click to jump |
| `E` or the **Explain + example** button (slide footer) | Large panel with the slide in simple words, a worked example and a one-line “remember”. A coloured tag says whether the example uses made-up numbers, real thesis numbers or published numbers |
| `N` | Speaker notes panel for the current slide |
| `H` or `?` | Keyboard help |
| `Esc` | Close any panel |
| Hover a dotted word | Tooltip definition of the technical term |
| Click a metric chip | Pinned definition (slide 9) |
| Click an image, chart or diagram | Enlarge it (lightbox) |
| Click an outline card (slide 2) | Jump to that section |
| Swipe left / right | Next / previous on touch screens |
| URL `index.html#52` | Open directly at slide 52 |

The control bar (bottom right) fades out while presenting; move the mouse to show it.

## Folder structure

```
acmot_interactive_presentation/
├── index.html              all 82 slides, with hidden speaker notes (<aside class="notes">)
├── styles.css              light academic theme, layout, flowchart and chart styles
├── script.js               navigation, reveal steps, notes, overview, tooltips, lightbox, SVG charts
├── assets/
│   ├── data/
│   │   ├── results.js      ← every number shown in the deck (single source of truth)
│   │   ├── cue_examples.js ← measured cue values for the example images (generated)
│   │   └── explanations.js ← “Explain + example” text for every slide (keyed by data-title)
│   ├── figures/            images and GIFs from the seminar deck
│   │   └── generated/      edge maps, grayscale and blur examples (generated)
│   └── videos/             result videos and background clips
├── charts/                 (reserved for exported chart images — charts are drawn live as SVG)
├── tools/gen_figures.py    regenerates figures/generated/ and cue_examples.js
└── README.md
```

## Where the results come from

Every results slide carries a coloured **provenance label** in its footer. Never compare numbers
that carry different labels.

| Label | Data | Source (verified) |
|---|---|---|
| Early exploratory measurement | YOLO latency table | Values recorded by the author. **Raw timing log is not archived** in the frozen evidence. |
| Development ablation | A0 → A3 | `gptCODEX_STADE/Master/AC-MOT/supervisor_package_17seq_ablation/results/final_17seq_ablation_summary_proxy_hota.csv` (clean final table; HOTA* is a proxy) — same values as the seminar deck |
| Published (survey) | detector table, MOT17 MOTA/IDS, dataset table | values collected in the IEEE ICMISI 2026 survey, as in the seminar deck |
| Cue calibration | brightness/blur/edge/crowd percentiles | `FROZEN_DEFENSIBLE_ACMOT_CONFIG.json` → `cue_calibration_summary` |
| Historical custom protocol | Baseline_Default, Full AC-MOT, TRK_MATCH_090 | repo `OFFICIAL_RESULTS` (`config/metrics.py`, demo @ `9e3cdc18`); `claudecode/VERIFICATION_REPORT.md`; `ACMOT_FROZEN_2026-09-11/00_MASTER_README` |
| Validation result | V1 Trial 24, V2 Pareto trials, V2 Trial 22 | `FROZEN_DEFENSIBLE_ACMOT_CONFIG.json`; `docs/freeze/ACMOT_FINAL_SCIENTIFIC_FREEZE_2026-09-12.md` (branch `freeze/final-after-uavdt-2026-09-12`) |
| Held-out test-dev result | Baseline, Old AC-MOT, V1, V2 + bootstrap | `FINAL_TEST_RESULTS_3WORKER.json`; freeze doc §8, §13, §14 |
| External test (UAVDT) | Baseline, V1, V2 + bootstrap | freeze doc §15–§19 |
| Published value | YOLOv8n mAP 37.3 / 3.2 M params; Optuna; TPE; U2MOT pipeline | Ultralytics model card; the cited papers |
| Reproduced U2MOT · pending | U2MOT setup | Setup as recorded by the author; **not yet in the frozen evidence; no metrics shown** |
| Planned experiment | U2MOT + AC-MOT A0–A4, official-aligned protocol | — |
| Illustration | diagrams, worked examples | — |

All AC-MOT results in this deck use the **custom class-agnostic AC-MOT TrackEval protocol**. They are
**not** official VisDrone leaderboard results.

### Values intentionally corrected or excluded

* **ByteTrack 0.5 / 0.1 / 0.6 / 30 / 0.86** — matches no archived AC-MOT tracker configuration.
  Slide 44 shows the verified profiles: default 0.25/0.10/0.25/30/0.80, tuned (SCI studies)
  0.18/0.04/0.20/45/0.86, historical final run 0.18/0.04/0.24/45/0.88.
* **V2 trials** — the study planned 50 but completed exactly **49**; no trial is invented.
* **Seminar-deck slides 67–75** ("Trial 37", draft sweep curves, W=5 grid, 15-of-50 count) showed simulated /
  non-frozen values. v2 keeps those slide ideas but shows only the real frozen V1 results.
* **U2MOT metrics** — shown as *pending* until the official evaluation finishes.

## How to update metric values later

1. Open **`assets/data/results.js`** in any text editor.
2. Change the number (e.g. `u2mot.mota`) or add rows. Keep the `prov` text accurate.
3. Save and reload the browser. Charts and numbers marked `data-bind` update automatically.

When U2MOT results arrive: fill `u2mot.mota / idf1 / ids / hota`, then edit slide 70
(`id="u2setup"` area) and slide 72 in `index.html` to replace the word *pending*, and change the
footer label from `p-pend` to a result label. Do **not** add U2MOT numbers to the custom-protocol
charts — they use a different protocol.

### Editing the “Explain + example” panels

Open **`assets/data/explanations.js`**. Each entry is keyed by the slide's `data-title` and has
`simple`, `example`, `remember` and `kind` (`toy` = made-up numbers, `real` = thesis numbers,
`pub` = published numbers, `none` = idea only). Never type a thesis result by hand there — use
`B('path.in.results.js', decimals)` so the value is read from `results.js`.

Text sizes follow presentation practice (body text about 24–27 px on the 1600 × 900 stage, titles 52 px).

To regenerate the cue figures (after changing an example image):

```bash
python3 ~/Desktop/acmot_interactive_presentation/tools/gen_figures.py
```

## Printing / PDF

Use the browser's *Print → Save as PDF* with background graphics enabled; every slide prints on
its own page with all reveal steps visible.
