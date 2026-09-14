/* =====================================================================
   "Explain + example" panel content — one entry per slide, keyed by the
   slide's data-title. Opened with the button in each slide footer or E.

   kind:  toy  = made-up numbers, only to explain the idea
          real = real numbers from this thesis (bound live from results.js)
          pub  = published numbers (survey / papers)
          none = idea only, no numbers
   RULE: never type a thesis result by hand here — use B('path') so the
   value comes from assets/data/results.js.
   ===================================================================== */
(function () {
  function B(path, dec, k) {
    return '<b class="ex-num" data-bind="' + path + '"' + (dec != null ? ' data-dec="' + dec + '"' : '') + (k ? ' data-k' : '') + '>…</b>';
  }
  function steps(a) { return '<ol class="ex-steps">' + a.map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ol>'; }
  function list(a) { return '<ul>' + a.map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ul>'; }
  var A = 'devAblation.rows.';
  var T = 'testdev.rows.';
  var U = 'uavdt.rows.';

  window.EXPLAIN = {

  /* ---------------- Title + Section I ---------------- */
  'Title': { kind: 'none',
    simple: 'This thesis builds <b>AC-MOT</b>: a system that <b>finds</b> objects in video, <b>follows</b> each one with an ID number, and <b>changes the detector settings</b> when the scene becomes easier or harder.',
    example: 'A drone films a road. At noon the road has three big cars — <b>easy</b>. At night near a market there are forty small, dark people — <b>hard</b>. A normal system uses the same settings for both. AC-MOT notices the change and adjusts itself, like a driver who slows down in fog.',
    remember: 'Detect → Track → Adapt.' },

  'Outline': { kind: 'none',
    simple: 'The talk has eight parts. It goes from the basics, to the problem, to our method, to the tests, and ends with the conclusion.',
    example: list(['<b>I–II:</b> what tracking is, and what already exists.', '<b>III:</b> what is missing (the research gap).', '<b>IV:</b> our idea, AC-MOT.', '<b>V–VII:</b> how we tested it and what we found.', '<b>VIII:</b> what it means and what comes next.']),
    remember: 'Click any card on the slide to jump to that part.' },

  'Section I': { kind: 'none',
    simple: 'This part gives us the words we need: detection, tracking, and the numbers that score them.',
    example: 'Before watching a football match you learn the rules: goal, foul, offside. Here our “rules” are <b>IoU, precision, recall, MOTA, IDF1, HOTA</b> and <b>FPS</b>.',
    remember: 'Every later result uses these words.' },

  'Object detection': { kind: 'toy',
    simple: 'A detector looks at <b>one picture</b> and draws a box around every object it finds. Each box has a <b>class</b> (what it is) and a <b>score</b> (how sure it is, from 0 to 1).',
    example: 'One frame from a shop camera gives:' + list(['Box 1 → person, score 0.92', 'Box 2 → person, score 0.61', 'Box 3 → bag, score 0.35']) + 'The detector does <b>not</b> know that Box 1 is the same person as in the last frame. Every frame starts from zero.',
    remember: 'Detection = what and where, in one frame only.' },

  'Multi-object tracking': { kind: 'toy',
    simple: 'A tracker connects the boxes over time and gives each object a fixed <b>ID number</b>. Its job is to keep the same number for the same object.',
    example: steps(['Frame 1: a man near a car gets <b>ID 1</b>.', 'Frame 2: he moved a little — still ID 1. Correct.', 'Frame 3: he walks behind the car and is hidden.', 'Frame 4: he comes back, but now he is <b>ID 8</b>.']) + 'The change from 1 to 8 is an <b>identity switch</b>: a tracking mistake, even though he was detected every time.',
    remember: 'Detection asks “what is here?”. Tracking asks “who is who over time?”.' },

  'Applications': { kind: 'none',
    simple: 'Tracking is used whenever we need to <b>count</b>, <b>follow</b> or <b>watch</b> moving things.',
    example: list(['<b>Traffic:</b> count cars crossing a bridge. If one car gets two IDs, it is counted twice.', '<b>Stations:</b> see where crowds build up.', '<b>Crossings:</b> warn when a person walks into the road.', '<b>Drones:</b> follow vehicles from the air. Objects are tiny and the onboard computer is small — that is why we focus here.']),
    remember: 'Wrong IDs give wrong counts.' },

  'Challenges of real-time tracking': { kind: 'none',
    simple: 'The same camera sees very easy moments and very hard moments. Hard moments cause missed objects and ID switches.',
    example: list(['<b>Occlusion:</b> a person walks behind a bus for one second.', '<b>Small objects:</b> a car seen from 100 m is only a few pixels.', '<b>Low light:</b> at night the edges of people fade.', '<b>Motion blur:</b> a fast camera turn smears the image.', '<b>Look-alike objects:</b> two men in the same uniform cross, and their IDs get swapped.']),
    remember: 'Difficulty changes minute by minute. This is the start of our idea.' },

  'How we evaluate tracking': { kind: 'none',
    simple: 'We score a tracker with several numbers, because each number checks a different thing.',
    example: 'Think of grading a student: one mark for spelling, one for grammar, one for writing speed. A student can spell well but write very slowly. In the same way, a tracker can find every object (good recall) but keep swapping IDs (bad IDF1), or be accurate but too slow (low FPS).' +
      '<table><tr><th>Question</th><th>Metric</th></tr><tr><td>Are the boxes correct?</td><td>IoU, TP, FP, FN</td></tr><tr><td>Clean and complete?</td><td>Precision, Recall</td></tr><tr><td>Tracking accurate overall?</td><td>MOTA</td></tr><tr><td>Does each object keep its ID?</td><td>IDF1, IDS</td></tr><tr><td>Finding and linking balanced?</td><td>HOTA</td></tr><tr><td>Fast enough for live video?</td><td>FPS</td></tr></table>',
    remember: 'No single number is enough.' },

  'IoU vs NMS': { kind: 'toy',
    simple: '<b>IoU</b> is a number that says how much two boxes overlap. <b>NMS</b> is a cleaning step that deletes duplicate boxes, and it uses IoU to decide.',
    example: '<b>IoU:</b> two boxes, each with area 100. Their overlap is 60. Their union is 100 + 100 − 60 = 140. <b>IoU = 60 ÷ 140 ≈ 0.43</b>.<br><br>' +
      '<b>NMS:</b> the detector draws 3 boxes on one car, with scores 0.9, 0.8 and 0.7. NMS keeps the 0.9 box. The other two overlap it more than the NMS limit (say 0.45), so they are deleted. Result: <b>one car, one box</b>.',
    remember: 'IoU measures. NMS cleans.' },

  'TP, FP, FN and TN': { kind: 'toy',
    simple: 'Every box and every real object ends in one of four outcomes.',
    example: 'A picture has <b>5 real birds</b>. The detector draws <b>6 boxes</b>.' + list(['4 boxes sit on real birds with IoU ≥ 0.5 → <b>4 TP</b>', '2 boxes are on leaves → <b>2 FP</b> (false alarms)', '1 bird has no box → <b>1 FN</b> (missed)', 'TN = empty sky left empty. There are endless such places, so we do not count TN.']),
    remember: 'FP = false alarm. FN = missed object.' },

  'Precision and recall': { kind: 'toy',
    simple: '<b>Precision:</b> of the boxes we drew, how many were right? <b>Recall:</b> of the real objects, how many did we find?',
    example: 'A lake has <b>10 fish</b>. You pull out 8 things: <b>6 fish</b> and 2 old shoes.' + list(['Precision = 6 ÷ 8 = <b>0.75</b> — how clean your catch is.', 'Recall = 6 ÷ 10 = <b>0.60</b> — how much of the fish you got.']) + 'Use a bigger net (a lower confidence threshold): you catch more fish but also more shoes. Recall goes up, precision goes down.',
    remember: 'Lower threshold → recall ↑, precision often ↓.' },

  'AP and mAP': { kind: 'toy',
    simple: '<b>AP</b> gives one score for one class, using precision at every recall level. <b>mAP</b> is the average AP over all classes.',
    example: 'A detector is tested on 3 classes: car AP 0.90, person AP 0.70, bus AP 0.80.<br><b>mAP = (0.90 + 0.70 + 0.80) ÷ 3 = 0.80</b>.<br><br>A high mAP only says the boxes are good. It says nothing about keeping IDs over time.',
    remember: 'AP and mAP judge the detector, not the tracker.' },

  'MOTA': { kind: 'toy',
    simple: 'MOTA starts at 1 (perfect) and subtracts all mistakes — misses, false alarms and ID switches — divided by the number of real objects (GT).',
    example: 'A video has <b>GT = 100</b> real object appearances. The tracker misses 20 (FN), draws 10 false boxes (FP) and makes 5 ID switches (IDS).<br><b>MOTA = 1 − (20 + 10 + 5) ÷ 100 = 0.65</b><br><br>' +
      'Now it finds 15 more objects (FN = 5) but makes 10 more switches (IDS = 15):<br><b>MOTA = 1 − (5 + 10 + 15) ÷ 100 = 0.70</b><br>MOTA went <b>up</b>, yet the IDs got <b>worse</b>.',
    remember: 'MOTA can hide ID problems.' },

  'Identity switches': { kind: 'toy',
    simple: 'An identity switch happens when a tracked object suddenly gets a different ID number.',
    example: 'Two runners, <b>ID 4</b> and <b>ID 7</b>, cross each other. After crossing, the tracker calls the first runner 7 and the second runner 4. That is <b>2 identity switches</b>. A system that counts people by ID now has both paths wrong.',
    remember: 'Lower IDS is better. 0 means every object kept its number.' },

  'IDF1': { kind: 'toy',
    simple: 'IDF1 checks how long each object keeps its <b>correct</b> ID. It is a score from 0 to 100% for identity.',
    example: 'A bus is visible for 20 frames. Frames 1–15 it is <b>ID 3</b> (correct). Frames 16–20 it becomes <b>ID 9</b>.<br>Simple view: 15 ÷ 20 = <b>75%</b> of the time with the right ID.<br><br>The real formula matches IDs over the whole video, but the idea is the same: longer correct IDs give a higher IDF1.',
    remember: 'Higher IDF1 = more stable IDs.' },

  'HOTA and FPS': { kind: 'toy',
    simple: '<b>HOTA</b> combines two things: did we find the object (DetA) and did we keep its ID (AssA)? <b>FPS</b> is how many frames the system handles in one second.',
    example: '<b>HOTA:</b> DetA = 0.64 and AssA = 0.36 → HOTA = √(0.64 × 0.36) = √0.2304 = <b>0.48</b>. If either part is bad, HOTA falls.<br><br>' +
      '<b>FPS:</b> a camera sends 30 frames each second. If the system needs 50 ms per frame, it handles 1000 ÷ 50 = <b>20 FPS</b> — slower than the camera, so frames pile up. Our rule is <b>at least 25 FPS</b> (40 ms per frame).',
    remember: 'HOTA = quality. FPS = speed.' },

  /* ---------------- Section II ---------------- */
  'Section II': { kind: 'none',
    simple: 'Before building something new, we studied what exists: which detectors and trackers are fast, which are accurate, and how they are tested.',
    example: 'Like comparing cars before buying one: speed, fuel use and price. We compared models on accuracy (mAP, MOTA), speed (milliseconds per frame) and size (number of parameters).',
    remember: 'This part explains why we chose YOLOv8n + ByteTrack.' },

  'Detector families': { kind: 'none',
    simple: 'Detectors come in three families: <b>one-stage</b> (one fast look), <b>two-stage</b> (guess, then check) and <b>transformer</b> (compare the whole image together).',
    example: 'Finding your friends in a stadium photo:' + list(['<b>One-stage:</b> you glance once and point at everyone you know.', '<b>Two-stage:</b> you first circle every face that might be a friend, then check each circle.', '<b>Transformer:</b> you compare every part of the photo with every other part at once.']) + 'Live video needs speed, so we use one-stage (YOLO).',
    remember: 'One-stage = fastest. That fits real time.' },

  'Detector benchmark comparison': { kind: 'pub',
    simple: 'The table compares famous detectors on the same test (COCO, same GPU, same image size), so the numbers can be compared fairly.',
    example: 'Compare row 1 with our row:' + list(['Faster R-CNN: mAP 37.0, <b>172 ms</b> per frame', 'YOLOv8n: mAP 37.3, <b>3.2 ms</b> per frame']) + 'Almost the same accuracy. 172 ÷ 3.2 ≈ 54, so YOLOv8n is about <b>54× faster</b>.<br>One second of 30 FPS video: Faster R-CNN needs about <b>5.2 s</b>, YOLOv8n about <b>0.1 s</b>.',
    remember: 'Same accuracy, far faster → YOLOv8n.' },

  'Why YOLOv8n': { kind: 'pub',
    simple: 'YOLOv8n is small, fast and accurate enough. We keep it the <b>same in every experiment</b>, so any improvement comes from AC-MOT, not from the detector.',
    example: '3.2 ms per frame means about 1000 ÷ 3.2 ≈ <b>312 frames per second</b> for the detector alone — that is the “~300 FPS headroom”. The spare time is used by scene analysis and tracking.<br><br>Fair-test idea: to test a new tyre you keep the same car and the same driver. Otherwise you cannot tell what made the lap faster.',
    remember: 'Fixed detector = fair comparison.' },

  'Our own speed test': { kind: 'real',
    simple: 'We timed several YOLO models ourselves. The small “n” models were fastest; the big ones took more time per frame.',
    example: 'From our early test: YOLOv8n took ' + B('detectorTiming.rows.1.1', 2) + ' ms and YOLOv8x took ' + B('detectorTiming.rows.8.1', 2) + ' ms per frame — about <b>2.7×</b> more time for the largest model.<br><br><b>Careful:</b> this was an early exploratory test and its raw log was not kept. Use it only as support, not as a benchmark.',
    remember: 'Bigger model = slower. We need spare time for the full system.' },

  'Tracker families': { kind: 'none',
    simple: '<b>Tracking-by-detection:</b> detect boxes first, then link them. <b>Joint:</b> one network detects and also learns how objects look. <b>Transformer:</b> attention links objects.',
    example: 'Taking attendance in a moving class:' + list(['<b>Tracking-by-detection:</b> take a photo each minute, then match students to last minute’s list by position.', '<b>Joint:</b> while taking the photo, also note each student’s clothes to help matching.', '<b>Transformer:</b> look at all photos together and decide who is who.']) + 'We use the first: simple, fast, and we can change detector settings without touching the tracker.',
    remember: 'Detect first, then link.' },

  'Evolution of trackers': { kind: 'toy',
    simple: 'SORT used only positions. DeepSORT added appearance. ByteTrack also keeps <b>low-score boxes</b>. BoT-SORT adds camera-motion correction.',
    example: 'A person walks behind a tree and shows half the body, so the detector score drops to <b>0.3</b>.' + list(['A tracker that drops boxes below 0.5 loses the track → when the person comes back, they get a <b>new ID</b>.', 'ByteTrack gives the 0.3 box a second chance → the <b>same ID</b> continues.']) +
      'Life of a track: <b>create</b> (new object) → <b>update</b> (matched each frame) → <b>keep alive</b> (hidden for a few frames) → <b>delete</b> (gone too long).',
    remember: 'ByteTrack = speed + recovers weak objects.' },

  'ByteTrack baseline': { kind: 'toy',
    simple: 'ByteTrack matches in <b>two rounds</b>: strong boxes first, then weak boxes get a second chance to continue existing tracks.',
    example: 'Limit τ = 0.5. Boxes in this frame: A = 0.9, B = 0.8, C = 0.3. Tracks from the last frame: T1, T2, T3 (the Kalman filter predicts where they are now).' +
      steps(['Round 1 (strong boxes): A → T1, B → T2. T3 is still unmatched.', 'Round 2 (weak boxes): C overlaps T3’s predicted position → C → T3.', 'Without round 2, T3 would be lost and the object would later get a new ID.']),
    remember: 'This is why the confidence setting matters so much.' },

  'Published MOTA on MOT17': { kind: 'pub',
    simple: 'On the MOT17 street benchmark, published MOTA goes from 43.1% (SORT) to 81.7% (SMILEtrack). ByteTrack reaches 80.3%.',
    example: '80.3% sounds great. But MOT17 cameras are close to people, so people look large. Our drone videos have objects only 5–30 pixels wide, so our MOTA values are much lower.<br><br>Comparing 80% on MOT17 with 25% on VisDrone is like comparing a 100 m time on a running track with a 100 m time in deep sand.',
    remember: 'Only compare numbers from the same dataset and protocol.' },

  'Quick question: fewest ID switches': { kind: 'pub',
    simple: 'A short question to keep the audience thinking: which tracker makes the fewest ID switches?',
    example: 'Let people choose: SORT, DeepSORT, ByteTrack or OC-SORT. Hint: the tracker with the best accuracy is <b>not</b> the winner on identity.<br><br>Answer on the next slide: <b>OC-SORT</b>, with 784 switches.',
    remember: 'Wait a few seconds before moving on.' },

  'ID switches on MOT17': { kind: 'pub',
    simple: 'Judged on ID switches, the order changes: OC-SORT is best (784), SORT is worst (4,852), ByteTrack is in the middle (2,196).',
    example: 'ByteTrack had the best MOTA of these trackers, but 2,196 switches is about <b>2.8×</b> OC-SORT’s 784. One number never tells the full story.<br><br>In our own development ablation, only tuning ByteTrack changed ID switches from ' + B(A + '0.ids') + ' to ' + B(A + '1.ids') + '.',
    remember: 'Accuracy and identity must be read together.' },

  'Benchmark datasets': { kind: 'toy',
    simple: 'Each dataset tests a different situation. <b>VisDrone</b> is our main test because objects are tiny and crowded. <b>UAVDT</b> is a second drone test, used with no tuning.',
    example: 'A car in a street photo (COCO) may be about 300 pixels wide. The same car in VisDrone, filmed from high up, may be about 15 pixels — <b>20× smaller</b>. A method that works on large objects can fail badly on drone video.',
    remember: 'Test where the problem is hardest.' },

  'Conclusions of the survey': { kind: 'pub',
    simple: 'The field has become much faster and more accurate, but <b>no single model is best for every job</b>.',
    example: list(['Speed: Faster R-CNN 172 ms → RF-DETR-S 3.5 ms ≈ <b>49× faster</b>.', 'Accuracy: 37.0 → 52.9 mAP, that is (52.9 − 37.0) ÷ 37.0 ≈ <b>43% more</b>.']) +
      'Choosing a model is like choosing a vehicle: a truck carries more, a motorbike is faster. For a real-time drone system we chose the light pair <b>YOLOv8n + ByteTrack</b>.',
    remember: 'Our question is not “which model?” but “can smart settings help?”.' },

  /* ---------------- Section III ---------------- */
  'Section III': { kind: 'none',
    simple: 'This part explains the exact problem: detectors use <b>one fixed setting</b> while the scene keeps changing.',
    example: 'Like wearing the same sunglasses all day: perfect at noon, dangerous at night.',
    remember: 'Fixed settings vs a changing scene.' },

  'One fixed threshold': { kind: 'toy',
    simple: 'A normal tracker uses the same confidence (0.25), NMS IoU (0.45) and input size (640) for <b>every</b> frame, easy or hard.',
    example: 'Confidence 0.25 means “keep boxes with a score of at least 0.25”.' + list(['<b>Easy road:</b> cars score 0.8–0.9. The line at 0.25 does not matter.', '<b>Crowded night scene:</b> many real people score only 0.15–0.24. All of them are thrown away.']) + 'So one number is too strict for the hard scene and does nothing for the easy one.',
    remember: 'The gap: fixed settings do not react to the scene.' },

  'Research question and contributions': { kind: 'none',
    simple: 'Main question: can detector settings that <b>follow the scene</b> give better tracking — in real time and <b>without retraining</b> the detector?',
    example: 'Think of auto-brightness on a phone. The screen is not replaced; a light sensor measures the room and adjusts the brightness.' + list(['<b>SCI</b> is our “light sensor” for difficulty.', 'The <b>Smart Calibrator</b> is the “brightness control” for the detector.', 'A <b>fair test</b> keeps the same detector for every system.', 'An <b>honest negative</b>: a colour-histogram ReID did not help, so we report it and do not use it.']),
    remember: 'Nothing is retrained. Only the settings change.' },

  /* ---------------- Section IV ---------------- */
  'Section IV': { kind: 'none',
    simple: 'Our method: measure how hard the frame is (<b>SCI</b>), then set the detector for it (<b>Smart Calibrator</b>). The detector and tracker stay unchanged.',
    example: 'A home thermostat: the thermometer (SCI) reads the room, the controller (Smart Calibrator) decides, and the heater (YOLOv8n) is the same device as before.',
    remember: 'Measure → decide → same detector.' },

  'What we add': { kind: 'toy',
    simple: 'AC-MOT adds only <b>two steps</b> before the detector: measure the scene, and re-calibrate the settings.',
    example: list(['<b>Frame 100, open road:</b> measured easy → normal confidence, small input size → fast.', '<b>Frame 900, crowded night market:</b> measured hard → in the original design, lower confidence and a bigger input, so tiny people can be seen.']) + 'Both frames use the same YOLOv8n and the same ByteTrack. Only the settings passed to them change.',
    remember: 'Two blue steps = the whole contribution.' },

  'The pipeline for each frame': { kind: 'toy',
    simple: 'SCI is <b>one number from 0 (easy) to 1 (hard)</b> that describes how difficult the current frame is.',
    example: list(['<b>SCI 0.10:</b> a highway at noon with four large trucks.', '<b>SCI 0.50:</b> a street with some parked cars and trees.', '<b>SCI 0.63</b> (the dial): a crowded, dark scene with many small objects.']) + 'SCI does not find objects. It is like a weather report the detector reads before it starts work.',
    remember: 'SCI = difficulty meter.' },

  'SCI from frame to score': { kind: 'toy',
    simple: 'Seven small steps turn one frame into one stable difficulty number.',
    example: steps(['Take the frame.', 'Shrink it to 25% and make it gray (1920 × 1080 → 480 × 270, 16× fewer pixels).', 'Measure five clues: crowd, tiny, edges, night, blur.', 'Mix them with weights → for example 0.63.', 'Clip the result into 0 … 1.', 'Average with the last readings: 0.50, 0.55, 0.58, 0.60, 0.62, 0.63, 0.63 → mean ≈ 0.59.', 'The final SCI (0.59) sets the detector for the next frames.']),
    remember: 'Measure, mix, clip, smooth.' },

  'Step 1: measure scene complexity': { kind: 'toy',
    simple: 'SCI uses five cheap clues, each with a weight: crowd 0.30, tiny 0.30, edges 0.20, night 0.10, blur 0.05.',
    example: list(['<b>Crowd:</b> last frame had 15 boxes → 15 ÷ 30 = 0.5.', '<b>Tiny:</b> 6 of those 15 boxes are smaller than 32 × 32 px → 6 ÷ 15 = 0.4.', '<b>Edges:</b> a busy parking lot has many lines → high edge value.', '<b>Night:</b> average brightness 55, which is below 80 → night is on.', '<b>Blur:</b> a shaking camera → low sharpness → blur is on.']) + 'These weights were our first hand-picked design. Section VII re-learns them from data.',
    remember: 'Five clues → one score.' },

  'Three clues on real pictures': { kind: 'real',
    simple: 'The same measurements, computed on real example images: a busy scene has more edges, a night image is darker, and a blurred image has low sharpness.',
    example: list(['<b>Edges:</b> calm sky ' + B('CUE.edgeEasy', 3) + ' vs busy parking lot ' + B('CUE.edgeHard', 3) + ' — many times more edges.', '<b>Night:</b> day mean gray ' + B('CUE.grayDay', 1) + ' (80 or more → flag 0); night ' + B('CUE.grayNight', 1) + ' (below 80 → flag 1).', '<b>Blur:</b> sharp image variance ' + B('CUE.lapSharp', 0, true) + '; blurred copy ' + B('CUE.lapBlur', 0) + ' (below 180 → flag 1).']) +
      'These values were computed on these example images only, to show the idea.',
    remember: 'Each clue is simple image math you can see.' },

  'SCI example 0.63': { kind: 'toy',
    simple: 'To get SCI, multiply each clue by its weight and add the results.',
    example: 'Try a new one — a calm evening street: crowd 0.2, tiny 0.5, edges 0.3, night 1, blur 0.<br><br>SCI = 0.30×0.2 + 0.30×0.5 + 0.20×0.3 + 0.10×1 + 0.05×0<br>= 0.06 + 0.15 + 0.06 + 0.10 + 0 = <b>0.37</b><br><br>0.37 is between 0.35 and 0.60 → label <b>MEDIUM</b>.',
    remember: 'Weight × clue, then add.' },

  'SCI formulas': { kind: 'toy',
    simple: 'These are the exact rules in the code. Crowd and tiny come from the <b>previous frame’s boxes</b>; edges, night and blur come from the <b>small gray image</b>.',
    example: list(['Previous frame had 45 boxes → c = min(45 ÷ 30, 1) = <b>1</b> (capped at 1).', '9 of those boxes are tiny → t = 9 ÷ 45 = <b>0.2</b>.', 'Mean gray 120 → not below 80 → n = <b>0</b>.', 'Laplacian variance 90 → below 180 → b = <b>1</b> (blurry).']) + 'No ground truth is used. SCI only uses the system’s own boxes and pixels, so it works on live video.',
    remember: 'The weights add to 0.95 — they were design priorities, later re-learned.' },

  'One frame becomes one setting': { kind: 'toy',
    simple: 'In the original design, a harder frame gets a <b>lower confidence</b> (keep weak boxes) and a <b>bigger input size</b> (more pixels).',
    example: list(['<b>SCI 0.20 → CLEAR:</b> conf 0.245, size 640. A car scoring 0.30 is kept; a person scoring 0.22 is dropped.', '<b>SCI 0.80 → CROWDED:</b> conf about 0.20, size 832. Now the 0.22 person is kept.']) + 'The image is fed 832 ÷ 640 = 1.3× larger, so a 10-pixel person becomes about 13 pixels.',
    remember: 'Hard frame: keep weak boxes and zoom in. Easy frame: stay strict and fast.' },

  'Step 2: use SCI to choose settings': { kind: 'toy',
    simple: 'Confidence and NMS IoU slide down slowly as SCI rises. The input size jumps up in two steps, at SCI 0.35 and 0.60.',
    example: 'Take <b>SCI = 0.40</b>:' + steps(['conf = 0.245 − 0.050 × 0.40 = <b>0.225</b>', 'iou = 0.490 − 0.050 × 0.40 = <b>0.470</b>', 'SCI > 0.35 → imgsz = <b>736</b>', 'If the label is “crowded”: conf − 0.012 → <b>0.213</b>', 'Check the limits: 0.213 is inside 0.19 … 0.28, so it stays.']),
    remember: 'Smooth lines for conf and IoU, steps for size.' },

  'Smart Calibrator exact settings': { kind: 'none',
    simple: 'Only <b>three detector settings</b> change every frame. The tracker settings are tuned once and then frozen.',
    example: 'There are two different IoU values:' + list(['<b>Detector NMS IoU</b> — deletes duplicate boxes inside one frame. This one moves.', '<b>Tracker match_thresh = 0.86</b> — decides if a box belongs to an existing track across frames. This one never moves.']) + 'Simple picture: NMS removes duplicate names from today’s list. Matching compares today’s list with yesterday’s.',
    remember: 'Don’t mix the two IoU values.' },

  'What AC-MOT changes and keeps': { kind: 'toy',
    simple: 'The whole Scene Analyzer is about 15 lines of simple image math.',
    example: 'One call, step by step:' + steps(['Shrink the frame and make it gray.', 'Brightness 70 → below 80 → night: <b>+0.10</b>.', 'Sharpness 400 → not below 180 → no blur.', 'Edges e = 0.07 → min(0.07 ÷ 0.14, 1) = 0.5 → 0.20 × 0.5 = <b>0.10</b>.', '12 boxes → c = 0.4 → 0.30 × 0.4 = <b>0.12</b>.', '6 of 12 are tiny → t = 0.5 → 0.30 × 0.5 = <b>0.15</b>.', 'r = 0.12 + 0.15 + 0.10 + 0.10 = <b>0.47</b>. Add it to the history; SCI = mean of the last 7.']),
    remember: 'Changes: 3 detector settings. Keeps: weights, tracker, data, hardware.' },

  'Confidence threshold': { kind: 'toy',
    simple: 'The confidence threshold decides which boxes are kept. <b>High</b> = clean but misses weak objects. <b>Low</b> = finds more but lets noise in.',
    example: 'Four boxes with scores 0.9, 0.8, 0.4 and 0.1:' + list(['Threshold <b>0.5</b> → keeps 2. The real object at 0.4 is lost → FN.', 'Threshold <b>0.2</b> → keeps 3. The object is found.', 'Threshold <b>0.05</b> → keeps 4, but the 0.1 box is a shadow → FP.']) + 'The best line is different in every scene.',
    remember: 'That is why AC-MOT moves the line with SCI.' },

  'Algorithm: SmartCalibrator.params': { kind: 'toy',
    simple: 'Start from the defaults, adjust with SCI, then clip into safe limits. Two switches turn each part on or off for the ablation.',
    example: 'SCI = 0.9, label “tiny”, tiny share r = 0.6:' + steps(['conf = 0.245 − 0.045 = 0.200; minus 0.012 for “tiny” = 0.188 → clipped up to <b>0.19</b>.', 'iou = 0.490 − 0.045 = <b>0.445</b>.', 'SCI > 0.60 → imgsz = <b>832</b>.', 'Result: (0.19, 0.445, 832).']) + 'With <b>adaptive_resolution</b> switched off (system A2), the size stays 640.',
    remember: 'Safety floor: confidence never below 0.19.' },

  'Implementation of the calibrator': { kind: 'toy',
    simple: 'Two tricks keep AC-MOT stable and cheap: <b>average the last 7 SCI readings</b>, and <b>analyse only every 10th frame</b>.',
    example: 'Readings: 0.25, 0.27, then one strange frame 0.80, then 0.29, 0.31.' + list(['Without smoothing, reading 3 would switch the detector to “crowded” for no reason.', 'With averaging: (0.25 + 0.27 + 0.80) ÷ 3 = <b>0.44</b> — a small bump, not a jump.', 'At 30 FPS, every 10th frame means only 3 analyses per second.']) +
      'Development ablation speed: A3 ' + B(A + '3.fps', 2) + ' FPS vs A0 ' + B(A + '0.fps', 2) + ' FPS.',
    remember: 'One odd frame should not change the whole setup.' },

  /* ---------------- Section V ---------------- */
  'Section V': { kind: 'none',
    simple: 'Here we fix the test: which data, which objects, and which scoring rules.',
    example: 'A fair exam needs the same questions and the same marking scheme for every student.',
    remember: 'Same rules for every system.' },

  'Choosing the test domain': { kind: 'toy',
    simple: 'We test on drone video because it is the hardest case: tiny objects and big changes within one flight.',
    example: 'A drone climbs from 10 m to 100 m. A person who was about 100 pixels tall becomes about <b>10 pixels</b> tall. The best detector setting at 10 m is not the best at 100 m — exactly where adaptive settings should help.',
    remember: 'Changing scenes = the right place to test adaptation.' },

  'The VisDrone2019-MOT benchmark': { kind: 'real',
    simple: 'VisDrone2019-MOT is Full-HD drone video with very small objects. We <b>tune on 7 validation videos</b> and <b>test on 17 test-dev videos</b>.',
    example: 'Test-dev has ' + B('visdroneTest.frames', null, true) + ' frames and ' + B('visdroneTest.gtBoxes', null, true) + ' labelled boxes → about ' + B('visdroneTest.density') + ' objects in every frame.<br><br>In a 1920-pixel-wide frame, a 20-pixel car is only about <b>1%</b> of the width.',
    remember: 'Tune on validation, judge on test-dev.' },

  'Object classes evaluated': { kind: 'toy',
    simple: 'We score five classes: pedestrian, car, van, truck and bus. In our protocol the classes are merged, so a correct box counts even if car and van are confused.',
    example: 'A frame has 3 cars, 1 van and 2 bicycles.' + list(['We count <b>4 objects</b> (3 cars + 1 van).', 'The bicycles are ignored: at 100 m they are a few unclear pixels, and even human labellers disagree.', 'If YOLO calls the van a “car”, it still counts as found.']),
    remember: 'Five clear classes, the same for every system.' },

  'Ground-truth filtering rules': { kind: 'toy',
    simple: 'Before scoring, we remove labels that are too hidden or too cut off, and the “ignore” areas.',
    example: list(['Label A: fully visible (occlusion 0) → <b>kept</b>.', 'Label B: slightly hidden behind a tree (occlusion 1) → <b>kept</b>.', 'Label C: almost fully hidden (occlusion 2) → <b>removed</b>.', 'Label D: a large part outside the image (truncation 2) → <b>removed</b>.']) + 'If we kept Label C, a tracker would be punished for missing something a person can hardly see.',
    remember: 'Measure the tracker, not label doubt.' },

  'Evaluation protocol': { kind: 'toy',
    simple: 'Every system is scored the same way, and the tracker <b>restarts for every video</b>.',
    example: '<b>No leakage:</b> if the tracker were not reset, IDs from video 1 would continue into video 2, and old tracks could wrongly match new objects. Resetting means every video starts clean.<br><br>' +
      '<b>DetA example:</b> TP = 60, FP = 20, FN = 20 → DetA = 60 ÷ (60 + 20 + 20) = <b>0.60</b>.',
    remember: 'Reset, filter, match at IoU 0.5, add up, report.' },

  'Fair and attributable design': { kind: 'none',
    simple: 'Each system differs from the one before it in <b>exactly one part</b>, so we know which part caused which change.',
    example: 'A cooking test:' + list(['A0: the base recipe.', 'A1: add salt only.', 'A2: add pepper too.', 'A3: add garlic too.']) + 'If the taste jumps at A3, the garlic caused it. Same detector, same videos, same GPU — only one ingredient changes each time.',
    remember: 'One change at a time.' },

  'Two protocols': { kind: 'toy',
    simple: 'Our numbers use our own AC-MOT protocol (five classes merged). The official VisDrone protocol keeps classes separate. The two cannot be mixed.',
    example: 'A van detected as “car”:' + list(['<b>Our protocol:</b> correct — class does not matter.', '<b>Official protocol:</b> wrong class.']) + 'So the same run can get two different scores — like marking an exam once for content only, and once for content plus spelling. Both are fair, but the marks are not comparable.',
    remember: 'Our results are not official leaderboard results.' },

  /* ---------------- Section VI ---------------- */
  'Section VI': { kind: 'none',
    simple: 'Stage 1 results: we add AC-MOT’s parts one at a time and measure each step.',
    example: steps(['A0: baseline ByteTrack.', 'A1: + tuned tracker settings.', 'A2: + adaptive confidence and NMS.', 'A3: + adaptive input size (full AC-MOT).']) + 'All on 17 sequences, with one fixed YOLOv8n.',
    remember: 'These are development numbers from an older evaluator.' },

  'Ablation A0 to A3': { kind: 'real',
    simple: 'The table shows the scores after each added part. Accuracy rises at every step; ID switches fall, then rise again at A3.',
    example: list(['MOTA: A0 ' + B(A + '0.mota', 2) + ' → A3 ' + B(A + '3.mota', 2) + ' (' + B('devDerived.m03') + ' points).', 'IDS: ' + B(A + '0.ids') + ' → ' + B(A + '1.ids') + ' → ' + B(A + '2.ids') + ' → ' + B(A + '3.ids') + '.']) +
      'How to read a row: A2 means “A1 plus adaptive confidence and NMS”. Only that part is new compared with the row above.',
    remember: 'HOTA* is a quick estimate. Never mix these with the final TrackEval numbers.' },

  'Accuracy improves at every step': { kind: 'real',
    simple: 'All three accuracy scores — MOTA, IDF1 and HOTA* — go up at every step.',
    example: 'IDF1: A0 ' + B(A + '0.idf1', 2) + ' → A3 ' + B(A + '3.idf1', 2) + ' (' + B('devDerived.i03') + ' points).<br><br>Like three school subjects all improving every term: the gain is not an accident of one measure.',
    remember: 'The biggest jump is the last step: adaptive input size.' },

  'Where the MOTA gain comes from': { kind: 'real',
    simple: 'Each arrow shows how much MOTA one added part gave.',
    example: list(['Tuning the tracker: <b>' + B('devDerived.m01') + '</b> points', 'Adaptive confidence: <b>' + B('devDerived.m12') + '</b> points', 'Adaptive input size: <b>' + B('devDerived.m23') + '</b> points — the largest single gain']) +
      'Simple picture: tuning and confidence are like better shoes; a bigger input size is like glasses for someone who could not see small things.',
    remember: 'Most of the gain comes from seeing small objects.' },

  'Recall explains the MOTA gain': { kind: 'real',
    simple: '<b>Recall</b> is the share of real objects we found. MOTA rose mainly because recall rose — fewer missed objects.',
    example: 'Recall: A0 ' + B(A + '0.recall', 2) + '% → A3 ' + B(A + '3.recall', 2) + '%.<br><br>Picture a frame with 100 real objects: A0 finds about 37 of them and A3 about 49 — roughly 12 more per 100. In crowded drone scenes, missed objects (FN) are the biggest part of the MOTA formula.',
    remember: 'Fewer misses → higher MOTA.' },

  'The identity-switch trade-off': { kind: 'real',
    simple: 'A3 finds more small objects, but more objects close together also means more chances to mix up IDs.',
    example: 'Tuning changed ID switches by ' + B('devDerived.ids01') + '. Adaptive input size changed them by ' + B('devDerived.ids23') + '.<br><br>Simple picture: following 10 people in a square gives few chances to swap two of them. Following 20 tiny people in the same square gives many more pairs that can be confused.',
    remember: 'This is the problem Stage 2 attacks.' },

  'Accuracy at real-time speed': { kind: 'real',
    simple: 'Adding AC-MOT cost only a little speed. All four systems stay above 25 FPS.',
    example: 'A0 ' + B(A + '0.fps', 2) + ' FPS → A3 ' + B(A + '3.fps', 2) + ' FPS (' + B('devDerived.fps03') + ').<br><br>25 FPS means a budget of 40 ms per frame. As long as a system stays above the red 25 FPS line, it keeps up with live video.',
    remember: 'Big accuracy gain, small speed cost.' },

  'Baseline A0 versus AC-MOT A3': { kind: 'toy',
    simple: 'Summary of Stage 1: much better accuracy and recall, a small speed cost, and more ID switches.',
    example: '<b>“pts” = percentage points.</b> If a score goes from 40% to 50%, that is <b>+10 points</b>. As a share of the old value it would be +25%. The table always uses points.<br><br>Green = better, red = worse. The same YOLOv8n is used in every row.',
    remember: 'The one thing to fix next: ID switches.' },

  'Same frames, different control': { kind: 'none',
    simple: 'The videos show the <b>same frames</b> with the <b>same detector</b>, side by side: without and with AC-MOT control.',
    example: 'What to look for:' + steps(['A group of small people — count the boxes on each side.', 'A vehicle passing under a tree — does its box stay?', 'Use the tabs to switch clips (the second clip has tiny objects).']) + 'The ID markers on screen are a visual aid, not the official ID-switch count.',
    remember: 'Videos show the idea; the numbers are the evidence.' },

  'Final live run: baseline vs Full AC-MOT': { kind: 'real',
    simple: 'The original full AC-MOT, scored with the official TrackEval tool on 17 test-dev videos, beat the baseline on accuracy and had fewer ID switches, while staying real-time.',
    example: list(['IDS: ' + B('historical.baseline.ids') + ' → ' + B('historical.full.ids') + ' (244 fewer, about 20%).', 'IDF1: ' + B('historical.baseline.idf1', 2) + ' → ' + B('historical.full.idf1', 2) + '.', 'FPS: ' + B('historical.baseline.fps', 1) + ' → ' + B('historical.full.fps', 1) + ', still well above 25.']) +
      'These numbers are lower than the Stage 1 table because this evaluator is stricter. Never mix the two.',
    remember: 'Stricter tool, same message: better and still real-time.' },

  'Choosing the winner among finalists': { kind: 'real',
    simple: 'Two systems passed the rules. The rule picked the highest MOTA, but the runner-up was better on HOTA, IDF1 and ID switches.',
    example: 'MOTA ' + B('historical.full.mota', 3) + ' vs ' + B('historical.match090.mota', 3) + ': a gap of only <b>0.046</b> points — like winning a race by one thousandth of a second.<br>Meanwhile TRK_MATCH_090 had ' + B('historical.match090.ids') + ' ID switches vs ' + B('historical.full.ids') + '.',
    remember: 'A rule based on one number can hide identity quality.' },

  /* ---------------- Section VII ---------------- */
  'Section VII': { kind: 'none',
    simple: 'Stage 1 improved accuracy, but ID switches rose. <b>Stage 2</b> replaces hand-picked settings with an automatic search that must obey rules. <b>Stage 3</b> looks for a better balance and tests on a new dataset.',
    example: 'Like moving from cooking “by feel” to a tested recipe with a checklist.',
    remember: 'Search with rules, chosen on validation only.' },

  'Quick question: higher MOTA': { kind: 'none',
    simple: 'Ask the audience: is a higher MOTA always a better tracker?',
    example: 'Let them guess. The answer on the next slide is <b>not always</b>: MOTA can rise while ID switches also rise.',
    remember: 'Wait a few seconds before moving on.' },

  'Accuracy up, ID switches back': { kind: 'real',
    simple: 'From A2 to A3, MOTA went up — and ID switches went up too. So a higher MOTA is not always a better tracker.',
    example: 'A2 → A3: MOTA ' + B('devDerived.m23') + ' points, ID switches ' + B('devDerived.ids23') + '.<br><br>Like a student whose exam mark rises because they answered more questions, while their careless mistakes also increased.',
    remember: 'Watch identity, not only accuracy.' },

  'Why one score can fool us': { kind: 'toy',
    simple: 'MOTA adds FN, FP and IDS into one number. A big drop in one mistake can hide a rise in another.',
    example: 'GT = 1,000.' + list(['<b>System X:</b> FN 500, FP 100, IDS 50 → MOTA = 1 − 650 ÷ 1000 = <b>35%</b>', '<b>System Y:</b> FN 350, FP 100, IDS 150 → MOTA = 1 − 600 ÷ 1000 = <b>40%</b>']) + 'Y has the higher MOTA but <b>3× more ID switches</b>. That is why Stage 2 makes IDS a hard rule.',
    remember: 'One score can hide a problem.' },

  'The new plan: a search with rules': { kind: 'real',
    simple: 'Instead of choosing settings by hand: narrow the options, let a search choose, freeze the winner, and test once.',
    example: 'Every candidate must pass two rules: <b>FPS ≥ 25</b> and <b>IDS ≤ ' + B('v1.oldA3val.ids') + '</b> (what the old AC-MOT got on the same validation videos).<br><br>Runs: 36 sweeps + 25 timing settings + 50 Optuna trials = <b>111 runs</b>, all on the 7 validation videos. Test-dev is used only once, at the end — like not seeing the final exam while you study.',
    remember: 'Validation to choose, test-dev to judge.' },

  'What is Optuna': { kind: 'toy',
    simple: 'Optuna is a free search tool. It picks settings, runs the system, reads the score, and uses what it learned to pick better settings next time.',
    example: 'By hand: 5 confidence values × 5 NMS values × 3 sizes = <b>75 runs</b> — and that is before trying any SCI weights.<br><br>Optuna with 50 trials: it tries some mixes first, notices that (for example) one confidence range scores well, and spends more trials near it.<br><br>It is <b>not</b> AI training: it trains nothing and only chooses numbers.',
    remember: 'Optuna = a smart way to try settings.' },

  'Step 1: sweeps shrink the search': { kind: 'real',
    simple: 'Before the big search, we changed <b>one setting at a time</b> to find the useful ranges.',
    example: list(['<b>Confidence:</b> 0.05, 0.10 … 0.50 = 10 runs. Kept 0.25 – 0.45.', '<b>Input size:</b> 512 to 960 in 32-pixel steps = 15 runs. Kept 512, 928, 960.', '<b>NMS IoU:</b> 0.30 to 0.80 = 11 runs. Kept 0.30 – 0.70.']) + '10 + 15 + 11 = <b>36 runs</b>. Like tasting one spice at a time before mixing a recipe.',
    remember: 'Only the good ranges go into the search.' },

  'Step 2: how often to look, how much to smooth': { kind: 'real',
    simple: 'Two timing settings: <b>S</b> = how often SCI is measured, <b>W</b> = how many readings are averaged.',
    example: 'The frozen choice is <b>W = 7, S = 10</b>. At 30 FPS, SCI is measured 3 times per second, and 7 readings cover 70 frames ≈ 2 seconds.' +
      list(['W too small (1): one strange frame flips the settings.', 'W too large: the system reacts late when the drone flies over a crowd.']),
    remember: '25 pairs tested on validation; W 7 · S 10 kept for every later study.' },

  'Step 3: learn what a hard scene looks like': { kind: 'real',
    simple: 'Instead of fixed limits like “dark means below 80”, we measured the real range of each clue on our validation videos and score each frame by its <b>rank</b>.',
    example: 'Brightness on validation frames: 25% of frames are below ' + B('calibration.brightness.q25', 0) + ', half are below ' + B('calibration.brightness.median', 0) + ', 75% are below ' + B('calibration.brightness.q75', 0) + '.<br><br>A frame darker than 75% of our frames gets a high “night” rank. The score now matches <b>our</b> videos, not a guess.',
    remember: 'Measured ranges replace hand-set limits. No ground truth is used.' },

  'Optuna-based optimization': { kind: 'toy',
    simple: 'Optuna TPE tunes <b>11 numbers together</b> over 50 trials, only on validation videos, and keeps the best trial that passes both rules.',
    example: '11 = 5 SCI weights + 2 confidence values + 2 NMS values + 2 SCI switch points.<br><br><b>Tie-break example:</b> Trial A has MOTA 23.0 and IDS 270; Trial B has MOTA 23.0 and IDS 250 → <b>B wins</b> (fewer ID switches).<br><br>Seed 42 means running the search again gives the same trials — repeatable.',
    remember: 'The test set is never used during the search.' },

  'Quick question: what did the search learn': { kind: 'none',
    simple: 'Ask the audience which clue the search trusted most.',
    example: 'Our hand-set guess gave <b>crowd</b> and <b>tiny</b> the largest weights (0.30 each). Let people guess among crowd, tiny, edges, night and blur. The answer comes right after the search result.',
    remember: 'Answer: edges.' },

  'Step 4 result: Trial 24': { kind: 'real',
    simple: 'Trial 24 passed both rules and had the highest MOTA among the trials that passed. It was then frozen.',
    example: 'Compared with the old AC-MOT on the same 7 validation videos:' + list(['MOTA ' + B('v1.oldA3val.mota', 2) + ' → ' + B('v1.val.mota', 2) + ' (about 5 points more)', 'IDS ' + B('v1.oldA3val.ids') + ' → ' + B('v1.val.ids') + ' (just inside the rule)', 'FPS ' + B('v1.oldA3val.fps', 1) + ' → ' + B('v1.val.fps', 1) + ' (slower, still above 25)']) +
      'Picture a selection: 50 candidates, some fail the speed or ID rule, and among the rest the highest MOTA wins.',
    remember: '“Trial 37” in the old seminar was a draft. The real winner is Trial 24.' },

  'What the search learned': { kind: 'real',
    simple: 'The search gave the most weight to <b>edges</b> and the least to <b>night</b>. It also picked settings we did not expect.',
    example: list(['Hand-set weights: crowd 0.30, tiny 0.30, edges 0.20.', 'Learned by V1: edges ' + B('v1.weights.edge', 2) + ', night ' + B('v1.weights.night', 2) + '.', 'Confidence: ' + B('v1.params.conf_easy', 2) + ' (easy) → ' + B('v1.params.conf_hard', 2) + ' (hard) — it goes <b>up</b>, the opposite of our Stage 1 guess.', 'NMS IoU stays ' + B('v1.params.nms_easy', 2) + ' in easy and hard scenes.']),
    remember: 'Measured choices can beat intuition.' },

  'Validation builds it, test judges it': { kind: 'none',
    simple: '<b>Validation</b> videos are for choosing. <b>Test</b> videos are only for the final judgement, once.',
    example: list(['<b>Practice exams (validation):</b> study, try, and adjust as much as you like.', '<b>Final exam (test-dev):</b> taken once. You cannot change your answers after seeing the marks.']) + 'If we tuned on test-dev, the score would look better than the system really is.',
    remember: 'Learn, compare, choose, freeze — then test once.' },

  'Final test on test-dev': { kind: 'real',
    simple: 'On 17 unseen videos, V1 beat the baseline on MOTA, HOTA and IDF1. The ID-switch difference is <b>not certain</b>.',
    example: list(['MOTA +' + B('testdev.bootstrap.v1_vs_base.mota.0', 2) + ' points, 95% range [' + B('testdev.bootstrap.v1_vs_base.mota.1', 2) + ', ' + B('testdev.bootstrap.v1_vs_base.mota.2', 2) + ']. The whole range is above 0 → the gain is real.', 'ID switches: ' + B('testdev.bootstrap.v1_vs_base.idsRed.0') + ' fewer on average, but the range goes from 114 more to 219 fewer. It crosses 0 → not proven.']) +
      '<b>Bootstrap in plain words:</b> pick 17 videos at random from our 17 (some twice, some not at all), recompute the difference, repeat 5,000 times, and see where 95% of the results fall.',
    remember: 'V1 does not have the fewest ID switches — the old AC-MOT does.' },

  'What Stage 2 adds': { kind: 'real',
    simple: 'Stage 2 adds a better, defensible way to <b>choose settings</b> — not a new model.',
    example: 'Same YOLOv8n and ByteTrack. What changed:' + list(['111 logged validation runs', 'two hard rules: FPS ≥ 25 and IDS ≤ ' + B('v1.oldA3val.ids'), 'one frozen choice (Trial 24) and one final test']) +
      'Trial 24: IDS ' + B('v1.val.ids') + ' and ' + B('v1.val.fps', 1) + ' FPS on validation; ' + B(T + '2.fps', 1) + ' FPS on test-dev.',
    remember: 'Better choosing, not a bigger model.' },

  'Stage 3: why V2': { kind: 'toy',
    simple: 'V1 wanted the highest MOTA under an ID-switch limit. V2 searches for <b>both goals at once</b>: more MOTA and fewer ID switches.',
    example: 'Buying a phone:' + list(['<b>V1:</b> “Give me the best camera, but the price must stay under 500.”', '<b>V2:</b> “Show me every phone where you cannot get a better camera without paying more” — then pick a balanced one.']),
    remember: '50 trials were planned; 49 finished. We report 49.' },

  'V2 Pareto front': { kind: 'real',
    simple: 'Each dot is a trial that cannot improve one goal without getting worse on the other. Together these dots form the <b>Pareto front</b>.',
    example: '<b>Made-up first:</b> A = MOTA 22, IDS 300. B = MOTA 20, IDS 200. C = MOTA 19, IDS 250. C is worse than B on both → not on the front. A and B are both on the front; you choose by what matters more.<br><br>' +
      '<b>Real V2 points:</b>' + list(['T16 — highest MOTA: ' + B('v2.pareto.0.1', 2) + ', IDS ' + B('v2.pareto.0.2'), 'T8 — fewest IDS: ' + B('v2.pareto.16.2') + ', MOTA ' + B('v2.pareto.16.1', 2), 'T22 — balanced pick: MOTA ' + B('v2.val.mota', 2) + ', IDS ' + B('v2.val.ids')]),
    remember: 'Top-left is best: more MOTA, fewer ID switches.' },

  'V2 Trial 22': { kind: 'real',
    simple: 'V2’s balanced choice, Trial 22, has far fewer ID switches and runs faster, but gives up some MOTA.',
    example: 'On test-dev, V1 → V2:' + list(['IDS ' + B(T + '2.ids', null, true) + ' → ' + B(T + '3.ids') + ' (265 fewer)', 'FPS ' + B(T + '2.fps', 1) + ' → ' + B(T + '3.fps', 1), 'MOTA ' + B(T + '2.mota', 2) + ' → ' + B(T + '3.mota', 2)]) +
      'One visible difference in the settings: V2 uses NMS ' + B('v2.params.nms_easy', 2) + ' in easy scenes and ' + B('v2.params.nms_hard', 2) + ' in hard scenes, so duplicates are removed more strongly when the scene is hard.',
    remember: 'Honest: test-dev had already been used for V1, so this is a second test after selection.' },

  'All systems on test-dev': { kind: 'real',
    simple: 'One chart per metric, for all four systems on the same 17 test-dev videos.',
    example: list(['<b>V1</b> wins MOTA (' + B(T + '2.mota', 2) + '), HOTA (' + B(T + '2.hota', 2) + ') and IDF1 (' + B(T + '2.idf1', 2) + ').', '<b>V2</b> wins ID switches (' + B(T + '3.ids') + ') and speed (' + B(T + '3.fps', 1) + ' FPS).', '<b>Old AC-MOT</b> has fewer ID switches than V1 (' + B(T + '1.ids', null, true) + ' vs ' + B(T + '2.ids', null, true) + ').']) +
      'There is no single “best” — it depends on whether accuracy or identity matters more for the job.',
    remember: 'Every AC-MOT version beats the baseline on MOTA, HOTA and IDF1.' },

  'Are the differences real': { kind: 'real',
    simple: 'A difference is “real” when its <b>95% range does not include zero</b>.',
    example: '<b>Made-up first:</b> 6 heads in 10 coin flips could easily be luck; 600 heads in 1,000 flips is not. Bootstrap checks this with our 17 videos.<br><br>' +
      '<b>Real:</b>' + list(['V2 vs V1 ID switches: ' + B('testdev.bootstrap.v2_vs_v1.idsRed.0') + ' fewer, range [' + B('testdev.bootstrap.v2_vs_v1.idsRed.1') + ', ' + B('testdev.bootstrap.v2_vs_v1.idsRed.2') + '] → all above 0 → <b>real</b>.', 'V1 vs baseline ID switches: the range goes from 114 more to 219 fewer → crosses 0 → <b>not proven</b>.']),
    remember: 'Bar crosses zero = not proven.' },

  'UAVDT with zero tuning': { kind: 'real',
    simple: 'We ran the frozen systems on a <b>different drone dataset</b> without changing anything. Both V1 and V2 still beat the baseline.',
    example: 'UAVDT: ' + B('uavdt.sequences') + ' sequences, ' + B('uavdt.frames', null, true) + ' frames.' + list(['V1 MOTA: ' + B(U + '0.mota', 2) + ' → ' + B(U + '1.mota', 2), 'V1 ID switches: ' + B(U + '0.ids') + ' → ' + B(U + '1.ids') + ' (237 fewer)']) +
      '“Zero tuning” means no training, no new search and no re-calibration — like a student who studied one textbook and still passes an exam written from a different one.',
    remember: 'The gain carries over to new data.' },

  'Results across both datasets': { kind: 'real',
    simple: 'On both datasets: V1 is the most accurate; V2 has the fewest ID switches and the fewest false boxes.',
    example: 'False boxes (FP) on UAVDT: V1 ' + B(U + '1.fp', null, true) + ' vs V2 ' + B(U + '2.fp', null, true) + ' → 4,138 fewer for V2.' +
      list(['Choose <b>V1</b> when finding as many objects as possible matters most.', 'Choose <b>V2</b> when stable IDs and fewer false alarms matter more.']),
    remember: 'V2 does not beat V1 overall — it is a different trade-off.' },

  /* ---------------- Section VIII ---------------- */
  'Section VIII': { kind: 'none',
    simple: 'The final part: what we showed, what we did not claim, and what comes next.',
    example: 'Like the end of a report: the findings, the limits, and the next steps.',
    remember: 'A clear, narrow claim.' },

  'What we focused on and why': { kind: 'none',
    simple: 'The claim is narrow: with the <b>same detector and tracker</b>, scene-adaptive settings improve tracking quality at real-time speed.',
    example: 'What we did <b>not</b> claim: a bigger detector, a new tracker, an official leaderboard result, or deep ReID.<br><br>Like saying “a better driving style saves fuel” — not “we built a better engine”.',
    remember: 'Smart settings, not a bigger model.' },

  'Next step: U2MOT': { kind: 'none',
    simple: 'Next we test whether the SCI idea also helps a very different, much heavier published tracker: <b>U2MOT</b>.',
    example: 'If AC-MOT only helped YOLOv8n + ByteTrack, it might be a lucky fit. If it also helps U2MOT — a large YOLOX-X detector with ReID and camera-motion compensation — the idea is more general.',
    remember: 'U2MOT tests the idea. It does not replace our real-time system.' },

  'U2MOT reproduction status': { kind: 'real',
    simple: 'The U2MOT reproduction is set up exactly as published, but its metrics are <b>pending</b>, so no accuracy numbers are shown.',
    example: 'Speed seen so far: about <b>5–6 FPS</b> on a Tesla T4 — our V1 runs at ' + B(T + '2.fps', 1) + ' FPS on test-dev.<br><br>Plan: add one AC-MOT part at a time (confidence → NMS → input size), exactly like our A0 → A3 ablation.',
    remember: 'No result is claimed until the evaluation is finished.' },

  'Conclusion: what AC-MOT delivers': { kind: 'real',
    simple: 'AC-MOT adapts detector settings to the scene, <b>without retraining</b>, and the gains hold on unseen videos and on a second dataset.',
    example: 'Three numbers to remember:' + list(['Stage 1 (development): MOTA A0 → A3 ' + B('devDerived.m03') + ' points.', 'Test-dev: V1 +' + B('testdev.bootstrap.v1_vs_base.mota.0', 2) + ' MOTA vs baseline at ' + B(T + '2.fps', 1) + ' FPS.', 'UAVDT: V1 +' + B('uavdt.bootstrap.v1_vs_base.mota.0', 2) + ' MOTA and ' + B('uavdt.bootstrap.v1_vs_base.idsRed.0') + ' fewer ID switches, with no tuning.']) +
      'Honest limits: hand-designed clues, our own protocol, two drone datasets, one GPU.',
    remember: 'Scenes change; fixed settings don’t. AC-MOT adapts.' },

  'Directions for future work': { kind: 'none',
    simple: 'Each future step fixes a weakness we actually measured.',
    example: list(['<b>Camera-motion compensation:</b> when the drone turns, every object seems to jump. Predicting that jump should reduce ID switches.', '<b>Density-gated input size:</b> use the big input only when many tiny objects are present, to save time on easy frames.', '<b>Deep ReID:</b> recognise a person by appearance when they come back.', '<b>SCI beyond YOLO:</b> try the idea with RT-DETR or DINO, and on AU-AIR.']),
    remember: 'Next steps come from measurements, not guesses.' },

  'Thank you': { kind: 'none',
    simple: 'The end of the talk — time for questions.',
    example: 'Short answers to prepare:' + list(['<b>Why not a bigger detector?</b> A fixed detector keeps the test fair.', '<b>Is Optuna AI?</b> No — it is a search method; it trains nothing.', '<b>Are these official VisDrone results?</b> No — our own protocol, the same for every system.', '<b>Did V2 beat V1?</b> No — it is a different trade-off.']),
    remember: 'Press O to jump to any slide during questions.' }
  };
})();
