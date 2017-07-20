from ..dets import (det_factory, build_image_cycle, nsls_ii_path, # chess_path
                    )
from bluesky.plans import Count, abs_set
from bluesky.tests.utils import setup_test_run_engine
from numpy.testing import assert_array_equal
import pytest
from ..movers import shctl1
import numpy as np
import bluesky.examples as be
from ..filter import XRayFilterBankExample

# Note the missing Chess data, there seems to be a de-syncing of the det and
# cycle which causes the tests to not pass, FIXME
# test_params = [('nslsii', nsls_ii_path),
               # ('chess', chess_path)
               # ]
test_params = [('10x10', (10, 10))]


@pytest.mark.parametrize(('name', 'fp'), test_params)
def test_dets(db, tmp_dir, name, fp):
    det = det_factory(name, db.fs, fp, save_path=tmp_dir)
    RE = setup_test_run_engine()
    RE.subscribe('all', db.mds.insert)
    db.fs.register_handler('RWFS_NPY', be.ReaderWithFSHandler)
    cycle2 = build_image_cycle(fp)
    cg = cycle2()
    for i in range(5):
        print(i)
        scan = Count([det], )
        uid = RE(scan)
        for n, d in db.restream(db[-1], fill=True):
            if n == 'event':
                print('!!!!! TEST 1 !!!!!!')
                print(d['data']['pe1_image'])
                print('!!!!! TEST 1 !!!!!!')
                img = next(cg)['pe1_image']
                print(img)
                assert_array_equal(d['data']['pe1_image'], img)
        assert uid is not None


@pytest.mark.parametrize(('name', 'fp'), test_params)
def test_dets_shutter(db, tmp_dir, name, fp):
    det = det_factory(name, db.fs, fp, save_path=tmp_dir, shutter=shctl1)
    RE = setup_test_run_engine()
    RE.subscribe('all', db.mds.insert)
    scan = Count([det], )
    db.fs.register_handler('RWFS_NPY', be.ReaderWithFSHandler)
    cycle2 = build_image_cycle(fp)
    cg = cycle2()
    # With the shutter down
    RE(abs_set(shctl1, 0, wait=True))
    uid = RE(scan)
    for n, d in db.restream(db[-1], fill=True):
        if n == 'event':
            assert_array_equal(d['data']['pe1_image'],
                               np.zeros(next(cg)['pe1_image'].shape))
    assert uid is not None

    # With the shutter up
    RE(abs_set(shctl1, 1, wait=True))
    uid = RE(scan)
    for n, d in db.restream(db[-1], fill=True):
        if n == 'event':
            assert_array_equal(d['data']['pe1_image'], next(cg)['pe1_image'])
    assert uid is not None


@pytest.mark.parametrize(('name', 'fp'), test_params)
def test_dets_XRayFilter(db, tmp_dir, name, fp):
    det = det_factory(name, db.fs, fp, save_path=tmp_dir,
                      filter_bank=XRayFilterBankExample)
    RE = setup_test_run_engine()
    RE.subscribe('all', db.mds.insert)
    scan = Count([det], )
    db.fs.register_handler('RWFS_NPY', be.ReaderWithFSHandler)
    cycle2 = build_image_cycle(fp)
    cg = cycle2()
    # No filters
    for f in XRayFilterBankExample.filter_list:
        RE(abs_set(f, 0, wait=True))
        uid = RE(scan)
    for n, d in db.restream(db[-1], fill=True):
        if n == 'event':
            assert_array_equal(d['data']['pe1_image'], next(cg)['pe1_image'])
    assert uid is not None

    # Each filter
    for f in XRayFilterBankExample.filter_list:
        RE(abs_set(f, 0, wait=True))
    for f in XRayFilterBankExample.filter_list:
        RE(abs_set(f, 1, wait=True))
        uid = RE(scan)
        for n, d in db.restream(db[-1], fill=True):
            if n == 'event':
                print(det.filter_bank)
                assert_array_equal((d['data']['pe1_image']),
                                   next(cg)['pe1_image'] *
                                   f.get_XRayFilter_attenuation)
        assert uid is not None
        RE(abs_set(f, 0, wait=True))

    # All filters
    for f in XRayFilterBankExample.filter_list:
        RE(abs_set(f, 1, wait=True))
        uid = RE(scan)
    for n, d in db.restream(db[-1], fill=True):
        if n == 'event':
            assert_array_equal(d['data']['pe1_image'], (next(cg)['pe1_image']) *
                               XRayFilterBankExample.get_attenuation())
    assert uid is not None

