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

class AcqT():
    def __init__(self):
        pass
    
    def put(self):
        pass    
        
class Cam(AcqT):
    def __init__(self,time):
        self.acquire_time = time       
        #self = collections.namedtuple('cam',['acquire_time'])
 
#cam = Cam(0.5)        
#

class AreaDetector(Cam):
    ''' fake area detector class '''
    def __init__(self, cam, name):
        import collections
        self.name = name
        self.cam = cam
        print('name of detector = %s' % self.name)
        print('acquire_time of %s is %s' % (name, self.cam.acquire_time))

#self.cam.acquire_time.put()
    
