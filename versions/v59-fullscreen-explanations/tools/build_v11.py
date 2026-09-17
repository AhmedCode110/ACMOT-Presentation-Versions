#!/usr/bin/env python3
"""v11: remove every mention of the earlier seminar / old superseded results; add the fair-comparison reason
for the five classes (slide 49)."""
import os, re

ROOT = os.path.expanduser("~/Desktop/ACMOT-Presentation-Versions/versions/v11-remove-old-seminar-mentions")


def load(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def save(p, s): open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)


def rep(s, old, new, n=1):
    assert s.count(old) == n, (s.count(old), old[:90])
    return s.replace(old, new)


# ---------------- index.html ----------------
h = load("index.html")
h = rep(h, '      <div class="note">The first seminar used a 12-sequence subset (4,106 frames). All final results in this talk use the full 17-sequence test-dev split.</div>\n', '')
h = rep(h, '<p><b>Later finding:</b> the optimizer showed this NMS direction is not always right — see Section VII.</p>', '')
h = rep(h, 'This is the historical test-set comparison of the four systems.', 'This is the final test-set comparison of the four systems.')
h = rep(h, '<li>higher FPS in this historical comparison</li>', '<li>higher FPS: 36.528 → 41.957</li>')
h = rep(h, '<h3>Why exactly these five</h3><ul class="clean">',
        '<h3>Why exactly these five</h3><ul class="clean">'
        '<li><b>The reference papers on this dataset use the same classes</b>, so our comparison with them is fair.</li>')
h = rep(h, 'Tiny bikes and tricycles are too unclear even for people."',
        'Tiny bikes and tricycles are too unclear even for people. The reference papers on this dataset use the same classes, so the comparison is fair."')
# unused U2MOT setup filler script
h, n = re.subn(r"<script>\s*\(function \(\) \{\s*var t = document\.getElementById\('u2setup'\).*?</script>\n", "", h, flags=re.S)
assert n == 1
save("index.html", h)

# ---------------- script.js: drop charts that only served the old development / historical runs ----------------
j = load("script.js")
j, n = re.subn(r"  function stepBars\(h, key, o\) \{.*?\n  \}\n\n", "", j, flags=re.S); assert n == 1
a = j.index("    'dev-quality': function (h) {")
b = j.index("    /* v6: original AC-MOT ablation (separate experiment) */")
j = j[:a] + j[b:]
a = j.index("    'dev-mota-steps': function (h)"); b = j.index("\n  };", a)
j = j[:a].rstrip().rstrip(",") + j[b:]
j = rep(j, "    ['U2MOT', 'Uncertainty-aware Unsupervised Multi-Object Tracking'],\n", "")
assert not re.search(r"devAblation|D\.historical|stepBars|U2MOT", j)
save("script.js", j)

# ---------------- results.js: remove superseded data blocks ----------------
r = load("assets/data/results.js")
a = r.index("  /* Development ablation — legacy v10 evaluator"); b = r.index("  /* Original (hand-set) SCI and Smart Calibrator. */")
r = r[:a] + r[b:]
a = r.index("  /* U2MOT cross-pipeline experiment"); b = r.index("};", a)
r = r[:a].rstrip().rstrip(",") + "\n" + r[b:]
r = rep(r, "/* ---------------- added for v2 (content of the original seminar deck) ---------------- */\n\n", "")
r = rep(r, "/* Published values collected in the IEEE ICMISI 2026 survey, as shown in the seminar deck. */",
        "/* Published values collected in the IEEE ICMISI 2026 survey. */")
a = r.index("/* Real cue calibration from FROZEN_DEFENSIBLE_ACMOT_CONFIG.json"); b = r.index("};", a) + 3
r = r[:a] + r[b:].lstrip("\n")
a = r.index("/* Step-by-step differences, computed from devAblation"); b = r.index("})();", a) + 6
r = r[:a] + r[b:]
r = rep(r, "/* Final live run density (VERIFICATION_REPORT.md", "/* Test-dev density (VERIFICATION_REPORT.md")
assert not re.search(r"seminar|devAblation|historical|u2mot|U2MOT|calibration", r, re.I), "leftover"
save("assets/data/results.js", r.rstrip() + "\n")

# ---------------- meaning.js: drop texts of slides that no longer exist; fix one wrong sentence ----------------
m = load("assets/data/meaning.js")
titles = set(re.findall(r'<section class="slide"[^>]*data-title="([^"]*)"', h))
entry = re.compile(r"^  '([^']+)'\s*:\s*\{.*?\}\s*,?[ \t]*\n", re.M | re.S)
removed = [k for k in entry.findall(m) if k not in titles]
m = entry.sub(lambda mo: mo.group(0) if mo.group(1) in titles else "", m)
m = re.sub(r",(\s*(?:/\*[^*]*\*/\s*)*)\};\s*$", r"\1};\n", m)
m = rep(m, "the <b>limits and weights were our first guess</b>, later replaced by learned values.",
        "the <b>limits are our own design constants</b>, and the <b>first weights were set by hand</b> (V1 later learned new weights).")
assert not re.search(r"U2MOT|official scoring|HOTA\*|seminar", m)
save("assets/data/meaning.js", m)
print("ok · removed meaning entries:", len(removed))
