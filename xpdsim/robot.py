# Detector will get the sample information from the robot via a mediator to
# determine which image to display.
import time as ttime
from ophyd.utils import set_and_wait
from ophyd import EpicsSignal
from ophyd import Component as Cpt
from ophyd import Device


class Robot(Device):
    sample_number = Cpt(EpicsSignal, 'ID:Tgt-SP')
    load_cmd = Cpt(EpicsSignal, 'Cmd:Load-Cmd.PROC')
    unload_cmd = Cpt(EpicsSignal, 'Cmd:Unload-Cmd.PROC')
    execute_cmd = Cpt(EpicsSignal, 'Cmd:Exec-Cmd')
    status = Cpt(EpicsSignal, 'Sts-Sts')
    current_sample_number = Cpt(EpicsSignal, 'Addr:CurrSmpl-I')

    # Map sample types to load position and measurement position
    TH_POS = {'capillary': {'load': None, 'measure': None},
              'plate': {'load': 0, 'measure': 90},
              None: {'load': None, 'measure': None}}

    # init is unlike robot api - that produces error message
    # how to resolve ?
    def __init__(self, name, fields, initial_set, theta, sample_map, **kwargs):
        self.theta = theta  # theta is a motor
        self.sample_map = sample_map  # sample_map is a dict
        self._current_sample_geometry = None
        super().__init__(name, fields, initial_set, **kwargs)

    def _poll_until_idle(self):
        ttime.sleep(3)  # gives robot plenty of time to start
        while self.status.get() != 'Idle':
            ttime.sleep(.1)

    def _poll_until_sample_cleared(self):
        while self.current_sample_number.get() != 0:
            ttime.sleep(.1)

    def load_sample(self, sample_number, sample_geometry=None):
        # If no sample is loaded, current_sample_number = 0
        # is reported by the robot
        if self.current_sample_number.get() != 0:
            raise RuntimeError("Sample %d is already loaded."
                               % self.current_sample_number.get())

        # Rotate theta into loading position if necessary
        load_pos = self.TH_POS[sample_geometry]['load']
        if load_pos is not None:
            print('Moving theta to load position')
            self.theta.move(load_pos, wait=True)

        # Loading the sample is a three-step procedure:
        # Set sample_number; issue load_cmd; issue execute_cmd.
        set_and_wait(self.sample_number, sample_number)
        set_and_wait(self.load_cmd, 1)
        # set_and_wait is an ophyd.utils import
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

    def unload_sample(self):
        if self.current_sample_number.get() == 0:
            # there is nothing to do
            return

        # Rotate theta into loading position if necessary (e.g. flat plate
        # model)
        load_pos = self.TH_POS[self._current_sample_geomgery]['load']
        if load_pos is not None:
            print('Moving theta to unload position')
            self.theta.move(load_pos, wait=True)

        set_and_wait(self.unload_cmd, 1)
        self.execute_cmd.put(1)
        print('Unloading...')
        self._poll_until_idle()
        self._poll_until_sample_cleared()
        self._current_sample_geometry = None

    def stop(self):
        self.theta.stop()
        super().stop()
