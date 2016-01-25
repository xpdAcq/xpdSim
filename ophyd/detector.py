#!/usr/bin/env python
##############################################################################
#
# detector          by Billinge Group
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
## fake detector objects

class AreaDetector(object):
    ''' fake area detector class '''
    def __init__(self, name, time = 0.5):
        self.name = name
        print('name of detector = %s' % name)
        self.acquire_time = time
        print('acquire_time of %s is %s' % (name, time))
