# EduWorld

`EduWorld` is an educational `python` package designed for students to learn computational thinking, algorithms, and other basic programming concepts. Through this process they learn how to divide a problem into smaller steps and refine them; to abstract; to recognize patterns; and to design and implement algorithms;

See the `eduworld.sample` package for the list of the available procedural commands

## Interactive mode

```
from eduworld.simple import setup, shutdown


setup(world="demo-world", interactive=True)
shutdown(keep_window=True)

```

Command keys

* W - move up
* S - move down
* A - move left
* D - move right
* E - paint tile
* R - pickup beeper
* F - put beeper
* Q - quit

## Simple procedural sample

```
from eduworld.simple import setup, shutdown, up, down, left, right, put


setup(world="demo-world")

up()
left()
put()
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

r: Robot = board.get_default_robot()

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
