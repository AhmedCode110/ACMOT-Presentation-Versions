
# Slide 1

Real-Time Object Detection and Tracking

By

Capt. Eng. Ahmed Gouda Ismail

Under Supervision of

Dr. Tarek Ahmed Mahmoud

Dr. Mohamed S. Mohamed

Military Technical College

Electrical Engineering Branch

Computer Engineering and Artificial Intelligence Department

OUTLINE

## Notes



# Slide 2

PRESENTATION STRUCTURE

Outline

I

Introduction and Motivation

Detection, tracking and how we measure them

slides 3 - 16

II

Related Work: Detectors and Trackers

YOLO, ByteTrack and the benchmarks

slides 17 - 28

III

Problem Formulation and Research Gap

Why one fixed threshold fails

slides 29 - 30

IV

Proposed Framework: AC-MOT

Scene score (SCI) and Smart Calibrator

slides 31 - 45

V

Experimental Setup: Dataset and Protocol

VisDrone and a fair test design

slides 46 - 52

VI

Results and Ablation Study

Stage 1: A0 to A3, speed and ID switches

slides 53 - 61

VII

VIII

Stage 2: Constrained Optimization

Sweeps, Optuna search and the final result

2

slides 62 - 77

Conclusion and Future Work

What we delivered and what comes next

slides 78 - 82

## Notes



# Slide 3

SECTION I

Introduction and Motivation

I

What object detection and multi-object tracking are, where they are used, what makes them difficult, and how their quality is measured.

MENU

<

>

## Notes



# Slide 4

SECTION I - FUNDAMENTALS

Object Detection: Definition and Output

4

A single video frame. Every object the detector found is enclosed in a box and given an identifier.

OBJECT DETECTION
Examining a single frame and answering: what objects are present, and where?

The detector returns three things
▸  A bounding box - the location
▸  A class label - pedestrian, car, bus
▸  A confidence score - certainty, from 0 to 1

NOTE:
Look at the frame on the left. Each coloured box is one detection. The box shows where the object is, the label shows what it is, and each one has a confidence score. The detector got all of this from this one frame. It does not remember the frame before.

The detector used throughout this work is YOLOv8n (YOLO = You Only Look Once), applied to every frame to locate pedestrians, cars, vans, trucks and buses.

MENU

<

>

## Notes



# Slide 5

SECTION I - FUNDAMENTALS

Multi-Object Tracking: Following IDs Across Frames

5

Frame t: the person beside the white car carries identity 1.

Frame t+k: the same person now has ID 8 — an identity switch.

Tracking: keep the same ID for the same object across frames.

Failure: the same object receives a new ID in a later frame.

Read left to right: the person beside the white car changes from ID 1 to ID 8. The person is the same, but the tracker has lost identity continuity.

MENU

<

>

## Notes



# Slide 6

SECTION I - APPLICATION DOMAINS

Applications of Multi-Object Tracking

6

Traffic management: road footage counts vehicles and keeps every vehicle ID stable.

Security and surveillance: the animated scene follows people across frames.

Retail, robotics, healthcare: track customers, mobile robots, and patient movement.

Different applications, same need: detect each object, then keep its identity stable while it moves.

MENU

<

>

## Notes



# Slide 7

SECTION I - MOTIVATION

The Challenges of Real-Time Tracking

7

A difficult frame: dense crowd, heavy occlusion, poor light. Identities are hard to hold.

An easy frame: few objects, large, well separated, good light.

What makes a scene hard
▸  Occlusion - objects hide one another, then return
▸  Illumination - low light and shadows destroy contrast
▸  Scale - the same object can be huge or a few pixels

And what it costs
Hard objects score only 0.10 to 0.35. Background noise scores in the same range, so the tracker drops them and gives out new IDs.

NOTE:
Both frames come from the same system. One is easy and one is very hard. A single detector setting has to serve both. That problem is what this thesis solves.

MENU

<

>

## Notes



# Slide 8

SECTION I  ·  EVALUATION METRICS

How We Evaluate Tracking Quality

Before the detailed slides, we ask six simple questions:

Detection Metrics
• Are the boxes correct?  Intersection over Union (IoU), True Positive (TP), False Positive (FP), False Negative (FN)
• How reliable and complete are detections?  Precision and Recall

Tracking Metrics
• Is overall tracking accurate?  Multiple Object Tracking Accuracy (MOTA)
• Does each object keep its identity?  Identification F1 Score (IDF1) and Identity Switches (IDS)
• Is detection and association balanced?  Higher Order Tracking Accuracy (HOTA)

Performance Metric
• Is it fast enough for live use?  Frames Per Second (FPS)

Key message: no single metric is enough. We read detection, identity, tracking, and speed together.

8

## Notes



# Slide 9

SECTION I · EVALUATION METRICS

IoU vs NMS — What Is the Difference?

IoU

Intersection over Union

A measurement of how much two boxes overlap.

It gives one number from 0 to 1.

Ground truth

Prediction

IoU = 0.60

Good overlap

NMS

Non-Maximum Suppression

A process that removes duplicate detection boxes.

It uses IoU to decide which boxes overlap too much.

Before NMS: 3 boxes

After NMS: 1 box

KEY DIFFERENCE

IoU measures overlap.  NMS uses IoU to remove duplicate boxes.

9

## Notes



# Slide 10

SECTION I - EVALUATION METRICS

TP, FP, FN and TN: Detection Outcomes

10

FALSE POSITIVE: a detection in the wrong location (IoU 0.22).

FALSE NEGATIVE: the object is present but was not reported.

TP - True Positive
A real object was detected correctly.

FP - False Positive
The detector reported an object that was not really there.

FN - False Negative
A real object was present, but the detector missed it.

NOTE:
There is a real bird in the image. Box it correctly and it is a TP. Box empty background and it is a FP. Miss the bird and it is a FN.

TN - True Negative: No object was present, and the detector correctly reported nothing.

MENU

<

>

## Notes



# Slide 11

SECTION I - EVALUATION METRICS

Precision and Recall

11

A surveillance frame: four people have been boxed and given identities.

PRECISION
How many detections were correct?
Precision = TP / (TP + FP)

RECALL
How many real objects were found?
Recall = TP / (TP + FN)

TP = 4   FP = 1   FN = 1

Precision = 4/5 = 0.80      Recall = 4/5 = 0.80

Precision and Recall use different denominators.

NOTE:
Precision: the detector reported 10 objects and 8 were correct, so precision is 80%.
Recall: there were 10 real objects and the detector found 8, so recall is 80%.

MENU

<

>

## Notes



# Slide 12

SECTION I  ·  DETECTION METRICS

Average Precision (AP) and Mean Average Precision (mAP)

They summarize detector performance using Precision and Recall.

Average Precision (AP)
AP measures detector performance for one class only.
• Higher Average Precision (AP) means better detection quality.

Mean Average Precision (mAP)
mAP computes AP for each class, then takes the average.
It summarizes the whole detector.

Precision + Recall   →  Average Precision (AP)  →  Mean Average Precision (mAP)

Example: if Car Average Precision (AP) = 0.90 and Person Average Precision (AP) = 0.80,
Mean Average Precision (mAP) = (0.90 + 0.80) / 2 = 0.85

The difference

