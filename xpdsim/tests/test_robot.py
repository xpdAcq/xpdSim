import bluesky.examples as be
from bluesky.plans import Count
from bluesky.tests.utils import setup_test_run_engine
from numpy.testing import assert_array_equal
from ..dets import robot_factory, nsls_ii_path, build_image_cycle, \
    chess_path, det_factory


test_params = [('nslsii', nsls_ii_path), ('chess', chess_path)]


# @pytest.mark.parametrize(('name', 'fp'), test_params)
def test_robot(db, tmp_dir):
    th = be.Mover('theta', {'theta': lambda x: x}, {'x': 0})
    sm = {}
    for i, (name, path) in enumerate(test_params):
        cycle = build_image_cycle(path)
        gen = cycle()

        def nexter():
            return next(gen)['pe1_image']
        sm[i] = {'pe1_image': lambda: nexter()}
    r = robot_factory(th, sample_map=sm)
    det = det_factory(name, db.fs, path, save_path=tmp_dir, Robot=r)
    RE = setup_test_run_engine()
    RE.subscribe('all', db.mds.insert)
    scan = Count([det], )
    uid = RE(scan)
    db.fs.register_handler('RWFS_NPY', be.ReaderWithFSHandler)
    cycle2 = build_image_cycle()
    cg = cycle2()
    for n, d in db.restream(db[-1], fill=True):
        if n == 'event':
            assert_array_equal(d['data']['pe1_image'], next(cg)['pe1_image'])
    assert uid is not None
