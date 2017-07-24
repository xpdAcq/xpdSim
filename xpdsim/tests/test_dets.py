from xpdsim.dets import (det_factory, build_image_cycle,
                         nsls_ii_path, chess_path)
from bluesky.plans import Count, abs_set
from bluesky.tests.utils import setup_test_run_engine
from numpy.testing import assert_array_equal
import pytest
from xpdsim.movers import shctl1
import numpy as np
import bluesky.examples as be
import bluesky.plans as bs

test_params = [('nslsii', nsls_ii_path), ('chess', chess_path)]


@pytest.mark.parametrize(('name', 'fp'), test_params)
def test_dets(db, tmp_dir, name, fp):
    det = det_factory(name, db.reg, fp, save_path=tmp_dir)
    RE = setup_test_run_engine()
    RE.subscribe(db.mds.insert, 'all')
    scan = bs.count([det])
    uid = RE(scan)
    db.reg.register_handler('RWFS_NPY', be.ReaderWithRegistryHandler)
    cycle2 = build_image_cycle(fp)
    cg = cycle2()
    for n, d in db.restream(db[-1], fill=True):
        if n == 'event':
            assert_array_equal(d['data']['pe1_image'],
                               next(cg)['pe1_image'])
    assert uid is not None


@pytest.mark.parametrize(('name', 'fp'), test_params)
def test_dets_shutter(db, tmp_dir, name, fp):
    det = det_factory(name, db.reg, fp, save_path=tmp_dir, shutter=shctl1)
    RE = setup_test_run_engine()
    RE.subscribe(db.mds.insert, 'all')
    scan = bs.count([det], )
    db.reg.register_handler('RWFS_NPY', be.ReaderWithRegistryHandler)
    cycle2 = build_image_cycle(fp)
    cg = cycle2()
    # With the shutter down
    RE(abs_set(shctl1, 0, wait=True))
    uid = RE(scan)
    for n, d in db.restream(db[-1], fill=True):
        if n == 'event':
            assert_array_equal(d['data']['pe1_image'],
                               np.zeros(d['data']['pe1_image'].shape))
    assert uid is not None

    # With the shutter up
    RE(abs_set(shctl1, 1, wait=True))
    uid = RE(scan)
    next(cg)
    for n, d in db.restream(db[-1], fill=True):
        if n == 'event':
            assert_array_equal(d['data']['pe1_image'],
                               next(cg)['pe1_image'])
    assert uid is not None
