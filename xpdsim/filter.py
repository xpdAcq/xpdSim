import bluesky.exammples as be


class FilterBank():
    def __init__(self, attenuations=None):
        if attenuations is None:
            attenuations = {'filter1': .5, 'filter2': .5, 'filter3': .5,
                            'filter4': .5}
        self.filter_list = []
        for k, v in attenuations.items():
            f = Filter(k, {'rad': lambda x: x}, {'x': 0}, v)
            self.filter_list.append(f)
            setattr(self, k, f)

    def getAttenuation(self):
        totalAttenuation = 1
        for i in self.filter_list:
            totalAttenuation *= filter.attenuation
        return totalAttenuation


class Filter(be.Mover):
    def __init__(self, name, fields, initial_set, attenuation, **kwargs):
        self.attenuation = attenuation
        super().__init__(name, fields, initial_set, **kwargs)

