#!/usr/bin/env python3
"""v22 (from v21): the "TP, FP, FN and TN" slide follows the layout and wording of slide 10 of the Keynote
seminar deck (b9_claude): two example pictures (false positive IoU 0.22, false negative IoU 0.00),
three coloured definition cards (TP, FP, FN), the bird NOTE and a separate TN box."""
import os

P = os.path.expanduser("~/Desktop/ACMOT-Presentation-Versions/versions/v22-tp-fp-slide-like-keynote/index.html")
h = open(P, encoding="utf-8").read()

i = h.index('data-title="TP, FP, FN and TN"')
a = h.rindex('<section', 0, i)
b = h.index('</section>', i) + len('</section>')

new = '''<section class="slide" data-sec="1" data-secname="I · Introduction" data-title="TP, FP, FN and TN" data-explain="x-iou#2|When Is a Box Correct?" data-nostrip>
  <header class="s-head"><div class="kicker">Section I · Evaluation metrics</div><h2>TP, FP, FN and TN: Detection Outcomes</h2></header>
  <div class="s-body col" style="gap:16px">
    <div class="row grow" style="gap:20px">
      <div class="card col" style="flex:1 1 0;min-width:0;gap:8px;padding:12px 14px">
        <div class="img contain zoomable grow" style="background:#fff"><img data-src="assets/figures/image13.jpeg" alt="False positive, IoU 0.22"></div>
        <p class="tc" style="font-size:22px;margin:0"><b class="bad">FALSE POSITIVE:</b> a detection in the wrong location (IoU 0.22).</p></div>
      <div class="card col" style="flex:1 1 0;min-width:0;gap:8px;padding:12px 14px">
        <div class="img contain zoomable grow" style="background:#fff"><img data-src="assets/figures/image14.jpeg" alt="False negative, IoU 0.00"></div>
        <p class="tc" style="font-size:22px;margin:0"><b style="color:#B45309">FALSE NEGATIVE:</b> the object is present but was not reported.</p></div>
      <div class="col" style="flex:0 0 520px;gap:12px">
        <div class="card col" style="flex:1;gap:4px;padding:12px 20px;border-left:8px solid #15803D"><h3 style="color:#15803D;margin:0">TP — True Positive</h3><p style="color:#166534;font-size:26px">A real object was detected correctly.</p></div>
        <div class="card col" style="flex:1;gap:4px;padding:12px 20px;border-left:8px solid #B91C1C"><h3 style="color:#B91C1C;margin:0">FP — False Positive</h3><p style="color:#991B1B;font-size:26px">The detector reported an object that was not really there.</p></div>
        <div class="card col" style="flex:1;gap:4px;padding:12px 20px;border-left:8px solid #B45309"><h3 style="color:#B45309;margin:0">FN — False Negative</h3><p style="color:#92400E;font-size:26px">A real object was present, but the detector missed it.</p></div>
      </div>
    </div>
    <div class="note" style="font-size:26px;padding:14px 22px;border-left-width:8px"><b>NOTE:</b> There is a real bird in the image. <b class="good">Box it correctly</b> and it is a <b>TP</b>. <b class="bad">Box empty background</b> and it is a <b>FP</b>. <b style="color:#B45309">Miss the bird</b> and it is a <b>FN</b>.</div>
    <div class="card flat" style="padding:12px 22px;font-size:26px;border:2px solid #CBD5E1"><b>TN — True Negative:</b> no object was present, and the detector correctly reported nothing.</div>
  </div>
  <aside class="notes"><p><b>Say:</b> "Every detection result is one of four outcomes. TP: a real object detected correctly. FP: the detector reported an object that was not really there — like the left picture, where the box is in the wrong place with IoU 0.22. FN: a real object was present but missed — the right picture, where the bird has no correct box. TN: nothing was there, and the detector correctly reported nothing."</p><p><b>Simple example:</b> "There is a real bird. Box it correctly: TP. Box empty background: FP. Miss the bird: FN."</p><p><b>If asked:</b> "A box counts as correct when its IoU with the real object is at least 0.5 — that is the α = 0.5 written on the pictures."</p></aside>
</section>'''

h = h[:a] + new + h[b:]
assert h.count('data-title="TP, FP, FN and TN"') == 1
# AP / mAP slide: say what AP shows first, then that it is one score for one class
old_ap = '<p><b>AP</b> is one score for <b>one class</b>, for example “car”: how precise the detector stays while it finds more and more cars. <b>mAP</b> is the <b>average AP over all classes</b>.</p>'
new_ap = '<p><b>AP</b> shows <b>how precise the detector stays while it finds more and more objects</b>. AP is one score for <b>one class</b>, for example “car”. <b>mAP</b> is the <b>average AP over all classes</b>.</p>'
assert h.count(old_ap) == 1
h = h.replace(old_ap, new_ap)
open(P, "w", encoding="utf-8").write(h)
print("ok")
