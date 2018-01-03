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

from pathlib import Path

import numpy as np
from cycler import cycler
from ophyd import sim, Device
from pkg_resources import resource_filename as rs_fn
from tifffile import imread

XPD_SHUTTER_CONF = {'open': 60, 'close': 0}

DATA_DIR_STEM = 'xpdsim.data'
nsls_ii_path = rs_fn(DATA_DIR_STEM+'.XPD', 'ni')
xpd_wavelength = 0.1823
chess_path = rs_fn(DATA_DIR_STEM, 'chess')


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


class SimulatedCam(Device):
    acquire_time = sim.SynSignal(name='acquire_time')
    acquire = sim.SynSignal(name='acquire')


def det_factory(reg, *, shutter=None,
                src_path=None, **kwargs):
    """Build a detector using real images

    Parameters
    ----------
    reg: Registry
        The filestore to save all the data in
    src_path: str
        The path to the source tiff files
    full_img : bool, keyword-only
        Option on if want to return full size imag.
        Deafult is False.

    Returns
    -------
    pe1c: SimulatedPE1C instance
        The detector
    """

    if src_path:
        cycle = build_image_cycle(src_path)
        gen = cycle()
        _img = next(gen)
        def nexter(shutter):
            # instantiate again
            gen = cycle()
            if shutter:
                status = shutter.get()
                if np.allclose(status.readback,
                               XPD_SHUTTER_CONF['close']):
                    return np.zeros_like(_img)
                elif np.allclose(status.readback,
                                 XPD_SHUTTER_CONF['open']):
                    return next(gen)['pe1_image']
            else:
                return next(gen)['pe1_image']
        pe1c = sim.SynSignalWithRegistry(name='pe1_image',
                                         func=lambda: nexter(shutter),
                                         reg=reg)
    else:
        pe1c = sim.SynSignalWithRegistry(name='pe1_image',
                                         func=lambda: np.ones((5,5)),
                                         reg=reg)
    # plug-ins
    pe1c.images_per_set = sim.SynSignal(name='images_per_set')
    pe1c.number_of_sets = sim.SynSignal(name='number_of_sets')
    pe1c.cam = SimulatedCam(name='cam')
    # set default values
    pe1c.cam.acquire_time.put(0.1)
    pe1c.cam.acquire.put(1)
    return pe1c
