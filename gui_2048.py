import tkinter as tk

# Background and grid properties
GRID_PADDING = 10
TILE_SIZE = 100

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {   2:"#eee4da", 4:"#ede0c8", 8:"#f2b179", 16:"#f59563", \
                            32:"#f67c5f", 64:"#f65e3b", 128:"#edcf72", 256:"#edcc61", \
                            512:"#edc850", 1024:"#edc53f", 2048:"#edc22e" }
CELL_COLOR_DICT = { 2:"#776e65", 4:"#776e65", 8:"#f9f6f2", 16:"#f9f6f2", \
                    32:"#f9f6f2", 64:"#f9f6f2", 128:"#f9f6f2", 256:"#f9f6f2", \
                    512:"#f9f6f2", 1024:"#f9f6f2", 2048:"#f9f6f2" }
FONT = ("Verdana", 40, "bold")

KEY_UP = 'Up'
KEY_DOWN = 'Down'
KEY_LEFT = 'Left'
KEY_RIGHT = 'Right'

# Directions
DIR_DICT = {KEY_UP: 1, KEY_DOWN: 2, KEY_LEFT: 3, KEY_RIGHT: 4}


class GameGrid(tk.Tk):
    """
    Class to run game GUI.
    """

    def __init__(self, game):
        super().__init__()
        self._game = game
        self._rows = game.get_grid_height()
        self._cols = game.get_grid_width()
        self._width = TILE_SIZE + TILE_SIZE * self._cols
        self._height = TILE_SIZE + TILE_SIZE * self._rows
        self.title('2048')
        self.bind("<Key>", self.key_down)

        self._grid_cells = []
        self.init_grid()
        self.update_grid()

        self.mainloop()

    def init_grid(self):
        """
        Construct the backbone grid with empty cells
        """
        background = tk.Frame(master=self, bg=BACKGROUND_COLOR_GAME, width=self._width, height=self._height)
        background.grid()
        for i in range(self._rows):
            row_cells = []
            for j in range(self._cols):
                cell = tk.Frame(master=background, width=self._width/TILE_SIZE, height=self._height/TILE_SIZE)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                num_label = tk.Label(master=cell, bg=BACKGROUND_COLOR_CELL_EMPTY, justify=tk.CENTER, font=FONT, width=4, height=2)
                num_label.pack()
                row_cells.append(num_label)

            self._grid_cells.append(row_cells)

    def key_down(self, event):
        """
        Keydown handler
        Read the input arrow key stroke and pass the corresponding direction variable into the game object.
        After grid cells being moved and new cell being added, check the game status and display 'Win' or 'Lose' if necessary
        """
        game = self._game
        if game.get_game_status() != game.GAME_STATUS['CONTINUE']:
            return

        key = event.keysym
        if key in DIR_DICT:
            game.move(DIR_DICT[key])
            self.update_grid()
            if game.get_game_status() == game.GAME_STATUS['WIN']:
                self._grid_cells[1][1].configure(text='You', bg=BACKGROUND_COLOR_CELL_EMPTY)
                self._grid_cells[1][2].configure(text='Win!', bg=BACKGROUND_COLOR_CELL_EMPTY)
            if game.get_game_status() == game.GAME_STATUS['LOSE']:
                self._grid_cells[1][1].configure(text='You', bg=BACKGROUND_COLOR_CELL_EMPTY)
                self._grid_cells[1][2].configure(text='Lose!', bg=BACKGROUND_COLOR_CELL_EMPTY)

    def update_grid(self):
        """
        Update the gui grid cells according to the game grid
        """
        for i in range(self._rows):
            for j in range(self._cols):
                tile = self._game.get_tile(i, j)
                if tile == 0:
                    self._grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self._grid_cells[i][j].configure(text=str(tile), bg=BACKGROUND_COLOR_DICT[tile], fg=CELL_COLOR_DICT[tile])
        self.update_idletasks()

    def start(self):
        self._game.reset()


def run_gui(game):
    """
    Instantiate and run the GUI.
    """
    gui = GameGrid(game)
    gui.start()
