from ophyd import Device
from ophyd import Signal
from ophyd import Component as C
# require real ophyd, prettytable, pyepicse
from ophyd.areadetector import TIFFPlugin

class Cam(Device):
    acquire_time = C(Signal, value=1, add_prefix=())


class AreaDetector(Device):
    images_per_set = C(Signal, value=1, add_prefix=())
    number_of_sets = C(Signal, value=1, add_prefix=())
    cam = C(Cam,'', add_prefix=())

