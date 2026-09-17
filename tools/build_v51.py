from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
dest = ROOT / 'versions/v51-intro-literature-motivation/index.html'
old = ROOT / 'versions/v49-fast-media-loading/index.html'
text = dest.read_text(encoding='utf-8')
source = old.read_text(encoding='utf-8')

def top_level_sections(html):
    marker = '<div class="overlay xview"'
    main = html.split(marker, 1)[0]
    tag_re = re.compile(r'<(/?)section\b[^>]*>', re.I)
    found, depth, start = [], 0, None
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
                found.append((tm.group(1) if tm else '', block))
                start = None
    return found

source_blocks = dict(top_level_sections(source))
assert all(k in source_blocks for k in ['Applications', 'Detector benchmark comparison', 'Conclusions of the survey'])

main, tail = text.split('<div class="overlay xview"', 1)
insert_at = main.find('<section', main.find('data-title="Outline"'))
assert insert_at >= 0
intro = source_blocks['Applications'].replace('<section class="slide" data-sec="1"', '<section class="slide" id="sec-1" data-sec="1"', 1)
survey = source_blocks['Detector benchmark comparison']
survey_conclusion = source_blocks['Conclusions of the survey']
main = main[:insert_at] + intro + '\n\n' + survey + '\n\n' + survey_conclusion + '\n\n' + main[insert_at:]
new_text = main + '<div class="overlay xview"' + tail

# Make the short outline reflect the added opening story.
start = new_text.find('<div class="ol-ppt">')
assert start >= 0
depth, end = 0, None
for m in re.finditer(r'</?div\b[^>]*>', new_text[start:], re.I):
    depth += -1 if m.group(0).startswith('</') else 1
    if depth == 0:
        end = start + m.end()
        break
assert end
rows = '''<div class="ol-ppt">
      <button class="ol-row" data-goto="sec-1"><span class="n">I</span><span class="t"><h3>Introduction and literature survey</h3><p>Why the problem matters and what the survey showed</p></span></button>
      <button class="ol-row" data-goto="sec-3"><span class="n">II</span><span class="t"><h3>Problem and baseline</h3><p>Why one fixed detector setting is limited</p></span></button>
      <button class="ol-row" data-goto="sec-4"><span class="n">III</span><span class="t"><h3>AC-MOT method</h3><p>Measure the scene, score it, and adapt the detector</p></span></button>
      <button class="ol-row" data-goto="sec-5"><span class="n">IV</span><span class="t"><h3>Data and first result</h3><p>VisDrone2019-MOT and the component study</p></span></button>
      <button class="ol-row" data-goto="sec-6"><span class="n">V</span><span class="t"><h3>V1: validation-driven search</h3><p>Screening, temporal settings, Optuna, and the test result</p></span></button>
      <button class="ol-row" data-goto="sec-7"><span class="n">VI</span><span class="t"><h3>V2: quality and identity trade-off</h3><p>Multi-objective search and the final choice</p></span></button>
      <button class="ol-row" data-goto="sec-8"><span class="n">VII</span><span class="t"><h3>Statistical and external checks</h3><p>Paired bootstrap and zero-tuning UAVDT</p></span></button>
      <button class="ol-row" data-goto="sec-9"><span class="n">VIII</span><span class="t"><h3>Transfer to U2MOT</h3><p>Independent reproduction, recalibration, and final test</p></span></button>
      <button class="ol-row" data-goto="sec-10"><span class="n">IX</span><span class="t"><h3>Conclusion</h3><p>What was delivered and what comes next</p></span></button>
    </div>'''
new_text = new_text[:start] + rows + new_text[end:]

# The original method overview is too dense for the short talk. Keep the science,
# but present the three actions and the unchanged tracker in a simpler layout.
method = '''<section class="slide" data-sec="4" data-secname="IV · AC-MOT" data-title="What we add">
  <header class="s-head"><div class="kicker">Section IV · The idea</div><h2>What AC-MOT Adds</h2></header>
  <div class="s-body col">
    <div class="meaning"><div class="tag">The main idea</div><p>AC-MOT measures scene difficulty before detection, turns it into one score, and chooses detector settings for that scene.</p></div>
    <div class="g3 grow" style="gap:18px">
      <div class="card sec"><div class="tag">1 · Measure</div><h3>Scene Analyzer</h3><p>It uses five low-cost cues from the last boxes and a small gray image.</p><p class="strong">Output: five cue values</p></div>
      <div class="card sec"><div class="tag">2 · Score</div><h3>Scene Complexity Index</h3><p>The five cues are mixed into one score from <b>0 = easy</b> to <b>1 = hard</b>.</p><p class="strong">Output: one SCI score</p></div>
      <div class="card sec"><div class="tag">3 · Set</div><h3>Smart Calibrator</h3><p>The score selects confidence, NMS IoU, and input size.</p><p class="strong">Output: detector settings</p></div>
    </div>
    <div class="flow"><div class="node fx">YOLOv8n detector</div><div class="arr"></div><div class="node good">ByteTrack stays fixed</div><div class="arr"></div><div class="node io">Fair comparison</div></div>
  </div>
  <footer class="s-foot"><span class="prov p-val">AC-MOT method · scene-based detector control</span></footer>
  <aside class="notes"><p><b>Say:</b> "AC-MOT adds three steps before detection. It measures the scene, makes one SCI score, and selects detector settings. YOLOv8n and ByteTrack remain the same, so later gains come from the control method."</p></aside>
</section>'''
new_text, n = re.subn(r'<section\b[^>]*data-title="What we add"[^>]*>.*?</section>', method, new_text, count=1, flags=re.S)
assert n == 1
new_text = new_text.replace('<h2>Short presentation roadmap</h2>', '<h2>Short presentation roadmap</h2>', 1)
new_text = new_text.replace('This short talk covers the full project story in about 20 minutes: problem, method, search, results, checks, transfer, and conclusion.', 'This short talk covers the full story in about 20 minutes: motivation, literature survey, problem, method, results, checks, transfer, and conclusion.', 1)
dest.write_text(new_text, encoding='utf-8')
print('Built v51 with 31 main slides')
