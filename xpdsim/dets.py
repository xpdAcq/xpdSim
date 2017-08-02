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
import time as ttime
from itertools import chain

import bluesky.examples as be
import numpy as np
from cycler import cycler
from pims import ImageSequence
from pkg_resources import resource_filename as rs_fn
from .robot import Robot

DATA_DIR = rs_fn('xpdsim', 'data/')


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
class SimulatedPE1C(be.ReaderWithFileStore):
    """Subclass the bluesky plain detector examples ('Reader');

    also add realistic attributes and shutter stuff.
    """

    def __init__(self, name, read_fields, fs, shutter=None,
                 dark_fields=None, Robot=None, **kwargs):
        self.images_per_set = PutGet()
        self.number_of_sets = PutGet()
        self.cam = SimulatedCam()
        self.shutter = shutter
        self.robot = Robot
        self._staged = False
        super().__init__(name, read_fields, fs=fs, **kwargs)
        self.ready = True  # work around a hack in Reader
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
            print('======Triggered shutter======')
            print(rv)
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
    imgs = ImageSequence(os.path.join(path, '*.tif*'))
    return cycler(pe1_image=[i for i in imgs])


nsls_ii_path = os.path.join(DATA_DIR, 'XPD/ni/')

chess_path = os.path.join(DATA_DIR, 'chess/')


def robot_factory(self, theta, sample_map=None, **kwargs):
    return Robot(theta, sample_map)


def det_factory(name, fs, path, shutter=None, Robot=None, **kwargs):
    """Build a detector using real images

    Parameters
    ----------
    name: str
        Name of the detector
    fs: filestore.FileStore instance
        The filestore to save all the data in
    path: str
        The path to the tiff files

    Returns
    -------
    detector: SimulatedPE1C instance
        The detector
    """
    cycle = build_image_cycle(path)
    gen = cycle()

    def nexter():
        return next(gen)['pe1_image']

    if shutter:
        stream_piece = next(gen)
        sample_img = stream_piece['pe1_image']
        gen = chain((i for i in [stream_piece]), gen)
        # put the piece on top

        def dark_nexter():
            return np.zeros(sample_img.shape)

        if Robot is None:
            return SimulatedPE1C(name, {'pe1_image': lambda: nexter()},
                                 fs=fs, shutter=shutter, dark_fields=
                                 {'pe1_image': lambda: dark_nexter()},
                                 **kwargs)
        else:
            return SimulatedPE1C(name, {'pe1_image': lambda: nexter()},
                                 fs=fs, shutter=shutter,
                                 dark_fields={'pe1_image': lambda:
                                              dark_nexter()},
                                 Robot=Robot, **kwargs)

    if Robot is None:
        return SimulatedPE1C(name, {'pe1_image': lambda: nexter()}, fs=fs,
                             **kwargs)
    else:
        return SimulatedPE1C(name, {'pe1_image': lambda: nexter()}, fs=fs,
                             Robot=Robot, **kwargs)
