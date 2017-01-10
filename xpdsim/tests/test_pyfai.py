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
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator
from xpdsim.utils import pyfai_path
import yaml


def test_smoke_load():
    with open(pyfai_path) as f:
        pyfai_dict = yaml.load(f)
    ai = AzimuthalIntegrator()
    ai.setPyFAI(**pyfai_dict)

if __name__ == '__main__':
    test_smoke_load()
