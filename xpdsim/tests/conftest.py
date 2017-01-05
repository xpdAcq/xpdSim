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
import sys
import tempfile

import pytest
from databroker.tests.conftest import build_pymongo_backed_broker

if sys.version_info >= (3, 0):
    pass


def clean_database(database):
    for sub_db_name in ['mds', 'fs']:
        sub_db = getattr(database, sub_db_name)
        sub_db._connection.drop_database(sub_db.config['database'])


@pytest.fixture(params=[
    # 'sqlite',
    'mongo'], scope='module')
def db(request):
    print('Making DB')
    param_map = {
        # 'sqlite': build_sqlite_backed_broker,
        'mongo': build_pymongo_backed_broker}
    databroker = param_map[request.param](request)
    yield databroker
    print('CLEAN DB')
    clean_database(databroker)


@pytest.fixture(scope='module')
def tmp_dir():
    td = tempfile.mkdtemp()
    print('creating {}'.format(td))
    yield td
    if os.path.exists(td):
        print('removing {}'.format(td))
        shutil.rmtree(td)
