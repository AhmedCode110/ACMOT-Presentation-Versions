"""Graphify links for the official U2MOT + AC-MOT final freeze."""

DRIVE_FOLDER_ID = "1PgeAEKYEWRTsqLjQCcAuBXba4y8YdW2w"
OFFICIAL_SUMMARY = "00_SUMMARY/FINAL_SCIENTIFIC_SUMMARY.txt"
FINAL_METRICS = "06_FINAL_TESTDEV_17SEQ/FINAL_METRICS.json"
FINAL_COMPARISON = "06_FINAL_TESTDEV_17SEQ/FINAL_COMPARISON.csv"
FROZEN_CONFIG = "05_VALIDATED_CONTROLLER_FREEZE/FROZEN_CONFIG.json"
U2MOT_CODE = "07_CODE_SNAPSHOT"


def official_freeze_evidence():
    """Connect the official freeze stages to their evidence folders."""
    return {
        "summary": "00_SUMMARY",
        "baseline": "01_A0_BASELINE",
        "sci_calibration": "02_SCI_CALIBRATION",
        "validation": "03_VALIDATION_COMPARISON",
        "matched_runtime": "04_MATCHED_RUNTIME",
        "controller_freeze": "05_VALIDATED_CONTROLLER_FREEZE",
        "final_testdev": "06_FINAL_TESTDEV_17SEQ",
        "code": "07_CODE_SNAPSHOT",
        "provenance": "08_PROVENANCE",
    }
