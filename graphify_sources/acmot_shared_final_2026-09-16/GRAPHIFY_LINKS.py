"""Graphify-only links for immutable AC-MOT evidence files.

This file does not implement an experiment and does not change any result.
It makes non-code evidence files discoverable in the project graph.
"""

DRIVE_FOLDER_ID = "1RRjzBy1Q_K4415A1x4FCD7B4xb60QYBs"
LOCAL_FROZEN_V1 = "../acmot_frozen_v1_implementation_2026-09-16"

FINAL_TEST_EVIDENCE = (
    "FINAL_TEST_3WORKER_PROTOCOL.json",
    "FINAL_TEST_DONE.json",
    "FINAL_TEST_RESULTS_3WORKER.json",
    "FINAL_TEST_COMPARISON_3WORKER.csv",
    "FINAL_TEST_WORKER_1_BASELINE_DEFAULT.json",
    "FINAL_TEST_WORKER_2_OLD_ACMOT_FROZEN.json",
    "FINAL_TEST_WORKER_3_NEW_ACMOT_FROZEN.json",
)

FROZEN_AND_CALIBRATION_EVIDENCE = (
    "FROZEN_DEFENSIBLE_ACMOT_CONFIG.json",
    "FROZEN_TEMPORAL_CONFIG.json",
    "SCIENTIFIC_SEARCH_SPACE.json",
    "DETECTOR_DERIVED_CUE_CALIBRATION.json",
    "OLD_A3_VALIDATION_W7_S10.json",
)

SEARCH_AND_ABLATION_EVIDENCE = (
    "EMPIRICAL_OPTUNA_TRIALS.csv",
    "EMPIRICAL_OPTUNA.db",
    "EMPIRICAL_STUDY_SIGNATURE.json",
    "EMPIRICAL_PARAMETER_IMPORTANCE_MOTA.json",
    "OPERATING_RESOLUTION_SWEEP.csv",
    "OPERATING_CONFIDENCE_SWEEP.csv",
    "OPERATING_NMS_SWEEP.csv",
    "OPERATING_ABLATION_REPORT.json",
    "TEMPORAL_ABLATION_FULL.csv",
    "TEMPORAL_ABLATION_RANKED.csv",
    "OLD_ACMOT_COMPONENT_ABLATION.csv",
    "OLD_ACMOT_COMPONENT_ABLATION_REPORT.json",
    "OLD_ACMOT_COMPONENT_ABLATION_DONE.json",
    "NEW_ACMOT_COMPONENT_ABLATION.csv",
    "NEW_ACMOT_COMPONENT_ABLATION_REPORT.json",
    "NEW_ACMOT_COMPONENT_ABLATION_DONE.json",
    "NEW_ABLATION_A0.json",
    "NEW_ABLATION_A1.json",
    "NEW_ABLATION_A2.json",
    "NEW_ABLATION_A3.json",
    "NEW_ABLATION_HIST.json",
    "WORKER3_JOINT_DONE.json",
)

TEMPORAL_GRID_EVIDENCE = tuple(
    f"TEMPORAL_W{window}_S{stride}.json"
    for window in (1, 3, 5, 7, 9)
    for stride in (1, 5, 10, 15, 20)
)

EXCLUDED_SMOKE_FILES = (
    "OPERATING_RESOLUTION_SWEEP_SMOKE.csv",
    "OPERATING_CONFIDENCE_SWEEP_SMOKE.csv",
    "OPERATING_NMS_SWEEP_SMOKE.csv",
    "TEMPORAL_ABLATION_SMOKE.csv",
    "WORKER2_TEMPORAL_SMOKE_DONE.json",
)


def evidence_groups():
    """Return the evidence groups used by the AC-MOT final graph."""
    return {
        "final_test": FINAL_TEST_EVIDENCE,
        "frozen_calibration": FROZEN_AND_CALIBRATION_EVIDENCE,
        "search_ablation": SEARCH_AND_ABLATION_EVIDENCE,
        "temporal_grid_25_completed": TEMPORAL_GRID_EVIDENCE,
        "excluded_smoke": EXCLUDED_SMOKE_FILES,
    }
