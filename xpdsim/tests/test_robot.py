import bluesky.examples as be
import pytest
from ..dets import robot_factory, nsls_ii_path, chess_path, det_factory

test_params = [('nslsii', nsls_ii_path), ('chess', chess_path)]


@pytest.mark.parametrize(('name', 'fp'), test_params)
def test_robot():
    th = be.Mover('theta', {'theta': lambda x: x}, {'x': 0})
    s_m = {'nslsii': nsls_ii_path, 'chess': chess_path}
    r = robot_factory(th, sample_map=s_m)
    print(r.current_sample_number)
    assert r.sample_map.get('nslsii') is nsls_ii_path
    det_factory(name, db.fs, fp, save_path=tmp_dir, Robot=r)
