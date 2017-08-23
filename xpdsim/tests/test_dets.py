from xpdsim.dets import (det_factory, build_image_cycle,
                         nsls_ii_path, chess_path)
from pathlib import Path
from tifffile import imread
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
def test_img_shape(name, fp):
    p = Path(fp)
    shape_check = [imread(str(fp)).shape == (2048, 2048)
                   for fp in p.glob('*.tif*')]
    assert all(shape_check)

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
    for name, doc in db.restream(db[-1], fill=True):
        if name == 'event':
            db_img = doc['data']['pe1_image']
            cycler_img = next(cg)['pe1_image']
            assert_array_equal(db_img, cycler_img)
            assert db_img.squeeze().shape == (2048, 2048)
            assert cycler_img.squeeze().shape == (2048, 2048)
    assert uid is not None


@pytest.mark.parametrize(('name', 'fp'), test_params)
def test_dets_shutter(db, tmp_dir, name, fp):
    det = det_factory(name, db.reg, fp, save_path=tmp_dir, shutter=shctl1)
    RE = setup_test_run_engine()
    RE.subscribe(db.mds.insert, 'all')
    scan = bs.count([det])
    db.reg.register_handler('RWFS_NPY', be.ReaderWithRegistryHandler)
    cycle2 = build_image_cycle(fp)
    cg = cycle2()
    # With the shutter down
    RE(abs_set(shctl1, 0, wait=True))
    uid = RE(scan)
    for name, doc in db.restream(db[-1], fill=True):
        if name == 'event':
            assert_array_equal(doc['data']['pe1_image'],
                               np.zeros(doc['data']['pe1_image'].shape))
    assert uid is not None

    # With the shutter up
    RE(abs_set(shctl1, 60, wait=True))
    scan = bs.count([det])
    uid = RE(scan)
    # Note: since reader.describe takes trial data we must advance
    # the cycle by one as well
    next(cg)
    for name, doc in db.restream(db[-1], fill=True):
        if name == 'event':
            assert_array_equal(doc['data']['pe1_image'],
                               next(cg)['pe1_image'])
    assert uid is not None
