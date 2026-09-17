# AC-MOT — Interactive Master's Presentation (v40)

Open `index.html` in a browser. No internet or libraries needed.

## Content
103 main slides (16:9, 1600 × 900) in ten sections: Introduction & metrics · Related work (incl. detectors through the ages) ·
Problem & baseline · AC-MOT (Step 1 measure · Step 2 score · Step 3 set the detector) · Setup & first result ·
V1 optimization (including pre-Optuna screening) · V2 multi-objective · Statistics & UAVDT · Transfer to published U2MOT · Conclusion.
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

The V1 section now also explains that every screening point was a complete pipeline run: one parameter changed, the rest
fixed, seven validation videos, YOLOv8n → ByteTrack → TrackEval, then MOTA / HOTA / IDF1 / IDS / FPS were recorded.
The temporal slide lists every tested value: smoothing windows 1 / 3 / 5 / 7 / 9 and analysis strides 1 / 5 / 10 / 15 / 20.
It explains the 5 × 5 Cartesian sweep, the validation feasibility filter (FPS ≥ 25 and IDS ≤ 271), and the selected
reference metrics for window 7 / stride 10. The source filenames are not shown on the slide.

The temporal slide also separates the 25 temporal configurations from the 50 V1 Optuna trials: 75 validation
configurations in total, while Optuna Trial 24 remains the Optuna-internal trial name and is not called trial 49.

The new screening text uses short, professional English for the supervisor-facing explanation.

## v36 addition
Section IX adds the transfer study on the published U2MOT pipeline. It records the published reproduction,
the new SCI boundary calibration, the fixed scene-dependent controller, validation results, matched runtime,
the frozen setup, and the final test result. The supported claim is careful: AC-MOT preserved quality approximately
while reducing identity switches and false positives. It does not claim that AC-MOT beat U2MOT overall.

## v37 addition
The U2MOT SCI slide now separates the two ideas clearly: the V1 weights define how SCI is calculated, while
the new boundaries define Easy, Medium and Hard. It shows the exact rules, the validation range, the 33rd and
67th percentile method, and why the old V1 boundaries would make nearly all U2MOT points Hard.

## v38 addition
The fourth contribution now explains the measured balance between tracking quality, identity stability and speed.
It also states why the paired bootstrap and the zero-tuning UAVDT test matter. The speaker note says this point
may be merged into the validation contribution when presentation time is short, but keeps it because it records
the evidence checks.

## v39 addition
The tracking-challenge overview now gives a complete plain-English definition for each challenge: what happens
in the image and how it can affect detection or identity tracking.

## v40 addition
The main slide titled “Benchmark Datasets” was removed at the user's request. The section ranges and all later
slide numbers were updated. Dataset facts still remain where they are needed for the experiment setup and results.
