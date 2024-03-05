from eduworld.simple import setup, shutdown, up, down, left, right, put

setup(world="demo-world")

up()
left()
down()
right()
put()

shutdown(keep_window=True)
