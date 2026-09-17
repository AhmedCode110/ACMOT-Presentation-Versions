# AC-MOT — Interactive Master's Presentation (v30)

Open `index.html` in a browser. No internet or libraries needed.

## Content
94 main slides (16:9, 1600 × 900) in nine sections: Introduction & metrics · Related work (incl. detectors through the ages) ·
Problem & baseline · AC-MOT (Step 1 measure · Step 2 score · Step 3 set the detector) · Setup & first result ·
V1 optimization · V2 multi-objective · Statistics & UAVDT · Conclusion.
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
