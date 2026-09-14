# HANDOFF PROMPT — continue the AC-MOT interactive presentation (paste everything below into a new chat)

You are continuing work on my interactive HTML Master's presentation **“AC-MOT: Adaptive Control for Real-Time Multi-Object Tracking”** (Capt. Eng. Ahmed Gouda Ismail, Military Technical College, Electrical Engineering Branch, Computer Engineering and Artificial Intelligence Department; supervisors Dr. Tarek Ahmed Mahmoud and Dr. Mohamed S. Mohamed). I present it to an examination committee. I write in Egyptian Arabic (often Franco-Arabic); answer in simple English unless I ask otherwise. Do NOT rebuild the presentation and do NOT invent any numbers.

## 1. Where everything is

All versions: `~/Desktop/ACMOT-Presentation-Versions/`

    ACMOT-Presentation-Versions
    ├── versions
    │   ├── v01-original-reference                (82 slides, reference only)
    │   ├── v02-seminar-content-simple-english    (96)
    │   ├── v03-explanation-strip-on-slides       (96)
    │   ├── v04-abbreviations-and-meaning-first   (96)
    │   ├── v05-main-idea-on-every-slide          (94)
    │   ├── v06-original-research-story           (78)
    │   ├── v07-explanations-and-present-mode     (78)
    │   ├── v08-story-ends-with-v2-no-u2mot       (75)
    │   └── v09-complete-advanced-explanations    (75)  ← newest
    ├── current            → symlink to versions/v09-complete-advanced-explanations
    ├── README.md          → structure, controls, new-version workflow
    ├── VERSION_HISTORY.md → what changed in every version and why (read it)
    ├── SOURCE_MAP.md      → provenance of every number, constant status, open questions (read it)
    ├── HANDOFF_PROMPT.md  → this file
    └── .gitignore

Each version folder: `index.html` (slides + optional explanation pages), `styles.css`, `script.js` (engine), `assets/data/results.js` (single source of numbers), `assets/data/meaning.js` (big “main idea” boxes, loaded since v05), `assets/data/cue_examples.js`, `assets/figures/`, `assets/videos/` (5 MP4s), `tools/` (v06/v07/v09 contain `build_v6.py`, `build_v7.py`, `build_v9.py` — they still use OLD paths `~/Desktop/acmot_interactive_presentation_vN`; change ROOT before re-running), `README.md`.

Never edit, outside this folder: `~/Desktop/DONT TOUCH/` (original seminar deck `b9_claude.key`), `CLAUDECODEX/Master/macneo_wrk/ACMOT_FROZEN_2026-09-11`, `ACMOT_V1_FINAL_POST_SNAPSHOT_2026-09-12`. `~/Desktop/html versions/` is an empty leftover folder (only .DS_Store).

## 2. ABSOLUTE VERSION RULE (my explicit instruction)

- **Never modify an existing version. v01–v09 are read-only.**
- For every change: copy `current` to the NEXT folder `~/Desktop/ACMOT-Presentation-Versions/versions/v10-short-description` (then v11, v12 …), edit ONLY that copy.
- Verify it (section 7). **Only after verification** repoint `current`: `cd ~/Desktop/ACMOT-Presentation-Versions && ln -sfn versions/v10-… current`, and add a section to `VERSION_HISTORY.md` (and `SOURCE_MAP.md` if numbers/sources change).
- End every delivery with a runnable command: `open ~/Desktop/ACMOT-Presentation-Versions/current/index.html`

## 3. What v09 contains (current)

