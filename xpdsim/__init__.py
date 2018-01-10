from pkg_resources import resource_filename as rs_fn

from ophyd.sim import (NumpySeqHandler,
                       SynSignalRO)

from xpdsim.area_det import det_factory, nsls_ii_path, xpd_wavelength
from xpdsim.build_sim_db import build_sim_db
from xpdsim.movers import shctl1, cs700

__version__ = '0.1.1'

pyfai_path = rs_fn('xpdsim', 'data/pyfai/pyFAI_calib.yml')


sim_db_dir, db = build_sim_db()  # default is sqlite
db.reg.register_handler('NPY_SEQ', NumpySeqHandler)
# detector with 5 by 5 image -> for testing functionality
simple_pe1c = det_factory(db.reg)
# detector with full image -> for testing data reduction
xpd_pe1c = det_factory(db.reg, full_img=True,
                       src_path=nsls_ii_path)
# synthetic ring current
ring_current = SynSignalRO(lambda: 300, name='ring_current')
