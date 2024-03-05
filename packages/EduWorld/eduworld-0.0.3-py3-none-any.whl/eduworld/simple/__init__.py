r"""
This package provides the following functions defined in __all__ for writing
simple procedural style programs with AlgoWorld Robots

This file is part of eduworld package

=== LICENSE INFO ===

Copyright (c) 2024 - Stanislav Grinkov

The eduworld package is free software: you can redistribute it
and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3
of the License, or (at your option) any later version.

The package is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with the algoworld package.
If not, see `<https://www.gnu.org/licenses/>`_.
"""

import sys
import tkinter as tk
from eduworld import Application, AlgoWorldBoard, Robot

app: Application = Application()
r: Robot = Robot(app.canvas)
initialized: bool = False


def _hide_tk_err(f):
    def w(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except tk.TclError:
            sys.exit(1)

    return w


def step_delay(delay) -> None:
    """Set the delay between robot steps"""
    Robot.step_delay = min(max(0, delay), 2)


def setup(world: str, x: int, y: int, beepers: int = -1) -> None:
    """Setup the board and the robot"""
    global initialized
    if not initialized:
        initialized = True
        board = AlgoWorldBoard(world=world)
        app.set_board(board=board)
        r.setup(x=x, y=y, beepers=beepers)
        board.add_robot(robot=r)
        app.run()


def shutdown(keep_window: bool = False) -> None:
    """Shut down the app"""
    app.shutdown(keep_window)


@_hide_tk_err
def up() -> None:
    """Move default robot up"""
    r.up()


@_hide_tk_err
def down() -> None:
    """Move default robot down"""
    r.down()


@_hide_tk_err
def left() -> None:
    """Move default robot left"""
    r.left()


@_hide_tk_err
def right() -> None:
    """Move default robot right"""
    r.right()


@_hide_tk_err
def put() -> None:
    """Put beeper down"""
    r.put()


@_hide_tk_err
def pickup() -> None:
    """Pickup beeper"""
    r.pickup()


@_hide_tk_err
def paint(color: str = "tan2") -> None:
    """Paint tile with color"""
    r.paint(color=color)


def has_beepers() -> bool:
    """Test if robot has beepers"""
    return r.has_beepers()


def next_to_beeper() -> bool:
    """Test if tile the robot on has beepers"""
    return r.next_to_beeper()


def tile_color() -> str:
    """Return tile color"""
    return r.tile_color()


def tile_radiation() -> int:
    """Return tile radiation"""
    return r.tile_radiation()


def tile_temperature() -> int:
    """Return tile temperature"""
    return r.tile_temperature()


def up_is_wall() -> bool:
    """Test if up of robot is wall"""
    return r.up_is_wall()


def down_is_wall() -> bool:
    """Test if down of robot is wall"""
    return r.down_is_wall()


def left_is_wall() -> bool:
    """Test if left of robot is wall"""
    return r.left_is_wall()


def right_is_wall() -> bool:
    """Test if right of robot is wall"""
    return r.right_is_wall()


__all__ = [
    # setup
    "setup",
    "shutdown",
    "step_delay",
    # movement
    "up",
    "down",
    "left",
    "right",
    # check movement
    "up_is_wall",
    "down_is_wall",
    "left_is_wall",
    "right_is_wall",
    # color paint
    "tile_color",
    "paint",
    # beepers
    "put",
    "pickup",
    "has_beepers",
    "next_to_beeper",
    # other sensors
    "tile_radiation",
    "tile_temperature",
]