**75 main slides, 16:9 stage 1600×900, light theme.** Sections (ids sec-1…sec-8):
1 Title · 2 Outline (8 cards, clickable) · **I Introduction & metrics** 3 divider, 4 Object detection, 5 Multi-object tracking, 6 Applications, 7 Challenges, 8 How we evaluate (every abbreviation written in full), 9 IoU vs NMS (IoU 0/0.5/1 table + NMS steps), 10 TP/FP/FN/TN, 11 Precision and recall (detailed text, no big picture), 12 AP and mAP, 13 MOTA, 14 Identity switches, 15 IDF1, 16 HOTA and FPS · **II Related work** 17 divider, 18 Detector families, 19 Detector benchmark, 20 Why YOLOv8n, 21 Our own speed test, 22 Tracker families, 23 Evolution of trackers, 24 ByteTrack baseline (steps table, no code), 25 Published MOTA MOT17, 26 Quick question (no spoiler), 27 ID switches MOT17, 28 Datasets, 29 Survey conclusions · **III Problem** 30 divider, 31 Aerial scenes are not equally difficult, 32 The main question (“Why should the detector use the same operating point when scene difficulty changes over time?”) · **IV AC-MOT** 33 divider, 34 AC-MOT = control layer (Frame → Scene Analyzer → SCI → Adaptive Controller → Detector → Tracker → Tracks), 35 SCI dial, 36 SCI 7 steps, 37 The five SCI cues (continuous vs binary; 30, 32×32, 0.14, 80, 180 = empirical design constants, not chosen by Optuna; refs COCO/Canny/Pech-Pacheco), 38 Three clues on real pictures, 39 Initial SCI (0.30/0.30/0.20/0.10/0.05, clip, window 7, every 10 frames), 40 SCI example 0.63, 41 SCI → settings table, 42 Step 2: controller rules (charts + rule tables), 43 Smart Calibrator exact settings, 44 Confidence threshold, 45 Implementation (smoothing + stride) · **V Setup** 46 divider, 47 Test domain, 48 VisDrone2019-MOT, 49 Classes, 50 GT filtering, 51 Evaluation steps (table, no code), 52 Fair ablation design (OLD-A0…A3) · **VI Ablation** 53 divider, 54 Original ablation table, 55 What each component changed (charts), 56 Same frames video (tabs Clip 1/2/3) · **VII Optimization** 57 divider, 58 Why Optuna, 59 What Optuna changed in V1, 60 One Optuna trial, 61 Quick question, 62 V1 Trial 24 weights, 63 V1 Trial 24 regimes, 64 V1 validation selection, 65 Validation builds it / test judges it, 66 Final test-set comparison (chart + table), 67 Reading the test-set result, 68 Why V2, 69 V2 Pareto front, 70 UAVDT (charts + table) · **VIII Contributions & conclusion** 71 divider, 72 Main contributions (4), 73 Conclusion, 74 Future work, 75 Thank you.

Every content slide starts with a big “The main idea / What it means” box (from `meaning.js` or inline). No bottom strip. No pseudo-code boxes. Footers carry provenance labels.

**Optional detailed explanations (v07+, expanded in v09):** 16 topics / 51 pages in `<div class="overlay xview" id="xview"><div class="xstage" id="xstage">` placed after `</main>` — OUTSIDE the slide list (not in Next/Previous, not in slide numbering). Topics (id · pages): x-controller 6 (confidence, NMS IoU, input size, small fixes, clamping, complete example 0.208/0.453/832), x-cues 5, x-sci 3 (weighted example SCI 0.47, clip/smooth/stride, frame preparation), x-optuna 3, x-regimes 2, x-nms 1 (detector NMS ≠ tracker match threshold), x-metrics 6 (example, MOTA 0.70, IDF1 0.70, HOTA DetA 0.818, AssA 0.644 → HOTA 0.726, IDS), x-v1v2 3, x-iou 3, x-ap 3 (AP 0.683, COCO mAP), x-fps 2, x-bench 1, x-bytetrack 4, x-eval 3, x-ablation 3, x-pareto 3. Pages are `<section class="xpage" data-sec=…>` using slide classes; engine adds a nav bar (“← Back to main slide (slide N)”, part counter, ‹ ›). Buttons: `data-explain="deckid|Label;deckid2|Label2"` on the main `<section class="slide">` → footer `.xbtn`. 45 buttons on 39 slides: 8–16, 19, 20, 23, 24, 35–37, 39–45, 49–52, 54, 55, 58–60, 62, 63, 66–70. **Every explanation always opens at part 1.** Back / Esc / Backspace return to the originating slide; arrows change parts. Every page tags number origin with `.origin` chips: manual (manually designed) · empirical (empirical design constant) · optuna (optimization-selected) · illus (illustration / made-up numbers). JS API: `window.ACMOT_X.open(id, page)`, `.close()`, `.show(i)`.

**Presentation mode (v07+):** “▶ Start full-screen presentation” button (bottom-left), “Present” button in bar, keys F / P → fullscreen, `body.present`: black letterbox, no progress bar, bar/cursor hidden until mouse moves. I want it to look like PowerPoint, not a web page.

**Engine features (script.js):** keyboard nav, O overview (`.ov-grid button`), N notes, H help, lightbox, tabs, reveal steps `.frag`, SVG charts registry `CHARTS` (`data-chart`, incl. oab-quality, oab-ids, oab-fps, td4-quality, td-ids, td-fps, uav-quality/ids/fps, weights-v1, pareto, calib-conf, calib-size, smooth …), `data-bind="path"` from results.js, footer buttons, **auto-fit** of each `.s-body` (scale ≥ 0.72, `data-fit` attribute), **abbreviation expander** (`ABBR` glossary: first occurrence per slide gets “(full name)”, prose first, skips titles/formulas/code/charts/`.node small`, skips when full name already present, avoids double brackets), main-idea injection from `window.MEANING`.

