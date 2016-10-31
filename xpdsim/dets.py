"""
Spoof detectors
"""
from cycler import cycler
from pims import ImageSequence
from pkg_resources import resource_filename as rs_fn
import os


DATA_DIR = rs_fn('xpdsim', 'data/')

def build_image_cycle(path):
    imgs = ImageSequence(path)
    return cycler(img=[i for i in imgs])

nsls_ii_ni = build_image_cycle(
    os.path.join(DATA_DIR,
                 'XPD/ni/sub_nickel_std_ct_for_10_20160309-1742_0.tiff'))
