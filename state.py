"""

    State object allowing agent to easily keep
    track of the game board, the board score,
    as well as update node values and ucb_1
    values.

    The MCTS object back-propogates these scores.


"""


import math, random
import numpy as np


class State:

    def __init__(self, board_state, board_value, move=None):

        self.board_state = board_state
        self.board_value = board_value
        self.node_value = 0
        self.node_visits = 0
        self.ucb_1 = math.inf
        self.star = False
        self.move = move

    def __repr__(self):

        return f"State Object"

    def reset_state(self):

        self.board_state = [[-1, -1, -1, -1],
                            [-1, -1, -1, -1],
                            [-1, -1, -1, -1],
                            [-1, -1, -1, -1]]

        self.board_value = 0

    def set_star(self):

        self.star = True

    def drop_tile(self):

        # Access the random tile list every time we
        # drop a tile.

        from tile_list import tile_list

        rand_row = random.randint(0, 3)
        rand_col = random.randint(0, 3)
        tile = random.choice(tile_list)

        while self.board_state[rand_row][rand_col] != -1:

            rand_row = random.randint(0, 3)
            rand_col = random.randint(0, 3)

        self.board_state[rand_row][rand_col] = tile

    def get_board_state(self):

        return self.board_state

    def get_board_value(self):

        return self.board_value

    def set_node_value(self, value):

        self.node_value += value
        self.set_node_visits()

    def get_node_value(self):

        return self.node_value

    def set_node_visits(self):

        self.node_visits += 1

    def get_node_visits(self):

        return self.node_visits

    def set_ucb_1(self, parent_visits):

        if parent_visits == 0:

            self.ucb_1 = math.inf

        else:
                if self.node_visits == 0:
                    self.ucb_1 = math.inf
                else:
                    avg_value = self.node_value / self.node_visits
                    nat_log_par = np.log(parent_visits)
                    sqr_root_division = math.sqrt(nat_log_par/self.node_visits)
                    ucb_1 = avg_value + (750 * sqr_root_division)
                    self.ucb_1 = ucb_1

    def get_ucb_1(self):

        return self.ucb_1