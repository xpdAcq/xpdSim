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