AP = one class
mAP = mean of all class AP values

## Notes



# Slide 13

SECTION I - EVALUATION METRICS

MOTA - Multiple Object Tracking Accuracy

13

MOTA = 1 - (FP + FN + IDS) / GT
MOTA counts false positives (FP), missed objects (FN) and identity switches (IDS) against the ground truth (GT) in one score. Higher is better.

Four people are being tracked in this frame, carrying identities 2, 3, 4 and 5.

GT = 4     FP = 1     FN = 1     IDS = 1

MOTA = 1 - (1 + 1 + 1) / 4  =  0.25

How to read it
▸  1.00 means no errors at all. 0.00 means as many errors as objects.
▸  Negative values are possible, and 0.20 on hard footage is a good score.

NOTE:
There are 10 real objects, with 1 false positive, 1 missed object, and 1 identity switch. MOTA = 1 - 3/10 = 0.70.

MENU

<

>

## Notes



# Slide 14

SECTION I - EVALUATION METRICS

Identity Switches (IDS)

14

Before occlusion: identity 4.

After occlusion: the same person, now ID 8 — one switch.

IDENTITY SWITCH
The tracker gives a new ID to an object it was already following. Lower is better.

NOTE:
A car has ID 4 in one frame and ID 8 in the next frame. That is one identity switch.

Baseline A0: 2537 identity switches. AC-MOT A3: 2675. Adaptive resolution finds more objects but also swaps more identities.

MENU

<

>

## Notes



# Slide 15

SECTION I · EVALUATION METRICS

IDF1 - Identity F1 Score

Simple example

One car appears in 10 frames.

Frames

1

2

3

4

5

6

7

8

9

10

Tracker ID

7

7

7

7

7

7

7

7

3

9

Frames 1–8: correct ID kept

Frames 9–10: wrong ID assigned

IDF1 = time with correct ID / total time

Example: 8 correct frames / 10 total frames = 80%

IDF1

How well the tracker keeps the correct ID for an object over time.

Why we need it

• MOTA can look good while IDs still switch.

• IDF1 shows whether the same object keeps the same ID.

• Higher IDF1 means more stable identities.

NOTE

IDF1 focuses on identity consistency, not only detection quality.

15

## Notes



# Slide 16

SECTION I · EVALUATION METRICS

HOTA and Processing Speed

HOTA

Higher Order Tracking Accuracy

Measures tracking quality in one balanced score.

It checks both detection quality and identity quality.

FPS

Frames Per Second

Shows how fast the system processes video.

Higher FPS means smoother real-time operation.

Key difference

HOTA = accuracy and identity quality

FPS = processing speed

16

HOTA example:
Object was detected correctly, and kept the same ID through the video → HOTA is high.
FPS example:
If the system processes 30 frames in 1 second → FPS = 30.

## Notes



# Slide 17

SECTION II

Related Work: Detectors and Trackers

II

The state of the art from our IEEE ICMISI 2026 survey: detector families, tracker families, benchmarks, datasets, and the speed-versus-accuracy trade-off that showed us the research gap.

MENU

<

>

## Notes



# Slide 18

SECTION II - DETECTORS

Methodological Taxonomy of Detectors

1. One-stage detectors

Predict boxes and classes in one direct step.
YOLO, SSD, RetinaNet.

SIMPLE EXAMPLE

2. Two-stage detectors

First propose object areas, then refine them.
Faster R-CNN, Mask R-CNN.

SIMPLE EXAMPLE

3. Transformer detectors

Use attention to understand the whole image context.
DETR, Deformable DETR, RT-DETR.

SIMPLE EXAMPLE

Why we choose family 1

- Real-time speed
- Small compute footprint
- Confidence can be calibrated
- Pairs well with ByteTrack

TAKEAWAY:

One-stage is fastest. Two-stage is more careful. Transformer uses global context.

YOLO looks at the image once and immediately says: car here, person here.

Faster R-CNN first says: maybe an object is here. Then it tightens the box and decides the class.

DETR compares all image regions together, then predicts objects with fewer repeated guesses.

## Notes



# Slide 19

SECTION II - DETECTORS

State-of-the-Art Detectors: Benchmark Comparison

19

Year | Model | Type | mAP | Speed | Size | What it is good for

2015 | Faster R-CNN | Two-stage | 37.0 | 172 ms | 41.8M | Accurate, far too slow for live video

2018 | YOLOv3 | One-stage | 31.0 | 28.6 ms | 61.9M | The first genuinely real-time one

2023 | YOLOv8n | One-stage | 37.3 | 3.2 ms | 3.2M | Best balance - our choice

2023 | YOLOv8s | One-stage | 44.9 | 12.5 ms | 11.2M | More accurate, 4x slower

2025 | YOLO12m | One-stage | 52.5 | 4.86 ms | 20.2M | Real-time accuracy leader

2020 | DETR R101 | Transformer | 42.9 | 145 ms | 60.6M | Elegant, but very slow

2025 | RF-DETR-S | Transformer | 52.9 | 3.5 ms | 32.1M | Best published trade-off

All numbers on COCO val2017, T4 GPU, TensorRT FP16, 640x640, batch 1 - so they are directly comparable.

NOTE:
Compare the first row with the green row. Faster R-CNN and YOLOv8n are almost equally accurate (37.0 vs 37.3 mAP). But YOLOv8n is 54 times faster (3.2 ms vs 172 ms per frame) and 13 times smaller. That is why we chose it.

MENU

<

>

## Notes



# Slide 20

SECTION II — DETECTORS

Why We Chose YOLOv8n

37.3

mAP on COCO

3.2 ms

per frame on a T4

3.2M

parameters

~300

FPS detector headroom

Why YOLOv8n fits

Fast enough for real-time use on one GPU.
Small and lightweight for practical deployment.
Leaves computing room for ByteTrack and larger inputs.
Accurate enough to test the adaptive idea fairly.

Why not use a bigger YOLO?

Our contribution is the adaptive system, not a larger detector.
The same detector makes every comparison fair.
A bigger model costs more memory and time.
The adaptive method can be tested with other YOLO models later.

NOTE:

If one system used YOLOv8n and another used a much bigger detector, better results could simply come from the bigger detector. Keeping YOLOv8n fixed removes that doubt.

Same detector in every experiment  →  fair comparison  →  improvements come from the proposed system, not from a bigger model.

20

## Notes



# Slide 21

SECTION II · TAXONOMY

Methodological Taxonomy of Trackers

1. Tracking-by-detection

Detector finds boxes.
Tracker links them across frames.

SORT, DeepSORT, ByteTrack.
This is our family.

2. Joint detection + ReID (Re-Identification)

One network detects objects
and learns appearance features.

FairMOT, JDE, CenterTrack.

3. Transformer trackers

Attention looks at the whole frame
and links objects globally.

DETR, MOTR, TrackFormer.

Our chosen pipeline

Video
frame

Detector
boxes

Tracker
links IDs

Tracks

Simple idea: detect first, then keep the same ID over time.

Why we chose family 1

• Fast enough for real-time video.

• Detector and tracker can be improved separately.

• Easy to explain and debug.

• Pairs well with ByteTrack.

TAKEAWAY

We use tracking-by-detection because it is fast, modular, and clear for AC-MOT.

