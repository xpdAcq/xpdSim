##############################################################################
#
# xpdsim            by Billinge Group
#                   Simon J. L. Billinge sb2896@columbia.edu
#                   (c) 2016 trustees of Columbia University in the City of
#                        New York.
#                   All rights reserved
#
# File coded by:    Timothy Liu, Christopher J. Wright
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################
import tempfile

import pytest
from bluesky.tests.conftest import RE
from ophyd.sim import (NumpySeqHandler)


@pytest.fixture(scope='module')
def db():
    temp_dir = tempfile.TemporaryDirectory()
    from xpdsim.build_sim_db import build_sim_db
    sim_db_dir, db = build_sim_db(temp_dir.name)
    db.reg.register_handler('NPY_SEQ', NumpySeqHandler)
    yield db
    temp_dir.cleanup()
