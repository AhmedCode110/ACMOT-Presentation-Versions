# Version history

All versions were produced on 2026-09-14 (v01 existed before this session). Each version is a full copy
of the previous one plus the listed changes; older versions were never overwritten.

| Version | Main slides | Explanation pages | Summary |
|---|---|---|---|
| v01 | 82 | — | Original redesigned interactive deck (reference only) |
| v02 | 96 | pop-up per slide | Seminar-deck content in simple English, PowerPoint-size fonts, “Explain + example” pop-up |
| v03 | 96 | — | Explanation + example strip built into every slide |
| v04 | 96 | — | Abbreviations written in full, metric slides start with the meaning, no AC-MOT before Section IV |
| v05 | 94 | — | Big “main idea” box on every slide, honest SCI number sources, no code boxes |
| v06 | 78 | — | The original AC-MOT research story in chronological order |
| v07 | 78 | 27 (8 topics) | Optional detailed explanations + full-screen presentation mode |
| v08 | 75 | 27 (8 topics) | U2MOT removed — the story ends with V2 and UAVDT |
| **v09** | **75** | **51 (16 topics)** | **Complete advanced explanations, each opening at part 1 — current** |

---

## v01-original-reference
- The first interactive HTML deck (redesigned content, light theme, charts, notes, overview, lightbox, tabs, videos).
- Kept only as a reference. Not edited.

## v02-seminar-content-simple-english
- Content follows the author’s seminar deck `b9_claude.key` slide by slide, in simpler English; new material marked **NEW**.
- Visual check of all slides; fixed image-caption overlap (slides 5, 7, 14) and a clipped SCI formula (slide 39).
- Fonts raised to presentation size (body ≈ 24–27 px on the 1600 × 900 stage, titles 52 px); chart labels enlarged.
- “Explain + example” button and **E** key: a large pop-up per slide (`assets/data/explanations.js`), tagged made-up / real / published numbers.

## v03-explanation-strip-on-slides
- Request: merge the explanation into the slide. Each slide got an “In simple words + Example” strip (`assets/data/explain_inline.js`).
- Engine auto-fits each slide body above the strip (never below 0.72 scale). Pop-up removed.
- Quick-question slides give hints without answers; title and Thank-you slides stay clean.

## v04-abbreviations-and-meaning-first
- Full name written next to the first abbreviation on each slide (glossary `ABBR` in `script.js`); titles, formulas, code and charts untouched.
- Slide 9 (IoU vs NMS) rebuilt with IoU 0 / 0.5 / 1 table and drawings; NMS as a step table.
- Metric slides 10–16 rebuilt: big “What it means” first, formula in words, smaller example after; strip removed there.
- AC-MOT no longer named before Section IV.

## v05-main-idea-on-every-slide
- Big “The main idea” box at the top of every content slide (`assets/data/meaning.js`); bottom strip removed.
- Slide 8 spells out every abbreviation.
- SCI constants: “Where the number comes from” column — published methods (COCO small-object size, Canny, Laplacian variance, ExDark motivation) vs our own starting values; weights marked as first guess, learned V1 weights shown.
- All algorithm / pseudo-code boxes removed (ByteTrack and evaluation as step tables; formulas as tables; two all-code slides deleted).

## v06-original-research-story
- Rebuilt in the exact chronological story supplied by the author: problem → main question → AC-MOT as a control layer → five cues (constants fixed, not chosen by Optuna) → initial SCI → **original ablation OLD-A0…A3 incl. A2R** → why Optuna → what V1 changed / did not change → one Optuna trial → V1 Trial 24 exact weights, regimes, detector parameters → V1 validation selection → final test-set comparison (Baseline, Old AC-MOT, V1, V2) → why V2 → UAVDT → (transfer section) → contributions → conclusion.
- Removed to avoid mixing experiments: older development ablation (MOTA 35.85 …), historical finalist run (TRK_MATCH_090), official-protocol slide, sweep / temporal-grid / cue-calibration slides, combined two-dataset table, V2 detail, dashboard and bootstrap slides.
- Build script: `tools/build_v6.py`.

## v07-explanations-and-present-mode
- Optional detailed explanations in a separate full-screen view (`#xstage`), outside the slide sequence: 8 topics / 27 pages — controller logic (6 parts incl. complete example), SCI cues, SCI calculation, Optuna V1, V1 SCI ranges, NMS vs tracker match, tracking metrics, V1 vs V2.
- Footer buttons on 23 main slides; **← Back to main slide**, **Esc** or **Backspace** return to the originating slide; ‹ › / arrows change parts. Number-origin tags: manually designed · empirical constant · optimization-selected · illustration.
- Presentation mode: ▶ Start button, **F** / **P**, black letterbox, hidden bar and cursor.
- Build script: `tools/build_v7.py`.

## v08-story-ends-with-v2-no-u2mot
- Request: no U2MOT anywhere. Transfer section (divider + 2 U2MOT slides), Outline card and the U2MOT phrase on the future-work slide removed; Contributions and Conclusion became Section VIII.

## v09-complete-advanced-explanations  ← current
- Request: explain every advanced detail on demand, main slides unchanged.
- New explanation topics: IoU computation and NMS algorithm; precision–recall table, AP area and COCO mAP; full HOTA (DetA + AssA worked example); FPS budget; detector benchmark columns; ByteTrack in depth (Kalman prediction, two-round matching, track life cycle, every setting); evaluation in depth; ablation metric by metric (interpretations labelled); V2 multi-objective / Pareto search; SCI frame preparation.
- Totals: 75 main slides · 16 topics · 51 explanation pages · 45 buttons on 39 slides.
- Every explanation button opens at **part 1**.
- Build script: `tools/build_v9.py`.