21

## Notes



# Slide 22

SECTION II · TRACKERS

Evolution of Trackers: SORT to ByteTrack

SORT
2016

Uses box position only.
Very fast, but IDs can switch.

DeepSORT
2017

Adds appearance features.
Fewer ID switches, but slower.

ByteTrack
2022

Keeps weak boxes too.
Fast and strong for real time.

BoT-SORT
2022

Adds camera motion help.
Strong, but more complex.

What every tracker does

1

Create track

2

Update ID

3

Keep alive

4

Delete

A track starts when an object appears, then keeps the same ID while it moves.

Why ByteTrack fits our work

• Real-time speed

• Simple tracking-by-detection design

• Uses low-score boxes to recover objects

• Works well with adaptive detector settings

TAKEAWAY

SORT is fastest but simple. DeepSORT adds identity. ByteTrack keeps speed and improves recovery.

22

## Notes



# Slide 23

SECTION II - TRACKERS

ByteTrack as the Baseline of This Work

23

Algorithm 1   ByteTrack two-stage association

Require: video V, detector Det, threshold τ

Ensure:  set of tracks T

1

T ← empty set

2

for each frame f in V do

3

D ← Det(f)

4

D_high ← { d in D : score(d) > τ }

5

D_low  ← { d in D : score(d) ≤ τ }

6

predict every t in T with a Kalman filter

7

associate T with D_high by IoU     (first pass)

8

T_rem, D_rem ← unmatched tracks, unmatched D_high

9

associate T_rem with D_low by IoU  (second pass)

10

delete tracks unmatched for too long

11

initialise a new track for each d in D_rem

12

end for

13

return T

The key insight
▸  Earlier trackers discarded every weak detection
▸  ByteTrack gives them a second matching round

Why that matters in the air
▸  A weak box is usually a genuine small object, not noise
▸  Retaining it is precisely what prevents identity switches

NOTE:
The first pass matches only the confident boxes. The second pass takes the tracks that found no match and offers them the weak boxes. That is how the 0.4 and 0.1 detections keep their ID instead of being thrown away.

AC-MOT and ByteTrack work well together: the calibrator produces more weak-but-real detections in hard scenes, and ByteTrack is built to use them.

MENU

<

>

## Notes



# Slide 24

SECTION II - BENCHMARKS

Published Tracking MOTA Accuracy on MOT17

24

SORT

43.1%

DeepSORT

59.8%

FairMOT

67.5%

ByteTrack

80.3%  <- our base

SMILEtrack

81.7%

NOTE:
These are MOT17 scores, from an easier benchmark. The numbers later in this talk are much lower because our footage is much harder. Comparing the two directly would not be fair.

MOTA alone hides ID mistakes. A tracker can score 80% and still rename the same car three times in one video. So next, we look at ID switches.

MENU

<

>

## Notes



# Slide 25

QUICK QUESTION

Which Tracker Switches IDs the Least?

?

SORT, DeepSORT, ByteTrack or OC-SORT? Hint: the most accurate tracker on the last slide is not the winner here. The answer is on the next slide.

MENU

<

>

## Notes



# Slide 26

SECTION II - BENCHMARKS

The Same Trackers Judged on ID Switches

26

SORT

4,852 switches - worst

ByteTrack

2,196

DeepSORT

1,455

OC-SORT

784 - best

NOTE:
The order flipped. SORT was 3rd on accuracy but is by far the worst on identity. ByteTrack has the best MOTA here but only average IDS. This is why one metric is never enough.

ByteTrack is not the lowest-IDS tracker. We chose it for balance: strong MOTA, real-time speed, and a second matching pass for weak boxes. Cutting ID switches is a goal of this work: tuning alone cuts them from 2537 to 2146.

MENU

<

>

## Notes



# Slide 27

SECTION II - DATASETS

Benchmark Datasets

27

Dataset | Size | Camera | Why it matters here

COCO (2014) | 330K images, 80 classes | Ground photos | The standard for scoring detectors (mAP)

MOT17 / MOT20 | 14 and 8 videos | Street CCTV | The standard pedestrian tracking benchmark

KITTI (2012) | 15K stereo pairs | Car roof | Driving, with LiDAR and GPS

VisDrone2019 | 288 videos, 262K frames | Elevated, 5-120 m | Very small objects, heavy occlusion

NOTE:
All three photos are valid test footage, but they are not the same. An object that fills a third of one frame is a few pixels in another. A method tuned on the easy case can fail on the hard one, so the benchmark must match the real conditions.

MENU

<

>

## Notes



# Slide 28

SECTION II - SYNTHESIS

Conclusions of the Survey

28

~49x lower latency
Faster R-CNN (2015): 172 ms/frame
RF-DETR-S (2025): 3.5 ms/frame

+43% higher mAP
Faster R-CNN (2015): 37.0 mAP
RF-DETR-S (2025): 52.9 mAP

81.7% MOTA
SMILEtrack: highest in
MOT17 comparison

3.5 ms latency
RF-DETR-S (2025): lowest
in detector comparison

Survey conclusion
No single model is best everywhere. The right choice is a balance between speed, compute and accuracy.

Our chosen baseline
After comparing several detector and tracker combinations, YOLOv8n + ByteTrack gave the best trade-off for a real-time modular system.

What this system evaluates:
Other models may score higher in some scenarios. Our goal is to test whether the SCI-based adaptive strategy improves tracking while maintaining real-time speed and low computational cost.

MENU

<

>

## Notes



# Slide 29

SECTION III

Problem Formulation and Research Gap

III

Why a single fixed confidence threshold cannot hold when the scene keeps changing, and the research question this thesis answers.

MENU

<

>

## Notes



# Slide 30

SECTION III - MOTIVATION

The Problem: One Fixed Threshold Cannot Fit Every Scene

30

DIFFICULT: crowding and occlusion.

DARK: low contrast and shadows.

EASY: few clear objects.

THE SIMPLE IDEA   One UAV (Unmanned Aerial Vehicle) video can contain all three scenes. Each needs a different detector sensitivity.

NOTE:  A high threshold misses partly hidden people, so their IDs are lost. A low threshold lets noise in, so false tracks appear.

MENU

<

>

## Notes



# Slide 31

SECTION IV

Proposed Framework: AC-MOT

IV

A scene-aware control loop: the Scene Complexity Index, the Smart Calibrator, and an unmodified detector-tracker pair.

MENU

<

>

## Notes



# Slide 32

SECTION III - CONTRIBUTION

Research Question and Contributions

32

“Can scene-aware, adaptive detection thresholds reduce identity switches without losing accuracy - in real time, and with no detector retraining?”

1. SCI - a scene difficulty meter
One number from 0 to 1, built from five cheap visual clues, computed on the CPU in under 0.2 ms.
Crowd, edges, tiny objects, darkness, blur.

2. Smart Calibrator
Turns that number into three detector settings, every frame, with small and explainable moves.
conf, IoU and input size.

3. A fair test
Four systems, one identical detector - so any gain must come from the design, not from a better detector.
Plus BoT-SORT as an outside reference.

4. An honest negative
We tried a colour-histogram ReID. It made things worse, so we report it as A4 and did not adopt it.
Reported, not hidden.

