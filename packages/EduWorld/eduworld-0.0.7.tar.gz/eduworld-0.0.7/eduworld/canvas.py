r"""
This file is part of eduworld package.

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

import tkinter as tk

from .tile import Tile
from .robot import Robot

PADDING = 20


# pylint: disable=too-many-ancestors, too-many-instance-attributes
class Canvas(tk.Canvas):
    """Class for drawing the board (with all the stuff) and robots"""

    def __init__(self, parent):
        super().__init__(parent, width=320, height=240, background="gray90")
        self.root = parent
        self.cell_size = 0
        self.half_cell = 0
        self.x_left = 0
        self.y_top = 0
        self.x_right = 0
        self.y_bottom = 0
        self.board = None
        self.grid(column=0, row=0, sticky="NEWS")
        self.bind("<Configure>", lambda _: self.redraw())

    def redraw(self) -> None:
        """Redraw the board and the robots on window resize"""
        if self.board is None or not self.board.initialized:
            return
        self._delete_all()
        self._calculate_cell_size()
        self._draw_tiles()
        self._draw_robots()
        self._draw_border()
        self._draw_box_numbers()
        self.root.update()

    def _delete_all(self):
        self.delete("numbers")
        self.delete("wall")
        self.delete("cell")
        self.delete("beeper")

    def _draw_box_numbers(self):
        self._draw_xy_text()
        self._draw_row_numbers()
        self._draw_col_numbers()

    def _draw_xy_text(self):
        qc = self.half_cell * 0.5
        x = self.x_left
        y = self.y_top
        tags = ("numbers",)
        self.create_text(x - qc, y, text=r"y", font="Mono 12 bold", tags=tags)
        self.create_text(x, y - qc, text=r"x", font="Mono 12 bold", tags=tags)

    def _draw_col_numbers(self):
        y = self.y_top - self.half_cell * 0.5
        x_shift = self.half_cell
        tags = ("numbers",)
        for c in range(0, self.board.ncols):
            x = self.x_left + self.cell_size * c + x_shift
            self.create_text(x, y, text=str(c + 1), font="Mono 12 bold", tags=tags)

    def _draw_row_numbers(self):
        x = self.x_left - self.half_cell * 0.5
        y_shift = self.half_cell * 0.95
        tags = ("numbers",)
        for r in range(0, self.board.nrows):
            y = self.y_top + self.cell_size * r + y_shift
            self.create_text(x, y, text=str(r + 1), font="Mono 12 bold", tags=tags)

    def _draw_tiles(self):
        """Draw board tiles"""
        for y in range(1, self.board.nrows + 1):
            dy = (y - 1) * self.cell_size + self.y_top
            for x in range(1, self.board.ncols + 1):
                dx = (x - 1) * self.cell_size + self.x_left
                tile: Tile = self.board.tiles[x, y]
                self._draw_cell(tile, dx, dy)
                self._draw_walls(tile, dx, dy)
                if tile.has_beepers():
                    self._draw_beepers(tile, dx, dy)
                    self._draw_beeper_text(tile, dx, dy)

    def _draw_beepers(self, tile, shift_x, shift_y) -> None:
        r"""Draw beeper outline
        0+shift         x (cell_size) + shift
        +---------------+
        | os+innr_shft  |  os - oval start (x, y)
        |   + _-=-_     |  oe - oval end   (x, y)
        |    /     \    |
        |   |-diam--|   |  diam - oval diameter
        |    \     /    |  innr_shft = cell_size - od
        |     --=-- +   |
        |           oe  |
        +---------------+
        y (cell_size) + shift
        """
        name = f"b-{tile.x}-{tile.y}"
        diam = self.cell_size * 0.85
        ishift = self.cell_size - diam
        os = [shift_x + ishift, shift_y + ishift]
        oe = [shift_x + diam, shift_y + diam]
        c = os + oe
        tags = ("beeper", name)
        self.create_oval(c, width=2, outline="black", fill="gray95", tags=tags)

    def _draw_beeper_text(self, tile, shift_x, shift_y) -> None:
        name = f"b-{tile.x}-{tile.y}-t"
        hc_x = self.half_cell + shift_x
        hc_y = self.half_cell + shift_y
        tags = ("beeper", name)
        count = "*" if tile.beepers == -1 else str(tile.beepers)
        self.create_text(hc_x, hc_y, text=count, font="Mono 12 bold", tags=tags)

    def _draw_walls(self, tile: Tile, shift_x, shift_y) -> None:
        """Draw cell walls.
        mall cross in the center of the cell
        coordinates are relative to the cell_size
          0+shift         x (cell_size) + shift
          +===============+
          H               H
          H               H
          H               H
          H       +       H
          H               H
          H               H
          H               H
          +===============+
          y (cell_size) + shift
        """
        wall_width = 6
        hw = wall_width / 2

        wall_x_len = shift_x + self.cell_size + hw
        wall_y_len = shift_y + self.cell_size + hw
        tag = ("wall",)

        if tile.top_is_wall():
            coords = [shift_x - hw, shift_y, wall_x_len, shift_y]
            self.create_line(coords, width=wall_width, tags=tag)
        if tile.bottom_is_wall():
            bottom_y = shift_y + self.cell_size
            coords = [shift_x - hw, bottom_y, wall_x_len, bottom_y]
            self.create_line(coords, width=wall_width, tags=tag)
        if tile.left_is_wall():
            coords = [shift_x, shift_y - hw, shift_x, wall_y_len]
            self.create_line(coords, width=wall_width, tags=tag)
        if tile.right_is_wall():
            right_x = shift_x + self.cell_size
            coords = [right_x, shift_y - hw, right_x, wall_y_len]
            self.create_line(coords, width=wall_width, tags=tag)

    def _draw_cell(self, tile, shift_x, shift_y):
        r"""Create cell background with small cross in the center of the cell
        coordinates are relative to the cell_size
        shift     hc      x (cell_size) + shift
          +-------|-------+
          |       |       |
          |               |
          |       |  ---------\  line_start
        hc----  --+--     |   ~  line_length
          |       |  ---------/  line_end
          |               |
          |               |
          +---------------+
          y (cell_size) + shift
        """
        tags = ("cell",)
        line_length = 0.15 * self.cell_size
        pad = 0.05 * self.cell_size
        hc_x = self.half_cell + shift_x
        hc_y = self.half_cell + shift_y
        line_start_x = (self.cell_size - line_length) / 2 + shift_x
        line_end_x = line_start_x + line_length
        line_start_y = (self.cell_size - line_length) / 2 + shift_y
        line_end_y = line_start_y + line_length
        cross = [line_start_x, hc_y, line_end_x, hc_y]  # horizontal
        cross += [hc_x, hc_y]  # center
        cross += [hc_x, line_start_y, hc_x, line_end_y]  # vertical
        rect = [
            shift_x + pad,
            shift_y + pad,
            shift_x + self.cell_size - pad,
            shift_y + self.cell_size - pad,
        ]
        self.create_rectangle(rect, width=1, fill=tile.color, outline="", tags=tags)
        self.create_line(cross, width=1, fill="gray25", tags=tags)

    def _draw_border(self) -> None:
        """Draw border around the board to simulate the walled garden"""
        self.delete("border")
        coords = [self.x_left, self.y_top, self.x_right, self.y_bottom]
        self.create_rectangle(coords, width=6, tags=("border",))

    def _calculate_cell_size(self) -> None:
        """Calculate the w/h of the tile in pixels"""
        h_size = (self.winfo_height() - 2 * PADDING) / self.board.nrows
        w_size = (self.winfo_width() - 2 * PADDING) / self.board.ncols
        self.cell_size = min(h_size, w_size, 80)
        self.half_cell = self.cell_size / 2
        bw = self.cell_size * self.board.ncols
        bh = self.cell_size * self.board.nrows
        self.x_left = (self.winfo_width() - bw) / 2
        self.y_top = (self.winfo_height() - bh) / 2
        self.x_right = self.x_left + bw
        self.y_bottom = self.y_top + bh

    def _draw_robots(self):
        """Draw all robots"""
        for r in self.board.robots:
            if r.canvas is None:
                r.canvas = self
            self._draw_robot(r)

    def _draw_robot(self, r: Robot):
        """Draw robot on the canvas"""
        shift_x = (r.x - 1) * self.cell_size + self.x_left
        shift_y = (r.y - 1) * self.cell_size + self.y_top
        fill = r.color
        tag = (r.name,)
        coords = [0.3, 0, 0, 0.3, 0.3, 0.6, 0.6, 0.3]
        coords = [v * self.cell_size for v in coords]

        self.delete(r.name)
        self.create_polygon(coords, width=1, outline="gray25", fill=fill, tags=tag)
        self.moveto(r.name, shift_x, shift_y)
        self.move(r.name, self.cell_size * 0.18, self.cell_size * 0.18)
