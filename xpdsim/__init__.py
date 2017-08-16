import numpy as np
import bluesky.examples as be

from xpdsim.build_db import build_pymongo_backed_broker
from xpdsim.movers import shctl1, cs700
from xpdsim.dets import SimpleSimulatedPE1C

db = build_pymongo_backed_broker()
db.fs.register_handler('RWFS_NPY', be.ReaderWithRegistryHandler)
simple_pe1c = SimpleSimulatedPE1C('pe1c', {'pe1_image':
                                           lambda: np.ones((5, 5))},
                                  reg=db.fs)