NOTE:
Nothing is retrained. The intelligence sits in WHAT the detector is asked to do, frame by frame.

MENU

<

>

## Notes



# Slide 33

SECTION IV - THE PROPOSED FRAMEWORK

AC-MOT: What We Add to a Standard Tracker

33

Video frame
1920 x 1080

Measure the scene
how difficult is it?

Re-calibrate
conf, IoU, imgsz

YOLOv8n
unmodified

ByteTrack
unmodified

Tracks
stable identities

Traditional approach
One detector setting is chosen before the video starts and never changes, for easy and hard scenes alike.
One setting fits no scene well.

The AC-MOT approach
We measure how hard the scene is, then adjust the detector settings every frame inside safe, tested limits.
No retraining and no extra hardware.

NOTE:
Remember the two frames from before: a crowded night scene and an open road. Normally both go to the SAME detector with the SAME threshold. AC-MOT adds one step first: it checks how hard the frame is, then gives it its own threshold and input size.

The two shaded stages above are the whole contribution. Every other stage is standard and unchanged.

MENU

<

>

## Notes



# Slide 34

SECTION IV - THE PROPOSED FRAMEWORK

The AC-MOT Pipeline: What Happens for Each Frame

34

0.63

SCI right now

SCENE COMPLEXITY INDEX (SCI)
One number between 0 and 1 that says how hard the current frame is for the detector.

How to read it
▸  Near 0.0  →  CLEAR: open road, few large objects, good light
▸  Around 0.5  →  MEDIUM: some crowding or some clutter
▸  Near 1.0  →  CROWDED: dense, tiny, dark or blurred

Computed every 10 frames on a 25% grayscale copy, using only OpenCV and NumPy on the CPU. Under 0.2 ms per frame, and no GPU time taken from the detector.

NOTE:
The dial reads 0.63 for a crowded frame: many small objects and poor light. An open road reads below 0.2. SCI does not detect anything itself. It only says how hard the next frame is, so the detector can be set up for it.

MENU

<

>

## Notes



# Slide 35

SCI — From Frame to Difficulty Score

1

INPUT FRAME

I = current image

2

PREPARE

Downscale to 25%

Iₛ = downscale(I, 0.25)

Then grayscale → G

3

MEASURE 5 CLUES

Previous boxes B

c

Crowd

t

Tiny

e

Edges

n

Night

b

Blur

object difficulty

visual difficulty

4

NORMALIZE + MIX

e_norm = min(e / 0.14, 1)

0.30c + 0.30t + 0.20e_norm
+ 0.10n + 0.05b

Weighted difficulty score

5

SCI_raw

clip(r, 0, 1)

0 = easy

1 = hard

6

SMOOTH THE SCORE

1

2

3

4

5

6

7

mean(last 7 SCI_raw readings)

7

FINAL SCI

0.59

stable difficulty

SMART CALIBRATOR

conf

↓

IoU

↕

imgsz

↑

Detector settings for the next pass

Read it left → right:

Prepare the frame

→

measure difficulty

→

combine + clip

→

smooth 7 readings

→

final SCI drives conf / IoU / imgsz

previous detections

## Notes



# Slide 36

SECTION IV - STEP 1

Step 1: Measure Scene Complexity (SCI)

36

1. CROWD - how many objects

2. EDGES - background clutter

3. TINY - how small the objects

4. NIGHT - is the frame dark

Clue | Weight | How it is measured | What it warns about

crowd | 0.30 | number of boxes last frame / 30 | many objects overlap and get confused

tiny | 0.30 | share of boxes smaller than 32x32 px | real objects score too low to keep

edges | 0.20 | Canny edge pixels / 255, capped at 0.14 | busy background creates ghost boxes

night | 0.10 | average brightness below 80 | contrast collapses, everything gets weaker

blur | 0.05 | Laplacian variance below 180 | smeared objects, a shaking or panning camera

How SCI is computed cheaply
1. Make a 25% grayscale copy: 1920x1080 colour becomes about 480x270 in gray.
2. Measure crowding, tiny objects, edges, low light and blur, then combine them into SCI (0 = easy, 1 = hard).
3. SCI picks conf and imgsz for the next detector pass. Detection still uses the full-size frame, so GPU load barely changes.

MENU

<

>

## Notes



# Slide 37

SECTION IV - STEP 1

SCI: Turn Five Cues Into One Score

37

Clue | Value | What was actually seen

crowd | 0.7 | 21 objects in the frame (21 / 30)

tiny | 0.8 | 8 of every 10 boxes are under 32 px

edges | 0.4 | busy road texture and markings

night | 1 | average brightness measured 60 - dark

blur | 0 | the frame is sharp

SCI = 0.30(0.7) + 0.30(0.8)

+ 0.20(0.4) + 0.10(1) + 0.05(0)

= 0.21 + 0.24 + 0.08 + 0.10 + 0

= 0.63

0.63

SCI = 0.63

So the calibrator decides
▸  0.63 is above 0.60  →  this frame is labelled CROWDED
▸  Confidence drops toward the 0.19 safety floor - keep the weak boxes
▸  Input size jumps to 832 px - give the tiny objects more pixels
▸  NMS tightens slightly - trim the duplicate boxes that come with it

NOTE:
Five measurements taken from one frame, combined into a single number the calibrator can act on.

MENU

<

>

## Notes



# Slide 38

SECTION IV - STEP 1

SCI: Exact Formulas and Pseudocode

38

c = min(count(B) / 30, 1)                         # crowd from previous-frame boxes
t = 0 if count(B) = 0 else count(area(b) < 32*32 for b in B) / count(B)
e = mean(Canny(G, 50, 120)) / 255                 # edge density
n = 1 if mean(G) < 80 else 0                       # night flag
b = 1 if var(Laplacian(G)) < 180 else 0            # blur flag

Input preparation
I_s = downscale(I, 0.25); G = grayscale(I_s). B is the set of boxes from the previous frame.

Edge normalization
Before weighting, use e_norm = min(e / 0.14, 1). This prevents a very busy background from dominating SCI.

Combine and smooth
r = 0.30c + 0.30t + 0.20e_norm + 0.10n + 0.05b. Append clip(r, 0, 1); SCI = mean(last 7 values).

How to read the pseudocode
B and G are the only inputs. The first two lines measure object difficulty. The last three measure visual difficulty. A high SCI means the next detector pass gets a better-suited setting.

MENU

<

>

## Notes



# Slide 39

SECTION IV - STEP 1

Example: One Frame Becomes One SCI Score

39

SCI | Label | conf | Input size | What it means

below 0.35 | CLEAR | 0.245 | 640 | Easy frame. Stay strict and stay fast.

0.35 to 0.60 | MEDIUM | ~0.228 | 736 | Some crowding. Loosen a little.

0.60 and up | CROWDED | 0.202 | 832 | Hard frame. Keep weak boxes, zoom in.

1.00 | CROWDED | 0.190 (floor) | 832 | Worst case. Never goes below 0.190.

Confidence goes DOWN
In a hard scene a weak detection is usually a real small object, not noise - so lowering the line recovers it.

Resolution goes UP
A 5-10 pixel object needs more pixels to be detectable at all. Only hard frames pay that cost.

