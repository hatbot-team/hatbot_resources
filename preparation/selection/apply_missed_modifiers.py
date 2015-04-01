__author__ = 'moskupols'

import os

from hb_res.storage import get_storage, FileExplanationStorage
from preparation import modifiers
from preparation.resources.Resource import gen_resource, applied_modifiers

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(CUR_DIR, 'Selected.asset')
OUTPUT_PATH = os.path.join(CUR_DIR, 'SelectedAfterMissedModifiers.asset')

missed_modifiers = [
    modifiers.str_replace('p', 'р'),
    modifiers.re_replace(r'\s+', ' '),
    modifiers.re_replace(r'([,:])(?=[^ ])', r'\1 '),
    modifiers.str_replace(r' :', ':'),
    modifiers.str_replace(r' ,', ','),
]

with FileExplanationStorage(INPUT_PATH) as inp:
    PatchedResource = gen_resource('SelectedResource', missed_modifiers)(inp.entries)
    with FileExplanationStorage(OUTPUT_PATH) as outp:
        outp.clear()
        for e in applied_modifiers(PatchedResource()):
            outp.add_entry(e)

    from preparation.tools.show_evolution import print_evolution
    print_evolution(resource=PatchedResource(), title='анекдот')
