import bluesky.examples as be


class Robot(be.Mover):
    def __init__(self, name, fields, initial_set, theta, sample_map=None):
        theta = be.Mover('theta', {'rad': lambda x: x}, {'x': 0})
        self.theta = theta
        if sample_map is None:
            # sample_map maps positions with image cycles @ build_image_cycle
            # sample_map = {path (str): Cycler (iterable like object to cycle
            # through images}
        self._current_sample_geometry = None
        super().__init__(name, fields, initial_set, **kwargs)

    def load_sample(self, saple_number, sample_geometry=None):
        # If no sample is loaded, current_sample_number = 0
        # is reported by the robot
        if self.current_sample_number.get() != 0:
            raise RuntimeError("Sample %d is already loaded."
                               % self.current_sample_number.get())

        #Rotate theta into loading position if necessary
        load_pos = self.TH_POS[sample_geometry]['load']
        if load_post is not None:
            print('Moving theta to load position')
            self.theta.move(load_pos, wait=True)

        # Loading the sample is a three-step procedure:
        # Set sample_number; issue load_cmd; issue execute_cmd.
        set_and_wait(self.sample_number, sample_number)
        set_and_wait(self.load_cmd, 1)
        self.execute_cmd.put(1)
        print('Loading...')
        self._poll_until_idle()

        # Rotate theta into measurement position if necessary
        measure_pos = self.TH_POS[sample_geometry]['measure']
        if measure_pos is not None:
            print('Moving theta to measure position')
            self.theta.move(measure_pos, wait=True)

        # Stash the current sample geomtery for reference when we unload
        self._current_sample_geometry = sample_geometry




    # What functions should be included?

