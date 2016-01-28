#!/usr/bin/env python
##############################################################################
#
# scans             by Billinge Group
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
class Count(object):
    '''
    fake object but it needs to be able behave like Count([pe1], num=10)
    
    '''
    def __init__(self, detector, num=1):
        self.det = detector
        self.num = num

class Count3(object):
    '''
    testing...delete when done!
    
    '''
    def __init__(self, detector, num=1):
        self.det = detector
        self.num = num
