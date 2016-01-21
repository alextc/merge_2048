"""
Clone of 2048 game.
"""

import unittest
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def merge_step1(lst):
    '''
    Implements step1 of the merge algorithm by moving all zeros to the end
    '''
    return [element for element in lst if element != 0] + [element for element in lst if element == 0]


def merge_step2(lst):
    '''
    Implements step2 of the merge algorithm by merging tiles with identical value
    '''
    result = []
    merged = False
    for idx in range(len(lst)):
        if merged:
            merged = False
            continue
        elif idx < (len(lst) - 1) and lst[idx] == lst[idx+1]:
            result.append(lst[idx]*2)
            result.append(0)
            merged = True
        else:
            result.append(lst[idx])
            merged = False

    return result


def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    step_1_result = merge_step1(line)
    step_2_result = merge_step2(step_1_result)
    step_3_result = merge_step1(step_2_result)
    return step_3_result


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid = [[]]
        self._grid_width = grid_width
        self._grid_height = grid_height

        self._initial_tiles = {UP: [], DOWN: [], LEFT: [], RIGHT: []}
        self.init_initial_tiles()

        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for col in range(self._grid_width)] for row in range(self._grid_height)]
        self.new_tile()
        self.new_tile()

    def init_initial_tiles(self):
        """
        Function that initializes the initial tiles lists
        :return:
        """
        for idx in range(self.get_grid_width()):
            self._initial_tiles[UP].append((0, idx))

        for idx in range(self.get_grid_width()):
            self._initial_tiles[DOWN].append((self.get_grid_height() - 1, idx))

        for idx in range(self.get_grid_height()):
            self._initial_tiles[LEFT].append((idx, 0))

        for idx in range(self.get_grid_height()):
            self._initial_tiles[RIGHT].append((idx, self.get_grid_width() - 1))

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        result = "["
        for row in range(self.get_grid_height()):
            if row == 0:
                result += str(self._grid[row]) + '\n'
            else:
                result += " " + str(self._grid[row]) + '\n'
        result = result[:-1] + "]"
        return result

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        initial_tiles = self._initial_tiles[direction]
        offset = OFFSETS[direction]
        if direction == UP or direction == DOWN:
            number_of_steps = self.get_grid_height()
        else:
            number_of_steps = self.get_grid_width()

        merge_happened = False
        for tile in initial_tiles:
            slice_to_merge = self.get_slice(tile, offset, number_of_steps)
            merged_slice = merge(slice_to_merge)
            if slice_to_merge != merged_slice:
                merge_happened = True
            self.apply_merges(merged_slice, tile, offset)

        if merge_happened:
            self.new_tile()

    def get_slice(self, start_cell, offset, num_steps):
        """
        Function that iterates through the cells in a grid
        in a linear direction

        Both start_cell is a tuple(row, col) denoting the
        starting cell

        direction is a tuple that contains difference between
        consecutive cells in the traversal
        """

        slice_to_merge = []
        for step in range(num_steps):
            row = start_cell[0] + step * offset[0]
            col = start_cell[1] + step * offset[1]
            slice_to_merge.append(self._grid[row][col])

        return slice_to_merge

    def apply_merges(self, merged_list, start_cell, offset):
        """
        Function that applies merged lists back into the grid
        :param merged_list:
        :param start_cell:
        :param offset:
        :return:
        """
        for step in range(len(merged_list)):
            row = start_cell[0] + step * offset[0]
            col = start_cell[1] + step * offset[1]
            self._grid[row][col] = merged_list[step]

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        if self.is_grid_full():
            return

        digit = self.get_two_or_four()

        while True:
            random_row = random.randint(0, self.get_grid_height() - 1)
            random_col = random.randint(0, self.get_grid_width() - 1)
            if self._grid[random_row][random_col] == 0:
                self._grid[random_row][random_col] = digit
                return

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

    def get_two_or_four(self):
        """
        Function that randomly selects 2 or 4 based on the 0.9 and 0.1 distribution
        :return:
        """
        distribution = [(2, 0.1), (4, 0.9)]
        random_float_between_0_and_1 = random.random()
        threshold = 0
        for item, prob in distribution:
            threshold += prob
            if threshold >= random_float_between_0_and_1:
                return item
        return item

    def is_grid_full(self):
        """
        Function that checks if the grid is full - no zeros left
        :return:
        """
        for row in range(self.get_grid_height()):
            for col in range(self.get_grid_width()):
                if self._grid[row][col] == 0:
                    return False
        return True