## 4. Numbers (use exactly; never change; never merge experiments in one table)

- **Original ablation (author-supplied, `results.js → oldAblation`)** — Stage | MOTA | HOTA | IDF1 | IDS | FPS: OLD-A0 Baseline 17.633 29.837 30.892 283 44.09 · OLD-A1 Tuned ByteTrack 17.802 30.864 32.854 217 44.51 · OLD-A2 Adaptive Confidence + NMS 17.636 31.384 33.727 210 40.65 · OLD-A2R Adaptive Resolution Only 18.425 32.446 35.669 241 39.56 · OLD-A3 Full AC-MOT 18.165 33.064 36.296 271 37.96. Reading: A1 better association + lower IDS; A2 lowest IDS; A2R highest MOTA; A3 highest HOTA & IDF1; no stage wins everything.
- **V1 Trial 24 (validation, 7 seq):** MOTA 23.0381, HOTA 36.1102, IDF1 40.7578, IDS 270, FPS 37.1686. Weights crowd 0.12949277455301997, tiny 0.22174766876599927, edge 0.43371337893805056, night 0.05355765312756694, blur 0.16148852461536325. threshold_mid 0.13534938199219218, threshold_high 0.28728676236279177 → Easy SCI < 0.13535, Medium 0.13535 ≤ SCI < 0.28729, Hard ≥ 0.28729 (optimization parameters, not hand-set). conf_easy 0.30, conf_hard 0.40, nms_easy 0.35, nms_hard 0.35. V1 rules: FPS ≥ 25, IDS ≤ 271, highest MOTA; 50 trials, TPE, seed 42. Optuna did NOT change 30, 32×32, 0.14, 80, 180, window 7, stride 10.
- **Test set (VisDrone2019-MOT test-dev, 17 seq)** — System | MOTA | HOTA | IDF1 | IDS | FPS: Baseline 19.729 28.430 32.724 1235 36.528 · Old AC-MOT 23.236 32.698 39.516 1061 41.957 · V1 26.948 33.835 41.546 1184 38.985 · V2 23.792 31.218 37.870 919 46.024. V1 = quality-oriented; V2 = identity/efficiency trade-off; V1 is not best in every metric; V2 is not universally better.
- **V2:** multi-objective (max MOTA, min IDS, FPS ≥ 25), 50 planned / 49 completed, Trial 22 chosen by pre-fixed equal-weight rule; validation MOTA 19.33, IDS 168, FPS 51.4; Pareto: T16 22.83/308, T8 11.54/114.
- **UAVDT (20 seq, 16,592 frames, zero tuning)** — Baseline 13.841 24.085 27.887 558 65.015 · V1 17.399 28.390 34.453 321 58.353 · V2 16.118 26.930 32.014 308 61.462. Supports transfer; not a state-of-the-art claim.
- **Original controller (manually designed):** confidence = 0.245 − 0.050×SCI clipped 0.19–0.28; NMS IoU = 0.490 − 0.050×SCI clipped 0.40–0.52 (with blur fix NMS stays 0.428–0.490, clamp never triggers); input 832 if SCI > 0.60, 736 if > 0.35, else 640; crowded/tiny/dark → confidence −0.012 (once); blur → NMS −0.012; tiny share > 0.50 → 832; limits applied again.
- **ByteTrack:** default 0.25/0.10/0.25/30/0.80 → tuned & frozen 0.18/0.04/0.20/45/0.86 (track_high, track_low, new_track, buffer, match_thresh).
- **Cues:** Crowd = min(previous tracked boxes/30, 1); Tiny = boxes < 32×32 / all; Edge = min(Canny edge density/0.14, 1); Night = 1 if mean gray < 80; Blur = 1 if Laplacian variance < 180. Only 32×32 has a literature basis (COCO small objects); Canny and variance-of-Laplacian are published methods; the other constants and the initial weights are our own. **Never claim the constants came from papers** (I once asked for that — refuse politely and use the honest wording in SOURCE_MAP.md).
- Published survey values (detector table, MOT17 MOTA/IDS, datasets) come from my IEEE ICMISI 2026 survey. YOLO timing chart = early exploratory, raw log not archived.

## 5. Story and content rules (my preferences)

