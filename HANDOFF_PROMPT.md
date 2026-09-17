# HANDOFF PROMPT — continue the AC-MOT interactive presentation (paste everything below into a new chat)

You are continuing work on my interactive HTML Master's presentation **“AC-MOT: Adaptive Control for Real-Time
Multi-Object Tracking”** (Capt. Eng. Ahmed Gouda Ismail, Military Technical College, Electrical Engineering Branch,
Computer Engineering and Artificial Intelligence Department; supervisors Dr. Tarek Ahmed Mahmoud and Dr. Mohamed S.
Mohamed). I present it to an examination committee. I write in Egyptian Arabic / Franco-Arabic; answer me in **simple
English**. **Never invent numbers. Never edit an existing version.** Updated 2026-09-15 (current = **v30**).

---

## 0. First thing to do in the new chat (graphify + context)

1. Read, in this order: `~/Desktop/ACMOT-Presentation-Versions/README.md` (research roadmap: where every file and
   number lives), `SOURCE_MAP.md` (cheat sheet + provenance of every slide number), `VERSION_HISTORY.md` (what
   changed in v01…v26 and why), and this file.
2. **Graphify (knowledge graph) — keep it linked to the work:**
   - The repo root has `CLAUDE.md` with graphify rules and `graphify-out/`. The graph was rebuilt on 2026-09-15 and
     updated for v30. Its corpus is set by the repo-root `.graphifyignore`: the text of the current version folder
     (`script.js`, `assets/data/`, `tools/`, version `README.md`) plus the repo docs. graphify does **not** parse
     `index.html` or `styles.css` — find slides by searching `index.html`. The old v18 graph is kept as
     `graphify-out/graph_v18_backup.json`.
   - For each new version: change the version folder name in `.graphifyignore`, then run `graphify update .` from the
     repo root.
   - Before changing slides, use `graphify query "<question>"`, `graphify path "<A>" "<B>"`,
     `graphify explain "<concept>"` to find where a slide, chart, number or build step lives.
   - After every new version: rebuild or `graphify update` on the new `current`, so the graph always matches the
     newest version.
3. Wait for my next request.

---

## 1. Where everything is

`~/Desktop/ACMOT-Presentation-Versions/` (a git repo: `AhmedCode110/ACMOT-Presentation-Versions`, branch `main`)

    versions/v01 … v30        one folder per version (v01–v29 are read-only history)
    current  → versions/v30-chart-zoom-redraw
    index.html                 root page used by GitHub Pages (redirects to one version; now v21)
    README.md                  research roadmap (freeze paths, V1/V2/UAVDT files, commits, cheat sheet)
    SOURCE_MAP.md              cheat sheet + where each slide number comes from + open questions
    VERSION_HISTORY.md         every version and every change
    HANDOFF_PROMPT.md          this file
    CLAUDE.md, graphify-out/   graphify rules and output (ignored by git)

Each version: `index.html` (main slides + optional explanation pages in `#xstage`), `styles.css`, `script.js`
(engine), `assets/data/results.js` (numbers), `assets/data/meaning.js` (main-idea boxes injected by slide title when a
slide has no inline `.meaning`), `assets/data/cue_examples.js`, `assets/figures/`, `assets/videos/`, `tools/build_vNN.py`.
v26 also has `assets/data/source/EMPIRICAL_OPTUNA_TRIALS.csv`.

**Never edit:** `~/Desktop/DONT TOUCH/` (seminar Keynote `b9_claude.key`), `CLAUDECODEX/Master/macneo_wrk/ACMOT_FROZEN_2026-09-11`,
`ACMOT_V1_FINAL_POST_SNAPSHOT_2026-09-12`. The modified `versions/v02…/_source/b9_claude.key` in git status is not mine to commit.

---

## 2. Version rule (my explicit instruction)

- Copy `current` to the next folder: `rsync -a --exclude '.DS_Store' versions/v30-chart-zoom-redraw/ versions/v31-short-description/`
- Edit ONLY the copy, with a build script `tools/build_v31.py` (exact string replacements with `assert count == 1`).
  Build scripts are **not idempotent**: back up the files first and restore them if the script fails.
