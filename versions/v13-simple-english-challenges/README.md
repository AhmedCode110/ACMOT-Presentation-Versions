# AC-MOT — Interactive Master's Presentation (v13)

Open `index.html` in a browser. No internet or libraries needed.

## Content
75 main slides (16:9, 1600 × 900) in eight sections: Introduction & metrics · Related work · Problem ·
AC-MOT · Setup · Ablation · Optimization (V1, test set, V2, UAVDT) · Contributions & conclusion.
17 optional explanation topics (59 pages) open from footer buttons and always start at part 1.

## Controls
← / → next / previous · **O** overview · **N** speaker notes · **H** help · **F** / **P** full-screen presentation ·
inside an explanation: ‹ › or arrows change the part, **← Back to main slide**, **Esc** or **Backspace** return.

## Files
- `index.html` — slides and explanation pages
- `styles.css`, `script.js` — look and engine (charts, auto-fit, abbreviations, explanations, presentation mode)
- `assets/data/results.js` — every number shown (single source)
- `assets/data/meaning.js` — the big “main idea” boxes
- `assets/data/cue_examples.js` — cue values computed on the example pictures
- `assets/figures/`, `assets/videos/` — pictures and videos
- `tools/` — build scripts (`build_v9.py`, `build_v10.py`, `build_v11.py`, `build_v12.py`, `build_v13.py`, `gen_figures.py`)

## Results shown
Original ablation (OLD-A0 … OLD-A3) · V1 Trial 24 on validation (7 sequences) · test set VisDrone2019-MOT
test-dev (17 sequences, 6,635 frames): Baseline, Old AC-MOT, V1, V2 · V2 Pareto search · UAVDT (20 sequences,
16,592 frames, zero tuning). All AC-MOT results use the custom class-agnostic AC-MOT TrackEval protocol.
