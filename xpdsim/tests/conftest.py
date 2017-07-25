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
import importlib
from databroker.tests.utils import build_pymongo_backed_broker, \
                                   build_sqlite_backed_broker
params = []
param_map = {}

for name, builder, mod in zip(['mongo', 'sqlite'],
                              [build_pymongo_backed_broker,
                               build_sqlite_backed_broker],
                              ['metadatastore', 'portable_mds']):
    try:  # pragma: no cover
        importlib.import_module(mod)
    except ImportError:
        pass
    else:
        params.append(name)
        param_map.update({name: builder})

if sys.version_info >= (3, 0):
    pass


@pytest.fixture(params=params, scope='module')
def db(request):
    print('Making DB')
    databroker = param_map[request.param](request)
    yield databroker


@pytest.fixture(scope='module')
def tmp_dir():
    td = tempfile.mkdtemp()
    print('creating {}'.format(td))
    yield td
    if os.path.exists(td):
        print('removing {}'.format(td))
        shutil.rmtree(td)
