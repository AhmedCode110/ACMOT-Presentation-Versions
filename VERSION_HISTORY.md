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
| v09 | 75 | 51 (16 topics) | Complete advanced explanations, each opening at part 1 |
| v10 | 75 | 60 (17 topics) | Slide 7: “Explain each challenge” — one part per tracking challenge, with a picture |
| v11 | 75 | 60 (17 topics) | No mention of the earlier seminar or old superseded results; fair-comparison reason for the five classes |
| v12 | 75 | 60 (17 topics) | Outline slide laid out like the PowerPoint deck |
| v13 | 75 | 59 (17 topics) | Challenge explanations in easy English; fast-motion page removed |
| v14 | 75 | 59 (17 topics) | Datasets slide moved before the MOT17 results |
| v15 | 93 | 59 (17 topics) | Full research story from Section III: baseline → initial AC-MOT → V1 → V2 → bootstrap → UAVDT → literature comparison and protocol audit |
| v16 | 90 | 59 (17 topics) | Section IX removed; detectors through the ages; problem and AC-MOT explained step by step in simple words |
| v17 | 91 | 59 (17 topics) | Cue pictures before the cue formulas; simple clue slides (Canny, brightness, Laplacian explained); too-high / too-low examples for the detector settings |
| **v18** | **91** | **59 (17 topics)** | **Richer AC-MOT idea slide (each block explains what happens, output and detail slides); no “NEW” tags — current** |

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

## v18-rich-acmot-idea-no-new-tags  ← current
- Request: the pipeline blocks on the AC-MOT idea slide should explain more, in simple words, so the idea is exactly clear, with the details on the next slides; and no yellow “NEW” tag on any slide.
- “The Idea: Measure the Scene, Then Set the Detector” rebuilt: six blocks (Frame → Step 1 Measure / Scene Analyzer → Step 2 Score / SCI → Step 3 Set / Smart Calibrator → Detector YOLOv8n → Tracker ByteTrack), each with what happens, its output, and “details: slides x–y”; a loop note (boxes reused in Step 1 for the next frame) and a worked example (SCI 0.63 → lower confidence, input 832). Blocks reveal step by step.
- All “NEW” tags removed (4 yellow tags: Our own speed test, Benchmark datasets, VisDrone benchmark ×2; the purple NEW badges on the idea slide are gone with the rebuild).
- Totals unchanged: 91 main slides. Build script: `tools/build_v18.py`.

## v17-simple-cues-and-setting-examples
- Request: put the cue-pictures slide before the slide that explains how the five cues are calculated; explain “Canny edge density ÷ 0.14, at most 1” clearly; make that slide simpler; show the problems of a too-high or too-low threshold with an object example on the right slide.
- Step 1 order now: “First, See the Clues in Real Pictures” → new “Two Clues From the Detector’s Boxes” (Crowd: count ÷ 30, stop at 1, examples 3/15/30/45 boxes; Tiny: share of boxes under 32 × 32 px, examples 2 of 10 and 7 of 10) → new “Three Clues From the Picture Itself” (Canny draws edges where brightness changes sharply, edge density = edge pixels ÷ all pixels, ÷ 0.14 → 14% already fully busy, examples 0.021 → 0.15 and 0.295 → 1; brightness 0–255, average below 80 = night, 110.6 → 0 and 40.5 → 1; Laplacian reacts to sharp details, variance below 180 = blurry, 4,074 → 0 and 4 → 1). The old five-cue table slide was replaced by these two slides; constants note and references kept.
- “Step 3: The Three Detector Settings We Change” now shows too high / too low for each setting with an illustrated example (tiny car scoring 0.4 vs thresholds 0.5 / 0.2 and a shadow at 0.25; two boxes on one car overlapping 0.6 vs NMS limits 0.45 / 0.7 and two close people at 0.5; a few-pixel person at input 640 vs 832). Examples labelled as illustrations.
- Totals: 91 main slides · 17 topics · 59 explanation pages. Build script: `tools/build_v17.py`.

