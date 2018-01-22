import pyFAI

from xpdsim import *


def test_load_pyfai():
    print(pyfai_poni)
    assert pyFAI.load(pyfai_poni)
