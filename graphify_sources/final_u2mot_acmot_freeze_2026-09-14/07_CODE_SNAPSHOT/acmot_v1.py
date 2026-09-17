
from collections import deque

import cv2
import numpy as np


class SceneComplexityV1:
    """
    AC-MOT V1 Scene Complexity Index.

    SCI weights transferred directly from the
    previously validated AC-MOT V1 configuration.

    Detector/action mapping is NOT transferred.
    """

    def __init__(
        self,
        analysis_interval=10,
        smoothing_window=7
    ):
        self.analysis_interval = analysis_interval

        self.history = deque(
            maxlen=smoothing_window
        )

        self.last_sci = 0.0

        # V1 SCI weights
        self.w_crowd = 0.12949277455301997
        self.w_tiny  = 0.22174766876599927
        self.w_edge  = 0.43371337893805056
        self.w_night = 0.05355765312756694
        self.w_blur  = 0.16148852461536325

    def compute_raw(
        self,
        frame_bgr,
        previous_tlwh
    ):
        # ----------------------------------------------
        # Downscale frame to 25%
        # ----------------------------------------------

        small = cv2.resize(
            frame_bgr,
            None,
            fx=0.25,
            fy=0.25,
            interpolation=cv2.INTER_AREA
        )

        gray = cv2.cvtColor(
            small,
            cv2.COLOR_BGR2GRAY
        )

        # ----------------------------------------------
        # Crowd density
        # ----------------------------------------------

        count = len(previous_tlwh)

        crowd = min(
            count / 30.0,
            1.0
        )

        # ----------------------------------------------
        # Tiny-object ratio
        # ----------------------------------------------

        if count == 0:

            tiny = 0.0

        else:

            tiny_count = 0

            for box in previous_tlwh:

                x, y, w, h = box

                if w * h < (32.0 * 32.0):
                    tiny_count += 1

            tiny = tiny_count / float(count)

        # ----------------------------------------------
        # Edge complexity
        # ----------------------------------------------

        edge_map = cv2.Canny(
            gray,
            50,
            120
        )

        edge = (
            float(edge_map.mean())
            / 255.0
        )

        edge_norm = min(
            edge / 0.14,
            1.0
        )

        # ----------------------------------------------
        # Low light
        # ----------------------------------------------

        night = (
            1.0
            if float(gray.mean()) < 80.0
            else 0.0
        )

        # ----------------------------------------------
        # Blur
        # ----------------------------------------------

        lap_var = float(
            cv2.Laplacian(
                gray,
                cv2.CV_64F
            ).var()
        )

        blur = (
            1.0
            if lap_var < 180.0
            else 0.0
        )

        # ----------------------------------------------
        # V1 weighted SCI
        # ----------------------------------------------

        raw = (
            self.w_crowd * crowd
            + self.w_tiny * tiny
            + self.w_edge * edge_norm
            + self.w_night * night
            + self.w_blur * blur
        )

        raw = float(
            np.clip(
                raw,
                0.0,
                1.0
            )
        )

        cues = {
            "crowd": crowd,
            "tiny": tiny,
            "edge_norm": edge_norm,
            "night": night,
            "blur": blur,
            "raw": raw,
            "laplacian_variance": lap_var,
        }

        return raw, cues

    def update(
        self,
        frame_bgr,
        previous_tlwh,
        frame_id
    ):

        update_now = (
            len(self.history) == 0
            or (frame_id - 1)
               % self.analysis_interval == 0
        )

        cues = None

        if update_now:

            raw, cues = self.compute_raw(
                frame_bgr,
                previous_tlwh
            )

            self.history.append(raw)

            self.last_sci = float(
                np.mean(self.history)
            )

        return (
            self.last_sci,
            cues,
            update_now
        )


class U2MOTA1ConfidencePolicy:
    """
    A1 validation policy.

    IMPORTANT:
    This is NOT copied from the old YOLOv8 controller.

    U2MOT baseline detector confidence = 0.09.
    U2MOT tracker low threshold = 0.10.

    Therefore:
    hard scenes return to baseline 0.09.

    Easy scenes may use a stricter confidence threshold.

    easy_conf=0.15 is an INITIAL VALIDATION VALUE,
    not a claimed optimal value.
    """

    def __init__(
        self,
        baseline_conf=0.09,
        easy_conf=0.15
    ):

        self.baseline_conf = float(
            baseline_conf
        )

        self.easy_conf = float(
            easy_conf
        )

        assert (
            self.easy_conf
            >= self.baseline_conf
        )

    def confidence(
        self,
        sci
    ):

        sci = float(
            np.clip(
                sci,
                0.0,
                1.0
            )
        )

        # Easy scene:
        # SCI = 0 -> easy_conf
        #
        # Hard scene:
        # SCI = 1 -> official baseline 0.09

        conf = (
            self.baseline_conf
            +
            (1.0 - sci)
            *
            (
                self.easy_conf
                - self.baseline_conf
            )
        )

        return float(conf)
