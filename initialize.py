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
'''module to initialize the directories for a local simulation of and XPD session
'''
import os


def initialize():
    '''creates the environment for an xpd simulation
    
    checks for the presence of ./xpdUser and ./xpdConfig directories
    if absent it creates them.  If present it leaves them in the current state.
    '''
    from xpdacq.config import WORKING_DIR, CONFIG_DIR
    STEM = './'
        
    if os.path.isdir(STEM+WORKING_DIR):
        print(STEM+WORKING_DIR+' already exists.  Leaving it.')
    else:
        os.mkdir(STEM+WORKING_DIR)
        print(STEM+WORKING_DIR+' created.  Ready to play.')
    
    if os.path.isdir(STEM+CONFIG_DIR):
        print(STEM+CONFIG_DIR+' already exists.  Leaving it.')
    else:
        os.mkdir(STEM+CONFIG_DIR)
        print(STEM+CONFIG_DIR+' created.  Ready to play.')

        
    # now move to xpdUser and create the Import and Export directories
    os.chdir(STEM+WORKING_DIR)
    # copy the ipython_profile file to the current directory
    # [fixme]
    os.mkdir('Import')
    os.mkdir('Export')
    
    print('to get going type ipython')
    print('when ipython starts type import loadsim')
        
    print('simulation environment initialized.\n')

if __name__ == '__main__':
    try:
        initialize()
    except RuntimeError as e:
        print(e, file=sys.stderr)
        print("Ask beamline scientist what to do next.", file=sys.stderr)
        sys.exit(1)
