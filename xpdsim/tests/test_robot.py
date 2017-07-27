from ..robot import Robot
import bluesky.examples as be


def test_robot():
    th = be.Mover('theta', {'theta': lambda x: x}, {'x': 0})
    sm = {1: 'cycle1', 2: 'cycle2'}
    r = Robot('XF:28IDC-ES:1{SM}', {lambda x: x}, {'x': 0},
              theta=th, sample_map=sm)
    # Crashes : 2 extra parameters
    assert r.sample_map.get(1) == 'cycle1'
