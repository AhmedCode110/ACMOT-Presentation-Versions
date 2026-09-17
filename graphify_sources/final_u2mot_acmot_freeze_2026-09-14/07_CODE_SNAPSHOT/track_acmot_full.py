#!/usr/bin/env python3

from loguru import logger

import argparse
import csv
import os
import os.path as osp
import time

from glob import glob
from pathlib import Path

import cv2
import numpy as np
import torch

# ------------------------------------------------------------
# Import unchanged official U2MOT helpers
# ------------------------------------------------------------

from track import (
    make_parser,
    get_image_list,
    Predictor,
    parse_benchmark,
)

from yolox.exp import get_exp
from yolox.data.data_augment import preproc

from yolox.utils import (
    fuse_model,
    get_model_info,
    postprocess,
)

from yolox.tracker.u2mot_tracker import U2MOTTracker
from yolox.tracking_utils.timer import Timer

from acmot_v1 import SceneComplexityV1
from acmot_full_policy import FullACMOTV1Policy


# ============================================================
# Dynamic detector inference
# ============================================================

def inference_dynamic(
    predictor,
    raw_img,
    test_size,
    timer,
):

    height, width = raw_img.shape[:2]

    img, ratio = preproc(
        raw_img,
        test_size,
        Predictor.rgb_means,
        Predictor.std,
    )

    img = torch.from_numpy(img)
    img = img.unsqueeze(0)

    img = img.float().to(
        predictor.device
    )

    if predictor.fp16:
        img = img.half()

    with torch.no_grad():

        timer.tic()

        outputs, reid_feat = predictor.model(
            img
        )

        if predictor.decoder is not None:

            outputs = predictor.decoder(
                outputs,
                dtype=outputs.type()
            )

        outputs = postprocess(
            outputs,
            predictor.num_classes,
            predictor.confthre,
            predictor.nmsthre,
        )

    info = {
        "height": height,
        "width": width,
        "raw_img": raw_img,
        "ratio": ratio,
    }

    return (
        outputs,
        reid_feat,
        info,
    )


# ============================================================
# Full AC-MOT sequence processing
# ============================================================

