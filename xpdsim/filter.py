import bluesky.examples as be


class FilterBank():
    def __init__(self, attenuations=None):
        if attenuations is None:
            attenuations = {'filter1': .5, 'filter2': .5, 'filter3': .5,
                            'filter4': .5}
        self.filter_list = []
        for k, v in attenuations.items():
            f = XRayFilter(k, {'rad': lambda x: x}, {'x': 0}, v)
            self.filter_list.append(f)
            setattr(self, k, f)

    def get_attenuation(self):
        totalAttenuation = 1
        for i in self.filter_list:
            totalAttenuation *= i.get_XRayFilter_attenuation()
        return totalAttenuation


class XRayFilter(be.Mover):
    def __init__(self, name, fields, initial_set, attenuation, **kwargs):
        self.attenuation = attenuation
        super().__init__(name, fields, initial_set, **kwargs)

    def get_XRayFilter_attenuation(self):
        position_info = self.read()
        position_info_subdict = position_info.get('rad')
        position_info_sub_subdict = position_info_subdict.get('value')
        if (position_info_sub_subdict == 0):
            return 1
        else:
            return self.attenuation


XRayFilterBankExample = FilterBank()
