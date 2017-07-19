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
                 dark_fields=None, filter_bank=None, **kwargs):
        self.images_per_set = PutGet()
        self.number_of_sets = PutGet()
        self.cam = SimulatedCam()
        self.shutter = shutter
        self._staged = False
        self.filter_bank = filter_bank
        super().__init__(name, read_fields, fs=fs, **kwargs)
        self.ready = True  # work around a hack in Reader
        if dark_fields:
            self._dark_fields = dict(self._fields)
            self._dark_fields.update(dark_fields)
        else:
            self._dark_fields = None

    def trigger_read(self):
        read_v = super().trigger_read()
        if self.shutter and self._dark_fields and \
                self.shutter.read()['rad']['value'] == 0:
            read_v = {field: {'value': func(), 'timestamp': ttime.time()}
                      for field, func in self._dark_fields.items()
                      if field in self.read_attrs}
        if self.filter_bank:
            print(self.filter_bank.get_attenuation())
            read_v['pe1_image']['value'] *= self.filter_bank.get_attenuation()
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
    if isinstance(path, str):
        imgs = ImageSequence(os.path.join(path, '*.tif*'), dtype=np.float64)
    else:
        imgs = [np.ones(path)]
        imgs = ImageSequence(os.path.join(path, '*.tif*'), dtype=np.float64)
    return cycler(pe1_image=[i for i in imgs])


nsls_ii_path = os.path.join(DATA_DIR, 'XPD/ni/')

chess_path = os.path.join(DATA_DIR, 'chess/')


def det_factory(name, fs, path, shutter=None, filter_bank=None, **kwargs):
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
    cycle = build_image_cycle(
        path)
    gen = cycle()

    def nexter():
        return next(gen)['pe1_image']

    kwargs['read_fields'] = {'pe1_image': lambda: nexter()}

    if shutter:
        stream_piece = next(gen)
        sample_img = stream_piece['pe1_image']
        gen = chain((i for i in [stream_piece]), gen)  # put the piece on top

        def dark_nexter():
            return np.zeros(sample_img.shape)

        kwargs.update(shutter=shutter,
                      dark_fields={'pe1_image': lambda: dark_nexter()})

    if filter_bank:
        kwargs.update(filter_bank=filter_bank,
                      dark_fields={'pe1_image': lambda: dark_nexter()})

    return SimulatedPE1C(name, fs=fs, **kwargs)