NOTE:
Both moves fix the same problem. Lowering the confidence keeps the weak-but-real box that would be deleted. Raising the input size gives that same object more pixels, so it is detected more strongly. Easy frames get neither, so they stay fast.

MENU

<

>

## Notes



# Slide 40

SECTION IV - STEP 2

Step 2: Use SCI to Choose Settings

40

conf  =  clip( 0.245 − 0.050 × SCI ,  0.19 , 0.28 )

iou   =  clip( 0.490 − 0.050 × SCI ,  0.40 , 0.52 )

(2)

imgsz =  832   if SCI > 0.60

736   if SCI > 0.35

640   otherwise

(3)

Algorithm 2   Per-frame refinement by scene label

Require: SCI, scene label s, tiny-object ratio r

1

if s ∈ {crowded, tiny, night} then  conf ← conf − 0.012

2

if s = blur then  iou ← iou − 0.012

3

if r > 0.50 then  imgsz ← 832

4

apply the bounds of (2) again and return (conf, iou, imgsz)

The 0.19 floor
Below it, background patches scoring 0.10-0.35 begin to enter the output as false positives.

Only three resolutions
640, 736, 832 - fixed steps rather than a continuous slider, giving predictable memory and latency.

Deliberately small moves
Conservative by design: small, explainable adjustments rather than jumps that would destabilise the tracker.

NOTE:
Across the whole SCI range the confidence moves by only 0.055 and never drops below 0.190. Small, bounded, reversible - never enough to upset the tracker.

MENU

<

>

## Notes



# Slide 41

SECTION IV - STEP 2

Smart Calibrator: Exact Settings From SCI

41

Detector side - moves every frame
conf - the keep-or-drop line for a detection
iou - the NMS overlap threshold
imgsz - the size the frame is fed in at
Passed straight into model.track(conf=, iou=, imgsz=).

Tracker side - tuned once, then frozen
track_high_thresh = 0.18
track_low_thresh = 0.04
new_track_thresh = 0.20
track_buffer = 45      match_thresh = 0.86
Written into the ByteTrack YAML. Never adaptive.

There are two different IoU values here. The one the calibrator moves is the DETECTION-side NMS threshold. The one that matches tracks to detections is match_thresh = 0.86, and it never changes.

What NMS actually does
Lowering the NMS IoU makes suppression STRONGER - more overlapping boxes are deleted.

So why tighten it in hard scenes?
We already lowered conf and raised resolution, so more duplicates appear. Tightening trims them.

NOTE:
Lowering conf lets more boxes through, including duplicates. Tightening the NMS threshold then removes them. The two moves go together on purpose.

MENU

<

>

## Notes



# Slide 42

SECTION IV - WHAT CHANGES

Exactly What AC-MOT Changes and What It Keeps

42

Algorithm 3   SceneAnalyzer.analyze

Require: frame I, boxes B from the previous frame, history H (|H| ≤ 7)

Ensure:  SCI in [0,1] and a scene label s

1

I_s ← downscale(I, 0.25)                       — 16x fewer pixels

2

G   ← grayscale(I_s)

3

beta ← mean(G)                                 — brightness

4

phi  ← var(Laplacian(G))                       — sharpness

5

e    ← mean(Canny(G, 50, 120)) / 255           — edge density

6

c    ← min( |B| / 30 , 1 )                     — crowding

7

t    ← | { b in B : area(b) < 32×32 } | / |B|  — tiny ratio

8

r ← 0.30c + 0.30t + 0.20 min(e/0.14, 1)

9

if beta < 80  then r ← r + 0.10                — night flag

10

if phi  < 180 then r ← r + 0.05                — blur flag

11

append clip(r, 0, 1) to H;  drop the oldest if |H| > 7

12

SCI ← mean(H)                                  — anti-flicker

13

s ← label by severity: night, blur, tiny, crowded, clear

14

return (SCI, s)

Why 25% and grayscale
Using a 25% grayscale copy greatly reduces computation while preserving enough information to estimate scene complexity.

Why we divide by 30
Above about thirty objects, a frame is already fully crowded. The value comes from the object counts we measured in the evaluation data.

No learning involved
OpenCV and NumPy only. No training, no data dependency, fully interpretable - and incapable of overfitting.

MENU

<

>

## Notes



# Slide 43

SECTION IV - DETECTOR CONTROL

Confidence Threshold: The Main Detector Control

43

CONFIDENCE SCORE
A number from 0 to 1: how sure the detector is that a box holds a real object.

Row (a): the detector's own scores, written above each box - 0.9, 0.8, 0.4 and 0.1.

High: 0.80 to 0.95
A large, clear, well-illuminated object. The detector is effectively certain.

Intermediate: 0.30 to 0.60
Partially occluded or small. It may be genuine; it may be a shadow.

Low: 0.10 to 0.30
Small or poorly lit. Often a genuine object that simply resembles noise.

NOTE:
Follow the woman in the grey shirt in row (a). In frame t1 she scores 0.9. In frame t2 she is partly hidden and drops to 0.4. With the usual 0.25 threshold she stays. Raise it to 0.5 and she disappears mid-video, and her ID is lost. The white pole scores 0.1 in every frame and must NOT be kept.

MENU

<

>

## Notes



# Slide 44

SECTION IV - IMPLEMENTATION

Implementation: Computing SCI

44

Algorithm 4   SmartCalibrator.params

Require: SCI, scene label s, tiny ratio r, mode flags

Ensure:  detector settings (conf, iou, imgsz)

1

(conf, iou, imgsz) ← (0.25, 0.45, 640)        — defaults

2

if adaptive_threshold then

3

conf ← 0.245 − 0.050 × SCI

4

iou  ← 0.490 − 0.050 × SCI

5

if s ∈ {crowded, tiny, night} then conf ← conf − 0.012

6

if s = blur then iou ← iou − 0.012

7

end if

8

if adaptive_resolution then

9

if SCI > 0.60 or r > 0.50 then imgsz ← 832

10

else if SCI > 0.35 or s ∈ {crowded, tiny} then imgsz ← 736

11

end if

12

conf ← clip(conf, 0.19, 0.28)                  — false-positive floor

13

iou  ← clip(iou , 0.40, 0.52)

14

return (conf, iou, imgsz)

It can only loosen
As difficulty rises, confidence may fall but never rise. A single direction, with no surprises.

Everything is bounded
conf in [0.19, 0.28], IoU in [0.40, 0.52], resolution restricted to three steps - bounded by construction.

Sixteen lines in total
The entire contribution is two short procedures. This is deliberate: it must run on embedded hardware.

NOTE:
The procedure is simple on purpose. The contribution is not complex maths: it is noticing that this setting was always locked, and opening it up.

MENU

<

>

## Notes



# Slide 45

SECTION IV - IMPLEMENTATION

Implementation: Smart Calibrator

45

1. The 7-reading rolling mean
Without it, SCI would jump between CROWDED and CLEAR frame by frame, and the detector settings would swing back and forth. That hurts the tracker more than it helps.
It costs nothing: a 7-value running average.

2. Analyse only every 10 frames
Scenes change over seconds, not milliseconds. Checking every 10th frame is enough, and the cost stays invisible.
The result is reused for the frames in between.

10
frames between analyses

25%
grayscale copy size

0.2 ms
per frame, CPU only

0
GPU time taken

