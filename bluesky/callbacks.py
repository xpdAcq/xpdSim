#!/usr/bin/env python
##############################################################################
#
# callbacks         by Billinge Group
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
## fake callback module, mostly following the original strucutre
class CallbackBase(object):
    def __init__(self):
        super().__init__()

class LiveTable(CallbackBase):
    def __init__(self):
        print('hook LiveTable')
        return

class LivePlot(CallbackBase):
    def __init__(self):
        print('hook LivePlot')
        return