def image_track_acmot(
    predictor,
    res_folder,
    video_path,
    args,
):

    files = get_image_list(
        video_path
    )

    files.sort()

    num_frames = len(files)

    video_name = osp.basename(
        video_path
    )

    if args.cmc_method != "none":

        assert args.cmc_file_dir != ""

        args.cmc_seq_name = (
            video_name
        )

    # --------------------------------------------------------
    # Tracker remains completely fixed
    # --------------------------------------------------------

    tracker = U2MOTTracker(
        args,
        frame_rate=args.fps
    )

    # --------------------------------------------------------
    # AC-MOT controller
    # --------------------------------------------------------

    analyzer = SceneComplexityV1(
        analysis_interval=10,
        smoothing_window=7,
    )

    policy = FullACMOTV1Policy()

    # Previous tracked boxes for SCI
    previous_tlwh = []

    timer = Timer()

    results = []

    s = min(
        predictor.model.head.strides
    )

    result_file = osp.join(
        res_folder,
        f"{video_name}.txt"
    )

    acmot_log_dir = osp.join(
        osp.dirname(res_folder),
        "acmot_logs"
    )

    os.makedirs(
        acmot_log_dir,
        exist_ok=True
    )

    csv_file = osp.join(
        acmot_log_dir,
        f"{video_name}.csv"
    )

    csv_rows = []

    seq_start = time.perf_counter()

    # --------------------------------------------------------
    # Per-frame loop
    # --------------------------------------------------------

    for frame_id, img_path in enumerate(
        files,
        1
    ):

        frame_start = time.perf_counter()

        raw_img = cv2.imread(
            img_path
        )

        if raw_img is None:
            raise RuntimeError(
                f"Could not read {img_path}"
            )

        # ----------------------------------------------------
        # Scene Complexity Index
        # ----------------------------------------------------

        sci, cues, sci_updated = (
            analyzer.update(
                raw_img,
                previous_tlwh,
                frame_id,
            )
        )

        action = policy.action(
            sci
        )

        # ----------------------------------------------------
        # FULL AC-MOT
        #
        # Detector side ONLY
        # ----------------------------------------------------

        predictor.confthre = (
            action["conf"]
        )

        predictor.nmsthre = (
            action["nms"]
        )

        predictor.test_size = (
            action["size"]
        )

        current_size = (
            predictor.test_size
        )

        # ----------------------------------------------------
        # Detector
        # ----------------------------------------------------

        (
            outputs,
            reid_feat,
            img_info,
        ) = inference_dynamic(
            predictor,
            raw_img,
            current_size,
            timer,
        )

        ny, nx = (
            reid_feat.shape[1:3]
        )

        online_tlwhs = []
        online_ids = []
        online_scores = []
        online_cls = []

        # ----------------------------------------------------
        # Tracker
        # ----------------------------------------------------

        if outputs[0] is not None:

            outputs_np = (
                outputs[0]
                .cpu()
                .numpy()
            )

            # Preserve original U2MOT behavior
            outputs_np = outputs_np[
                np.argsort(
                    outputs_np[:, 0]
                )
            ]

            reid_np = (
                reid_feat[0]
                .cpu()
                .numpy()
            )

            x1, y1, x2, y2 = (
                outputs_np[:, :4].T
                / s
            )

            xc = (
                (x1 + x2) / 2.0
            ).clip(
                0,
                nx - 1
            ).astype(
                np.int32
            )

            yc = (
                (y1 + y2) / 2.0
            ).clip(
                0,
                ny - 1
            ).astype(
                np.int32
            )

            embeddings = (
                reid_np[
                    yc,
                    xc,
                    :
                ]
            )

            online_targets = (
                tracker.update(
                    outputs_np,
                    (
                        img_info["height"],
                        img_info["width"],
                    ),
                    current_size,
                    embeddings=embeddings,
                    img=img_info["raw_img"],
                    use_uncertainty=args.use_uncertainty,
                )
            )

            for t in online_targets:

                tlwh = t.tlwh
                tid = t.track_id

                if (
                    tlwh[2] * tlwh[3]
                    > args.min_box_area
                    and
                    tlwh[2] / tlwh[3]
                    < args.aspect_ratio_thresh
                    and
                    tlwh[3] / tlwh[2]
                    < 4.0
                ):

                    online_tlwhs.append(
                        tlwh.copy()
                    )

                    online_ids.append(
                        tid
                    )

                    online_scores.append(
                        t.score
                    )

                    online_cls.append(
                        t.cls
                    )

                    results.append(
                        f"{frame_id},"
                        f"{tid},"
                        f"{tlwh[0]:.2f},"
                        f"{tlwh[1]:.2f},"
                        f"{tlwh[2]:.2f},"
                        f"{tlwh[3]:.2f},"
                        f"{t.score:.2f},"
                        f"{int(t.cls)+1},"
                        f"-1,-1\n"
                    )

        # Important:
        # timer starts before model and ends after tracker,
        # matching original U2MOT timing style.

        timer.toc()

        previous_tlwh = [
            box.copy()
            for box in online_tlwhs
        ]

        frame_wall = (
            time.perf_counter()
            - frame_start
        )

        cue_data = cues or {}

        csv_rows.append({
            "frame": frame_id,
            "sci": float(sci),
            "sci_updated": int(sci_updated),
            "tier": action["tier"],
            "confidence": action["conf"],
            "nms": action["nms"],
            "input_h": current_size[0],
            "input_w": current_size[1],
            "tracked_boxes": len(online_tlwhs),
            "crowd": cue_data.get("crowd", ""),
            "tiny": cue_data.get("tiny", ""),
            "edge_norm": cue_data.get("edge_norm", ""),
            "night": cue_data.get("night", ""),
            "blur": cue_data.get("blur", ""),
            "sci_raw": cue_data.get("raw", ""),
            "laplacian_variance": cue_data.get(
                "laplacian_variance",
                ""
            ),
            "frame_wall_ms": (
                frame_wall * 1000.0
            ),
        })

        if frame_id % 100 == 0:

            logger.info(
                "Processing frame {}/{} "
                "({:.2f} core fps) | "
                "SCI {:.3f} | {} | "
                "conf {:.3f} | "
                "NMS {:.3f} | "
                "{}x{}".format(
                    frame_id,
                    num_frames,
                    1.0 / max(
                        1e-5,
                        timer.average_time
                    ),
                    sci,
                    action["tier"],
                    action["conf"],
                    action["nms"],
                    current_size[1],
                    current_size[0],
                )
            )

    # --------------------------------------------------------
    # Save MOT results
    # --------------------------------------------------------

    with open(
        result_file,
        "w"
    ) as f:

        f.writelines(
            results
        )

    # --------------------------------------------------------
    # Save AC-MOT controller log
    # --------------------------------------------------------

    with open(
        csv_file,
        "w",
        newline=""
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=list(
                csv_rows[0].keys()
            )
        )

        writer.writeheader()
        writer.writerows(
            csv_rows
        )

    seq_elapsed = (
        time.perf_counter()
        - seq_start
    )

    wall_fps = (
        num_frames
        / seq_elapsed
    )

    logger.info(
        f"save results to {result_file}"
    )

    logger.info(
        f"save AC-MOT log to {csv_file}"
    )

    logger.info(
        "AC-MOT sequence summary | "
        f"frames={num_frames} | "
        f"wall_time={seq_elapsed:.3f}s | "
        f"wall_fps={wall_fps:.3f} | "
        f"core_fps="
        f"{1.0 / max(1e-5, timer.average_time):.3f}"
    )


