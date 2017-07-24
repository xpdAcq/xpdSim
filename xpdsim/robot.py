import bluesky.examples as be


class Robot(be.Mover):
    # Include class variables (and the mpas) that appear in reference code?
    def __init__(self, name, fields, initial_set, theta, sample_map, **kwargs):
        theta = be.Mover('theta', {'rad': lambda x: x}, {'x': 0})
        self.theta = theta
        self._current_sample_gemorety = None
        super().__init__(name, fields, initial_set, **kwargs)

    # What functions should be included?

