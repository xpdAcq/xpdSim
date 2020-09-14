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
import asyncio

import pytest
from ophyd.sim import (NumpySeqHandler)
from bluesky import RunEngine


@pytest.fixture(scope='module')
def db():
    temp_dir = tempfile.TemporaryDirectory()
    from xpdsim.build_sim_db import build_sim_db
    sim_db_dir, db = build_sim_db(temp_dir.name)
    db.reg.register_handler('NPY_SEQ', NumpySeqHandler)
    yield db
    temp_dir.cleanup()


@pytest.fixture(scope='function')
def RE(request):
    loop = asyncio.new_event_loop()
    loop.set_debug(True)
    RE = RunEngine({}, loop=loop)

    def clean_event_loop():
        if RE.state not in ('idle', 'panicked'):
            try:
                RE.halt()
            except TransitionError:
                pass
        loop.call_soon_threadsafe(loop.stop)
        RE._th.join()
        loop.close()

    request.addfinalizer(clean_event_loop)
    return RE