## v16-clear-problem-acmot-detector-history
- Request: remove the literature-comparison / protocol-audit part (author chose: all of Section IX); add Related Work slides on detectors through the ages (oldest → newest: algorithm, how it works, result, traditional or deep learning, best, strengths and weaknesses — short); present the problem simply and clearly; explain AC-MOT in a clear, smooth order; keep the comparison numbers.
- Removed: Section IX (DroneMOT comparison, protocol audit, official protocol, van class, two kinds of results, correction freeze), the “Proven and open” slide, the third row of “The story in one line”, the official-VisDrone row in the conclusion and the official re-evaluation box in future work. Section X became Section IX.
- Related Work: 3 new slides after the divider — “Object Detectors Through the Ages” (traditional 2001–2012 → two-stage 2014–2015 → one-stage 2016 → transformers 2020), “Before Deep Learning: Traditional Detectors” (Viola–Jones, HOG + SVM, DPM — how it works, good at, weak at; no scores, as chosen by the author), “Deep Learning Detectors: From Careful to Fast” (R-CNN … RF-DETR-S with family, how it works, mAP and time only from the survey table, strong / weak).
- Section III (problem) rewritten in simple words: “One Drone Video, Very Different Frames”, new “The Problem: The Detector Never Changes Its Settings”, simpler “Main Question” with the three settings explained in one line each; baseline slide unchanged.
- Section IV (AC-MOT) re-ordered and relabelled: The Idea (driver analogy, pipeline Step 1 Measure → Step 2 Score → Step 3 Set) → Step 1: five clues (simpler table: question / how we measure / value) → three clues on pictures → Step 2: SCI meaning → formula and weights → example 0.63 → stable and cheap → all steps together → Step 3: new “The Three Detector Settings We Change” → confidence in detail → SCI to settings → exact rules → what changes and what never changes.
- All numbers unchanged. Outline rebuilt for 9 sections. Totals: 90 main slides · 17 topics · 59 explanation pages. Build script: `tools/build_v16.py`.