NOTE:
A scene changes over seconds, not milliseconds, so checking every 10th frame is enough. The 7-frame average stops one odd frame from flipping the setting back and forth.

This is why AC-MOT stays real-time: 27.47 FPS against 29.57 for the baseline. The scene check runs on the CPU, beside the GPU, never on it.

MENU

<

>

## Notes



# Slide 46

SECTION V

Experimental Setup: Dataset and Protocol

V

The application domain is chosen here: UAV aerial surveillance. VisDrone2019-MOT, seventeen sequences, and every scoring decision stated explicitly.

MENU

<

>

## Notes



# Slide 47

SECTION V - DOMAIN

Choosing the Test Domain: UAV Aerial Surveillance

47

Everything so far has been general. To evaluate the method we must now commit to one domain - and we deliberately chose the hardest one available.

From altitude, a person is a blob about ten pixels wide.

The same kind of scene at night: contrast collapses.

And minutes later, an open road with large, easy objects.

Why aerial footage is the ideal test
▸  Objects are 5 to 30 pixels wide - confidence is always low
▸  The camera itself translates, rotates and changes altitude
▸  Scene difficulty swings widely inside one recording

Which is exactly what AC-MOT addresses
▸  A fixed threshold is at its most wrong here
▸  So the benefit of adapting it is at its most visible
▸  If the idea works anywhere, it must work here

NOTE:
All three photos can happen in one recording. A threshold that is right for the third is badly wrong for the first two - exactly the problem this method solves.

MENU

<

>

## Notes



# Slide 48

SECTION V - DATA

The VisDrone2019-MOT Benchmark

48

Property | Value

Resolution | 1920 x 1080 (Full HD)

Altitude | 5 to 120 m above the ground

Camera angle | straight down (nadir) to tilted

Object size | 5 to 30 pixels wide - extremely small

Conditions | clear daylight, low light, motion blur

Our subset | 12 sequences, 4,106 frames, 111,308 boxes

Density | 27.1 objects per frame on average

Why this dataset
It is the only large public UAV tracking benchmark with dense per-frame labels at real aerial altitudes.
288 videos, 262,000+ frames, 14 cities.

NOTE:
These are typical VisDrone frames: a dense crowd from above, the same scene at night, and vehicles only a few pixels wide. They are much harder than the street-level benchmarks in Section II.

MENU

<

>

## Notes



# Slide 49

SECTION V - DATA

Object Classes Evaluated

49

ID | VisDrone class | Used?

1 | Pedestrian | YES

2 | People (group) | no

3 | Bicycle | no

4 | Car | YES

5 | Van | YES

6 | Truck | YES

7 | Tricycle | no

8 | Awning-tricycle | no

9 | Bus | YES

10 | Motor | no

Why exactly these five
▸  They are the real targets of UAV surveillance
▸  They have enough labels for stable statistics
▸  YOLOv8n detects them reliably from altitude

Why the others are excluded
▸  We follow the standard VisDrone MOT protocol
▸  A bicycle at 100 m is a few unclear pixels, hard to tell from a motorcycle or tricycle
▸  Even human annotators disagree on them

NOTE:
At these altitudes a bicycle and a motorbike are both a dark smudge a few pixels wide. If a human cannot tell them apart, scoring the tracker on that difference measures label noise, not tracking ability.

MENU

<

>

## Notes



# Slide 50

SECTION V - PROTOCOL

Ground-Truth Filtering Rules

50

Occlusion level | Meaning | Kept?

0 | Fully visible | KEPT

1 | Slightly hidden | KEPT

2 | Heavily hidden | excluded

3 | Almost fully hidden | excluded

Truncation level | Meaning | Kept?

0 | Fully inside the frame | KEPT

1 | A small part outside | KEPT

2 | A large part outside | excluded

3 | Mostly outside | excluded

Why we exclude the hard ones
If a box is not clear enough for a human to label correctly, it is unfair to count it as a tracking error. That would measure label uncertainty, not tracker quality.

The annotation score field
Each label has a score from 0 to 5. A score of 0 means the region should be ignored, so we remove it. We keep all labels with a score of 1 or higher.

NOTE:
If an object is almost fully hidden, its box may be unclear. It is unfair to count a miss as an error. So we remove these cases, and we use the same rule for every system.

Occlusion: object is hidden by another object.               ·           Truncation: Part of the object is outside the image frame.

MENU

<

>

## Notes



# Slide 51

SECTION V - PROTOCOL

Tracker State Reset and Evaluation Formulas

51

Algorithm 5   Evaluation protocol, applied to every system

Require: sequences S, system M, ground truth G

1

for each sequence q in S do

2

reset the tracker state of M      — no leakage

3

G_q ← { g in G(q) : class(g) in {1,4,5,6,9},

4

occ(g) < 2, trunc(g) < 2, score(g) ≥ 1 }

5

R_q ← M(q)

6

accumulate TP, FP, FN, IDS by matching R_q to G_q at IoU 0.5

7

end for

8

report MOTA, IDF1, HOTA*, IDS and FPS over all sequences

MOTA  = 1 - (FP + FN + IDS) / GT

DetA  = TP / (TP + FP + FN)

AssA  = 1 - IDS / TP

HOTA* = √( DetA × AssA )

(4)

NOTE:
Line 3 of the algorithm is the important one. Without it, tracks still alive at the end of one sequence carry into the next, fail to match anything, and create ID switches that belong to no video. The measured IDS would then describe our script, not the tracker.

Hardware: Google Colab T4 GPU, FP16, batch 1. FPS is wall-clock over the full sequence, including reading frames from disk - so it is the real throughput.

NOTE:
In tracking, the smallest evaluation decision moves the final number. Stating them explicitly is what makes the comparison reproducible.

MENU

<

>

## Notes



# Slide 52

SECTION V - PROTOCOL

A Fair and Attributable Experimental Design

52

A0 - Baseline_Default
Stock ByteTrack out of the box. conf 0.25, size 640. The reference point for everything.

A1 - Baseline_Tuned
Same detector, only the ByteTrack config corrected for UAV footage. No adaptive logic at all.

A3 - AC-MOT (ours)
Tuned config + adaptive confidence + adaptive resolution. The full proposed system.

BoT-SORT
A strong published tracker, on the identical detector, as an outside reference.

All four systems run the IDENTICAL YOLOv8n detector, with no retraining. So every improvement must come from the design. It cannot come from a bigger or better-trained detector.

NOTE:
The four systems differ in exactly one thing each. A1 adds a corrected config. A3 adds the adaptive layer on top. BoT-SORT swaps in a different matching strategy. The detector, sequences, ground-truth filter and hardware stay the same for all four.

The ablation adds one component at a time - A0 to A4 - so each contribution is isolated and additive, including the one we did not adopt.

MENU

<

>

## Notes



# Slide 53

SECTION VI

Results and Ablation Study

VI

The 17-sequence development ablation. Four systems, one fixed YOLOv8n detector, one component added at a time.

MENU

<

>

## Notes



# Slide 54

SECTION VI - ABLATION

Our Ablation Study: A0 to A3

54

NOTE:
Every step adds one component and keeps the same detector. All three accuracy scores rise at each step. Identity switches fall at A1 and A2, then rise at A3 - that trade-off has its own slide.

