from ..robot import Robot
import bluesky.examples as be


def test_robot():
    th = be.Mover('theta', {'theta': lambda x: x}, {'x': 0})
    robot = Robot('XF:28IDC-ES:1{SM}', theta=th)
    # Crashes : Cannot find Epics CA DLL, but taken from Robot API reference
    # file?
# What features of the robot should be tested ?
