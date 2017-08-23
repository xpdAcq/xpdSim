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
from databroker.tests.utils import (build_sqlite_backed_broker,
                                    #build_pymongo_backed_broker,
                                    #build_hdf5_backed_broker,
                                    #build_client_backend_broker,
                                    #start_md_server,
                                    #stop_md_server
                                    )

params = ['sqlite', #'mongo',
          #'hdf5', 'client'
          ]

@pytest.fixture(params=params, scope='module')
def db(request):
    param_map = {'sqlite': build_sqlite_backed_broker,
                 #'mongo': build_pymongo_backed_broker,
                 #'hdf5': build_hdf5_backed_broker,
                 #'client': build_client_backend_broker
                 }
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

""" holding place
import sys
import uuid
import ujson
import time
import requests.exceptions
import tzlocal
import databroker.headersource.mongoquery as mqmds
from databroker.headersource import sqlite as sqlmds
for name, builder, mod in zip(['mongo', 'sqlite'],
                              [build_pymongo_backed_broker,
                               build_sqlite_backed_broker],
                              ['metadatastore', 'portable_mds']):
    try:
        importlib.import_module(mod)
    except ImportError:
        pass
    else:
        params.append(name)
        param_map.update({name: builder})

if sys.version_info >= (3, 0):
    pass
"""
