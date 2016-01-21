# xpdSim
simulator objects for bluesky, ophyd

**Step 0: (Recommended)**

Create a new conda environment as a sandbox:`conda create -n name_of_env python=3 ipython`

Activate this environment: `source activate name_of_env`

**Step 1: Installation**

Install with pure git:
  1. Clone both repo: `xpdAcq` and `xpdSim`. After clone, there should be two separate directories in your computer
  2. Navigate to each directory and run `python setup.py install`

Install with conda:
  1. Under your sandbox environment, type: `conda install -c cl3077 xpdacq xpdsim`
  
**Step 2: Testing**

Run `from bluesky.scans import Count` in python/ipython section. If no exception is raised, these simulators work.
