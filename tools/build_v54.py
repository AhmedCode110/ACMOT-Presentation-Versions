from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'versions/v54-journal-publication-future-work/index.html'
text = path.read_text(encoding='utf-8')

old = '''    <div class="note"><b>Note:</b> these ideas come from what we measured, not from guesses.</div>'''
new = '''    <div class="callout" style="border-left-color:#4F46E5"><b>5 · Journal publication:</b> prepare an extended paper on AC-MOT for journal submission. The target journal and submission date will be chosen after supervisor review.</div>
    <div class="note"><b>Note:</b> these ideas come from what we measured, not from guesses.</div>'''
assert text.count(old) == 1
text = text.replace(old, new, 1)

old_note = '''<aside class="notes"><p><b>Say:</b> "The most useful next step is to combine image detections with radar position and speed. Radar can help when an object is hidden, blurry, or affected by camera motion. We can also improve ReID and test the same SCI idea with other detectors and datasets."</p></aside>'''
new_note = '''<aside class="notes"><p><b>Say:</b> "The most useful next step is to combine image detections with radar position and speed. Radar can help when an object is hidden, blurry, or affected by camera motion. We can also improve ReID and test the same SCI idea with other detectors and datasets. Finally, we plan to prepare an extended journal paper. The journal choice and submission will follow supervisor review."</p></aside>'''
assert text.count(old_note) == 1
text = text.replace(old_note, new_note, 1)

path.write_text(text, encoding='utf-8')
print('Built v54 journal publication future-work item')
