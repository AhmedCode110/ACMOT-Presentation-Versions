# AC-MOT Final Evidence Index

This index connects the downloaded result files to the implemented AC-MOT experiment and the frozen V1 implementation.

## Authority chain

`frozen implementation` -> `frozen configuration` -> `validation search and sweeps` -> `final three-worker test` -> `presentation results`

The files are copies from Drive folder `1RRjzBy1Q_K4415A1x4FCD7B4xb60QYBs`. The original files remain in Drive.

## Final test evidence

- `FINAL_TEST_3WORKER_PROTOCOL.json`
- `FINAL_TEST_DONE.json`
- `FINAL_TEST_RESULTS_3WORKER.json`
- `FINAL_TEST_COMPARISON_3WORKER.csv`
- `FINAL_TEST_WORKER_1_BASELINE_DEFAULT.json`
- `FINAL_TEST_WORKER_2_OLD_ACMOT_FROZEN.json`
- `FINAL_TEST_WORKER_3_NEW_ACMOT_FROZEN.json`

These files support the held-out final comparison between the baseline, old AC-MOT, and new AC-MOT.

## Frozen and calibration evidence

- `FROZEN_DEFENSIBLE_ACMOT_CONFIG.json`
- `FROZEN_TEMPORAL_CONFIG.json`
- `SCIENTIFIC_SEARCH_SPACE.json`
- `DETECTOR_DERIVED_CUE_CALIBRATION.json`
- `OLD_A3_VALIDATION_W7_S10.json`

These files define the frozen settings, search limits, detector-derived cue calibration, and the old-A3 validation reference.

## Search and ablation evidence

- `EMPIRICAL_OPTUNA_TRIALS.csv`
- `EMPIRICAL_OPTUNA.db`
- `EMPIRICAL_STUDY_SIGNATURE.json`
- `EMPIRICAL_PARAMETER_IMPORTANCE_MOTA.json`
- `OPERATING_RESOLUTION_SWEEP.csv`
- `OPERATING_CONFIDENCE_SWEEP.csv`
- `OPERATING_NMS_SWEEP.csv`
- `OPERATING_ABLATION_REPORT.json`
- `TEMPORAL_ABLATION_FULL.csv`
- `TEMPORAL_ABLATION_RANKED.csv`
- `TEMPORAL_W1_S1.json` through `TEMPORAL_W9_S20.json` for all 25 completed temporal pairs
- `OLD_ACMOT_COMPONENT_ABLATION.csv`
- `OLD_ACMOT_COMPONENT_ABLATION_REPORT.json`
- `OLD_ACMOT_COMPONENT_ABLATION_DONE.json`
- `NEW_ACMOT_COMPONENT_ABLATION.csv`
- `NEW_ACMOT_COMPONENT_ABLATION_REPORT.json`
- `NEW_ACMOT_COMPONENT_ABLATION_DONE.json`
- `NEW_ABLATION_A0.json`, `NEW_ABLATION_A1.json`, `NEW_ABLATION_A2.json`, `NEW_ABLATION_A3.json`, and `NEW_ABLATION_HIST.json`
- `WORKER3_JOINT_DONE.json`

These are retained because they contain complete results or explain how the final configuration was selected.

## Excluded files

The four `*_SMOKE.csv` files and `WORKER2_TEMPORAL_SMOKE_DONE.json` were not copied. They are smoke or temporary checks and are not evidence for reported results.

## Verification notes

The downloaded JSON files parse successfully. The downloaded Optuna database passes SQLite integrity check. The eight overlapping final and frozen files match the local frozen V1 snapshot byte-for-byte.

The presentation must keep validation, search, ablation, and held-out test numbers separate. If timing values differ between ablation, frozen reference, and temporal sweep files, preserve the source label and do not treat them as interchangeable.
