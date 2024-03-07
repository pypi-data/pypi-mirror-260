"""
This file is part of eduworld package.

This is a main application window class with Canvas and board and etc

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
import time
import sys
from concurrent.futures import ThreadPoolExecutor

from .canvas import Canvas


class Application:
    """Defines an Tkinter application with canvas, board and other stuff"""

    def __init__(self, title=""):
        background = "gray75"
        window_width = 800
        window_height = 600
        self.initialized = False
        self.root: tk.Tk = tk.Tk()
        self.canvas: Canvas = Canvas(self.root)
        self.root.title("AlgoWorld" if title == "" else f"AlgoWorld-{title}")
        self.root.configure(background=background)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.bind("<Q>", lambda _: self._quit())
        self.root.bind("<q>", lambda _: self._quit())

    def set_board(self, board):
        """Set canvas's board"""
        self.canvas.board = board
        self.initialized = board.initialized

    def _quit(self):
        self.root.quit()
        self.root.quit()

    def run(self) -> None:
        """Runs tkinter TK main loop in a separate thread, to allow
        this main thread to continue the work.
        You have ot call app.shutdown() function to keep the window open
        when your code done its work"""
        if not self.initialized:
            print("Board is not initialized! Exiting!")
            sys.exit(1)
        with ThreadPoolExecutor(max_workers=1) as ex:
            ex.submit(self.root.mainloop)
        self.canvas.redraw()
        self.root.update()
        time.sleep(1)

    def shutdown(self, keep_window: bool = False) -> None:
        """Join tkinter Tk mainloop to the main thread to keep the window open"""
        if keep_window:
            self.root.mainloop()
        else:
            time.sleep(3)
