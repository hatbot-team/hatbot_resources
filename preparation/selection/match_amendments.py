import os

__author__ = 'moskupols'

from hb_res.storage import list_storages, get_storage, FileExplanationStorage
from pprint import pprint
from diff_match_patch import diff_match_patch

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
SEL_PATH = os.path.join(CUR_DIR, 'SelectedAfterMissedModifiers.asset')


all_expls = []
by_key = {}
by_text = {}
by_title = {}

for trunk in list_storages():
    with get_storage(trunk) as stor:
        for expl in stor.entries():
            expl.trunk = trunk
            all_expls.append(expl)
            by_key[expl.key] = expl
            by_text[expl.text] = expl
            by_title.setdefault(expl.title, []).append(expl)

abused = set()

matched_by_key = 0
matched_by_text = 0

dmp = diff_match_patch()
fuzzies = []

with FileExplanationStorage(SEL_PATH) as inp:
    for sel in inp.entries():
        if sel.key in by_key:
            abused.add(sel.key)
            matched_by_key += 1
        elif sel.text in by_text:
            abused.add(by_text[sel.text].key)
            matched_by_text += 1
        else:
            best = min(
                (dmp.diff_levenshtein(dmp.diff_main(e.text, sel.text)), e)
                for e in by_title[sel.title]
                if e.key not in abused
            )
            fuzzies.append((best, sel))

print('matched by key', matched_by_key)
print('matched by text', matched_by_text)

fuzzies.sort()
pprint([(dist, b.title, b.text, sel.text) for (dist, b), sel in fuzzies])
