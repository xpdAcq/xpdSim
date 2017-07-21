from ..filter import XRayFilter, FilterBank


def test_filter():
    f = XRayFilter('filter1', {'rad': lambda x: x}, {'x': 0}, 0.5)

    assert f.attenuation == .5

