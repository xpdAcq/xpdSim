#!/usr/bin/env python
##############################################################################
#
# xpdsim            by Billinge Group
#                   Simon J. L. Billinge sb2896@columbia.edu
#                   (c) 2016 trustees of Columbia University in the City of
#                        New York.
#                   All rights reserved
#
# File coded by:    Simon Billinge
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################
import os
from xpdacq.config import DataPath
from xpdacq.beamtimeSetup import _make_clean_env
from simulator.areadetector import AreaDetector

WORKING_DIR = 'xpdUser'
B_DIR = os.getcwd()
datapath = DataPath(B_DIR)
pe1c = AreaDetector(0.1)

_make_clean_env(datapath)

# try and find our way to the right directory
#if os.path.isdir(bt.datapath.base):
    #print('moving to ' + bt.datapath.base) 
    #os.chdir(bt.datapath.base)
#else:
    # this logic could be better, but I was running out of time. Fix later if
    # necessary
    #print('in '+os.getcwd())
    #print('type pwd to check your current directory')
    #print('the current directory should be /yourpath/'+ WORKING_DIR)
    #print('if it is not, please move there manually and rerun loadsim\n')

print('Initializing the XPD data acquisition simulation environment') 

'''
print('Flush directories under simulation tree')
datapath = DataPath('./')
for dir in datapath.allfolders:
    try:
        flush_dir(dir)
    except FileNotFoundError:
        print(dir + ' error')
        pass

os.chdir(datapath.base)
print('\n')
'''

print('OK, ready to go.  To continue, follow the steps in the xpdAcq')
print('documentation at http://xpdacq.github.io/xpdacq')
        

