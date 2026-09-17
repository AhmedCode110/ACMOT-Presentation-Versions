from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'versions/v53-radar-future-work-no-retraining/index.html'
text = path.read_text(encoding='utf-8')

old_contribution = '''<b>Adaptive detector-side control</b> according to scene difficulty.'''
new_contribution = '''<b>Adaptive detector-side control</b> according to scene difficulty.<br><span class="muted" style="font-size:25px">It needs no retraining and no new training data.</span>'''
assert text.count(old_contribution) == 1
text = text.replace(old_contribution, new_contribution, 1)

old_future = '''      <div class="card" style="border-left:6px solid #2563EB"><h3>2 · Density-gated input size</h3><p>Raise the input size only when many tiny objects are present, not on SCI alone.</p></div>
      <div class="card" style="border-left:6px solid #7C3AED"><h3>3 · A proper deep ReID</h3><p>Replace the colour histogram with a small deep appearance model that stays real-time.</p></div>
      <div class="card" style="border-left:6px solid #B45309"><h3>4 · SCI beyond YOLO</h3><p>Drive RT-DETR or DINO with the same signal, and test on AU-AIR.</p></div>'''
new_future = '''      <div class="card" style="border-left:6px solid #0891B2"><h3>2 · Radar-assisted tracking</h3><p>Fuse radar position and speed with image detections. This can help keep IDs during occlusion, blur, and camera motion.</p></div>
      <div class="card" style="border-left:6px solid #7C3AED"><h3>3 · A proper deep ReID</h3><p>Replace the colour histogram with a small deep appearance model that stays real-time.</p></div>
      <div class="card" style="border-left:6px solid #B45309"><h3>4 · SCI beyond YOLO</h3><p>Drive RT-DETR or DINO with the same signal, and test on AU-AIR.</p></div>'''
assert text.count(old_future) == 1
text = text.replace(old_future, new_future, 1)

old_note = '''<aside class="notes"><p><b>Say:</b> "Next: camera-motion help, smarter input size, a better ReID, and other detectors and datasets."</p></aside>'''
new_note = '''<aside class="notes"><p><b>Say:</b> "The most useful next step is to combine image detections with radar position and speed. Radar can help when an object is hidden, blurry, or affected by camera motion. We can also improve ReID and test the same SCI idea with other detectors and datasets."</p></aside>'''
assert text.count(old_note) == 1
text = text.replace(old_note, new_note, 1)

old_names = 'Ahmed Gouda Ismail · Mohamed S. Mohamed · Tarek Ahmed Mahmoud'
new_names = 'Ahmed Gouda Ismail · Dr. Tarek Ahmed Mahmoud · Dr. Mohamed S. Mohamed'
assert text.count(old_names) == 1
text = text.replace(old_names, new_names, 1)

path.write_text(text, encoding='utf-8')
print('Built v53 updates')
