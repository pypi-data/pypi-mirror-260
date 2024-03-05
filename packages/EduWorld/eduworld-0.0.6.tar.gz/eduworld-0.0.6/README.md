# EduWorld

`EduWorld` is an educational `python` package designed for students to learn computational thinking, algorithms, and other basic programming concepts. Through this process they learn how to divide a problem into smaller steps and refine them; to abstract; to recognize patterns; and to design and implement algorithms;

See the `eduworld.sample` package for the list of the available procedural commands

## Simple procedural sample

```
import eduworld.simple


init(world="demo-world", x=3, y=4, beepers=2)

up()
put()
left()
put()
down()
right()

shutdown()
```


## Oop style sample

This sample is not as polished as simple version listed above, and not the final version

```
from eduworld import Application, Board, AlgoWorldBoard, Robot


app: Application = Application()
board: Board = AlgoWorldBoard("demo-world")
app.set_board(board)

r: Robot = Robot(app.canvas)
r.setup(x=5, y=5, beepers=2)
board.add_robot(r)
app.run()


r.put()
r.right()
r.put()
r.right()

r.left()
r.pickup()
r.left()
r.pickup()

a.shutdown()
```