All four systems use the same YOLOv8n detector with no retraining: 17 sequences, 4 systems, 68 runs.

MENU

<

>

## Notes



# Slide 55

SECTION VI - HEADLINE

Accuracy Improves at Every Step

55

NOTE:
MOTA, IDF1 and HOTA all rise from A0 to A3. The biggest jump is the last one, when adaptive input resolution is added.

MENU

<

>

## Notes



# Slide 56

SECTION VI - ATTRIBUTION

Where the MOTA Gain Comes From

56

NOTE:
Each arrow is one added component. Tuning adds 2.66 points, adaptive confidence adds 2.49 points, and adaptive input resolution adds 6.38 points - the largest single gain.

MENU

<

>

## Notes



# Slide 57

SECTION VI - WHY IT WORKS

Recall Explains the Big MOTA Gain

57

NOTE:
Recall is the share of real objects that were found. AC-MOT finds 11.92 points more objects than the baseline, and the biggest step is the last one: adaptive input size.

MENU

<

>

## Notes



# Slide 58

SECTION VI - TRADE-OFF

The Identity-Switch Trade-off

58

NOTE:
Tuning removed 391 ID switches. Adaptive input size added 551 back: finding more small objects also gives more chances to swap IDs. This is the problem Stage 2 attacks.

MENU

<

>

## Notes



# Slide 59

SECTION VI - SPEED

Accuracy at Real-Time Speed

59

NOTE:
All four systems stay above the 25 FPS real-time line, and speed drops by only 2.10 FPS from A0 to A3. An older 12-sequence run of BoT-SORT gave 9.4 FPS, far below real time, but it used a different protocol, so it is not compared here.

MENU

<

>

## Notes



# Slide 60

## Notes



# Slide 61

## Notes



# Slide 62

SECTION VII

Stage 2: Constrained Optimization

VII

Stage 1 raised accuracy, but ID switches went up too. Stage 2 stops hand-tuning: a search chooses the settings, under two strict rules.

MENU

<

>

## Notes



# Slide 63

QUICK QUESTION

Higher MOTA = a Better Tracker?

?

Take a guess before the next slide. Keep one eye on the ID switches, not only on the accuracy bars.

MENU

<

>

## Notes



# Slide 64

SECTION VII - WHY STAGE 2

Accuracy Went Up, but ID Switches Came Back

64

NOTE:
From A2 to A3, MOTA rose by 6.38 points, but ID switches rose by 551. A score that only rewards accuracy can hide this. So the answer is: not always.

MENU

<

>

## Notes



# Slide 65

SECTION VII - WHY STAGE 2

Why One Score Can Fool Us

65

MOTA adds three kinds of mistakes into one number. It cannot tell you which mistake went down and which went up.

Missed objects (FN)
A real object that the tracker never found.
Counted inside MOTA.

False alarms (FP)
A box drawn where there is no real object.
Counted inside MOTA.

ID switches (IDS)
The same person suddenly gets a new ID number.
Counted inside MOTA, but easy to hide.

The trap
Find many more objects and MOTA rises, even if ID switches rise too.
This is exactly what happened at A3.

NOTE:
So in Stage 2, ID switches become a hard rule that every candidate must pass, not just one part of a score.

MENU

<

>

## Notes



# Slide 66

SECTION VII - METHOD

The New Plan: A Search With Rules

66

Validation
7 sequences

Optuna TPE
50 trials

Freeze
Trial 37

Sweeps
36 runs

Temporal grid
25 runs

Test-dev
17 sequences, once

Old way: hand-tuning
We picked the SCI weights and detector settings by hand, one at a time, and hoped they worked together.
Hard to defend, easy to miss the best mix.

New way: a search with rules
A search tries many settings on the validation videos and keeps only those that pass both rules.
Rule 1: FPS ≥ 25.  Rule 2: IDS ≤ 271 (the old AC-MOT).

NOTE:
All 111 runs use the 7 validation sequences. The 17 test-dev sequences are never touched while choosing; they are used once, at the very end.

The two highlighted stages are new in Stage 2: a joint search, then one frozen setting.

MENU

<

>

## Notes



# Slide 67

SECTION VII - STEP 1

Step 1: Sweeps Shrink the Search

67

NOTE:
We changed one setting at a time (36 runs). Only the good ranges go forward: input sizes 512, 704 and 800; confidence 0.15 to 0.30; NMS 0.45 to 0.65.

MENU

<

>

## Notes



# Slide 68

SECTION VII - STEP 2

Step 2: How Often to Look, How Much to Smooth

68

NOTE:
We tried 25 pairs. Checking the scene every 10th frame and averaging the last 5 readings gave the best MOTA (19.04), with IDS 253 and 41.7 FPS.

MENU

<

>

## Notes



# Slide 69

SECTION VII - STEP 3

Step 3: Learn What a Hard Scene Looks Like

69

Instead of guessing what dark, blurry, busy or crowded means, we measured it on our own validation videos with the fixed YOLOv8n.

Brightness
Dark 54  ·  normal 104  ·  bright 151
10th / 50th / 90th percentile of frames

Sharpness (blur)
Blurry 72  ·  normal 181  ·  sharp 393
Laplacian variance

Edges (busy background)
Calm 11  ·  normal 25  ·  busy 43
Sobel edge strength

Crowd
Few 3  ·  normal 12  ·  crowded 31
Detector boxes per frame

NOTE:
Each clue is scaled with these real ranges before it enters the SCI score, so the score now matches our own videos.

MENU

<

>

## Notes



# Slide 70

SECTION VII - STEP 4

Optuna-Based Hyperparameter Optimization

70

Search space
11 parameters

Optuna TPE
proposes a trial

Trials 1 … 50
run on validation

Validation
MOTA · HOTA · IDF1
IDS · FPS

FPS + IDS rules
FPS ≥ 25 · IDS ≤ A3

Frozen AC-MOT
best feasible trial

What is Optuna, and why use it?
An open-source framework that searches for good parameter combinations automatically, instead of picking them by hand.
Why: picking by hand is subjective. Optuna tests candidates on validation and keeps the best one that meets our rules.

What Optuna tunes in AC-MOT
5 normalized SCI weights: crowding, tiny objects, edge complexity, night, blur
Easy / hard confidence  ·  easy / hard NMS IoU  ·  2 SCI switching thresholds

HOW TPE WORKS  ·  Tree-structured Parzen Estimator
A model-based sequential hyperparameter optimization method: it learns from the results of earlier trials and proposes more promising settings next, instead of testing combinations blindly.
Feasible: FPS ≥ 25 and IDS ≤ the old A3 validation reference.
Best: highest MOTA; ties → lower IDS → higher HOTA → higher IDF1 → higher FPS.

The test set is not used during Optuna optimization. Worker 3 runs all 50 trials on the VisDrone validation set only.

MENU

<

>

[1] T. Akiba, S. Sano, T. Yanase, T. Ohta, and M. Koyama, “Optuna: A Next-generation Hyperparameter Optimization Framework,” KDD, 2019.
[2] J. Bergstra, R. Bardenet, Y. Bengio, and B. Kégl, “Algorithms for Hyper-Parameter Optimization,” NIPS, 2011.

## Notes



# Slide 71

QUICK QUESTION

