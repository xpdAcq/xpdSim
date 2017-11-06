from ophyd.sim import SynAxis

cs700 = SynAxis(name='cs700', value=300)
cs700.readback.name = 'temperature'
shctl1 = SynAxis(name='shctl1', value=0)
shctl1.readback.name = 'rad'
