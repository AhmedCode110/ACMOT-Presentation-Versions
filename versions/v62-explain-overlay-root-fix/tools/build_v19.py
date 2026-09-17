#!/usr/bin/env python3
"""v19 (from v18): make the deck load fast when it is served from the web.

The four videos (47 MB) started downloading as soon as the page opened, which blocked
script.js on GitHub Pages and left the deck stuck on a blank screen. With preload="none"
a video is fetched only when it is actually played; posters and everything else are unchanged."""
import os, re

P = os.path.expanduser("~/Desktop/ACMOT-Presentation-Versions/versions/v19-web-friendly-media/index.html")
h = open(P, encoding="utf-8").read()

vids = re.findall(r'<video[^>]*>', h)
assert len(vids) == 4, len(vids)

h = h.replace(' preload="metadata"', ' preload="none"')


def add_preload(m):
    tag = m.group(0)
    return tag if 'preload=' in tag else tag[:-1] + ' preload="none">'


h, n = re.subn(r'<video[^>]*>', add_preload, h)
assert n == 4
assert h.count('preload="none"') == 4 and 'preload="metadata"' not in h
open(P, "w", encoding="utf-8").write(h)
print("ok · videos with preload=none:", h.count('preload="none"'))
