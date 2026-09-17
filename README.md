# ACMOT-Presentation-Versions

Interactive HTML versions of the AC-MOT Master's presentation (`versions/vNN-…`, newest = `current`), plus the
**research roadmap** below: where every number, config and result of the project lives, so any supervisor question
("where does this number come from?") can be answered from the right file.

- Open the newest deck: `open ~/Desktop/ACMOT-Presentation-Versions/current/index.html`
- What changed in each version: [`VERSION_HISTORY.md`](VERSION_HISTORY.md)
- Where the numbers on the slides come from: [`SOURCE_MAP.md`](SOURCE_MAP.md)

---

# Research roadmap — where is everything?

## Roots

| What | Path |
|---|---|
| Scientific root (Google Drive, Colab path) | `/content/drive/MyDrive/AC-MOT-shared/` |
| Final freeze after UAVDT | `/content/drive/MyDrive/AC-MOT-shared/[FROZEN][DO_NOT_MODIFY]_ACMOT_2026-09-12_FINAL_AFTER_UAVDT/` |
| **Top reference file** | `ACMOT_FINAL_SCIENTIFIC_FREEZE_2026-09-12.md` — the main scientific index: final V1, final V2, VisDrone test, UAVDT, commits, paths, frozen values, do-not-modify rules |
| V1 scientific root (canonical) | `/content/drive/MyDrive/AC-MOT-shared/defensible_acmot_3workers/` |
| V1 post-hoc statistics | `/content/drive/MyDrive/AC-MOT-shared/V1_POSTHOC_ANALYSIS_2026-09-12/` |
| Datasets | `/content/drive/MyDrive/AC-MOT-shared/AC-MOT-data/` → `VisDrone2019-MOT-val/`, `VisDrone2019-MOT-test-dev/` |

> On this Mac, `AC-MOT-shared` is **not** synced to Google Drive for Desktop (it is not in My Drive). Local copies
> found so far: `CLAUDECODEX/Master/macneo_wrk/ACMOT_V1_FINAL_POST_SNAPSHOT_2026-09-12/02_FINAL_DRIVE_ARTIFACTS/defensible_acmot_3workers/`
> (config + final test files) and `~/Downloads/EMPIRICAL_OPTUNA_TRIALS.csv` / `EMPIRICAL_OPTUNA.db` (copied into
> `versions/v26-v1-trials-curve/assets/data/source/`).

## Trust order when numbers disagree

1. Final scientific freeze (`ACMOT_FINAL_SCIENTIFIC_FREEZE_2026-09-12.md`)
2. Frozen JSON / CSV result
3. Frozen Git commit
4. Development output
5. Old notebook
6. Presentation slide — **a slide is never the original source of a number**

---

## 1. Which version is final and approved?
`[FROZEN][DO_NOT_MODIFY]_ACMOT_2026-09-12_FINAL_AFTER_UAVDT/ACMOT_FINAL_SCIENTIFIC_FREEZE_2026-09-12.md` — check it first for any conflict.

The current interactive deck is `versions/v64-media-libraries/`. It keeps all 32 local figure assets available through the Pictures toolbar button, and all five local videos in a separate Videos library. Explanation pages are fitted when opened so their text and media remain readable.

## 2. V1 and Optuna — `defensible_acmot_3workers/`
| File | Use it when asked |
|---|---|
| `EMPIRICAL_OPTUNA_TRIALS.csv` | every trial's MOTA / IDS / FPS, the rank of Trial 24, the Optuna curve, why Trial 24 was chosen |
| `EMPIRICAL_OPTUNA.db` | "do you have the original Optuna study, not just a CSV?" |
| `EMPIRICAL_STUDY_SIGNATURE.json` | study name, objective direction, search setup, metadata |
| `EMPIRICAL_PARAMETER_IMPORTANCE_MOTA.json` | which parameter affected MOTA most |

From the CSV: 50 completed trials (trial 33 started but never finished), 37 feasible, 13 broke IDS ≤ 271, none below 25 FPS; Trial 24 has the highest MOTA of all (23.038 %, IDS 270, FPS 37.17).

## 3. Trial 24 final parameters
`FROZEN_DEFENSIBLE_ACMOT_CONFIG.json` — `weight_crowd`, `weight_tiny`, `weight_edge`, `weight_night`, `weight_blur`, `conf_easy`, `conf_hard`, `nms_easy`, `nms_hard`, `threshold_mid`, `threshold_high`. Answer to "where did these weights come from?".

## 4. OLD-A3 reference
`OLD_A3_VALIDATION_W7_S10.json` — the reference used in the V1 selection rule:
MOTA 18.1647 % · HOTA 33.0640 % · IDF1 36.2962 % · IDS 271 · **FPS 42.08546**.
If asked "37.96 or 42.085?": the **OLD-A3 reference used in V1 selection = 42.085 FPS** (freeze). The deck's ablation
table shows 37.96 FPS (author's ablation table, kept by the author's decision on 2026-09-15).

