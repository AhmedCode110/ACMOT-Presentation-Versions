You are continuing work on an interactive HTML Master's presentation for "AC-MOT: Adaptive Control for Real-Time Multi-Object Tracking" (Capt. Eng. Ahmed Gouda Ismail, Military Technical College; supervisors Dr. Tarek Ahmed Mahmoud and Dr. Mohamed S. Mohamed). The previous agent built it. Do NOT rebuild it and do NOT invent any numbers. Your job is to finish visual verification and polish.

## Folders
- WORKING COPY (edit this one): ~/Desktop/acmot_interactive_presentation_v2/  — 96 slides
- REFERENCE ONLY (never edit): ~/Desktop/acmot_interactive_presentation/  — older 82-slide version
- NEVER edit: ~/Desktop/DONT TOUCH/, CLAUDECODEX/Master/macneo_wrk/ACMOT_FROZEN_2026-09-11, ACMOT_V1_FINAL_POST_SNAPSHOT_2026-09-12

## What the user wants (v2)
Same theme, animations and engine as v1, but the CONTENT must follow the user's original seminar deck ~/Desktop/DONT TOUCH/b9_claude.key slide by slide (same 8 sections, same examples, tables and ideas), written in simpler English. Only NEW concepts and results are added, each marked with <span class="newtag">NEW</span>. Light theme only. Every slide has speaker notes in <aside class="notes">.

## Files in v2
- index.html — all slides (<section class="slide">); section ids sec-1 … sec-8
- styles.css — theme (includes .newtag, .qmark, .note)
- script.js — engine: arrows/space, F fullscreen, O overview, N notes, tooltips (data-tip), click definitions (data-def), lightbox (.zoomable), tabs (data-tabs), reveal steps (.frag), SVG chart registry CHARTS (data-chart="id")
- assets/data/results.js — SINGLE SOURCE OF TRUTH for every number (+ published, calibration, visdroneTest, computed devDerived deltas); numbers appear in the HTML via data-bind="path"
- assets/data/cue_examples.js, assets/figures/, assets/figures/generated/, assets/videos/ (5 MP4s, all decode)
- README.md — controls, provenance table, how to update values

Slide map (v2): 1–16 Title+Section I · 17–32 Section II+III · 33–47 Section IV · 48–55 Section V · 56–66 Section VI · 67–89 Section VII (Stage 2 real V1 results + NEW Stage 3: V2, stats, UAVDT) · 90–96 Section VIII (scope, NEW U2MOT, conclusion, future, thanks).

## How to preview
A launch config already exists in /Users/ahmedgouda/CLAUDECODEX/claude/.claude/launch.json named "acmot-presentation-v2" (python http.server, port 8767). Start it with the Browser preview_start tool, open http://localhost:8767/index.html.
- Jump to slide N: document.querySelectorAll('.ov-grid button')[N-1].click()
- Show all reveal steps: document.querySelectorAll('.slide.active .frag').forEach(f=>f.classList.add('on'))
- Wait ~2 s before a screenshot (charts animate). Preview pane screenshots show videos as black — that is normal.
- Overflow audit: for each slide make it visible, turn on all .frag, and flag any element inside .s-body whose box leaves the .s-body box by >14 px.

## Status at handoff
DONE: 96 slides, 96 notes, all assets present, all 32 charts defined, no console errors, overflow audit = 0 issues on all 96 slides (last run after fixes). Visually checked and OK: 2, 21, 29, 35, 36, 37, 38, 47, 50, 57, 59, 65, 66, 73, 74, 75, 78, 79, 81, 84, 93, 94.

REMAINING:
1. Screenshot and visually check the slides not yet viewed: 1, 3–20, 22–28, 30–34, 39–46, 48, 49, 51–56, 58, 60–64, 67–72, 76, 77, 80, 82, 83, 85–92, 95, 96. Fix only real defects (overlap, unreadable or clipped text, awkward empty space); re-run the audit after edits.
2. When finished: stop the server with preview_stop and tell the user: open ~/Desktop/acmot_interactive_presentation_v2/index.html

## Scientific rules (the user is strict)
- Never invent or change results. Sources (verified):
  - A0–A3 ablation (35.85/47.44/58.16/IDS 2537/29.57 FPS…): gptCODEX_STADE/Master/AC-MOT/supervisor_package_17seq_ablation/results/final_17seq_ablation_summary_proxy_hota.csv — development evaluator, HOTA is a proxy.
  - Historical live run Baseline 19.718/28.418/32.716/1238/44.181, Full AC-MOT 22.999/33.017/40.021/994/37.686, TRK_MATCH_090 22.953/33.328/40.656/946/38.028 (repo OFFICIAL_RESULTS + VERIFICATION_REPORT.md).
  - V1 Trial 24, V2 Trial 22 (49 of 50 trials), test-dev results, bootstrap CIs, UAVDT: docs/freeze/ACMOT_FINAL_SCIENTIFIC_FREEZE_2026-09-12.md on GitHub branch freeze/final-after-uavdt-2026-09-12 (AhmedCode110/AC-MOT).
  - Detector table, MOT17 MOTA/IDS, dataset table: published values from the user's IEEE ICMISI 2026 survey (as in the seminar deck).
- Keep every provenance footer label. All AC-MOT results use the custom class-agnostic AC-MOT TrackEval protocol — never call them official VisDrone leaderboard results.
- Already corrected, do not revert: old deck's "Trial 37", draft sweep curves, W=5 grid and "15 of 50" were simulated → replaced with real frozen V1 values; ByteTrack tuned settings are 0.18/0.04/0.20/45/0.86; YOLO latency table is "early exploratory, raw log not archived"; U2MOT metrics stay "pending"; V1 does NOT have the fewest IDS on test-dev (Old AC-MOT does); V2 does not beat V1 overall.
- Keynote note (if asked for .key): Keynote here is "Keynote Creator Studio.app"; after a failed import it wedges — force-quit and relaunch before retrying.
