/* =====================================================================
   v5 — big "main idea" box at the top of every content slide (same style
   as the metric slides): the key idea in easy, simple-English words.
   Keyed by the slide's data-title:  { t: text, tag: optional label,
   r: 1 = this box replaces the slide's old one-line summary (first block) }
   Rules: no thesis numbers typed here; no AC-MOT before Section IV.
   Slides that already have their own .meaning box are skipped.
   ===================================================================== */
window.MEANING = {
  /* ---------------- Section I ---------------- */
  'Object detection': { tag: 'What it means',
    t: 'A detector looks at <b>one picture</b> and draws a <b>box</b> around each object. For each box it says <b>what</b> the object is and <b>how sure</b> it is — but it has no memory of the last frame.' },
  'Multi-object tracking': { tag: 'What it means',
    t: 'A tracker connects the boxes <b>from frame to frame</b> and gives each object an <b>ID number</b>. Its job is to keep the <b>same number for the same object</b> the whole time.' },
  'Applications': {
    t: 'Tracking is used whenever we must <b>count, follow or watch</b> moving things: cars, crowds, people near roads — and objects seen from <b>drones</b>, which is our focus.' },
  'Challenges of real-time tracking': {
    t: 'The same camera sees <b>easy moments and hard moments</b>. Hidden, tiny, dark or blurred objects make a tracker <b>miss objects</b> and <b>swap IDs</b>.' },
  'How we evaluate tracking': { tag: 'What it means',
    t: 'No single number tells the whole story. We ask <b>six simple questions</b>: are the boxes right, did we find everything, is tracking accurate, do IDs stay the same, is it balanced, and is it fast?' },
  'IoU vs NMS': { tag: 'What it means',
    t: '<b>IoU</b> is a <b>number</b> that says how much two boxes overlap. <b>NMS</b> is a <b>cleaning step</b> that deletes duplicate boxes — and it uses IoU to decide which ones.' },

  /* ---------------- Section II ---------------- */
  'Detector families': {
    t: 'Object detectors come in <b>three families</b>: one-stage (one fast look), two-stage (guess first, then check) and transformers (compare the whole image at once). We use <b>one-stage</b> because it is fast.' },
  'Detector benchmark comparison': {
    t: 'This table compares famous detectors <b>tested in exactly the same way</b>. The key point: <b>YOLOv8n is about as accurate as Faster R-CNN, but about 54× faster</b> and much smaller.' },
  'Why YOLOv8n': {
    t: 'We picked <b>YOLOv8n</b> because it is <b>small, fast and accurate enough</b> — and we keep the <b>same detector in every test</b>, so any gain comes from our method, not from the detector.' },
  'Our own speed test': {
    t: 'We also timed YOLO models ourselves: <b>smaller models run faster</b>. This early test agrees with the published table, but its raw log was not kept, so it is support only.' },
  'Tracker families': {
    t: 'Trackers also come in three families. We use <b>tracking-by-detection</b>: first find the boxes, then <b>link them across frames</b> — simple, fast and easy to control.' },
  'Evolution of trackers': {
    t: 'Trackers improved step by step: SORT used only <b>position</b>, DeepSORT added <b>appearance</b>, and ByteTrack also keeps <b>weak boxes</b>, so half-hidden objects keep their ID.' },
  'ByteTrack baseline': {
    t: 'ByteTrack matches <b>strong boxes first</b>, then gives <b>weak boxes a second chance</b>. If there is <b>no box at all</b>, it keeps the track for a while (the <b>track buffer</b>) before giving a new ID.' },
  'Published MOTA on MOT17': {
    t: 'On the MOT17 street benchmark, published trackers reach about <b>80% MOTA</b>. But people there are large and close to the camera — <b>drone video is much harder</b>, so our numbers will be lower.' },
  'ID switches on MOT17': {
    t: 'Judged on <b>ID switches</b>, the ranking changes: the most accurate tracker is <b>not</b> the one that keeps IDs best. There is a <b>trade-off between tracking accuracy (MOTA) and ID switches</b> — <b>one number is never enough.</b>' },
  'Benchmark datasets': {
    t: 'Each dataset tests a different situation. <b>VisDrone</b> is our main test because its objects are <b>tiny and crowded</b>; <b>UAVDT</b> is a second drone test.' },
  'Conclusions of the survey': {
    t: 'Detectors became <b>much faster and more accurate</b>, but <b>no model is best for every job</b>. For real-time drone video we chose a <b>light, fast pair</b>: YOLOv8n + ByteTrack.' },

  /* ---------------- Section III ---------------- */
  'One fixed threshold': {
    t: 'Normal trackers use <b>one fixed setting</b> for every frame. But scenes change from <b>easy to hard</b> — so one fixed setting is always wrong for some of them.' },

  /* ---------------- Section IV (AC-MOT may be named from here on) ---------------- */
  'What we add': {
    t: 'Our method, <b>AC-MOT</b>, adds only <b>two steps</b> before the detector: <b>measure how hard the scene is</b>, then <b>change the detector settings</b> to match. Everything else stays the same.' },
  'SCI from frame to score': {
    t: 'Seven small steps turn a video frame into <b>one stable difficulty number</b>: shrink it, measure five clues, mix them, keep the result between 0 and 1, and average the last readings.' },
  'Step 1: measure scene complexity': {
    t: 'SCI looks at <b>five cheap clues</b>: crowded, tiny, busy, dark and blurred. The <b>methods</b> are published; the <b>limits are our own design constants</b>, and the <b>first weights were set by hand</b> (V1 later learned new weights).' },
  'Three clues on real pictures': {
    t: 'Before any formula, just <b>look</b>: a busy scene has <b>many edges</b>, a night picture is <b>darker</b>, and a blurred picture has <b>no sharp details</b>.' },
  'SCI example 0.63': {
    t: 'To get SCI, <b>multiply each clue by its weight and add them up</b>. Here a crowded, tiny and dark scene gives <b>0.63 — a hard frame</b>.' },
  'One frame becomes one setting': {
    t: 'In the original design, a <b>harder frame</b> gets a <b>lower confidence</b> (keep weak but real boxes) and a <b>bigger input size</b> (more pixels for tiny objects). Easy frames stay fast.' },
  'Step 2: use SCI to choose settings': {
    t: 'The settings change <b>smoothly with SCI</b>: confidence and IoU slide down a little as the scene gets harder, and the input size <b>jumps up in two steps</b>.' },
  'Smart Calibrator exact settings': {
    t: 'Only <b>three detector settings</b> change every frame. The tracker settings are <b>tuned once and then frozen</b>. Do not mix the detector’s NMS IoU with the tracker’s match threshold.' },
  'Confidence threshold': { tag: 'What it means',
    t: 'The <b>confidence threshold</b> decides which boxes the detector keeps. <b>High</b> = clean but misses weak objects; <b>low</b> = finds more but lets noise in. The best line depends on the scene.' },
  'Implementation of the calibrator': {
    t: 'Two tricks keep it <b>stable and cheap</b>: <b>average the last 7 SCI readings</b>, so one odd frame changes nothing, and <b>analyse only every 10th frame</b>.' },

  /* ---------------- Section V ---------------- */
  'Choosing the test domain': { r: 1,
    t: 'To test the method we pick the <b>hardest domain: drone video</b>. Objects are tiny, and one flight goes from <b>very hard to very easy</b> scenes.' },
  'The VisDrone2019-MOT benchmark': {
    t: 'VisDrone2019-MOT is <b>Full-HD drone video</b> with objects only <b>5–30 pixels wide</b>. We <b>tune on 7 validation videos</b> and <b>test on 17 test-dev videos</b>.' },
  'Object classes evaluated': {
    t: 'We score <b>five kinds of objects</b>: pedestrian, car, van, truck and bus. Tiny bikes and tricycles are left out, because even people cannot label them clearly.' },
  'Ground-truth filtering rules': {
    t: 'Before scoring, we <b>remove labels that are too hidden or too cut off</b>. Otherwise a tracker would be punished for missing things a person can hardly see.' },
  'Evaluation protocol': {
    t: 'Every system is scored <b>in exactly the same way</b>, and the tracker <b>starts fresh on every video</b>, so one video cannot help the next.' },
  'Fair and attributable design': {
    t: 'Each system differs from the previous one in <b>exactly one part</b>. So when a score changes, we know <b>which part caused it</b>.' },

  /* ---------------- Section VI ---------------- */
  'Same frames, different control': {
    t: 'The same video frames with the same detector, <b>without and with our control</b>. Watch the hard parts: our system <b>keeps more objects tracked</b>.' },

  /* ---------------- Section VII ---------------- */
  'Step 4 result: Trial 24': {
    t: '<b>Trial 24</b> passed both rules and had the <b>highest MOTA</b> among the trials that passed — so it was <b>frozen</b> as our final setting.' },
  'Validation builds it, test judges it': { r: 1,
    t: '<b>Validation videos build the system; test videos judge it.</b> Everything is chosen on 7 validation videos; the 17 test videos are used <b>once</b>, at the end.' },
  'Stage 3: why V2': {
    t: 'V1 chased the <b>highest MOTA</b> under an ID-switch limit. V2 asks for <b>both at once</b>: more MOTA <b>and</b> fewer ID switches.' },
  'V2 Pareto front': { tag: 'What it means',
    t: 'Each dot is a setting that <b>cannot improve one goal without losing on the other</b>. Top-left is best; we picked the <b>balanced</b> point, Trial 22.' },
  'UAVDT with zero tuning': {
    t: 'We ran the frozen systems on a <b>new drone dataset without changing anything</b> — and both still <b>beat the baseline</b>.' },

  /* ---------------- Section VIII ---------------- */
  'Conclusion: what AC-MOT delivers': {
    t: 'Scenes change; fixed settings don’t. Our method <b>adapts the detector to each scene</b>, without retraining, and the gains <b>hold on unseen videos and on a new dataset</b>.' },
  'Directions for future work': {
    t: 'Every next step targets a <b>weakness we measured</b>: camera motion, a smarter input size, better appearance matching, and other detectors.' }
};
