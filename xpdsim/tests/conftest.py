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
import os
import shutil
import pytest
import tempfile
from bluesky.tests.conftest import RE

@pytest.fixture(scope='module')
def db():
    from xpdsim import db, sim_db_dir
    yield db
    if os.path.exists(sim_db_dir):
        print('Flush db dir')
        shutil.rmtree(sim_db_dir)
