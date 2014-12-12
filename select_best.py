#!/usr/bin/env python3

import sys
from hb_res.storage import get_storage


name = sys.argv[1]
count = int(sys.argv[2]) if len(sys.argv) >= 3 else 500

with get_storage(name) as stor:
    good = sorted(stor.entries(), key=lambda e: e.prior_rating, reverse=True)[:count]

for e in good:
    print(e)
