#Instructions for the installation of the XPD experiment simulation engine

**Step 0: (Recommended)**

  - Create a new conda environment as a sandbox:`conda create -n name_of_env python=3 ipython`

  - Activate this environment: `source activate name_of_env`

**Step 1: Installation**

Install with pure git:
  - Clone both repo: `xpdAcq` and `xpdSim`. After clone, there should be two separate directories in your computer
  - Navigate to each directory and run `python setup.py develop`

Install with conda:
  - Under your sandbox environment, type: `conda install -c cl3077 xpdacq xpdsim`
  
**Step 2: Testing**

  - Run `from bluesky.scans import Count` in python/ipython section. If no exception is raised, these simulators work.


**Step 3: Setting up working directories**
  - Under your conda environment with both `xpdacq` and `xpdsim` packeges properly installed, open an `ipython` section
  - In your ipython section, run `from xpdacq.start_beamtime import *` and then run `start_beamtime()`
  - Main working directory should be created under `home/user_name/xpdUser` and several sub-working directories will be created under main working directory.
  - Navigate to `xpdUser` directory by runnig `cd ~/xpdUser`
  - Now you are ready to run simulation
