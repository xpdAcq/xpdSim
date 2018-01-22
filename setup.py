from setuptools import setup, find_packages

setup(
    name='xpdsim',
    version='0.1.5',
    packages=find_packages(),
    description='simulators',
    zip_safe=False,
    package_data={'xpdsim.data': ['XPD/ni/*.tif*', 'pyfai/*']},
    include_package_data=True,
    url='https://github.com/xpdAcq/xpdSim'
)
