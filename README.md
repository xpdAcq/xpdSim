# xpdSim
simulator objects for bluesky, ophyd

simon testing a commit


Install without conda (temporary solution):
  0. (Recommanded) Create a new conda environment as a sand-box
  1. Clone both repo: `xpdAcq` and `xpdSim` After clone, there should be two separate directories in your computer
  2. Nevigate to each directory and run `python setup.py install`
  3. Open a python/ipython section
  4. Run `from bluesky.scan import Count` in python/ipython section. If no exception is raised, these simulators work.
