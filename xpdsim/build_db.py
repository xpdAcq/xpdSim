"""this module exists for simulation environment"""
import os
import uuid

from databroker import Broker, BrokerES
#from databroker.assets.handlers import NpyHandler
from databroker.headersource import HeaderSourceShim
from databroker.eventsource import EventSourceShim

def build_db_wrapper(option='mongo'):
    if option == 'mongo':
        print("BUILD mongo-backed db")
        db = build_pymongo_backed_broker(None)
    elif option == 'sqlite':
        print("BUILD sqlite-backed db")
        db = build_sqlite_backed_broker(None)

    return db

def build_sqlite_backed_broker(request):
    """Uses mongoquery + sqlite -- no pymongo or mongo server anywhere"""
    from databroker.headersource.sqlite import MDS
    from databroker.assets.sqlite import Registry

    tempdirname = tempfile.mkdtemp()
    mds = MDS({'directory': tempdirname,
               'timezone': tzlocal.get_localzone().zone,
               'version': 1})
    filenames = ['run_starts.json', 'run_stops.json', 'event_descriptors.json',
                 'events.json']
    for fn in filenames:
        with open(os.path.join(tempdirname, fn), 'w') as f:
            f.write('[]')

    def delete_mds():
        shutil.rmtree(tempdirname)

    #request.addfinalizer(delete_mds)

    tf = tempfile.NamedTemporaryFile()
    fs = Registry({'dbpath': tf.name})

    def delete_fs():
        os.remove(tf.name)

    #request.addfinalizer(delete_fs)

    return BrokerES(HeaderSourceShim(mds),
                    [EventSourceShim(mds, fs)],
                    {'': fs})

def build_pymongo_backed_broker(request):
    '''Provide a function level scoped MDS instance talking to
    temporary database on localhost:27017 with v1 schema.

    '''
    from databroker.headersource.mongo import MDS
    from databroker.assets.utils import create_test_database
    from databroker.assets.mongo import Registry

    db_name = "mds_testing_disposable_{}".format(str(uuid.uuid4()))
    md_test_conf = dict(database=db_name, host='localhost',
                        port=27017, timezone='US/Eastern',
                        version=1)
    mds = MDS(md_test_conf, auth=False)

    db_name = "fs_testing_base_disposable_{uid}"
    fs_test_conf = create_test_database(host='localhost',
                                        port=27017, version=1,
                                        db_template=db_name)
    fs = Registry(fs_test_conf)

    def delete_fs():
        print("DROPPING DB")
        fs._connection.drop_database(fs_test_conf['database'])
        mds._connection.drop_database(md_test_conf['database'])

    #request.addfinalizer(delete_fs)

    return Broker(mds, fs)
