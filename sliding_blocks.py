import random
from copy import deepcopy


class Node:
    def __init__(self, grid, grid_score, parent):
        self.grid = grid
        self.grid_score = grid_score
        self.parent = parent

        self.distance = self.calculate_distance()

    @property
    def heuristic(self):
        return self.grid_score

    def calculate_distance(self):
        parent = self.parent
        counter = 0

        while parent is not None:
            counter += 1
            parent = parent.parent

        return counter


class SlidingBlocks:
    MOVING_ELEMENT = 0

    def __init__(self, n):
        self.given_number = n
        self.max_element_value = n ** 2
        self.final_grid = self.generate_final_grid()
        self.grid = self.generate_random_grid()

        self.visited = []
        self.nodes = []

    def is_solvable(self, grid):
        moving_element_manhattan = self.manhattan(self.MOVING_ELEMENT, grid)

        elements = []
        permutations = 0
        for row in grid:
            elements.extend(row)

        for i in elements:
            for j in elements[1:]:
                if i < j:
                    permutations += 1

        return (moving_element_manhattan + permutations) % 2 == 0

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

        if not self.is_solvable(result):
            self.generate_random_grid()

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

    def get_grid_score(self, grid):
        result = 0

        for number in range(0, self.max_element_value):
            result += self.manhattan(number, grid)

        return result

    def manhattan(self, number, grid):
        perfect_place = self.find_perfect_place(number)
        place_in_grid = self.find_number(number, grid)

        x_to_target = abs(perfect_place[0] - place_in_grid[0])
        y_to_target = abs(perfect_place[1] - place_in_grid[1])

        return (x_to_target + y_to_target)

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
        for node in self.nodes:
            if node.grid in [n.grid for n in self.visited]:
                self.nodes.remove(node)

        sorted_nodes = sorted(self.nodes, key=lambda node: node.heuristic)

        return sorted_nodes[0]

    def extend_nodes(self):
        possible_moves = self.move()

        for move, target_number in possible_moves.items():
            if target_number:
                grid = self.reorder_grid(target_number)

                grid_score = self.get_grid_score(grid)
                parent = self.visited[-1]

                node = Node(grid=grid,
                            grid_score=grid_score,
                            parent=parent)

                if node.grid not in [n.grid for n in self.visited]:
                    self.nodes.append(node)

    def choose_next_node(self):
        best_node = self.get_best_possible_node()

        self.visited.append(best_node)
        self.grid = best_node.grid

    def play(self):
        # Add root of the tree
        intiial_node = Node(grid=self.grid,
                            grid_score=self.get_grid_score(self.grid),
                            parent=None)

        self.visited.append(intiial_node)
        self.nodes.append(intiial_node)

        while self.grid != self.final_grid:
            self.extend_nodes()
            self.choose_next_node()

        winner = self.visited[-1]
        parent = winner.parent
        print("SOLVED")
        print(winner.grid)
        while parent is not None:
            print(parent.grid)
            parent = parent.parent


if __name__ == '__main__':
    game = SlidingBlocks(4)
    game.play()
