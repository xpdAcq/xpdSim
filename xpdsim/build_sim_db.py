"""this module exists for simulation environment"""
import os
import tempfile
from databroker import Broker


def build_sim_db(sim_db_dir=None):
    if not sim_db_dir:
        sim_db_dir = tempfile.mkdtemp()
    config = {
        'metadatastore': {
            'module': 'databroker.headersource.sqlite',
            'class': 'MDS',
            'config': {
                'directory': sim_db_dir,
                'timezone': 'US/Eastern'}
        },
        'assets': {
            'module': 'databroker.assets.sqlite',
            'class': 'Registry',
            'config': {
                'dbpath': os.path.join(sim_db_dir, 'assets.sqlite')}
        }
    }
    return sim_db_dir, Broker.from_config(config)
