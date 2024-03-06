r"""This is a simple interactive demo program

WSAD to move robot
E to paint tile with random color
F to put the beeper
R to pick up the beeper
Q to quit"""

from eduworld.simple import setup, shutdown


setup(world="demo-world", interactive=True)
shutdown(keep_window=True)
