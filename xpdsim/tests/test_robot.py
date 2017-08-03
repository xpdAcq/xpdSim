from ..robot import Robot
import bluesky.examples as be


def test_robot():
    th = be.Mover('theta', {'theta': lambda x: x}, {'x': 0})
    s_m = {'sample1': 'img1', 'sample2': 'img2'}
    r = Robot('PV_PREFIX:', th, sample_map=s_m)
    assert r.sample_map.get('sample1') is 'img1'