## v15-full-research-story
- Request: rebuild from the problem / AC-MOT onward exactly in the author's new research story (supplied 2026-09-14, in Arabic), with the author's numbers, and add graphs and charts.
- Sections I–II unchanged. New structure (10 sections, Outline rebuilt in the PowerPoint style with 5 rows per column):
  III Problem & baseline (new baseline slide: YOLOv8n → ByteTrack, 19.729 / 28.430 / 32.724 / 1235 / 36.53, “not ByteTrack’s global score”) ·
  IV AC-MOT design (unchanged slides) ·
  V Setup & first result (new: Initial AC-MOT vs Baseline, 23.236 vs 19.729, +3.51 pp, IDS 1235 → 1061, charts) ·
  VI V1 (new: “Why these weights?”; V1 validation shown as 23.038 / 36.110 / 40.758 / 270 / 37.17 with rule IDS ≤ 271 (Old-A3) and 50 trials; weights shown as 0.129 / 0.222 / 0.434 / 0.054 / 0.161; new: V1 on the test set with V1 − Baseline row +7.220 pp / +5.405 / +8.822 / −51 / +2.46; new: the ID-switch problem — IDS was a constraint, not an objective) ·
  VII V2 (new: trade-off in simple words; V2 search 50 planned / 49 completed, balanced 50% MOTA + 50% IDS → Trial 22; V1 vs V2 on validation 19.330 / 31.651 / 34.226 / 168 / 51.41; V2 on the test set with V2 vs V1 losses and gains incl. about 5,397 fewer FP; V1 or V2?) ·
  VIII Statistics & UAVDT (new: paired bootstrap 5,000 resamples, V1 − Baseline MOTA +7.2195 [5.4362, 9.2934], HOTA +5.4051 [4.1273, 6.9022], IDF1 +8.8220 [6.9005, 11.0537]; IDS V1 51 [−114, 219] not significant, V2 316 [175, 470] significant; zero-tuning question; UAVDT slide now states V1 vs Baseline +3.558 / +4.305 / +6.565 / −237) ·
  IX Literature comparison & protocol audit (new: DroneMOT ICRA 2024 ByteTrack 25.1 / 40.8 / 1590 vs V1 old protocol; audit table old protocol vs official; official VisDrone protocol (class-aware, IoU 0.5, ignore regions 0 and 11); COCO has no van; two kinds of results; correction freeze) ·
  X Conclusion (new: story in one line; proven vs still open; contributions #4, conclusion table and future work updated with the official re-evaluation).
- Removed from the main slides: original ablation OLD-A0…A3 (fair-design slide, table, component charts), the combined four-system test slide and its reading slide. “Old AC-MOT” renamed “Initial AC-MOT” everywhere.
- New charts: init-quality/ids/fps, v1b-quality/ids/fps, td3-quality/ids/fps, val-quality/ids/fps, boot-v1q, boot-ids2, lit-quality, lit-ids. Abbreviation expander no longer writes full names inside table headers.
- Totals: 93 main slides · 17 topics · 59 explanation pages. Build script: `tools/build_v15.py`.

## v14-datasets-before-mot17-results
- Request: in Related Work, show the dataset slide before slide 25, so no dataset (MOT17) is used before it is introduced.
- “Benchmark datasets” moved from slide 28 to slide 25. New order: 24 ByteTrack baseline · 25 Benchmark datasets · 26 Published MOTA on MOT17 · 27 Quick question · 28 ID switches on MOT17 · 29 Survey conclusions.
- Datasets speaker notes end with a bridge to the next slide (published results on MOT17). Slide content unchanged; section II range (17–29) unchanged. Build script: `tools/build_v14.py`.

## v13-simple-english-challenges
- Request: the words on the challenge explanations were hard — use easy English and simple words; then remove “Fast Motion: A Big Jump Between Frames”.
- All “Explain each challenge” pages rewritten with short, simple sentences (e.g. motion blur: “When the object or the camera moves fast, the picture becomes blurry, like a shaky photo.”). Card heading “Why it breaks tracking” → “Why it is a problem”; picture labels and origin tags simplified.
- Fast-motion page, its drawing and the “fast motion” pill on slide 7 removed → 8 pages (overview “Seven Things That Make Tracking Hard” + 7 challenges). Same pictures and layout.
- Totals: 75 main slides · 17 topics · 59 explanation pages. Build script: `tools/build_v13.py`.

## v12-outline-like-ppt
- Request: make the Outline like the one in the PowerPoint slides (latest version).
- Slide 2 rebuilt after the Outline slide of the PowerPoint deck (`DONT TOUCH/b9_claude`): two columns of four rows; each row = Roman numeral, section title, subtitle, “slides X - Y”; light rows with thin dividers, navy numerals. Rows stay clickable (jump to the section).
- Titles and subtitles as in the PowerPoint; only the VII subtitle changed from “Sweeps, Optuna search and the final result” to “Optuna search, test set, V2 and UAVDT” because sweeps are no longer in the deck. Slide ranges computed from the current deck: I 3–16 · II 17–29 · III 30–32 · IV 33–45 · V 46–52 · VI 53–56 · VII 57–70 · VIII 71–75.
- The abbreviation expander skips the outline so its text stays exactly as written. Build script: `tools/build_v12.py`.

## v11-remove-old-seminar-mentions
- Request: remove anything about the earlier seminar and old wrong/superseded data — do not mention it at all.
- Slide 48: removed the note “The first seminar used a 12-sequence subset (4,106 frames) …”.
- Slide 45 notes: removed “Later finding: the optimizer showed this NMS direction is not always right”.
- Slides 66–67: “historical” wording removed (“final test-set comparison”; Old AC-MOT FPS shown as 36.528 → 41.957 from the same table).
- “Step 1: measure scene complexity” main idea corrected: limits are our own design constants, the first weights were hand-set, V1 later learned new weights (the old text wrongly said the limits were replaced).
- Slide 49 “Why exactly these five”: new first reason — the reference papers on this dataset use the same classes, so the comparison is fair (also in the speaker notes).
- Removed from the v11 files (never shown, all old material): `results.js` blocks `devAblation`, `devDerived`, `historical` (TRK_MATCH_090), `u2mot`, cue-percentile `calibration`, seminar comments; unused chart functions for them and the U2MOT glossary entry in `script.js`; the U2MOT setup script in `index.html`; 32 unused `meaning.js` texts from old slides; unused `explanations.js` and `explain_inline.js`; `_source/` (copies of the seminar deck); the outdated inner `HANDOFF_PROMPT.md`. README rewritten.
- Totals unchanged: 75 main slides · 17 topics · 60 explanation pages · 46 buttons on 40 slides. Build script: `tools/build_v11.py`.

## v10-challenges-explained
- Request: a button on slide 7 that explains every tracking challenge, with a picture for each.
- New explanation topic `x-challenges` (9 pages): overview of the 8 challenges, then occlusion, small objects, crowds, camera motion, low light, motion blur, fast motion, look-alike objects. Each page: what it means · why it breaks tracking · example · picture.
- Pictures reuse existing deck figures only: occlusion = public DeepSORT + YOLOv5 demo frames (id 1 → id 8, labelled “not our system”); small objects / blur / night = `generated/` cue pictures (blur added on purpose, labelled); crowds, low light, look-alike = real frames (picture only, no numbers); camera motion and fast motion = drawings labelled “illustration”.
- No numbers added or changed; AC-MOT is not named in this Section I explanation. Slide 9 left unchanged (it already says green = real object, red = detector box).
- Totals: 75 main slides · 17 topics · 60 explanation pages · 46 buttons on 40 slides.
- Build script: `tools/build_v10.py`.

## v09-complete-advanced-explanations
- Request: explain every advanced detail on demand, main slides unchanged.
- New explanation topics: IoU computation and NMS algorithm; precision–recall table, AP area and COCO mAP; full HOTA (DetA + AssA worked example); FPS budget; detector benchmark columns; ByteTrack in depth (Kalman prediction, two-round matching, track life cycle, every setting); evaluation in depth; ablation metric by metric (interpretations labelled); V2 multi-objective / Pareto search; SCI frame preparation.
- Totals: 75 main slides · 16 topics · 51 explanation pages · 45 buttons on 39 slides.
- Every explanation button opens at **part 1**.
- Build script: `tools/build_v9.py`.