- Verify (section 8). Only then `ln -sfn versions/v31-… current`, add a `VERSION_HISTORY.md` section + table row,
  bump the version's `README.md`, update `SOURCE_MAP.md` if numbers/sources change, update Outline slide ranges.
- Finish every delivery with: `open ~/Desktop/ACMOT-Presentation-Versions/current/index.html`
- **Every request = a new version folder** (never overwrite any existing version, even the one just finished). At the end of
  every reply, give the terminal command that opens the NEW version by its folder path, in its own ```bash block, e.g.
  `open ~/Desktop/ACMOT-Presentation-Versions/versions/v30-chart-zoom-redraw/index.html`
- If I say "leave it as it is", undo the prepared version (delete the unused copy, restore docs).

---

## 3. v30 structure — 94 main slides, nine sections (Outline slide in PowerPoint style, 5 + 4 rows)

- **1** Title · **2** Outline
- **I Introduction & metrics (3–16):** divider (tracking-video background), object detection, multi-object tracking,
  applications, challenges (button: 7 challenge pages, easy English), how we evaluate, IoU vs NMS (NMS example: 4 boxes → 2 boxes, keep / delete table with IoU vs the 0.45 limit), TP/FP/FN/TN
  (Keynote layout: two bird pictures IoU 0.22 / 0.00, TP/FP/FN cards, NOTE, TN box), precision & recall, AP & mAP
  (“AP shows how precise the detector stays while it finds more and more objects. AP is one score for one class…”),
  MOTA, IDS, IDF1, HOTA & FPS.
- **II Related work (17–31):** divider, detectors through the ages (timeline), detector families,
  deep-learning detectors table (24 px; after the families since v28), benchmark, why YOLOv8n, own speed test, tracker families, evolution of trackers, ByteTrack
  (v28: rule cards + film strip of 5 frame pictures + “simple tracker gets new ID 8” line; worked example car ID 7: frames 100 0.85 · 101 0.72 strong → 102 0.30 weak second chance IoU 0.75 →
  103–105 no box track buffer 30 → 106 back ID 7; illustration settings 0.50/0.10/30, real tuned 0.18/0.04/45),
  benchmark datasets, published MOTA MOT17, quick question, ID switches MOT17 (MOTA vs IDS trade-off), survey
  conclusions (~49× faster = Faster R-CNN 172 ms → RF-DETR-S 3.5 ms; +43% mAP = 37.0 → 52.9; 81.7% MOTA SMILEtrack;
  3.5 ms RF-DETR-S). *Traditional detectors slide was deleted on request.*
- **III Problem & baseline (32–36):** divider, one drone video / very different frames, the detector never changes its
  settings, main question (three settings in one line each), baseline YOLOv8n → ByteTrack (19.729 MOTA, “not
  ByteTrack's global score”).
- **IV AC-MOT (37–51):** divider, the idea (six rich blocks: Frame → Step 1 Measure / Scene Analyzer → Step 2 Score /
  SCI → Step 3 Set / Smart Calibrator → YOLOv8n → ByteTrack, loop note, example SCI 0.63), **From a Frame to SCI — All Steps Together** (whole-path overview, moved here in v27), Step 1: clue pictures
  first, two clues from boxes (crowd ÷30, tiny <32×32), three clues from the picture (Canny edge density ÷0.14,
  brightness <80, Laplacian variance <180 — example-value lines removed), Step 2: SCI definition only (“one number
  from 0 to 1 that says how hard the current frame is for the detector”), formula & weights, example 0.63, stable &
  cheap, Step 3: the three detector settings (too high / too low with object examples),
  confidence in detail, SCI → settings, exact rules, what changes / never changes.
- **V Setup & first result (52–60):** divider, domain, VisDrone2019-MOT (whole benchmark 288 videos · 262K frames from the
  survey table; 7 + 17 = 24 sequences used), classes (fair-comparison reason), GT filtering, **Ablation Study** (validation;
  small percent change vs OLD-A0 next to every value) and **Baseline vs Full
  AC-MOT: What Went Up** (validation), **Old AC-MOT on the Test Set**, same-frames videos.
- **VI V1 (61–74):** divider, why these weights, why Optuna, what Optuna changed, one trial, V1 selection on
  validation, **All V1 Trials: The Trade-off Curve** (new in v26), **Why Trial 24?** (rule charts), quick question,
  weights, regimes, validation builds / test judges, V1 on the test set, the ID-switch problem (V1 removed only 51 IDS).
- **VII V2 (75–82):** divider, why V2, trade-off in simple words, Pareto front, V2 search 49/50 → Trial 22, V1 vs V2
  on validation, V2 on the test set, V1 or V2?
- **VIII Statistics & UAVDT (83–88):** divider, **what a paired bootstrap is and why**, bootstrap results, bootstrap on
  IDS, zero-tuning question, UAVDT result.
- **IX Conclusion (89–93):** divider, story in one line, contributions, conclusion, future work · **94** Thank you.
- **Removed on request (do not bring back):** U2MOT; “How We Score Every System — the Same Way” (v27); literature comparison / DroneMOT / protocol audit / official
  VisDrone / van class / correction freeze section; “Proven and open”; seminar mentions; NEW tags.
- Optional explanations: 17 topics / 59 pages (`data-explain="deckid|Label"` → footer button; always opens at part 1;
  Back/Esc/Backspace return).

---

## 4. Engine features you must keep

- Top of every slide: **‹ previous · ☰ Outline · next ›** (`.top-nav` inside the stage; M key = Outline; titles keep
  `padding-right:290px`). Bottom bar: Sections menu (S), slide navigator (O), notes (N), present (F/P), help (H).
- **Media loads per slide**: every non-title `<img>`/`<video>` uses `data-src` and is loaded in `enter()` for the
  current and neighbouring slides and explanation pages; all videos have `preload="none"` (needed for GitHub Pages).
- **Title fit**: `fitSlide()` shrinks two-line titles (52 → 40 px) and moves `.s-body` below the header if needed,
  then auto-fits the body (scale ≥ 0.72).
- **Abbreviation expander** (`ABBR` in script.js) adds full names once per slide; it skips `.tbl th`, `.noabbr`,
  `.ol-ppt`, titles, formulas, charts.
- Click on a chart (v30+): `openChartZoom()` redraws it at lightbox size with animation (click again = replay); keep this.
- Charts registry `CHARTS` in script.js (e.g. `oab-quality/ids/fps`, `oab-a0a3`, `init-*`, `v1b-*`, `td3-*`, `val-*`,
  `boot-v1q`, `boot-ids2`, `v1-rule-fps/ids/mota`, `v1-trials`, `pareto`, `uav-*`, `weights-v1`). `scatter()` supports
  `vline`. Minimum text size policy: nothing below ~20 px on the 1600×900 stage.
- Every content slide: big “The main idea / What it means” box first, speaker notes in `<aside class="notes">`,
  provenance label in the footer (`.prov p-val / p-test / p-ext / p-pub / p-hist / p-illus`).

---

## 5. Numbers (use exactly; label the split; never mix experiments in one table)

- **Baseline (test-dev 17 seq):** MOTA 19.729 · HOTA 28.430 · IDF1 32.724 · IDS 1235 · FPS 36.53 (freeze 36.528)
- **Old AC-MOT (test):** 23.236 · 32.698 · 39.516 · 1061 · 41.96 (freeze 41.957); change +3.507 / +4.268 / +6.792 / 174 fewer / +5.43
- **Ablation (validation, author table):** OLD-A0 17.633/29.837/30.892/283/44.09 · OLD-A1 17.802/30.864/32.854/217/44.51 ·
  OLD-A2 17.636/31.384/33.727/210/40.65 · OLD-A2R 18.425/32.446/35.669/241/39.56 · OLD-A3 18.165/33.064/36.296/271/**42.085**.
  A0→A3: MOTA +0.532 · HOTA +3.227 · IDF1 +5.404 · 12 fewer IDS · FPS −2.005.
  **v45 correction:** the slides now use the frozen OLD-A3 validation reference FPS **42.085** from `OLD_A3_VALIDATION_W7_S10.json`. The final test Old AC-MOT speed remains **41.957 FPS**.
- **V1 Trial 24 (validation 7 seq):** MOTA 23.038 · HOTA 36.110 · IDF1 40.758 · IDS 270 · FPS 37.17; weights 0.129 / 0.222 /
  0.434 / 0.054 / 0.161; rule: FPS gate and IDS ≤ Old-A3 271, then highest MOTA (ties: lower IDS, HOTA, IDF1, FPS).
- **V1 Optuna trials (CSV):** 50 completed (trial 33 RUNNING, never finished) · 37 feasible · 13 broke IDS ≤ 271 · no
  trial below 25 FPS (slowest 34.49) · Trial 24 = highest MOTA of all.
- **V1 test:** 26.948 · 33.835 · 41.546 · 1184 · 38.98 (freeze 38.985); V1 − Baseline +7.220 pp · +5.405 · +8.822 · −51 · +2.46.
- **V2:** 50 planned / 49 completed, balanced 50% MOTA + 50% IDS → Trial 22; validation 19.330 / 31.651 / 34.226 / 168 / 51.41;
  test 23.792 / 31.218 / 37.870 / 919 / 46.02; vs V1: −3.157 pp MOTA, −2.617 HOTA, −3.676 IDF1, 265 fewer IDS, +7.04 FPS, ~5,397 fewer FP.
- **Bootstrap (5,000 paired resamples of 17 sequences, seed 42):** V1 − Baseline MOTA +7.2195 [5.4362, 9.2934] ·
  HOTA +5.4051 [4.1273, 6.9022] · IDF1 +8.8220 [6.9005, 11.0537]; IDS removed V1 51 [−114, 219] not significant ·
  V2 316 [175, 470] significant.
- **UAVDT (20 seq, 16,592 frames, zero tuning):** Baseline 13.841/24.085/27.887/558/65.015 · V1 17.399/28.390/34.453/321/58.353 ·
  V2 16.118/26.930/32.014/308/61.462; V1 − Baseline +3.558 / +4.305 / +6.565 / −237.
- All AC-MOT results use the custom class-agnostic AC-MOT TrackEval protocol — never call them official leaderboard results.
- **On the slides (v27+), count changes are written as percent of the compared system:** ablation A0→A3 4.2% fewer IDS ·
  Old AC-MOT test 14.1% fewer · V1 test −4.1% · V2 vs V1 test 22.4% fewer IDS and 28.4% fewer FP (19,029 → 13,632) ·
  UAVDT V1 vs Baseline −42.5% · bootstrap IDS V1 4.1% [−9.2%, 17.7%], V2 25.6% [14.2%, 38.1%] of the baseline's 1235.
- v29: the UAVDT table shows the percent change against the Baseline next to every V1 / V2 value (V1: MOTA +25.7% · HOTA +17.9% · IDF1 +23.5% · IDS −42.5% · FPS −10.2%; V2: MOTA +16.5% · HOTA +11.8% · IDF1 +14.8% · IDS −44.8% · FPS −5.5%).
- v27 also added: VisDrone2019 whole benchmark = 288 videos · 262K frames (survey table; MOT-part train / test-challenge
  sizes are NOT in the local sources) and percent change vs OLD-A0 next to every ablation value.

---

## 6. Content and style rules (my preferences)

- Easy English, short sentences, meaning first then example; spell out abbreviations; no AC-MOT name before Section IV.
- In comparisons, write a change in a count (ID switches, false positives) as **a percent** (“14.1% fewer ID switches”),
  not as a number (“174 fewer”). Say which system is the reference.
- One idea per slide, PowerPoint-size text (body ≥ ~24 px, titles 52 px), no tiny text, no pseudo-code boxes.
- Label illustrations as illustrations; label interpretations; say which split (validation / test / UAVDT).
- Slides must be real text, never text baked into images. Keep the visual identity and navigation.
- Numbers come only from the freeze / frozen files / my own tables — if a file is missing, say so and ask me for it.

---

## 7. Research files (see README.md for the full roadmap)

Scientific root `/content/drive/MyDrive/AC-MOT-shared/` (Colab path) · top reference
`[FROZEN][DO_NOT_MODIFY]_ACMOT_2026-09-12_FINAL_AFTER_UAVDT/ACMOT_FINAL_SCIENTIFIC_FREEZE_2026-09-12.md` · V1 root
`defensible_acmot_3workers/` · statistics `V1_POSTHOC_ANALYSIS_2026-09-12/`. Trust order: freeze → frozen JSON/CSV →
frozen commit → development output → old notebook → slide.
**AC-MOT-shared is NOT synced to this Mac** (not in My Drive of a7medgouda1@gmail.com). Ask me to download needed files
to `~/Downloads`. Local partial copy: `CLAUDECODEX/Master/macneo_wrk/ACMOT_V1_FINAL_POST_SNAPSHOT_2026-09-12/02_FINAL_DRIVE_ARTIFACTS/defensible_acmot_3workers/`.

---

## 8. How to verify a new version (mandatory before moving `current`)

- Add a launch config in `/Users/ahmedgouda/CLAUDECODEX/claude/.claude/launch.json` (pattern `acmot-presentation-vNN`,
  `python3 -m http.server <port> --bind 127.0.0.1 --directory …/versions/vNN-…`; v30 uses 8796 → next 8797; the Browser preview tool reads `.claude/launch.json` of the session's working folder, so add
  the entry there too if `preview_start` cannot find it) and start
  it with the Browser preview tool (not Bash).
- Before reload: `await fetch('index.html',{cache:'reload'})` (also script.js, styles.css, data files), then navigate
  with a new `?v=`.
- Checks in page JS: no console errors; slide count; charts built (`data-built` and no `.chart-missing`); no empty
  `[data-bind]`; no AC-MOT before `#sec-4`; no U2MOT; no `((`; overflow audit per slide in chunks of ~45 (click
  `.ov-grid button`, add `on shown in` to `.frag`, flag elements leaving `.s-body` by > 6 px and clipped
  `.card/.note/.callout/.kpi/.meaning`); title vs body (`head.offsetTop+offsetHeight ≤ body.offsetTop`); explanation
  buttons open at part 1 and Esc returns.
