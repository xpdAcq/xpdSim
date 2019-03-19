from pkg_resources import resource_filename as rs_fn
from functools import partial

from ophyd.sim import NumpySeqHandler, SynSignalRO

from xpdsim.area_det import det_factory, nsls_ii_path, xpd_wavelength, \
    det_factory_dexela
from xpdsim.build_sim_db import build_sim_db
from xpdsim.movers import shctl1, cs700, fb

import numpy as np

__version__ = "0.1.5"

pyfai_path = rs_fn("xpdsim", "data/pyfai/pyFAI_calib.yml")
pyfai_poni = rs_fn("xpdsim", "data/pyfai/test.poni")

image_file = rs_fn(
    "xpdsim",
    "data/XPD/ni/sub_20170626"
    "-150911_Ni_Tim_series_tseries_1_e910af_0250.tif",
)

sim_db_dir, db = build_sim_db()  # default is sqlite
db.reg.register_handler("NPY_SEQ", NumpySeqHandler)
# detector with 5 by 5 image -> for testing functionality
simple_pe1c = det_factory(db.reg)
# detector with full image -> for testing data reduction
xpd_pe1c = det_factory(
    db.reg,
    full_img=True,
    src_path=nsls_ii_path,
    shutter=shctl1,
    noise=np.random.poisson,
)
xpd_pe2c = det_factory(
    db.reg,
    full_img=True,
    src_path=nsls_ii_path,
    shutter=shctl1,
    noise=partial(np.random.normal, scale=100),
    name="pe2_image",
)
# synthetic ring current
ring_current = SynSignalRO(lambda: 300, name="ring_current")

dexela = det_factory_dexela(db.reg, shutter=shctl1)
