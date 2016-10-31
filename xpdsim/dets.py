"""
Spoof detectors
"""
from cycler import cycler
from pims import ImageSequence
from pkg_resources import resource_filename as rs_fn
import os


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
print(nsls_ii_ni)
