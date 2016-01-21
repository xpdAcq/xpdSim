class Count(object):
    '''
    fake object but it needs to be able behave like Count([pe1], num=10)
    
    '''
    def __init__(self, detector, num=1):
        self.det = detector
        self.num = num

class Count2(object):
    '''
    testing...delete when done!
    
    '''
    def __init__(self, detector, num=1):
        self.det = detector
        self.num = num
