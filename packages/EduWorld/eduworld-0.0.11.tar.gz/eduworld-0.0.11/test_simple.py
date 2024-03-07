"""This is a simple demo program"""

from eduworld.simple import setup, shutdown, up, down, left, right, put

setup(world="demo-world")

up()
left()
put()
down()
right()

shutdown()
