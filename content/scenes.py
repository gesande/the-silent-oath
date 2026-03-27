# ============================================================
#  content/scenes.py
#  Aggregates all act scene dictionaries into one SCENES dict.
#  Add new acts here as they are implemented.
# ============================================================

from content.act1 import SCENES as _ACT1
from content.act2 import SCENES as _ACT2

SCENES = {**_ACT1, **_ACT2}
