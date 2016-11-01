"""
Spoof detectors
"""
from cycler import cycler
from pims import ImageSequence
from pkg_resources import resource_filename as rs_fn
import os
from bluesky.examples import ReaderWithFileStore
from xpdsim.db import *


DATA_DIR = rs_fn('xpdsim', 'data/')

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
    imgs = ImageSequence(path)
    return cycler(img=[i for i in imgs])
nsls_ii_ni = build_image_cycle(
    os.path.join(DATA_DIR,
                 'XPD/ni/*.tiff'))

nsls_ii_ni_gen = nsls_ii_ni()


def nexter():
    next(nsls_ii_ni_gen)


nsls_ii_ni_det = ReaderWithFileStore('nsls_ii_ni', {'pe1_image': lambda: nexter()}, fs=fs)
print(nsls_ii_ni_det)
print(nsls_ii_ni_det.trigger())
print(nsls_ii_ni_det.read())
