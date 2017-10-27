import random
from copy import deepcopy

"""
g(x) - the steps I've made
h1(x) - the sum of how many numbers are not on their place
h2(x) - Manhattan distance with n = 1. We will use this!

heuristic(x) = g(x) + h2(x)
"""


class Node:
    def __init__(self, grid, heuristic, parent):
        self.grid = grid
        self.heuristic = heuristic
        self.parent = parent

        self.path_heuristic = self.calculate_path_heuristic()

    def __str__(self):
        return '\n'.join([str(row) for row in self.grid])

    def calculate_path_heuristic(self):
        result = self.heuristic
        node = self.parent

        while node:
            result += node.heuristic
            node = node.parent

        return result


class Table:
    MOVING_ELEMENT = 0

    def __init__(self, n):
        self.given_number = n
        self.max_element_value = n ** 2
        self.final_grid = self.generate_final_grid()
        self.grid = self.generate_random_grid()
        # self.grid = [
        #     [1,0,2],
        #     [3,4,5],
        #     [6,8,7]
        # ]

        self.distance = 0
        self.visited = []
        self.nodes = []
        self.last_node = None

    def generate_final_grid(self):
        result = []
        numbers = list(range(self.max_element_value))

        for _ in range(1, self.given_number + 1):
            result.append(numbers[:self.given_number])
            numbers = numbers[self.given_number:]

        return result

    def generate_random_grid(self):
        result = []
        numbers = list(range(self.max_element_value))
        random.shuffle(numbers)

        for _ in range(1, self.given_number + 1):
            result.append(numbers[:self.given_number])
            numbers = numbers[self.given_number:]

        return result

    def find_number(self, number, grid):
        for index, element in enumerate(grid):
            if number in element:
                return index, element.index(number)

    def find_perfect_place(self, number):
        return self.find_number(number, self.final_grid)

    def find_moving_element(self):
        return self.find_number(self.MOVING_ELEMENT, self.grid)

    def move(self):
        def move_left():
            row, col = self.find_moving_element()
            step = col - 1

            if step >= 0:
                target_number = self.grid[row][step]
                return target_number

            return False

        def move_right():
            row, col = self.find_moving_element()
            step = col + 1

            if step < self.given_number:
                target_number = self.grid[row][step]
                return target_number

            return False

        def move_up():
            row, col = self.find_moving_element()
            step = row - 1

            if step >= 0:
                target_number = self.grid[step][col]
                return target_number

            return False

        def move_down():
            row, col = self.find_moving_element()
            step = row + 1

            if step < self.given_number:
                target_number = self.grid[step][col]
                return target_number

            return False

        next_states = {
            'left': move_left(),
            'right': move_right(),
            'up': move_up(),
            'down': move_down(),
        }

        return next_states

    def update_distance(self):
        self.distance += 1

    def manhattan(self, grid):
        result = 0

        for number in range(0, self.max_element_value):
            perfect_place = self.find_perfect_place(number)
            place_in_grid = self.find_number(number, grid)

            x_to_target = abs(perfect_place[0] - place_in_grid[0])
            y_to_target = abs(perfect_place[1] - place_in_grid[1])

            result += (x_to_target + y_to_target)

        return result

    def heuristic(self, grid):
        return self.manhattan(grid)

    def reorder_grid(self, number):
        """
        Swaps the moving element (0) with the `number`.
        """
        grid = deepcopy(self.grid)

        target_row, target_col = self.find_number(number, grid)
        zero_row, zero_col = self.find_moving_element()

        grid[target_row][target_col] = self.MOVING_ELEMENT
        grid[zero_row][zero_col] = number

        return grid

    def get_best_possible_node(self):
        nodes = set(self.nodes) - set(self.visited)
        sorted_nodes = sorted(list(nodes), key=lambda node: node.path_heuristic)

        return sorted_nodes[0]

    def extend_nodes(self):
        possible_moves = self.move()

        for move, target_number in possible_moves.items():
            if target_number:
                grid = self.reorder_grid(target_number)
                grid_heuristic = self.heuristic(grid)
                parent = self.visited[-1]

                node = Node(grid=grid,
                            heuristic=grid_heuristic,
                            parent=parent)

                self.nodes.append(node)

    def choose_next_node(self):
        self.extend_nodes()

        best_node = self.get_best_possible_node()

        while best_node in self.visited:
            self.nodes.remove(best_node)
            best_node = self.get_best_possible_node()

        self.grid = best_node.grid
        self.visited.append(best_node)

    def play_sliding_blocks(self):
        # Add root of the tree
        intiial_node = Node(grid=self.grid,
                            heuristic=self.heuristic(self.grid),
                            parent=None)

        self.visited.append(intiial_node)
        self.nodes.append(intiial_node)

        while self.grid != self.final_grid:
            self.choose_next_node()
            self.update_distance()


if __name__ == '__main__':
    table = Table(3)
    table.play_sliding_blocks()
