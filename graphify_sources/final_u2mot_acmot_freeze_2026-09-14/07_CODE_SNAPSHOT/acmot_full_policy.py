
import numpy as np


class FullACMOTV1Policy:
    """
    Full AC-MOT direct-transfer policy for U2MOT.

    Transferred directly from V1:
      - SCI representation
      - SCI weights
      - mid/high SCI boundaries

    NOT copied directly:
      - old YOLOv8 detector operating values

    U2MOT-specific action values are anchored to
    its official baseline operating point.
    """

    def __init__(self):

        # --------------------------------------------------
        # V1 optimized SCI regime boundaries
        # --------------------------------------------------

        self.mid_threshold = 0.13534938199219218
        self.high_threshold = 0.28728676236279177

        # --------------------------------------------------
        # U2MOT detector-side operating points
        #
        # tuple format:
        # confidence, NMS IoU, (height, width)
        # --------------------------------------------------

        self.easy = {
            "conf": 0.15,
            "nms": 0.70,
            "size": (704, 1280),
        }

        self.medium = {
            "conf": 0.12,
            "nms": 0.65,
            "size": (800, 1440),
        }

        self.hard = {
            # Official U2MOT detector confidence floor
            "conf": 0.09,

            # Stronger duplicate suppression when
            # confidence is loosened.
            "nms": 0.60,

            # Official full input resolution
            "size": (896, 1600),
        }

    def action(self, sci):

        sci = float(
            np.clip(sci, 0.0, 1.0)
        )

        if sci < self.mid_threshold:
            tier = "easy"
            cfg = self.easy

        elif sci < self.high_threshold:
            tier = "medium"
            cfg = self.medium

        else:
            tier = "hard"
            cfg = self.hard

        return {
            "tier": tier,
            "sci": sci,
            "conf": float(cfg["conf"]),
            "nms": float(cfg["nms"]),
            "size": tuple(cfg["size"]),
        }