## 5. How the search space was chosen before Optuna
| File | Justifies |
|---|---|
| `OPERATING_RESOLUTION_SWEEP.csv` | resolution levels 512 · 928 · 960 |
| `OPERATING_CONFIDENCE_SWEEP.csv` | confidence values 0.25 · 0.30 · 0.35 · 0.40 · 0.45 |
| `OPERATING_NMS_SWEEP.csv` | NMS range 0.30 → 0.70 |

## 6. Smoothing window and analysis stride
`TEMPORAL_ABLATION_FULL.csv` (all runs) and `TEMPORAL_ABLATION_RANKED.csv` (ranked) → **window = 7, stride = 10**.

## 7. Cue calibration
`DETECTOR_DERIVED_CUE_CALIBRATION.json` — the freeze describes it as fixed detector outputs + validation image statistics; no ground-truth crowd counts. Open it first if asked whether V1 used cue calibration.

## 8. SCI constants
Crowd divisor 30 · tiny = box area < 32 × 32 · Canny 50 / 120 · edge normalisation 0.14 · night threshold 80 · blur Laplacian variance 180.
Look in `FROZEN_DEFENSIBLE_ACMOT_CONFIG.json`; code in the repo `AhmedCode110/AC-MOT`. The freeze records a fixed pretrained YOLOv8n and a fixed tuned ByteTrack.

## 9. Old AC-MOT component ablation
`OLD_ACMOT_COMPONENT_ABLATION.csv` (main) · `OLD_ACMOT_COMPONENT_ABLATION_REPORT.json` · `OLD_ACMOT_COMPONENT_ABLATION_DONE.json` — what tracker tuning, adaptive confidence / NMS and resolution each changed.

## 10. New AC-MOT (V1) component ablation
`NEW_ACMOT_COMPONENT_ABLATION.csv` · `NEW_ACMOT_COMPONENT_ABLATION_REPORT.json` · `NEW_ACMOT_COMPONENT_ABLATION_DONE.json`. Keep OLD AC-MOT and NEW AC-MOT / V1 separate.

## 11. Final VisDrone test (`defensible_acmot_3workers/`)
| File | Content |
|---|---|
| `FINAL_TEST_RESULTS_3WORKER.json` | **the final reference** for Baseline, Old AC-MOT and V1 |
| `FINAL_TEST_WORKER_1_BASELINE_DEFAULT.json` | Baseline details |
| `FINAL_TEST_WORKER_2_OLD_ACMOT_FROZEN.json` | Old AC-MOT details |
| `FINAL_TEST_WORKER_3_NEW_ACMOT_FROZEN.json` | V1 details |
| `FINAL_TEST_COMPARISON_3WORKER.csv` | quick comparison table |
| `FINAL_TEST_3WORKER_PROTOCOL.json` | how the evaluation was done |
| `FINAL_TEST_DONE.json` | completion proof |

## 12. Final test numbers (VisDrone2019-MOT test-dev, from the freeze)
| System | MOTA | HOTA | IDF1 | IDS | FPS |
|---|---|---|---|---|---|
| Baseline | 19.729 | 28.430 | 32.724 | 1235 | 36.528 |
| Old AC-MOT | 23.236 | 32.698 | 39.516 | 1061 | 41.957 |
| V1 | 26.948 | 33.835 | 41.546 | 1184 | 38.985 |

## 13. Statistical significance — `V1_POSTHOC_ANALYSIS_2026-09-12/`
| File | Use it when asked |
|---|---|
| `V1_PAIRED_BOOTSTRAP_SAMPLES.csv` | how the bootstrap was done (5,000 paired resamples, seed 42) |
| `V1_PAIRED_BOOTSTRAP_95CI.csv` | the confidence intervals |

V1 vs Baseline (freeze): MOTA +7.22 [5.44, 9.29] · HOTA +5.41 [4.13, 6.90] · IDF1 +8.82 [6.90, 11.05].

## 14. Per-sequence results
`V1_PER_SEQUENCE_METRICS.csv` — answers "maybe only one or two videos improved?" sequence by sequence.

## 15. Rebuilding tracker outputs (reproducibility)
In the post-hoc folder: `reconstructed_tracker_files/` · `RECONSTRUCTED_TRACKER_MANIFEST.csv` · `V1_PER_SEQUENCE_EVAL_INPUT/` · `V1_PER_SEQUENCE_TRACKEVAL/`.

## 16. V2
Freeze: `ACMOT_FINAL_SCIENTIFIC_FREEZE_2026-09-12.md` · branch `experiment/multiobjective-mota-ids-v2` · commit `2b400347584512ebc09527a3e0e01dad82299329`.
Code: `scripts/optuna_sci_v2_multiobjective_validation.py` · `scripts/run_v2_colab_shared.py` · `config/V2_COLAB_SHARED_PATHS.json` · `docs/V2_DEVELOPMENT_STATUS.md`.

