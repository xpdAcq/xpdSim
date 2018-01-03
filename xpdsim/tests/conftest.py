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
import pytest
from bluesky.tests.conftest import RE


@pytest.fixture(scope='module')
def db(tmpdir):
    from xpdsim.build_sim_db import build_sim_db
    db, sim_db_dir = build_sim_db(tmpdir)
    yield db