- Screenshots: wait ≥ 1.5 s (chart dots fade in after ~3–5 s); if “Browser pane is not displayed”, reopen with
  `preview_start {url}`; if the tab cap is reached, close old tabs. Keep each JS call under 45 s. Stop the server when done.

---

## 9. Publishing (GitHub Pages) — PAUSED

- Site: https://ahmedcode110.github.io/ACMOT-Presentation-Versions/ — root `index.html` currently opens **v21**
  (v18–v21 were pushed; v22–v30 are local only).
- **Do not push** until I say the deck is final. Then: point the root `index.html` (meta refresh + button + “Latest
  version”) at the final version, commit only that version + docs + root index, push, wait for the Pages build
  (`gh api repos/AhmedCode110/ACMOT-Presentation-Versions/pages`), verify with a cache-busting URL. Each version is ~78 MB.

---

## 10. Practical pitfalls

- Bash runs in a sandbox: writing under `~/Desktop` (copies, python writes, `ln`, git) needs `dangerouslyDisableSandbox: true`.
  Git network commands (fetch/push) also need it.
- Default shell is zsh; use `bash <<'EOF' … EOF` for bash-only syntax. `grep -o` with long `.{0,N}` patterns fails
  (ugrep complexity) — use python for context.
- Edit/Write need a prior Read of the same file in the chat.
- Keynote on this Mac is “Keynote Creator Studio.app”.
- Memory files for this project are in `~/.claude/projects/-Users-ahmedgouda-CLAUDECODEX-claude/memory/`.

---

## 11. Start of the new chat

1. Do section 0 (read the docs, rebuild the graphify graph on `current`).
2. Wait for my request. Then create `versions/v31-…` from `current`, implement, verify (section 8), update `current`,
   `VERSION_HISTORY.md` (and `SOURCE_MAP.md` / version README), run `graphify update` on the new version, and finish with:
   `open ~/Desktop/ACMOT-Presentation-Versions/current/index.html`
