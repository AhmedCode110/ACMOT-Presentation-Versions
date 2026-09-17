# Official U2MOT + AC-MOT Freeze

This folder is a copy of the official final freeze from Google Drive.

Drive folder: `FINAL_U2MOT_ACMOT_FREEZE_2026-09-14`

Drive folder ID: `1PgeAEKYEWRTsqLjQCcAuBXba4y8YdW2w`

Official summary: `00_SUMMARY/FINAL_SCIENTIFIC_SUMMARY.txt`

## Evidence chain

`07_CODE_SNAPSHOT` -> `02_SCI_CALIBRATION` -> `03_VALIDATION_COMPARISON` -> `04_MATCHED_RUNTIME` -> `05_VALIDATED_CONTROLLER_FREEZE` -> `06_FINAL_TESTDEV_17SEQ`

## Official result status

- The SCI weights from V1 are preserved.
- The Easy, Medium, and Hard boundaries are calibrated on validation data.
- The controller is frozen before the final test-dev run.
- The final test-dev run uses 17 sequences and 6635 frames.
- Test-dev is not used for tuning.
- The pinned U2MOT commit and checkpoint hash are recorded in the summary and final metrics.

## Included evidence

- Summary, manifest, and checksums.
- Baseline evaluation and tracking outputs.
- SCI values for all frames and update points.
- Validation comparison outputs and logs.
- Matched runtime frame logs and summaries.
- Frozen controller configuration and declaration.
- Final test-dev metrics, comparison, frame logs, tracking logs, and per-sequence outputs.
- Code snapshot and provenance files.

All files are retained because this is the official final freeze. No file was excluded as a smoke test.
