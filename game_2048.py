# -*- coding: utf-8 -*-
import random
import gui_2048

# Directions
UP = 1
DOWN= 2
LEFT = 3
RIGHT = 4

# New tile values for new_tile() in calss TwentyFortyEight
NEW_VALUES = [2 for dummy_num in range(9)] + [4]

# Offsets for computing tile indices in each direction.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """

    # slide tiles in line towards left and store in slid_line
    # merge pairs of tiles that have same number and slide towards left again
    # store the result in merged_line
    slid_line = []
    merged_line = []
    for dummy_idx in line:
        slid_line.append(0)
        merged_line.append(0)

    count = 0
    for tile in line:
        if tile != 0:
            slid_line[count] = tile
            count += 1

    for idx in range(1, len(slid_line)):
        if slid_line[idx] == slid_line[idx - 1]:
            slid_line[idx - 1] *= 2
            slid_line[idx] = 0

    count = 0
    for tile in slid_line:
        if tile != 0:
            merged_line[count] = tile
            count += 1

    return merged_line


class TwentyFortyEight():
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        self._init_tiles = {}
        self._init_tiles[UP] = [(0, col) for col in range(self._width)]
        self._init_tiles[DOWN] = [(self._height - 1, col) for col in range(self._width)]
        self._init_tiles[LEFT] = [(row, 0) for row in range(self._height)]
        self._init_tiles[RIGHT] = [(row, self._width - 1) for row in range(self._height)]
        self.GAME_STATUS = {'WIN': 1, 'CONTINUE': 0, 'LOSE': -1}
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [ [0 for dummy_col in range(self._width)] for dummy_row in range(self._height)]
        self.new_tile()
        self.new_tile()
        self._status = self.GAME_STATUS['CONTINUE']

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        ret_str = ""
        for row in self._grid:
            ret_str += "["
            for tile in row:
                ret_str += str(tile) + ", "
            ret_str = ret_str[:-2] + "]\n"

        return ret_str[:-1]

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        empty_tiles = []
        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == 0:
                    empty_tiles.append( (row, col) )

        tile_pos = random.choice(empty_tiles)
        self._grid[tile_pos[0]][tile_pos[1]] = random.choice(NEW_VALUES)
        self.judge()

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

    def get_game_status(self):
        return self._status

    def judge(self):
        """
        Return winning message when there exist a 2048 tile
        Return
        """
        is_full = True
        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == 0:
                    is_full = False
                if self._grid[row][col] == 2048:
                    self._status = self.GAME_STATUS['WIN']

        if is_full == True:
            game_over = True
            # Check whether no chance to merge by moving UP/DOWN
            for col in range(self._width):
                for row in range(self._height-1):
                    if self._grid[row][col] == self._grid[row+1][col]:
                        game_over = False
            # Check whether no chance to merge by moving LEFT/RIGHT
            for row in range(self._height):
                for col in range(self._width-1):
                    if self._grid[row][col] == self._grid[row][col+1]:
                        game_over = False
            if game_over == True:
                self._status = self.GAME_STATUS['LOSE']
                print(self)

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        init_tiles = self._init_tiles[direction]
        offset = OFFSETS[direction]
        moved = False
        # Retreive tile values of each line in specified direction and store in temp list
        # for each temp list, merge it and save the merged line back into self._grid
        # if any tile moved, add a new tile
        for lead_tile in init_tiles:
            row = lead_tile[0]
            col = lead_tile[1]
            line = []
            while row >= 0 and row < self._height and col >= 0 and col < self._width:
                line.append(self._grid[row][col])
                row += offset[0]
                col += offset[1]

            line = merge(line)

            row = lead_tile[0]
            col = lead_tile[1]
            idx = 0
            while row >= 0 and row < self._height and col >= 0 and col < self._width:
                if self._grid[row][col] != line[idx]:
                    self._grid[row][col] = line[idx]
                    moved = True
                idx += 1
                row += offset[0]
                col += offset[1]

        if moved:
            self.new_tile()

gui_2048.run_gui(TwentyFortyEight(4, 4))
