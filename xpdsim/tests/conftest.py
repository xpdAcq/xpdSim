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
from xpdsim.build_sim_db import build_sim_db

@pytest.fixture(scope='module')
def db():
    from xpdsim import db, db_path
    yield db
    if os.path.exists(db_path):
        print('Flush db dir')
        shutil.rmtree(db_path)
