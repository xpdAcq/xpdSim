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
from xpdacq.beamtimeSetup import *
from ophyd.detector import AreaDetector

WORKING_DIR = 'xpdUser'

B_DIR = './'   # this overloads the value loaded from config. Be careful, it will be set back if xpdacq.config is reloaded.
pe1c = AreaDetector('pe1c')

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

# initialization is done by start_beamtime
start_beamtime('./')

# samll trick to properly change dir
os.chdir('..')

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

print('OK, ready to go.  To continue, follow the steps in the xpdAcq')
print('documentation at http://xpdacq.github.io/xpdacq')
        