class TwentyFortyEightTests(unittest.TestCase):
    def test_must_return_str_representation_of_the_grid(self):
        sut = str(TwentyFortyEight(4,4))
        print sut

    def test_is_grid_full_should_return_true_when_no_zeros_exist(self):
        sut = TwentyFortyEight(4,4)
        for i in range(sut.get_grid_height()):
            for j in range(sut.get_grid_width()):
                sut._grid[i][j] = 1
        self.assertTrue(sut.is_grid_full())

    def test_is_grid_full_should_return_false_at_least_one_zeros_exist(self):
        sut = TwentyFortyEight(4,4)
        for i in range(sut.get_grid_height()):
            for j in range(sut.get_grid_width()):
                sut._grid[i][j] = 1
        sut.set_tile(0, 0, 0)
        self.assertFalse(sut.is_grid_full())

    def test_should_return_first_up_slice(self):
        sut = TwentyFortyEight(4,4)
        sut.set_tile(0, 0, 0)
        sut.set_tile(1, 0, 1)
        sut.set_tile(2, 0, 2)
        sut.set_tile(3, 0, 3)
        result = sut.get_slice((0, 0), OFFSETS[UP], sut.get_grid_height())
        self.assertEquals(result, [0, 1, 2, 3])

    def test_should_execute_up_move(self):
        sut = TwentyFortyEight(4,4)
        sut.set_tile(0, 0, 2)
        sut.set_tile(1, 0, 2)
        sut.set_tile(2, 0, 0)
        sut.set_tile(3, 0, 0)

        sut.move(UP)

        self.assertEquals(sut.get_tile(0,0), 4)

    def test_should_execute_up_move_owl(self):
        obj = TwentyFortyEight(4, 4)
        obj.set_tile(0, 0, 2)
        obj.set_tile(0, 1, 0)
        obj.set_tile(0, 2, 0)
        obj.set_tile(0, 3, 0)
        obj.set_tile(1, 0, 0)
        obj.set_tile(1, 1, 2)
        obj.set_tile(1, 2, 0)
        obj.set_tile(1, 3, 0)
        obj.set_tile(2, 0, 0)
        obj.set_tile(2, 1, 0)
        obj.set_tile(2, 2, 2)
        obj.set_tile(2, 3, 0)
        obj.set_tile(3, 0, 0)
        obj.set_tile(3, 1, 0)
        obj.set_tile(3, 2, 0)
        obj.set_tile(3, 3, 2)
        obj.move(UP)
        '''
         [[2, 2, 2, 2]
        [0, 0, 0, 0]
        [0, 0, 0, 0]
        [0, 0, 0, 0]]
        '''
        print obj

    def test_should_execute_move_right_owl(self):
        obj = TwentyFortyEight(4, 4)
        obj.set_tile(0, 0, 2)
        obj.set_tile(0, 1, 0)
        obj.set_tile(0, 2, 0)
        obj.set_tile(0, 3, 0)
        obj.set_tile(1, 0, 0)
        obj.set_tile(1, 1, 2)
        obj.set_tile(1, 2, 0)
        obj.set_tile(1, 3, 0)
        obj.set_tile(2, 0, 0)
        obj.set_tile(2, 1, 0)
        obj.set_tile(2, 2, 2)
        obj.set_tile(2, 3, 0)
        obj.set_tile(3, 0, 0)
        obj.set_tile(3, 1, 0)
        obj.set_tile(3, 2, 0)
        obj.set_tile(3, 3, 2),
        obj.move(RIGHT)
        print obj
        '''
        expected
        [[0, 0, 0, 2]
         [0, 0, 0, 2]
         [0, 0, 0, 2]
         [0, 0, 0, 2]]
         '''

    def test_should_execute_move_left_owl(self):
        obj = TwentyFortyEight(4, 4)
        obj.set_tile(0, 0, 2)
        obj.set_tile(0, 1, 0)
        obj.set_tile(0, 2, 0)
        obj.set_tile(0, 3, 0)
        obj.set_tile(1, 0, 0)
        obj.set_tile(1, 1, 2)
        obj.set_tile(1, 2, 0)
        obj.set_tile(1, 3, 0)
        obj.set_tile(2, 0, 0)
        obj.set_tile(2, 1, 0)
        obj.set_tile(2, 2, 2)
        obj.set_tile(2, 3, 0)
        obj.set_tile(3, 0, 0)
        obj.set_tile(3, 1, 0)
        obj.set_tile(3, 2, 0)
        obj.set_tile(3, 3, 2)
        obj.move(LEFT)
        print obj
        '''
        expected
        [[2, 0, 0, 0]
         [2, 0, 0, 0]
         [2, 0, 0, 0]
         [2, 0, 0, 0]]
        '''

    def test_should_execute_move_right_owl(self):
        obj = TwentyFortyEight(4, 4)
        obj.set_tile(0, 0, 2)
        obj.set_tile(0, 1, 0)
        obj.set_tile(0, 2, 0)
        obj.set_tile(0, 3, 0)
        obj.set_tile(1, 0, 0)
        obj.set_tile(1, 1, 2)
        obj.set_tile(1, 2, 0)
        obj.set_tile(1, 3, 0)
        obj.set_tile(2, 0, 0)
        obj.set_tile(2, 1, 0)
        obj.set_tile(2, 2, 2)
        obj.set_tile(2, 3, 0)
        obj.set_tile(3, 0, 0)
        obj.set_tile(3, 1, 0)
        obj.set_tile(3, 2, 0)
        obj.set_tile(3, 3, 2)
        obj.move(RIGHT)
        print obj
        '''
        expected
        [[0, 0, 0, 2]
         [0, 0, 0, 2]
         [0, 0, 0, 2]
         [0, 0, 0, 2]]
         '''

    def test_should_execute_move_up_owl_2(self):
        obj = TwentyFortyEight(4, 5)
        obj.set_tile(0, 0, 8)
        obj.set_tile(0, 1, 16)
        obj.set_tile(0, 2, 8)
        obj.set_tile(0, 3, 16)
        obj.set_tile(0, 4, 8)
        obj.set_tile(1, 0, 16)
        obj.set_tile(1, 1, 8)
        obj.set_tile(1, 2, 16)
        obj.set_tile(1, 3, 8)
        obj.set_tile(1, 4, 16)
        obj.set_tile(2, 0, 8)
        obj.set_tile(2, 1, 16)
        obj.set_tile(2, 2, 8)
        obj.set_tile(2, 3, 16)
        obj.set_tile(2, 4, 8)
        obj.set_tile(3, 0, 16)
        obj.set_tile(3, 1, 8)
        obj.set_tile(3, 2, 16)
        obj.set_tile(3, 3, 8)
        obj.set_tile(3, 4, 16)
        obj.move(UP)
        print obj
        '''
        expected
        [[8, 16, 8, 16, 8]
        [16, 8, 16, 8, 16]
        [8, 16, 8, 16, 8]
        [16, 8, 16, 8, 16]]
        '''

    def test_should_execute_move_down_owl(self):
        obj = TwentyFortyEight(4, 4)
        obj.set_tile(0, 0, 4)
        obj.set_tile(0, 1, 4)
        obj.set_tile(0, 2, 4)
        obj.set_tile(0, 3, 4)
        obj.set_tile(1, 0, 4)
        obj.set_tile(1, 1, 0)
        obj.set_tile(1, 2, 0)
        obj.set_tile(1, 3, 4)
        obj.set_tile(2, 0, 4)
        obj.set_tile(2, 1, 0)
        obj.set_tile(2, 2, 0)
        obj.set_tile(2, 3, 4)
        obj.set_tile(3, 0, 4)
        obj.set_tile(3, 1, 4)
        obj.set_tile(3, 2, 4)
        obj.set_tile(3, 3, 4)
        obj.move(DOWN)
        print obj
        '''
        expected
        [[0, 0, 0, 0]
         [0, 0, 0, 0]
         [8, 0, 0, 8]
         [8, 8, 8, 8]]
         '''

    def test_should_execute_move_up_owl_3(self):
        obj = TwentyFortyEight(4, 4)
        obj.set_tile(0, 0, 2)
        obj.set_tile(0, 1, 4)
        obj.set_tile(0, 2, 8)
        obj.set_tile(0, 3, 16)

        obj.set_tile(1, 0, 16)
        obj.set_tile(1, 1, 8)
        obj.set_tile(1, 2, 4)
        obj.set_tile(1, 3, 2)

        obj.set_tile(2, 0, 0)
        obj.set_tile(2, 1, 0)
        obj.set_tile(2, 2, 8)
        obj.set_tile(2, 3, 16)

        obj.set_tile(3, 0, 0)
        obj.set_tile(3, 1, 0)
        obj.set_tile(3, 2, 4)
        obj.set_tile(3, 3, 2)
        obj.move(UP)
        print obj
        '''
        expected
        [[2, 4, 8, 16]
        [16, 8, 4, 2]
        [0, 0, 8, 16]
        [0, 0, 4, 2]]
        '''

if __name__ == '__main__':
    unittest.main()
