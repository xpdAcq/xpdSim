from ..dets import *
from bluesky.plans import Count
from bluesky.tests.utils import setup_test_run_engine
from numpy.testing import assert_array_equal
import pytest

test_params = [('nslsii', nsls_ii_path), ('chess', chess_path)]


@pytest.mark.parametrize(('name', 'fp'), test_params)
def test_nsls_ii(db, tmp_dir, name, fp):
    det = det_factory(name, db.fs, fp, save_path=tmp_dir)
    RE = setup_test_run_engine()
    RE.subscribe('all', db.mds.insert)
    scan = Count([det], )
    uid = RE(scan)
    db.fs.register_handler('RWFS_NPY', be.ReaderWithFSHandler)
    cycle2 = build_image_cycle(fp)
    cg = cycle2()
    for n, d in db.restream(db[-1], fill=True):
        if n == 'event':
            assert_array_equal(d['data']['pe1_image'], next(cg)['pe1_image'])
    assert uid is not None
