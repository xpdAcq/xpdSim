import bluesky.examples as be

shctl1 = be.Mover('shctl1', {'rad': lambda x: x}, {'x': 0})
cs700 = be.Mover('cs700', {'temperature': lambda x: x}, {'x': 300})
