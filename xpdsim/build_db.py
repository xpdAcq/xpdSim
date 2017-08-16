import os
import uuid

from databroker.broker import Broker
from databroker.headersource.mongo import MDS
from databroker.assets.utils import create_test_database
from databroker.assets.mongo import Registry
from databroker.assets.handlers import NpyHandler


def build_pymongo_backed_broker():
    '''Provide a function level scoped MDS instance talking to
    temporary database on localhost:27017 with v1 schema.

    '''

    db_name = "mds_testing_disposable_{}".format(str(uuid.uuid4()))
    md_test_conf = dict(database=db_name, host='localhost',
                        port=27017, timezone='US/Eastern',
                        version=1)
    #try:
        # nasty details: to save MacOS user
    #    mds = MDS(md_test_conf, 1, auth=False)
    #except TypeError:
    #    mds = MDS(md_test_conf, auth=False)
    mds = MDS(md_test_conf, auth=False)

    db_name = "fs_testing_base_disposable_{uid}"
    fs_test_conf = create_test_database(host='localhost',
                                        port=27017, version=1,
                                        db_template=db_name)
    fs = Registry(fs_test_conf)
    fs.register_handler('npy', NpyHandler)

    def delete_fs():
        print("DROPPING DB")
        fs._connection.drop_database(fs_test_conf['database'])
        mds._connection.drop_database(md_test_conf['database'])


    return Broker(mds, fs)
