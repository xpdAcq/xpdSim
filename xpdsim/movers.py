from ophyd.sim import SynAxis

# NOTE: device field name has been deprecated. The readback field is
# default to device name for all devices.
#shutter_read_field = 'rad'
#temp_controller_read_field = 'temperature'

cs700 = SynAxis(name='cs700', value=300)
shctl1 = SynAxis(name='shctl1', value=0)
