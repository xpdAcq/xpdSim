""" Spoof detectors """
##############################################################################
#
# xpdsim            by Billinge Group
#                   Simon J. L. Billinge sb2896@columbia.edu
#                   (c) 2016 trustees of Columbia University in the City of
#                        New York.
#                   All rights reserved
#
# File coded by:    Christopher J. Wright, Timothy Liu
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################

from pathlib import Path
from tempfile import mkdtemp

import numpy as np
from cycler import cycler
from ophyd import sim, Device
from pkg_resources import resource_filename as rs_fn
from tifffile import imread


# extra config
XPD_SHUTTER_CONF = {"open": 60, "close": 0}
DATA_DIR_STEM = "xpdsim.data"
# image size
PE_IMG_SIZE = (2048, 2048)
DEXELA_IMG_SIZE = (3072, 3088)
BLACKFLY_IMG_SIZE = (20, 24)
# package filepath
nsls_ii_path = rs_fn(DATA_DIR_STEM + ".XPD", "ni")
xpd_wavelength = 0.1823
chess_path = rs_fn(DATA_DIR_STEM, "chess")


def build_image_cycle(path, key='pe1_image'):
    """Build image cycles, essentially generators with endless images

    Parameters
    ----------
    path: str
        Path to the files to be used as the base for the cycle.
    key: str, optional
        key of the entire image sequence. Default to ``'pe1_image'``.

    Returns
    -------
    Cycler:
        The iterable like object to cycle through the images
    """
    p = Path(path)
    imgs = [imread(str(fp)) for fp in p.glob("*.tif*")]
    # TODO: switch back to pims if the error is resolved
    # imgs = ImageSequence(path)
    return cycler(key, imgs)


class SimulatedCam(Device):
    acquire_time = sim.SynSignal(name="acquire_time")
    acquire = sim.SynSignal(name="acquire")


def add_fake_cam(det):
    """Adding simulated cam device signals to the detoctor

    Parameters
    ----------
    det: SimulatedPE1C instance
        The detector

    Returns
    -------
    det: SimulatedPE1C instance
        The detector
    """
    # plug-ins
    det.images_per_set = sim.SynSignal(name="images_per_set")
    det.number_of_sets = sim.SynSignal(name="number_of_sets")
    det.cam = SimulatedCam(name="cam")
    # set default values
    det.cam.acquire_time.put(0.1)
    det.cam.acquire.put(1)
    det.images_per_set.put(1)
    return det


def det_factory(img_gen, *, name="pe1_image"):

    """Build a Perkin-Elmer like detector using real images

    Parameters
    ----------
    img_gen : callable
        function to return image sequence will be output from this
        detector
    name : str, optional
        name of image field name. Default to ``pe1_image``

    Returns
    -------
    det: SimulatedPE1C instance
        The detector
    """
    det = sim.SynSignalWithRegistry(
        name=name,
        func=lambda: img_gen,
        save_path=mkdtemp(prefix="xpdsim"),
    )
    return add_fake_cam(det)


def img_gen(cycle=None, *, size=PE_IMG_SIZE,
            shutter=None, noise=None):
    """Generator of diffraction images from 2D detector.

    The output images is determined by ``cycle`` argument.

    Parameters
    ----------
    cycle: cycler.Cycler, optional
        The iterable like object to cycle through the images.
        Default to images with standard Gaussian noise in
         input size.
    size : tuple, optional
        Tuple to specify image size from the simulated detetor.
        Default to ``(2048, 2048)`` (PE detector). Overriden when
        ``cycle`` argument is passed.
    shutter : settable, optional
        Ophyd objects to represent the shutter associated with
         with the detector. If it is not passed, assuming shutter
         is always open. If is given, assuming it follows the same
         configuration as XPD beamline.
    noise : callable, optional
        function to generate noise based on absolute scale of image.
        Default to noise-free.

    Returns
    -------
    img_gen : ndarray
        simulated (2048, 2048) 2D diffraction image
    """
    if not cycle:
        cycle = cycler(pe1_image=np.random.random(size))
    key = cycle.keys
    if not len(key) == 1:
        raise RuntimeError('Only support single data key')
    key = key.pop()
    gen = cycle()
    _img = next(gen)[key]

    def nexter(cycle, shutter):
        # instantiate again
        key = cycle.keys.pop()
        gen = cycle()
        img = next(gen)[key].copy()
        # if shutter, consider more realistic situation
        # TODO: separate shutter logic in the future
        if shutter:
            status = shutter.get()
            if np.allclose(status.readback, XPD_SHUTTER_CONF["close"]):
                img = np.zeros(_img.shape)
            elif np.allclose(status.readback, XPD_SHUTTER_CONF["open"]):
                if noise:
                    img += noise(np.abs(img))
        return img.astype(np.float32)
    return nexter(cycle, shutter)
