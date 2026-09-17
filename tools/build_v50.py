from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / 'versions/v50-short-20-minute-department-talk/index.html'
text = src.read_text(encoding='utf-8')

# Keep only the top-level main slides. Explanation pages under xstage stay intact.
marker = '<div class="overlay xview" id="xview"'
assert marker in text, 'xstage marker not found'
main, tail = text.split(marker, 1)

selected = {
    'Title', 'Outline',
    'The main question', 'The baseline',
    'What we add', 'Three cues on real pictures',
    'SCI from frame to score', 'Smart Calibrator exact settings',
    'The VisDrone2019-MOT benchmark', 'Ablation result',
    'Pre-Optuna screening', 'Temporal screening before V1',
    'Step 4 result: Trial 24', 'V1 on the test set',
    'Stage 3: why V2', 'V2 on the test set', 'V1 or V2',
    'Paired bootstrap', 'UAVDT with zero tuning',
    'U2MOT reproduction', 'SCI recalibration for U2MOT',
    'U2MOT AC-MOT controller', 'U2MOT final test',
    'The story in one line', 'Main contributions',
    'Conclusion: what AC-MOT delivers', 'Directions for future work',
    'Thank you',
}

tag_re = re.compile(r'<(/?)section\b[^>]*>', re.I)
top_sections = []
depth = 0
start = None
for m in tag_re.finditer(main):
    if not m.group(1):
        if depth == 0:
            start = m.start()
        depth += 1
    else:
        depth -= 1
        if depth == 0 and start is not None:
            block = main[start:m.end()]
            tm = re.search(r'data-title="([^"]+)"', block)
            title = tm.group(1) if tm else ''
            if title in selected:
                top_sections.append(block)
            start = None
if len(top_sections) != len(selected):
    kept_titles = {re.search(r'data-title="([^"]+)"', b).group(1) for b in top_sections}
    print('Missing selected titles:', sorted(selected - kept_titles))
    raise AssertionError((len(top_sections), len(selected)))

new_main = main[:main.find('<section')] + '\n\n'.join(top_sections) + '\n\n'
new_text = new_main + marker + tail

# Keep outline jumps working even though section divider slides are removed.
for sec_value, target_id in [('3', 'sec-3'), ('4', 'sec-4'), ('5', 'sec-5'),
                             ('7', 'sec-6'), ('6', 'sec-7'), ('8', 'sec-8'),
                             ('9', 'sec-9'), ('10', 'sec-10')]:
    pattern = rf'(<section\b(?![^>]*\bid=)[^>]*data-sec="{sec_value}"[^>]*)>'
    new_text, n = re.subn(pattern, rf'\1 id="{target_id}">', new_text, count=1)
    assert n == 1, (sec_value, target_id, n)

# Replace the old long outline with a short roadmap matching the retained slides.
outline_start = new_text.find('<div class="ol-ppt">')
assert outline_start >= 0
depth = 0
end = None
for m in re.finditer(r'</?div\b[^>]*>', new_text[outline_start:], re.I):
    if not m.group(0).startswith('</'):
        depth += 1
    else:
        depth -= 1
        if depth == 0:
            end = outline_start + m.end()
            break
assert end
rows = '''<div class="ol-ppt">
      <button class="ol-row" data-goto="sec-3"><span class="n">I</span><span class="t"><h3>Problem and baseline</h3><p>Why one fixed detector setting is limited</p></span></button>
      <button class="ol-row" data-goto="sec-4"><span class="n">II</span><span class="t"><h3>AC-MOT method</h3><p>Measure the scene, score it, and adapt the detector</p></span></button>
      <button class="ol-row" data-goto="sec-5"><span class="n">III</span><span class="t"><h3>Data and first result</h3><p>VisDrone2019-MOT and the component study</p></span></button>
      <button class="ol-row" data-goto="sec-6"><span class="n">IV</span><span class="t"><h3>V1: validation-driven search</h3><p>Screening, temporal settings, Optuna, and the test result</p></span></button>
      <button class="ol-row" data-goto="sec-7"><span class="n">V</span><span class="t"><h3>V2: quality and identity trade-off</h3><p>Multi-objective search and the final choice</p></span></button>
      <button class="ol-row" data-goto="sec-8"><span class="n">VI</span><span class="t"><h3>Statistical and external checks</h3><p>Paired bootstrap and zero-tuning UAVDT</p></span></button>
      <button class="ol-row" data-goto="sec-9"><span class="n">VII</span><span class="t"><h3>Transfer to U2MOT</h3><p>Independent reproduction, recalibration, and final test</p></span></button>
      <button class="ol-row" data-goto="sec-10"><span class="n">VIII</span><span class="t"><h3>Conclusion</h3><p>What was delivered and what comes next</p></span></button>
    </div>'''
new_text = new_text[:outline_start] + rows + new_text[end:]

# Update the outline note and title so the time limit is explicit.
new_text = new_text.replace('<h2>Outline</h2>', '<h2>Short presentation roadmap</h2>', 1)
new_text = new_text.replace('The story goes in the order the work happened: the problem and the baseline, the first heuristic design and its ablation, V1, V2, and finally the statistics and UAVDT.', 'This short talk covers the full project story in about 20 minutes: problem, method, search, results, checks, transfer, and conclusion.', 1)
new_text = new_text.replace('AC-MOT — Real-Time Object Detection and Tracking (v9)', 'AC-MOT — Real-Time Object Detection and Tracking (v50 short talk)')
# Remove long-deck slide references from the retained method overview.
new_text = re.sub(r'<p class="muted" style="margin-top:auto;font-size:21px;font-weight:700">details: slides [^<]+</p>', '', new_text)
src.write_text(new_text, encoding='utf-8')
print(f'Built v50 with {len(top_sections)} main slides')
