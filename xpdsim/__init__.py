from cycler import cycler
from functools import partial
from pkg_resources import resource_filename as rs_fn

from ophyd.sim import NumpySeqHandler, SynSignalRO

from xpdsim.area_det import det_factory, nsls_ii_path, xpd_wavelength, \
    img_gen, build_image_cycle, DEXELA_IMG_SIZE, BLACKFLY_IMG_SIZE
from xpdsim.build_sim_db import build_sim_db
from xpdsim.movers import shctl1, cs700, fb

import numpy as np

__version__ = '0.4.0'

pyfai_path = rs_fn("xpdsim", "data/pyfai/pyFAI_calib.yml")
pyfai_poni = rs_fn("xpdsim", "data/pyfai/test.poni")

image_file = rs_fn(
    "xpdsim",
    "data/XPD/ni/sub_20170626"
    "-150911_Ni_Tim_series_tseries_1_e910af_0250.tif",
)

#sim_db_dir, db = build_sim_db()  # default is sqlite
#db.reg.register_handler("NPY_SEQ", NumpySeqHandler)

# simple detector that outputs 5 by 5 noisy images
simple_pe1c = det_factory()
# detector with real images
xpd_pe1c = det_factory(build_image_cycle(nsls_ii_path),
                       data_key="pe1_image",
                       shutter=shctl1,
                       noise=np.random.poisson)
xpd_pe2c = det_factory(build_image_cycle(nsls_ii_path, 'pe2_image'),
                       data_key="pe2_image",
                       shutter=shctl1,
                       noise=partial(np.random.normal, scale=100),
                       )
# other detectors
dexela = det_factory(data_key='dexela_image',
                     shutter=shctl1,
                     size=DEXELA_IMG_SIZE,
                     )
blackfly = det_factory(data_key='blackfly_det_image',
                       shutter=shctl1,
                       size=BLACKFLY_IMG_SIZE)
# this reports just ones, similar to a flat field
cycle = cycler("blackfly_det_image",
               [np.ones(BLACKFLY_IMG_SIZE)])
blackfly_full_field = det_factory(cycle,
                                  data_key='blackfly_det_image',
                                  shutter=shctl1,
                                  size=BLACKFLY_IMG_SIZE)
# synthetic ring current
ring_current = SynSignalRO(lambda: 300, name="ring_current")

