import random
import math
from copy import deepcopy


MAX_PLAYER = 'max'
MIN_PLAYER = 'min'

MAX_PLAYER_SYMBOL = 'X'
MIN_PLAYER_SYMBOL = 'O'


class Node:
    def __init__(self, grid, player, children=[]):
        self.grid = grid
        self.children = children
        self.player = player

    @property
    def is_terminal(self):
        return len(self.children) == 0

    def count_empty_boxes(self):
        result = 0

        for row in self.grid:
            for box in row:
                if box is None:
                    result += 1

        return result

    def add_children(self):
        children_player = opposite_player(self.player)
        children = [
            Node(grid=move, player=children_player)
            for move in get_possible_moves(grid=self.grid, player=children_player)
        ]

        self.children = children

    def check_for_finish(self, symbol):
        for i, row in enumerate(self.grid):
            # horizontals
            if all(box == symbol for box in row):
                return True

            # verticals
            if all(row[i] == symbol for row in self.grid):
                return True

        # diagonals
        center_x, center_y = 1, 1
        if self.grid[center_x][center_y] != symbol:
            return False
        else:
            offset = 1
            left_diagonal_win =\
                self.grid[center_x - offset][center_y - offset] == symbol and\
                self.grid[center_x + offset][center_y + offset] == symbol

            right_diagonal_win =\
                self.grid[center_x - offset][center_y + offset] == symbol and\
                self.grid[center_x + offset][center_y - offset] == symbol

            return left_diagonal_win or right_diagonal_win

        return False

    def check_for_win(self):
        return self.check_for_finish(symbol=MAX_PLAYER_SYMBOL)

    def check_for_loose(self):
        return self.check_for_finish(symbol=MIN_PLAYER_SYMBOL)

    def heusristics(self):
        empty_boxes = self.count_empty_boxes()

        if self.player == MAX_PLAYER:
            play = self.check_for_win()
            value = empty_boxes + play

        if self.player == MIN_PLAYER:
            play = self.check_for_loose()
            value = -(empty_boxes + play)

        return value


def generate_empty_grid():
    grid = [[None for _ in range(3)] for _ in range(3)]
    start_x = random.randint(0, 2)
    start_y = random.randint(0, 2)

    grid[start_x][start_y] = 'X'

    return grid


def generate_grid_from_file(file_name):
    with open(file_name, 'r') as f:
        elements = list(f.read().replace('\n', ''))

        for i in range(len(elements)):
            if elements[i] == ' ':
                elements[i] = None

        grid = []

        for i in range(3):
            grid.append(elements[:3])
            elements = elements[3:]

    return grid


def opposite_player(player):
    return player == MAX_PLAYER and MIN_PLAYER or MAX_PLAYER


def get_possible_moves(grid, player):
    moves = []

    symbol = player == MAX_PLAYER and MAX_PLAYER_SYMBOL or MIN_PLAYER_SYMBOL

    for i in range(3):
        for j in range(3):
            if grid[i][j] is None:
                grid_copy = deepcopy(grid)

                grid_copy[i][j] = symbol
                moves.append(grid_copy)

    return moves


def win_the_game(start_grid):
    solution = []

    def alpha_beta_pruning(node, alpha, beta):
        # Source: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode
        node.add_children()

        # import time
        # time.sleep(1)
        # print('\n'.join([str(row) for row in node.grid]), '\n')

        if node.is_terminal:
            solution.append(node)
            return node.heusristics()

        infinity = math.inf
        if node.player == MAX_PLAYER:
            val = -infinity

            for child in node.children:
                val = max(val, alpha_beta_pruning(child, alpha, beta))
                alpha = max(alpha, val)

                if beta <= alpha:
                    break  # beta prunning

            return val

        if node.player == MIN_PLAYER:
            val = infinity

            for child in node.children:
                val = min(val, alpha_beta_pruning(child, alpha, beta))
                beta = min(beta, val)

                if beta <= alpha:
                    break  # alpha prunning

            return val

    root = Node(grid=start_grid, player=MAX_PLAYER)

    infinity = math.inf

    alpha_beta_pruning(
        node=root,
        alpha=-infinity,
        beta=infinity
    )

    return solution


if __name__ == '__main__':
    start_prompt = """
    Choose an entry point:
    - Start from empty board: 1
    - Start from given board: 2

    Option: """

    game = input(start_prompt)

    if int(game) == 1:
        print("\nStarting from empty board...\n")
        start_grid = generate_empty_grid()

    elif int(game) == 2:
        file_name = input('Path to file containg the board: ')
        print("\nStarting from {} ...\n".format(file_name))
        start_grid = generate_grid_from_file(file_name=file_name)

    else:
        raise ValueError('Pick valid entry point!')

    solution = win_the_game(start_grid=start_grid)

    print('\n'.join([str(node.grid) for node in solution]))
