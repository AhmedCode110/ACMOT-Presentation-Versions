from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
dest = ROOT / 'versions/v52-detection-tracking-metrics/index.html'
text = dest.read_text(encoding='utf-8')
anchor = 'data-title="Applications"'
anchor_pos = text.find(anchor)
assert anchor_pos >= 0
start = text.rfind('<section', 0, anchor_pos)
assert start >= 0
end = text.find('</section>', start) + len('</section>')
assert end > start

slides = '''

<section class="slide" data-sec="1" data-secname="I · Introduction" data-title="Detection and tracking together">
  <header class="s-head"><div class="kicker">Section I · Core idea</div><h2>Detection Finds Objects; Tracking Keeps Their IDs</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>Detection answers <b>what is in one frame</b>. Tracking links those detections across frames so each object keeps the same ID.</p></div>
    <div class="g2 grow" style="gap:22px">
      <div class="card sec col"><div class="tag">Detection · one frame</div><div class="img zoomable" style="height:300px"><img data-src="assets/figures/image2.png" alt="Detection boxes on one frame"></div><p><b>Input:</b> one frame</p><p><b>Output:</b> boxes, class labels, and confidence scores</p></div>
      <div class="card sec col"><div class="tag">Tracking · many frames</div><div class="img zoomable" style="height:300px"><img data-src="assets/figures/image3.png" alt="Tracking an object over time"></div><p><b>Input:</b> detections over time</p><p><b>Output:</b> one stable ID for each object</p></div>
    </div>
    <div class="flow"><div class="node io">Frame</div><div class="arr"></div><div class="node hot">Detector</div><div class="arr"></div><div class="node io">Boxes</div><div class="arr"></div><div class="node hot">Tracker</div><div class="arr"></div><div class="node good">IDs over time</div></div>
  </div>
  <footer class="s-foot"><span class="prov p-illus">Concept explanation · example images from the presentation assets</span></footer>
  <aside class="notes"><p><b>Say:</b> "Detection finds objects in one frame. Tracking takes these boxes over time and keeps the identity of each object. AC-MOT controls the detector, while ByteTrack keeps the IDs."</p></aside>
</section>

<section class="slide" data-sec="1" data-secname="I · Introduction" data-title="Tracking metrics summary">
  <header class="s-head"><div class="kicker">Section I · Evaluation metrics</div><h2>Tracking Metrics: What Each One Tells Us</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>No single metric is enough. We report quality, identity, detection errors, and speed together.</p></div>
    <div class="g3 grow" style="gap:18px">
      <div class="card sec"><div class="tag">Overall quality</div><h3>MOTA</h3><p>How well the system detects and tracks objects overall.</p><p class="strong">Higher is better.</p></div>
      <div class="card sec"><div class="tag">Identity quality</div><h3>IDF1</h3><p>How well the system keeps the correct object identity.</p><p class="strong">Higher is better.</p></div>
      <div class="card sec"><div class="tag">Balanced tracking</div><h3>HOTA</h3><p>Balances finding objects with linking the right IDs.</p><p class="strong">Higher is better.</p></div>
    </div>
    <div class="g2" style="gap:18px">
      <div class="card"><h3>Identity and detection errors</h3><p><b>IDS:</b> identity switches · <b>FP:</b> false boxes · <b>FN:</b> missed objects</p><p class="strong">For IDS, FP, and FN, lower is better.</p></div>
      <div class="card"><h3>Speed</h3><p><b>FPS</b> means frames per second. It shows whether the system can run fast enough for live video.</p><p class="strong">Higher is better.</p></div>
    </div>
  </div>
  <footer class="s-foot"><span class="prov p-val">Metric definitions used in all AC-MOT evaluations</span></footer>
  <aside class="notes"><p><b>Say:</b> "We use several metrics because they answer different questions. MOTA measures overall quality, IDF1 measures identity, HOTA balances detection and association, IDS counts identity switches, and FPS measures speed."</p></aside>
</section>'''
text = text[:end] + slides + text[end:]
dest.write_text(text, encoding='utf-8')
print('Built v52 with two introduction slides')
