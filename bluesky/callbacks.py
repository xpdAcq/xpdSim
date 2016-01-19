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


