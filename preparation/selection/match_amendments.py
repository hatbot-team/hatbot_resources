import os
from preparation.modifiers import calculate_key

__author__ = 'moskupols'

from hb_res.storage import list_storages, get_storage, FileExplanationStorage
from diff_match_patch import diff_match_patch

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
SEL_PATH = os.path.join(CUR_DIR, 'SelectedAfterMissedModifiers.asset')
OUT_PATH = os.path.join(CUR_DIR, 'SelectedWithRightKeys.asset')


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

dmp = diff_match_patch()
with FileExplanationStorage(SEL_PATH) as inp:
    with FileExplanationStorage(OUT_PATH) as out:
        out.clear()

        for sel in inp.entries():
            if sel.key in by_key:
                abused.add(sel.key)
            elif sel.text in by_text:
                abused.add(by_text[sel.text].key)
                sel.key = by_text[sel.text].key
            else:
                best = min(
                    (dmp.diff_levenshtein(dmp.diff_main(e.text, sel.text)), e)
                    for e in by_title[sel.title]
                    if e.key not in abused
                )
                if best[0] <= 12:
                    # fuzzy match
                    sel.key = best[1].key
                else:
                    # something completely new
                    sel.key = None
                    sel = calculate_key()(sel)
            out.add_entry(sel)
