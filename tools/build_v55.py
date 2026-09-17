from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'versions/v55-journal-target-options/index.html'
text = path.read_text(encoding='utf-8')

old = '''    <div class="callout" style="border-left-color:#4F46E5"><b>5 · Journal publication:</b> prepare an extended paper on AC-MOT for journal submission. The target journal and submission date will be chosen after supervisor review.</div>'''
new = '''    <div class="callout" style="border-left-color:#4F46E5;font-size:22px"><b>5 · Journal publication:</b> prepare an extended paper on AC-MOT for submission.<br><b>Target options to review with the supervisors:</b> Journal of Real-Time Image Processing · Image and Vision Computing · IEEE Access.<br><span class="muted">Status: no journal selected and no paper submitted yet. Final choice follows supervisor review; check scope, APC, and author rules.</span></div>'''
assert text.count(old) == 1
text = text.replace(old, new, 1)

old_note = '''<aside class="notes"><p><b>Say:</b> "The most useful next step is to combine image detections with radar position and speed. Radar can help when an object is hidden, blurry, or affected by camera motion. We can also improve ReID and test the same SCI idea with other detectors and datasets. Finally, we plan to prepare an extended journal paper. The journal choice and submission will follow supervisor review."</p></aside>'''
new_note = '''<aside class="notes"><p><b>Say:</b> "The most useful next step is to combine image detections with radar position and speed. Radar can help when an object is hidden, blurry, or affected by camera motion. We can also improve ReID and test the same SCI idea with other detectors and datasets. For publication, the closest options are Journal of Real-Time Image Processing and Image and Vision Computing. IEEE Access is a broader practical option, but its open-access cost must be checked. No journal has been selected and no paper has been submitted yet; the final choice follows supervisor review."</p></aside>'''
assert text.count(old_note) == 1
text = text.replace(old_note, new_note, 1)

path.write_text(text, encoding='utf-8')
print('Built v55 journal target options')
