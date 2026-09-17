from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'versions/v56-clean-footer-radar-2/index.html'
text = path.read_text(encoding='utf-8')

# Remove source/provenance labels while leaving slide numbers and explanation buttons.
text, removed = re.subn(r'\s*<span class="prov\b[^>]*>.*?</span>', '', text, flags=re.S)
assert removed > 0

# Keep the future-work numbering and remove the status sentence as requested.
status = '<span class="muted">Status: no journal selected and no paper submitted yet. Final choice follows supervisor review; check scope, APC, and author rules.</span>'
assert text.count(status) == 1
text = text.replace(status, '', 1)

path.write_text(text, encoding='utf-8')
print(f'Built v56: removed {removed} provenance labels')
