
class FullACMOTV1Policy:

    def __init__(self):

        # Kept only for interface compatibility.
        self.mid_threshold = 0.5185453065646133
        self.high_threshold = 0.5895547895440134

    def action(self, sci):

        return {
            "tier": "baseline",
            "sci": float(sci),

            # Official reproduced U2MOT detector settings
            "conf": 0.09,
            "nms": 0.70,

            # (height, width)
            "size": (896, 1600),
        }
