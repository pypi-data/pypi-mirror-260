# oop version
from eduworld import Application, Board, AlgoWorldBoard, Robot

Robot.step_delay = 0.0

a: Application = Application()

# this can be substituted by world-gen class instead of file-reader based
b: Board = AlgoWorldBoard(world="demo-world")
a.set_board(board=b)

r: Robot = Robot(canvas=a.canvas)
r.setup(x=1, y=6, beepers=2)
b.add_robot(robot=r)

a.run()

r.put()
r.right()
r.put()
r.right()
r.paint(color="orange")

if r.tile_color() == "red":
    r.paint(color="green")

if r.tile_color() == "orange":
    r.paint(color="dodgerblue")

r.left()
r.pickup()
r.left()
r.pickup()

if r.down_is_wall():
    r.up()

# todo final pos validation (define it through world file ana validate on exit)
a.shutdown()
