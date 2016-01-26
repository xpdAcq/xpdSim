#!/usr/bin/env python
##############################################################################
#
# xpdsim            by Billinge Group
#                   Simon J. L. Billinge sb2896@columbia.edu
#                   (c) 2016 trustees of Columbia University in the City of
#                        New York.
#                   All rights reserved
#
# File coded by:    Timothy Liu
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################
import sys
import os.path


def _make_datapaths():
    '''Create all data directories if they do not exist yet.
    '''
    from xpdacq.config import datapath
    for d in datapath.allfolders:
        if os.path.isdir(d):
            continue
        os.mkdir(d)
    print('Working directories have been created:')
    print(datapath.allfolders, sep='\n')
    return


def _ensure_empty_datapaths():
    '''Raise RuntimeError if datapath.base has any file except those expected.
    '''

    from xpdacq.config import datapath
    allowed = set(datapath.allfolders)
    spurious = []
    # collect spurious files or directories within the base folder
    for r, dirs, files in os.walk(datapath.base):
        for d in dirs:
            if os.path.join(r, d) not in allowed:
                spurious.append(d)
            # all files are spurious
        spurious += [os.path.join(r, f) for f in files]
    if spurious:
        emsg = 'The working directory {} has unknown files:{}'.format(
                datapath.base, "\n  ".join([''] + spurious))
        raise RuntimeError(emsg)
    return

def start_beamtime():
    """ start_beamtime function

        setting up working directories in local computer

    Parameters
    -----------


    Returns
    --------
    None
        creates directory, nothing will return

    """
    _make_datapaths()
    _ensure_empty_datapaths()
    print('Everything is ready to begin.\nPlease continue with icollection.')
    return


if __name__ == '__main__':
    try:
        start_beamtime()
    except RuntimeError as e:
        print(e, file=sys.stderr)
        print("Ask beamline scientist what to do next.", file=sys.stderr)
        sys.exit(1)
