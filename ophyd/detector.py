## fake detector objects

class AreaDetector(object):
    ''' fake area detector class '''
    def __init__(self, name, time = 0.5):
        self.name = name
        print('name of detector = %s' % name)
        self.acquire_time = time
        print('acquire_time of %s is %s' % (name, time))
