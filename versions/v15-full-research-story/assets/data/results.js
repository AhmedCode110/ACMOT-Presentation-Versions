/* =====================================================================
   AC-MOT presentation — SINGLE SOURCE OF TRUTH for every number shown.
   Edit a value here and every chart and bound number updates.
   Each block names its provenance; the label is printed on the slide.
   Sources are listed in README.md ("Where the results come from").
   ===================================================================== */
window.ACMOT = {

  /* Early exploratory detector timing. Values as recorded by the author;
     the raw timing log is NOT archived in the frozen evidence. */
  detectorTiming: {
    prov: 'Early exploratory measurement · raw log not archived',
    rows: [
      ['YOLOv10n', 28.85], ['YOLOv8n', 29.22], ['YOLOv10s', 31.01], ['YOLOv8s', 31.10],
      ['YOLOv10m', 40.90], ['YOLOv8m', 49.75], ['YOLOv8l', 61.46], ['YOLOv9c', 78.62],
      ['YOLOv8x', 79.36], ['YOLOv9e', 122.84]
    ]
  },

  /* Published model-card values (Ultralytics YOLOv8n, COCO val mAP50-95). */
  yolov8nPublished: { mAP: 37.3, paramsM: 3.2 },

  /* Original (hand-set) SCI and Smart Calibrator. */
  original: {
    weights: { crowd: 0.30, tiny: 0.30, edge: 0.20, night: 0.10, blur: 0.05 },
    calibrator: { conf0: 0.245, confSlope: 0.050, confMin: 0.19, confMax: 0.28,
                  iou0: 0.490, iouSlope: 0.050, iouMin: 0.40, iouMax: 0.52,
                  sizes: [640, 736, 832], sciMid: 0.35, sciHigh: 0.60 }
  },

  /* V1 — defensible joint Optuna study, VALIDATION (VisDrone2019-MOT-val, 7 seq).
     Source: FROZEN_DEFENSIBLE_ACMOT_CONFIG.json / final freeze doc §7. */
  v1: {
    prov: 'Validation result · VisDrone2019-MOT-val · 7 sequences · custom class-agnostic protocol',
    trial: 24, budget: 50,
    val: { mota: 23.0381, hota: 36.1102, idf1: 40.7578, ids: 270, fps: 37.1686 },
    oldA3val: { mota: 18.165, hota: 33.064, idf1: 36.296, ids: 271, fps: 42.085 },
    weights: { crowd: 0.12949277455301997, tiny: 0.22174766876599927, edge: 0.43371337893805056, night: 0.05355765312756694, blur: 0.16148852461536325 },
    params: { conf_easy: 0.30, conf_hard: 0.40, nms_easy: 0.35, nms_hard: 0.35,
              threshold_mid: 0.13534938199219218, threshold_high: 0.28728676236279177 }
  },

  /* v6 — ORIGINAL AC-MOT component ablation, exactly as supplied by the author for the
     research story. Separate experiment: never merge with the test-set comparison. */
  oldAblation: {
    prov: 'Ablation study · original AC-MOT components · not the final test set',
    rows: [
      { id: 'A0',  name: 'OLD-A0 · Baseline',                  mota: 17.633, hota: 29.837, idf1: 30.892, ids: 283, fps: 44.09 },
      { id: 'A1',  name: 'OLD-A1 · Tuned ByteTrack',           mota: 17.802, hota: 30.864, idf1: 32.854, ids: 217, fps: 44.51 },
      { id: 'A2',  name: 'OLD-A2 · Adaptive Confidence + NMS', mota: 17.636, hota: 31.384, idf1: 33.727, ids: 210, fps: 40.65 },
      { id: 'A2R', name: 'OLD-A2R · Adaptive Resolution Only', mota: 18.425, hota: 32.446, idf1: 35.669, ids: 241, fps: 39.56 },
      { id: 'A3',  name: 'OLD-A3 · Full AC-MOT',               mota: 18.165, hota: 33.064, idf1: 36.296, ids: 271, fps: 37.96 }
    ]
  },

  /* V2 — two-objective Pareto study (max MOTA, min IDS, FPS >= 25), VALIDATION.
     Planned 50 trials; exactly 49 COMPLETE. Source: final freeze doc §10-12. */
  v2: {
    prov: 'Validation result · V2 Pareto study · 49 completed trials · custom class-agnostic protocol',
    planned: 50, completed: 49, trial: 22,
    /* [trial, MOTA %, IDS] — notable Pareto points listed in the freeze doc */
    pareto: [
      [16, 22.83317, 308], [17, 22.80793, 294], [20, 22.75002, 289], [5, 22.68320, 284],
      [4, 22.60450, 262], [26, 22.09667, 233], [42, 20.66078, 219], [34, 19.84706, 214],
      [22, 19.33031, 168], [10, 18.65914, 160], [3, 17.48756, 148], [43, 15.75470, 142],
      [32, 15.71906, 136], [45, 15.11619, 135], [28, 15.07759, 117], [44, 11.78707, 115],
      [8, 11.53612, 114]
    ],
    val: { mota: 19.3303, hota: 31.6514, idf1: 34.2261, ids: 168, fps: 51.4063, fn: 49301, fp: 4858 },
    weights: { crowd: 0.1646453, tiny: 0.1746265, edge: 0.5076113, night: 0.1206956, blur: 0.0324213 },
    params: { conf_easy: 0.40, conf_hard: 0.40, nms_easy: 0.60, nms_hard: 0.35,
              threshold_mid: 0.29271, threshold_high: 0.66617 }
  },

  /* Held-out VisDrone2019-MOT test-dev (17 seq), custom class-agnostic TrackEval.
     Baseline / Old / V1 from FINAL_TEST_RESULTS_3WORKER.json; V2 from
     V2_TRIAL22_TESTDEV_RESULT.json (post-selection). Freeze doc §8, §13, §14. */
  testdev: {
    prov: 'Held-out test-dev result · 17 sequences · custom class-agnostic AC-MOT TrackEval protocol',
    rows: [
      { id: 'base', name: 'Baseline',    mota: 19.729, hota: 28.430, idf1: 32.724, ids: 1235, fn: 155051, fp: 16308, fps: 36.528 },
      { id: 'old',  name: 'Initial AC-MOT', mota: 23.236, hota: 32.698, idf1: 39.516, ids: 1061, fn: 138967, fp: 25025, fps: 41.957 },
      { id: 'v1',   name: 'V1 Trial 24', mota: 26.948, hota: 33.835, idf1: 41.546, ids: 1184, fn: 136858, fp: 19029, fps: 38.985 },
      { id: 'v2',   name: 'V2 Trial 22', mota: 23.792, hota: 31.218, idf1: 37.870, ids: 919,  fn: 149307, fp: 13632, fps: 46.024 }
    ],
    /* 5000 paired per-sequence bootstrap resamples, seed 42: [estimate, lo95, hi95] */
    bootstrap: {
      v1_vs_base: { mota: [7.2195, 5.4362, 9.2934], hota: [5.4051, 4.1273, 6.9022], idf1: [8.8220, 6.9005, 11.0537], idsRed: [51, -114, 219] },
      v2_vs_base: { mota: [4.06, 0.95, 6.89], hota: [2.79, 0.75, 4.66], idf1: [5.15, 2.03, 8.08], idsRed: [316, 175, 470] },
      v2_vs_v1:   { mota: [-3.16, -6.15, -1.35], hota: [-2.62, -4.00, -1.69], idf1: [-3.68, -5.88, -2.24], idsRed: [265, 82, 502] },
      v1_vs_old:  { mota: [3.71, 2.39, 5.19], idsRed: [-123, -244, -14] }
    }
  },

  /* UAVDT external generalization — zero tuning, frozen systems. Freeze doc §15-19. */
  uavdt: {
    prov: 'External test · UAVDT · 20 sequences / 16,592 frames · zero tuning · frozen systems',
    sequences: 20, frames: 16592,
    rows: [
      { id: 'base', name: 'Baseline',    mota: 13.841, hota: 24.085, idf1: 27.887, ids: 558, fn: 270189, fp: 22974, fps: 65.015 },
      { id: 'v1',   name: 'V1 Trial 24', mota: 17.399, hota: 28.390, idf1: 34.453, ids: 321, fn: 258376, fp: 22896, fps: 58.353 },
      { id: 'v2',   name: 'V2 Trial 22', mota: 16.118, hota: 26.930, idf1: 32.014, ids: 308, fn: 266894, fp: 18758, fps: 61.462 }
    ],
    bootstrap: {
      v1_vs_base: { mota: [3.56, 1.45, 5.81], hota: [4.31, 2.74, 5.71], idf1: [6.57, 3.81, 8.82], idsRed: [237, 104, 377] },
      v2_vs_base: { mota: [2.28, 0.72, 4.16], hota: [2.85, 1.24, 4.35], idf1: [4.13, 1.63, 6.49], idsRed: [250, 110, 404] },
      v2_vs_v1:   { mota: [-1.28, -2.44, -0.20], hota: [-1.46, -2.19, -0.91], idf1: [-2.44, -3.74, -1.37], idsRed: [13, -20, 50], fpRed: [4138, 2335, 6295] }
    }
  }
};

/* Published values collected in the IEEE ICMISI 2026 survey. */
window.ACMOT.published = {
  /* DroneMOT (ICRA 2024) reports ByteTrack on VisDrone2019-MOT test-dev — as supplied by the author */
  droneMOTByteTrack: { mota: 25.1, idf1: 40.8, ids: 1590 },
  prov: 'Published values collected in our IEEE ICMISI 2026 survey',
  mot17Mota: [['SORT', 43.1], ['DeepSORT', 59.8], ['FairMOT', 67.5], ['ByteTrack', 80.3], ['SMILEtrack', 81.7]],
  mot17Ids: [['SORT', 4852], ['ByteTrack', 2196], ['DeepSORT', 1455], ['OC-SORT', 784]]
};

/* Test-dev density (VERIFICATION_REPORT.md: TrackEval GT_Dets = 215,014 over 6,635 frames). */
window.ACMOT.visdroneTest = { sequences: 17, frames: 6635, gtBoxes: 215014, density: 32.4 };