How Many of 50 Trials Passed Both Rules?

?

Rule 1: at least 25 frames per second. Rule 2: no more ID switches than the old AC-MOT on the same videos (271). Make a guess. The answer is on the next slide.

MENU

<

>

## Notes



# Slide 72

SECTION VII - STEP 4

Step 4: Optuna Search With Two Rules

72

NOTE:
Optuna (TPE) tuned the SCI weights, thresholds and detector settings together. Rule 2 uses the old AC-MOT's 271 ID switches on the same validation videos. Only 15 of 50 trials passed both rules; Trial 37 had the best MOTA among them.

MENU

<

>

## Notes



# Slide 73

SECTION VII - STEP 4

The Search Learns as It Goes

73

NOTE:
Each dot is one trial. The gold line shows the best passing trial so far: it kept climbing and reached its best at Trial 37.

MENU

<

>

## Notes



# Slide 74

SECTION VII - RESULT

What the Search Learned

74

NOTE:
Crowd and tiny objects stay the main clues; night and blur get more weight. Easy to hard scenes: confidence 0.30 to 0.15, NMS 0.50 to 0.60. Input size 512 / 704 / 800. SCI thresholds 0.34 and 0.67.

MENU

<

>

## Notes



# Slide 75

SECTION VII - FINAL RESULT

Final Result: Optimized AC-MOT (Trial 37)

75

20.742
MOTA

34.211
HOTA

39.018
IDF1

252
IDS  (old AC-MOT: 271)

38.74
FPS (min 25)

What this means
▸  19 fewer ID switches than the old AC-MOT (−7%)
▸  Real time with room to spare: 38.74 FPS
▸  Chosen on 7 validation videos, then frozen

NOTE:
All numbers are on the 7 validation sequences, the same videos where the old AC-MOT had 271 ID switches. The final verdict comes from one run on the 17 test-dev sequences: Baseline_Default vs the frozen AC-MOT.

MENU

<

>

## Notes



# Slide 76

SECTION VII - PROTOCOL

Validation Builds It, Test Judges It

76

Everything is chosen on 7 validation sequences. The 17 test-dev sequences are used only once, for the final verdict, and nothing is retuned after that.

Validation  ·  7 sequences
Sweeps, temporal grid, 50 Optuna trials and the new A0 to A3 ablation.
Every setting is chosen and frozen here.

Test-dev  ·  17 sequences
Only two systems, run once: Baseline_Default and the frozen AC-MOT.
No search, no tuning, no second try.

Old vs new AC-MOT, same videos
ID switches on the 7 validation sequences: 271  →  252.
19 fewer (−7%), at 38.74 FPS.

What we do not subtract
The Stage 1 numbers (A0 to A3) come from 17 other sequences, so we never compare them directly with these.
Different videos, different scale.

NOTE:
Validation = learn, compare, choose, freeze.   Test = judge the frozen system once.

MENU

<

>

## Notes



# Slide 77

SECTION VII - CONTRIBUTION

What Stage 2 Adds

77

Stage 2 adds a better way to choose settings, not a bigger model.

Accuracy with rules
We look for the best MOTA, but only among settings that pass both rules.
No trade-off is hidden.

Stable identities
ID switches may not exceed the old AC-MOT: 271 on the same videos.
Trial 37 reaches 252, 19 fewer.

Real-time speed
FPS ≥ 25 is a hard limit.
Trial 37 runs at 38.74 FPS.

Fair and repeatable
All choices on 7 validation videos: 111 logged runs, one frozen setting.
The 17 test-dev videos are used once, at the end.

NOTE:
Same YOLOv8n detector, same ByteTrack tracker, no retraining. Only the way we choose the settings changed.

MENU

<

>

## Notes



# Slide 78

SECTION VIII

Conclusion and Future Work

VIII

The scope of the present study, its contribution, and the research directions that follow from the measurements.

MENU

<

>

## Notes



# Slide 79

SECTION VIII - SCOPE

What We Focused On and Why

Fixed detector for a fair test

YOLOv8n is kept the same in all runs.
So any gain comes from AC-MOT design, not from using a larger detector.

Detector: YOLOv8n, FP16, NVIDIA T4.

Final evaluation setup

Evaluated on 17 VisDrone sequences.
Same data, same filtering, same hardware, same tracker family.

Classes: person, car, bus, truck.

What AC-MOT actually changes

SCI reads scene difficulty and adapts detector settings.
It changes confidence, NMS IoU, and image size.

ByteTrack matching settings stay fixed.

What we did not claim

We did not improve results by adding a bigger model.
Deep ReID was not the final claim; it is future work.

The claim is adaptive control, not model scaling.

CONCLUSION

We kept the detector fixed and proved that adaptive SCI control improves tracking quality.

79

## Notes



# Slide 80

SECTION VIII - CONCLUSION

Conclusion: What AC-MOT Delivers

80

+11.53
MOTA  (A0 → A3)

+10.00
IDF1  (A0 → A3)

+9.29
HOTA  (A0 → A3)

+138
IDS, worse  (A0 → A3)

27.47
FPS at A3, above 25

What AC-MOT contributes
▸  Scene-adaptive detector settings, no retraining
▸  A cheap, readable scene score (SCI) on the CPU
▸  A rule-based search: FPS ≥ 25 and IDS ≤ 271

NOTE:
Stage 1 (A0 → A3, 17 sequences): a big accuracy gain, but 138 more ID switches. Stage 2 (7 validation sequences): the frozen Trial 37 has 19 fewer ID switches than the old AC-MOT on the same videos (252 vs 271), at 38.74 FPS. The final test on the 17 test-dev sequences comes next.

MENU

<

>

## Notes



# Slide 81

SECTION VIII - FUTURE WORK

Directions for Future Work

81

1. Camera-motion compensation
The clearest next gain. Camera-motion compensation targets exactly the identity switches that adaptive resolution adds.
A0 2537 IDS  →  A3 2675 IDS.

2. Density-gated resolution
In the two densest sequences the 832 px step costs recall. Gating resolution on density as well as SCI should recover it.
Aimed at exactly s249a and s306.

3. A proper deep ReID
Replace the colour histogram with a compact deep embedding suited to aerial viewpoints - light enough to keep real-time speed.
Builds directly on configuration A4.

4. SCI beyond YOLO
Drive RT-DETR or DINO with the same signal, and extend to the 58-sequence split plus UAVDT and AU-AIR.
Tests whether the idea generalises.

NOTE:
The very first step: run Baseline_Default and the frozen Trial 37 once on the 17 test-dev sequences. The four ideas above come from numbers we measured, not from guesses.

MENU

<

>

## Notes



# Slide 82

Thank you

AC-MOT — adaptive scene calibration for real-time UAV tracking.

+11.53
MOTA  (A0 → A3)

+10.00
IDF1  (A0 → A3)

+9.29
HOTA  (A0 → A3)

+138
IDS, worse  (A0 → A3)

27.47
FPS at A3, above 25

IF YOU REMEMBER ONE THING
The scene tells you how carefully to look. Measure it, and let the detector listen.

Ahmed Gouda Ismail   ·   Mohamed S. Mohamed   ·   Tarek Ahmed Mahmoud

Questions?

MENU

<

>

## Notes