- Chronological original AC-MOT story only: problem → control layer → five cues → initial SCI → original ablation → Optuna V1 → test set → V2 → UAVDT → contributions → conclusion. **No U2MOT anywhere** (I said this twice). No VisDrone official-protocol correction story. No older development ablation (MOTA 35.85…), no TRK_MATCH_090 finalists, no mixed-experiment tables.
- Label Ablation / Validation / Test set / UAVDT clearly. All AC-MOT results use the custom class-agnostic AC-MOT TrackEval protocol — never call them official leaderboard results.
- Simple English, PowerPoint-size fonts (body ≥ ~24 px on the 1600 stage, titles 52 px), one idea per slide, the big meaning text first, examples after.
- Spell out every abbreviation next to it (at least the first time per slide; slide 8 everywhere).
- Do not name AC-MOT before Section IV (title slide name is fine).
- No algorithm/pseudo-code boxes; use step tables and formula tables.
- Detailed/advanced content ONLY inside the optional explanations; keep main slides normal; explanations must be complete (don't skip details) and open at part 1.
- Keep the visual identity, theme, navigation, charts style.
- Every slide has speaker notes in `<aside class="notes">`.
- Label interpretations as interpretations; label made-up examples.

## 6. Open questions (ask me, do not guess)

- OLD-A3 FPS: my table says 37.96, older record (`v1.oldA3val.fps`) 42.085 — other metrics identical.
- Old deck said V1 used percentile cue calibration on validation; my story says cue definitions stayed fixed. The deck follows my story.
- `results.js` contains a `u2mot` block marked final (not shown on slides).

## 7. How to verify a new version (mandatory before updating `current`)

- Launch configs are in `/Users/ahmedgouda/CLAUDECODEX/claude/.claude/launch.json` (`acmot-presentation-current` port 8775, `acmot-presentation-v2`…`-v9` ports 8767–8774). Add a new entry for v10 (e.g. port 8776, `--directory ~/Desktop/ACMOT-Presentation-Versions/versions/v10-…`) and start it with the Browser preview tool (not Bash). File:// previews outside the project folder are static snapshots — use the server.
- The browser caches script.js/styles.css hard: before reloading run `await fetch('script.js',{cache:'reload'})` (same for styles.css, index.html, data files) and navigate with a new `?v=` query.
- Checks (JavaScript in the page): no console errors; slide count; no `[data-bind]` left as “…”; all charts build (`window.ACMOT_CHARTS`); no “AC-MOT” in slides before `#sec-4`; no “U2MOT”; no double brackets `((…))`; `data-fit` values (flag < 0.86); overflow audit per slide in chunks of ~15 slides (activate via `document.querySelectorAll('.ov-grid button')[n-1].click()`, turn on `.frag`, flag elements leaving `.s-body` by > 6 px, `.card/.note/.callout/.kpi/.meaning` with scrollHeight > clientHeight, horizontal spill); audit every explanation page via `ACMOT_X.open(id,0)` + `ACMOT_X.show(i)`; test every `.xbtn` opens at part 1 and Back/Escape/Backspace return to the same slide; test → / ← still move between main slides.
- Screenshots: wait ≥ 1.5 s (fades), scale 0.5. If screenshots fail with “Browser pane is not displayed”, reopen with preview_start `{url: …}`; if “tab cap reached”, close old tabs with tabs_close. Keep JavaScript calls under 45 s (split long loops). Videos render black in the preview (normal).
- Stop the preview server when done.

## 8. Practical pitfalls

- Bash runs in a sandbox: writing to `~/Desktop` needs `dangerouslyDisableSandbox: true` (copying/moving/python writes). The Write/Edit tools can write directly but Edit needs a prior Read of that exact file.
- The default shell is zsh: use `bash <<'EOF' … EOF` for scripts with bash arrays (`${!ARR[@]}`).
- For big structural edits, write a Python build script (like `tools/build_v9.py`) with exact-count string replacements and assertions, keep it in the new version's `tools/` folder.
- Keynote on this Mac is “Keynote Creator Studio.app”; after a failed import it wedges — force-quit and relaunch before retrying.

## 9. Start of the new chat

1. Read `~/Desktop/ACMOT-Presentation-Versions/README.md`, `VERSION_HISTORY.md`, `SOURCE_MAP.md`.
2. Wait for my next request. When I ask for a change, create `versions/v10-…` from `current`, implement, verify (section 7), then update `current` and `VERSION_HISTORY.md`, and finish with:
   `open ~/Desktop/ACMOT-Presentation-Versions/current/index.html`