# ============================================================
# Main
# ============================================================

def main(exp, args):

    if not args.experiment_name:

        args.experiment_name = (
            exp.exp_name
            + "_ACMOT_FULL"
        )

    output_dir = osp.join(
        exp.output_dir,
        args.experiment_name
    )

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    res_folder = osp.join(
        output_dir,
        "track_res"
    )

    os.makedirs(
        res_folder,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Device — same logic as official script
    # --------------------------------------------------------

    if (
        args.device != "cpu"
        and
        isinstance(
            eval(args.device),
            int
        )
    ):
        os.environ[
            "CUDA_VISIBLE_DEVICES"
        ] = args.device

    args.device = torch.device(
        "cuda"
        if args.device != "cpu"
        else "cpu"
    )

    logger.info(
        f"Args: {args}"
    )

    # --------------------------------------------------------
    # Model
    # --------------------------------------------------------

    model = exp.get_model().to(
        args.device
    )

    logger.info(
        "Model Summary: {}".format(
            get_model_info(
                model,
                exp.test_size
            )
        )
    )

    model.eval()

    ckpt_file = args.ckpt

    logger.info(
        "loading checkpoint"
    )

    ckpt = torch.load(
        ckpt_file,
        map_location="cpu",
        weights_only=False,
    )

    model.load_state_dict(
        ckpt["model"]
    )

    logger.info(
        "loaded checkpoint done."
    )

    if args.fuse:

        logger.info(
            "\tFusing model..."
        )

        model = fuse_model(
            model
        )

    if args.fp16:

        model = model.half()

    predictor = Predictor(
        model,
        exp,
        None,
        None,
        args.device,
        args.fp16,
    )

    # --------------------------------------------------------
    # Sequence loop
    # --------------------------------------------------------

    for video_path in sorted(
        glob(
            osp.join(
                args.path,
                "*"
            )
        )
    ):

        # EXACT official benchmark configuration
        if not parse_benchmark(
            predictor,
            video_path,
            exp,
            args,
        ):
            continue

        # Detector-side adaptive layer starts here.
        image_track_acmot(
            predictor,
            res_folder,
            video_path,
            args,
        )


if __name__ == "__main__":

    parser = make_parser()

    args = parser.parse_args()

    exp = get_exp(
        args.exp_file,
        args.name
    )

    main(
        exp,
        args
    )
