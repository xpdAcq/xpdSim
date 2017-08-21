import numpy as np
import bluesky.examples as be

from xpdsim.build_db import build_db_wrapper
from xpdsim.movers import shctl1, cs700
from xpdsim.dets import SimulatedPE1C

db = build_db_wrapper() # default is mongo. build sqlite one by
                        # specific imports
simple_pe1c = SimulatedPE1C('pe1c', {'pe1_image':lambda: np.ones((5, 5))},
                            reg=db.reg)
