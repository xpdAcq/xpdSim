import numpy as np
import bluesky.examples as be

from xpdsim.build_sim_db import build_sim_db
from xpdsim.movers import shctl1, cs700
from xpdsim.dets import *

db = build_sim_db() # default is sqlite
db.reg.register_handler('RWFS_NPY', be.ReaderWithRegistryHandler)
simple_pe1c = SimulatedPE1C('pe1c', {'pe1_image':lambda: np.ones((5, 5))},
                            reg=db.reg)
# advanced detector
xpd_pe1c = det_factory('pe1c', db.reg, nsls_ii_path, shutter=shctl1)

