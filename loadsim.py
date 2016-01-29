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

from xpdacq import *
from xpdacq.config import WORKING_DIR, CONFIG_DIR

STEM = './'

# try and find our way to the right directory
if os.path.isdir(STEM+WORKING_DIR):
    print('moving to '+STEM+WORKING_DIR) 
    os.chdir(STEM+WORKING_DIR)
else:
    print('in '+os.getcwd())
    print('the current director should be '+WORKING_DIR)
    print('if it is not, please move there manually and rerun loadsim')

        

