""" Spoof detectors """
##############################################################################
#
# xpdsim            by Billinge Group
#                   Simon J. L. Billinge sb2896@columbia.edu
#                   (c) 2016 trustees of Columbia University in the City of
#                        New York.
#                   All rights reserved
#
# File coded by:    Christopher J. Wright
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################

import os
import numpy as np
import time as ttime
from cycler import cycler
from itertools import chain
from tifffile import imread
from pims import ImageSequence
from pkg_resources import resource_filename as rs_fn
import bluesky.examples as be
from pathlib import Path

DATA_DIR_STEM = 'xpdsim.data'

nsls_ii_path = rs_fn(DATA_DIR_STEM+'.XPD', 'ni')
xpd_wavelength = 0.1823
chess_path = rs_fn(DATA_DIR_STEM, 'chess')


class PutGet:
    """basic class to have set/put method"""

    def __init__(self, numeric_val=1):
        self._val = numeric_val

    def put(self, val):
        """set value"""
        self._val = val
        return self._val

    def get(self):
        """read current value"""
        return self._val


class SimulatedCam:
    """class to simulate Camera class"""

    def __init__(self, frame_acq_time=0.1, acquire=1):
        # default acq_time = 0.1s and detector is turned on
        self.acquire_time = PutGet(frame_acq_time)
        self.acquire = PutGet(acquire)


# define simulated PE1C
class SimulatedPE1C(be.ReaderWithRegistry):
    """Advanced version of simlulated detector, which includes reference to the
    Registry (FileStore in the past), shutter and dark strategy.
    Realistic attributes from the camera are also available in this
    simulated object

    Parameters
    ----------
    name : str
        name of this simulated detector
    read_fields : str
        name of data field readed from this detector
    reg : Registry
        object providing reference of the data
    shutter : object, optional
        a valid python object represents the shutter. Default is None.
    dark_fields: dict, optional
        a dictionary with key beining the name of the dark_field and
        the value represents the function of dark strategey. Default is
        None.
    """
    def __init__(self, name, read_fields, reg, shutter=None,
                 dark_fields=None, **kwargs):
        self.images_per_set = PutGet()
        self.number_of_sets = PutGet()
        self.cam = SimulatedCam()
        super().__init__(name, read_fields, reg=reg, **kwargs)
        self._staged = False
        self.ready = True  # work around a hack in Reader
        self.shutter = shutter
        if dark_fields:
            self._dark_fields = dict(self._fields)
            self._dark_fields.update(dark_fields)
        else:
            self._dark_fields = None

    def trigger_read(self):
        if self.shutter and self._dark_fields and \
                self.shutter.read()['rad']['value'] == 0:
            rv = {field: {'value': func(), 'timestamp': ttime.time()}
                  for field, func in self._dark_fields.items()
                  if field in self.read_attrs}
        else:
            rv = super().trigger_read()
        read_v = dict(rv)
        read_v['pe1_image']['value'] = read_v['pe1_image']['value'].copy()
        return read_v


def build_image_cycle(path):
    """Build image cycles, essentially generators with endless images

    Parameters
    ----------
    path: str
        Path to the files to be used as the base for the cycle, this can
        include some globing

    Returns
    -------
    Cycler:
        The iterable like object to cycle through the images
    """
    p = Path(path)
    imgs = [imread(str(fp)) for fp in p.glob('*.tif*')]
    # switch back to pims if the error is resolved
    #imgs = ImageSequence(path)

    return cycler(pe1_image=imgs)


def det_factory(name, reg, src_path, shutter=None, **kwargs):
    """Build a detector using real images

    Parameters
    ----------
    name: str
        Name of the detector
    reg: Registry
        The filestore to save all the data in
    src_path: str
        The path to the source tiff files

    Returns
    -------
    detector: SimulatedPE1C instance
        The detector
    """
    cycle = build_image_cycle(src_path)
    gen = cycle()

    def nexter():
        return next(gen)['pe1_image']

    if shutter:
        stream_piece = next(gen)
        sample_img = stream_piece['pe1_image']
        gen = chain((i for i in [stream_piece]), gen)  # put the piece on top

        def dark_nexter():
            return np.zeros(sample_img.shape)

        return SimulatedPE1C(name,
                             {'pe1_image': lambda: nexter()},
                             reg=reg, shutter=shutter,
                             dark_fields={'pe1_image': lambda: dark_nexter()},
                             **kwargs)

    return SimulatedPE1C(name,
                         {'pe1_image': lambda: nexter()}, reg=reg,
                         **kwargs)
