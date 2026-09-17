# AC-MOT — Interactive Master's Presentation (v32)

Open `index.html` in a browser. No internet or libraries needed.

## Content
96 main slides (16:9, 1600 × 900) in nine sections: Introduction & metrics · Related work (incl. detectors through the ages) ·
Problem & baseline · AC-MOT (Step 1 measure · Step 2 score · Step 3 set the detector) · Setup & first result ·
V1 optimization (including pre-Optuna screening) · V2 multi-objective · Statistics & UAVDT · Conclusion.
17 optional explanation topics (59 pages) open from footer buttons and always start at part 1.

## Controls
← / → next / previous · **M** back to the outline · **S** sections menu · **O** overview · **N** speaker notes · **H** help · **F** / **P** full-screen presentation ·
inside an explanation: ‹ › or arrows change the part, **← Back to main slide**, **Esc** or **Backspace** return.

## Files
- `index.html` — slides and explanation pages
- `styles.css`, `script.js` — look and engine (charts, auto-fit, abbreviations, explanations, presentation mode)
- `assets/data/results.js` — every number shown (single source)
- `assets/data/meaning.js` — the big “main idea” boxes
- `assets/data/cue_examples.js` — cue values computed on the example pictures
- `assets/figures/`, `assets/videos/` — pictures and videos
- `tools/` — build scripts (`build_v9.py`, `build_v10.py`, `build_v11.py`, `build_v12.py`, `build_v13.py`, `build_v14.py`, `build_v15.py`, `build_v16.py`, `build_v17.py`, `build_v18.py`, `build_v19.py`, `build_v20.py`, `build_v21.py`, `build_v22.py`, `build_v23.py`, `build_v24.py`, `build_v25.py`, `build_v26.py`, `build_v27.py`, `build_v28.py`, `build_v29.py`, `build_v30.py`, `gen_figures.py`)

## Results shown
Baseline and Initial AC-MOT · V1 Trial 24 on validation (7 sequences) · test set VisDrone2019-MOT
test-dev (17 sequences, 6,635 frames): Baseline, Old AC-MOT, V1, V2 · V2 Pareto search · UAVDT (20 sequences,
16,592 frames, zero tuning) · paired bootstrap.
All AC-MOT results use the custom class-agnostic AC-MOT protocol — not official VisDrone leaderboard numbers.

## v32 addition
The V1 section now explicitly shows the pre-Optuna screening stage: 15 input-size values, 10 confidence values,
11 NMS IoU values, and 25 temporal combinations on the 7 validation videos. It records the frozen choices that entered
Optuna (input sizes 512 / 928 / 960, confidence 0.25–0.45, NMS IoU 0.30–0.70, window 7 and stride 10).

The temporal slide lists every tested value: smoothing windows 1 / 3 / 5 / 7 / 9 and analysis strides 1 / 5 / 10 / 15 / 20.
It explains the 5 × 5 Cartesian sweep, the validation feasibility filter (FPS ≥ 25 and IDS ≤ 271), and the selected
reference metrics for window 7 / stride 10. The source filenames are not shown on the slide.
