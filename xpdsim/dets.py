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
from bluesky.utils import new_uid
import bluesky.examples as be

DATA_DIR_STEM = 'xpdsim.data'

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
class SimpleSimulatedPE1C(be.ReaderWithRegistry):
    """Simple simlulated detector, which only include reference to the
    Registry (FileStore in the past). This simulated detector has no
    information about shutter or dark strategy. Realistic attributes
    from the camera are also available in this simulated object

    Parameters
    ----------
    name : str
        name of this simulated detector
    read_fields : str
        name of data field readed from this detector
    reg : Registry
        object providing reference of the data
    """

    def __init__(self, name, read_fields, reg, **kwargs):
        self.images_per_set = PutGet()
        self.number_of_sets = PutGet()
        self.cam = SimulatedCam()
        self._staged = False
        super().__init__(name, read_fields, reg=reg, **kwargs)
        self.ready = True  # work around a hack in Reader



class SimulatedPE1C(SimpleSimulatedPE1C):
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
        self._staged = False
        if shutter:
            self.shutter = shutter
        if dark_fields:
            self._dark_fields = dict(self._fields)
            self._dark_fields.update(dark_fields)
        else:
            self._dark_fields = None
        super().__init__(name, read_fields, reg=reg, **kwargs)

    def trigger(self):
        if self.shutter and self._dark_fields and \
                        self.shutter.read()['rad']['value'] == 0:
            read_v = {field: {'value': func(), 'timestamp': ttime.time()}
                      for field, func in self._dark_fields.items()
                      if field in self.read_attrs}
            self._result.clear()
            for idx, (name, reading) in enumerate(read_v.items()):
                # Save the actual reading['value'] to disk and create a record
                # in FileStore.
                np.save('{}_{}.npy'.format(self._path_stem, idx),
                        reading['value'])
                datum_id = new_uid()
                self.fs.insert_datum(self._resource_id, datum_id,
                                     dict(index=idx))
                # And now change the reading in place, replacing the value with
                # a reference to FileStore.
                reading['value'] = datum_id
                self._result[name] = reading

            delay_time = self.exposure_time
            if delay_time:
                if self.loop.is_running():
                    st = be.SimpleStatus()
                    self.loop.call_later(delay_time, st._finished)
                    return st
                else:
                    ttime.sleep(delay_time)

            return be.NullStatus()

        else:
            return super().trigger()


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


#nsls_ii_path = os.path.join(DATA_DIR, 'XPD/ni/')

#chess_path = os.path.join(DATA_DIR, 'chess/')


def det_factory(name, fs, path, shutter=None, **kwargs):
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

    if shutter:
        stream_piece = next(gen)
        sample_img = stream_piece['pe1_image']
        gen = chain((i for i in [stream_piece]), gen)  # put the piece on top

        def dark_nexter():
            return np.zeros(sample_img.shape)

        return SimulatedPE1C(name,
                             {'pe1_image': lambda: nexter()}, fs=fs,
                             shutter=shutter,
                             dark_fields={'pe1_image': lambda: dark_nexter()},
                             **kwargs)

    return SimulatedPE1C(name,
                         {'pe1_image': lambda: nexter()}, fs=fs,
                         **kwargs)