## 17. V2 final test
Runner `scripts/run_v2_trial22_testdev_technical_rerun.py` · launcher `scripts/run_v2_trial22_testdev_colab_launcher.py` · final candidate **Trial 22** (confirmed in the freeze).

## 18. Why V2?
V1 = quality-oriented. V2 = maximise MOTA and minimise IDS under a real-time constraint — a **different operating trade-off**, not a replacement for V1.

## 19. UAVDT
Frozen runner `scripts/run_uavdt_external_generalization_frozen.py` (commit `17e9319036d403559ca005289750b7a62432fa1f`) · launcher `scripts/run_uavdt_external_colab_launcher.py` (commit `1882ece5dc0662f889c75f5ca48ac5d427489f42`).

## 20. UAVDT final numbers
| System | MOTA | HOTA | IDF1 | IDS | FPS |
|---|---|---|---|---|---|
| Baseline | 13.841 | 24.085 | 27.887 | 558 | 65.015 |
| V1 | 17.399 | 28.390 | 34.453 | 321 | 58.353 |
| V2 | 16.118 | 26.930 | 32.014 | 308 | 61.462 |

Message: V1 → best quality; V2 → fewer ID switches and faster than V1.

## 21. Datasets
`/content/drive/MyDrive/AC-MOT-shared/AC-MOT-data/` → validation `VisDrone2019-MOT-val/`, test `VisDrone2019-MOT-test-dev/`.

## 22. GitHub versions used
- **V1:** repo `AhmedCode110/AC-MOT` · branch `acmot-final-frozen-2026-09-11` · commit `a6c1fa49fce1d402513c2df05b7d04b962a6e89e` · tag `v1.0.0-acmot-frozen`
- **Final freeze after UAVDT:** branch `freeze/final-after-uavdt-2026-09-12`

## 23. Environment (from the freeze)
`ultralytics == 8.3.200` · `numpy == 2.2.6` · `scipy == 1.15.3` · `opencv-python-headless` · `pandas` · `matplotlib` · `lap` · GPU Tesla T4.

## 24. Old notebooks — historical / development only
`AC_MOT_v12_Colab.ipynb` · `AC_MOT_FULL17_Recorded_Replay_20260905.ipynb` · `AC_MOT_Optuna_Val_Test_Colab.ipynb` · `AC_MOT_Optuna_Val_Test_OfficialVisDrone.ipynb` · `AC_MOT_Optuna_Full_VisDrone_Official5.ipynb` · `AC_MOT_Optuna_SCI_Only_NoTraining.ipynb` · `AC_MOT_Optuna_SCI_Only_RUN_ALL.ipynb` · `AC_MOT_Optuna_SCI_Only_RUN_ALL_v2.ipynb`.
Never use them as the final source when a newer freeze exists.

---

# Quick cheat sheet

| Question | File |
|---|---|
| All V1 trials? | `EMPIRICAL_OPTUNA_TRIALS.csv` |
| Optuna database? | `EMPIRICAL_OPTUNA.db` |
| Trial 24 final params? | `FROZEN_DEFENSIBLE_ACMOT_CONFIG.json` |
| Old-A3 reference? | `OLD_A3_VALIDATION_W7_S10.json` |
| Old-A3 FPS (V1 reference)? | **42.085** |
| Resolution sweep? | `OPERATING_RESOLUTION_SWEEP.csv` |
| Confidence sweep? | `OPERATING_CONFIDENCE_SWEEP.csv` |
| NMS sweep? | `OPERATING_NMS_SWEEP.csv` |
| Window / stride? | `TEMPORAL_ABLATION_FULL.csv` |
| Cue calibration? | `DETECTOR_DERIVED_CUE_CALIBRATION.json` |
| Old ablation? | `OLD_ACMOT_COMPONENT_ABLATION.csv` |
| New ablation? | `NEW_ACMOT_COMPONENT_ABLATION.csv` |
| Final test? | `FINAL_TEST_RESULTS_3WORKER.json` |
| Baseline raw final? | `FINAL_TEST_WORKER_1_BASELINE_DEFAULT.json` |
| Old AC-MOT raw? | `FINAL_TEST_WORKER_2_OLD_ACMOT_FROZEN.json` |
| V1 raw final? | `FINAL_TEST_WORKER_3_NEW_ACMOT_FROZEN.json` |
| Bootstrap? | `V1_PAIRED_BOOTSTRAP_95CI.csv` |
| Per sequence? | `V1_PER_SEQUENCE_METRICS.csv` |
| V2 code? | `optuna_sci_v2_multiobjective_validation.py` |
| UAVDT runner? | `run_uavdt_external_generalization_frozen.py` |
| Top reference? | `ACMOT_FINAL_SCIENTIFIC_FREEZE_2026-09-12.md` |
