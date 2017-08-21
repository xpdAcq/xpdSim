import bluesky.examples as be

shutter_read_field = 'rad'
temp_controller_read_field = 'temperature'

shctl1 = be.Mover('shctl1', {shutter_read_field: lambda x: x}, {'x': 0})
cs700 = be.Mover('cs700', {temp_controller_read_field: lambda x: x},
                 {'x': 300})
