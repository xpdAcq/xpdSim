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
from tempfile import mkdtemp

import numpy as np
from cycler import cycler
from ophyd import sim, Device
from pkg_resources import resource_filename as rs_fn
from tifffile import imread

XPD_SHUTTER_CONF = {"open": 60, "close": 0}

DATA_DIR_STEM = "xpdsim.data"
nsls_ii_path = rs_fn(DATA_DIR_STEM + ".XPD", "ni")
xpd_wavelength = 0.1823
chess_path = rs_fn(DATA_DIR_STEM, "chess")


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
    imgs = [imread(str(fp)) for fp in p.glob("*.tif*")]
    # switch back to pims if the error is resolved
    # imgs = ImageSequence(path)
    return cycler(pe1_image=imgs)


class SimulatedCam(Device):
    acquire_time = sim.SynSignal(name="acquire_time")
    acquire = sim.SynSignal(name="acquire")





        det = sim.SynSignalWithRegistry(
            name=name,
            func=lambda: nexter(shutter),
            save_path=mkdtemp(prefix="xpdsim"),
        )
    else:
        det = sim.SynSignalWithRegistry(
            name=name,
            func=lambda: np.ones((5, 5)),
            save_path=mkdtemp(prefix="xpdsim"),
        )


def fake_pe1_cam(det):
    """faking the cam device of the true PE detoctor

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


def det_factory(img_gen, *, shutter=None,
                name="pe1_image", **kwargs):

    """Build a Perkin-Elmer like detector using real images

    Parameters
    ----------
    img_gen : callable
        function to return image sequence will be output from this
        detector
    shutter : settable object, optional
        abstraction of settable object in ophyd. Default to the
        simulated shutter in xpdsim
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
    return det


def simple_img_gen():
    """image generator for 2D images of size (5, 5)
    with values ones.

    Returns
    -------
    img_gen : func
    """

    return np.ones((5, 5))

def img_gen(src_path, *, shutter=None, noise=None, mover=None):
    cycle = build_image_cycle(src_path)
    gen = cycle()
    _img = next(gen)['pe1_image']

    def nexter(shutter):
        # instantiate again
        gen = cycle()
        img = next(gen)["pe1_image"].copy()
        # noise fro
        if shutter:
            status = shutter.get()
            if np.allclose(status.readback, XPD_SHUTTER_CONF["close"]):
                img = np.zeros(_img.shape)
            elif np.allclose(status.readback, XPD_SHUTTER_CONF["open"]):
                if noise:
                    img += noise(np.abs(img))
        return img.astype(np.float32)

    return nexter(shutter)

def det_factory_dexela(
    reg,
    *,
    shutter=None,
    noise=None,
    name="dexela_image",
    **kwargs
):
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
    det: SimulatedPE1C instance
        The detector
    """

    def nexter(shutter):
        shape = (3072, 3888)
        img = np.random.random(shape)
        # instantiate again
        if shutter:
            status = shutter.get()
            if np.allclose(status.readback, XPD_SHUTTER_CONF["close"]):
                img = np.zeros(shape)
            elif np.allclose(status.readback, XPD_SHUTTER_CONF["open"]):
                if noise:
                    img += noise(np.abs(img))
        return img.astype(np.float32)

    det = sim.SynSignalWithRegistry(
        name=name,
        func=lambda: nexter(shutter),
        reg=reg,
        save_path=mkdtemp(prefix="xpdsim"),
    )
    # plug-ins
    det.cam = SimulatedCam(name="cam")
    # set default values
    det.cam.acquire_time.put(0.1)
    det.cam.acquire.put(1)
    return det


def det_factory_blackfly(
    reg,
    *,
    shutter=None,
    noise=None,
    name="blackfly_det_image",
    full_field=False,
    **kwargs
):
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
    det: SimulatedPE1C instance
        The detector
    """

    def nexter(shutter):
        # shape = (2048, 2448)
        shape = (20, 24)
        base = np.random.random(shape)
        if full_field:
            base = np.ones(shape)
        # instantiate again
        if shutter:
            status = shutter.get()
            if np.allclose(status.readback, XPD_SHUTTER_CONF["close"]):
                return np.zeros(shape)
            elif np.allclose(status.readback, XPD_SHUTTER_CONF["open"]):
                if noise:
                    return base + noise(np.abs(base))
                return base
        else:
            return base

    det = sim.SynSignalWithRegistry(
        name=name,
        func=lambda: nexter(shutter),
        reg=reg,
        save_path=mkdtemp(prefix="xpdsim"),
    )
    # plug-ins
    det.cam = SimulatedCam(name="cam")
    # set default values
    det.cam.acquire_time.put(0.1)
    det.cam.acquire.put(1)
    return det
