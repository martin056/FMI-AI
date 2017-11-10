import random
import math
from copy import deepcopy
from collections import OrderedDict


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
        play = 0

        if self.player == MAX_PLAYER:
            play = self.check_for_win()

        if self.player == MIN_PLAYER:
            play = self.check_for_loose()

        # If the game is not finished, the `play` value stays `0`
        return empty_boxes + int(play)


def generate_empty_grid():
    grid = [[None for _ in range(3)] for _ in range(3)]
    start_x = random.randint(0, 2)
    start_y = random.randint(0, 2)

    grid[start_x][start_y] = 'X'

    return grid


def generate_grid_from_file(file_name):
    pass


def opposite_player(player):
    return player == MAX_PLAYER and MIN_PLAYER or MAX_PLAYER


def generate_game_tree(start_grid):
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

    # tree = {}
    player = MAX_PLAYER
    grid = start_grid

    root = Node(player=player, grid=grid)
    nodes = [root]
    visited_grids = []

    # i = 0
    while True:
        # tree[i] = nodes

        next_nodes = []

        for node in nodes:
            visited_grids.append(node.grid)

            next_player = opposite_player(node.player)
            moves = get_possible_moves(grid=node.grid, player=next_player)

            for move in moves:
                if move not in visited_grids:
                    child = Node(grid=move, player=next_player)
                    node.children.append(child)

                    next_nodes.append(child)

        if len(next_nodes) == 0:
            # i = -1  # break
            break
        else:
            nodes = next_nodes

    # return OrderedDict(sorted(tree.items(), key=lambda key_value_tuple: key_value_tuple[0]))
    return root


def win_the_game(start_grid):
    print('Generating solutions tree...')
    root = generate_game_tree(start_grid)

    def alpha_beta_pruning(node, alpha, beta, player):
        # Source: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode
        infinity = math.inf
        import ipdb; ipdb.set_trace()

        if node.is_terminal:
            return node.heusristics()

        if player == MAX_PLAYER:
            val = -infinity

            for child in node.children:
                import ipdb; ipdb.set_trace()
                val = max(val, alpha_beta_pruning(child, alpha, beta, MIN_PLAYER))
                alpha = max(alpha, val)

                if beta <= alpha:
                    break  # beta prunning

            return val

        if player == MIN_PLAYER:
            val = infinity

            for child in node.children:
                import ipdb; ipdb.set_trace()
                val = min(val, alpha_beta_pruning(child, alpha, beta, MAX_PLAYER))
                beta = min(beta, val)

                if beta <= alpha:
                    break  # alpha prunning

            return val

    # We start from the most left node
    # starting_node = tree[list(tree.keys())[-1]][0]
    # print(starting_node)
    # print(starting_node.grid)
    infinity = math.inf
    result = alpha_beta_pruning(
        node=root,
        alpha=infinity,
        beta=-infinity,
        player=root.player
    )
    print(result)


if __name__ == '__main__':
    start_prompt = """
    Choose an entry point:
    - Start from empty board: 1
    - Start from given board: 2
    """

    game = input(start_prompt)

    if int(game) == 1:
        print("Starting from empty board...\n")
        start_grid = generate_empty_grid()

    elif int(game) == 2:
        file_name = input('Path to file containg the board: ')
        print("Starting from {} ...\n".format(file_name))
        start_grid = generate_grid_from_file(file_name=file_name)

    else:
        raise ValueError('Pick valid entry point!')

    result = win_the_game(start_grid=start_grid)
    print(result)
