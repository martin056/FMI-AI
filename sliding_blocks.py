import random
from copy import deepcopy

"""
g(x) - the steps I've made
h1(x) - the sum of how many numbers are not on their place
h2(x) - Manhattan distance with n = 1. We will use this!

hevristics(x) = g(x) + h2(x)
"""


class Table:
    MOVING_ELEMENT = 0

    def __init__(self, n):
        self.given_number = n
        self.max_element_value = n ** 2
        self.final_grid = self.generate_final_grid()
        self.grid = self.generate_random_grid()

        self.distance = 0
        self.history = []
        self.fixed_elements = set()
        self.banned_move = ''

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

    def find_current_place(self, number):
        return self.find_number(number, self.grid)

    def find_moving_element(self):
        return self.find_current_place(self.MOVING_ELEMENT)

    def move(self):
        def move_left():
            row, col = self.find_moving_element()
            step = col - 1

            if step >= 0:
                target_number = self.grid[row][step]
                return target_number not in self.fixed_elements and target_number

            return False

        def move_right():
            row, col = self.find_moving_element()
            step = col + 1

            if step < self.given_number:
                target_number = self.grid[row][step]
                return target_number not in self.fixed_elements and target_number

            return False

        def move_up():
            row, col = self.find_moving_element()
            step = row - 1

            if step >= 0:
                target_number = self.grid[step][col]
                return target_number not in self.fixed_elements and target_number

            return False

        def move_down():
            row, col = self.find_moving_element()
            step = row + 1

            if step < self.given_number:
                target_number = self.grid[step][col]
                return target_number not in self.fixed_elements and target_number

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

    def manhattan(self, number):
        perfect_place = self.find_perfect_place(number)
        current_place = self.find_current_place(number)

        if perfect_place != current_place:
            x_to_target = abs(perfect_place[0] - current_place[0])
            y_to_target = abs(perfect_place[1] - current_place[1])

            return x_to_target + y_to_target

        return 0

    def reorder_grid(self, number):
        """
        Swaps the moving element (0) with the `number`.
        Returns the grid before the manipulation.
        """
        old_grid = deepcopy(self.grid)

        target_row, target_col = self.find_current_place(number)
        zero_row, zero_col = self.find_moving_element()

        self.grid[target_row][target_col] = 0
        self.grid[zero_row][zero_col] = number

        return old_grid

    # def ban_next_move(self, last_move):
    #     """
    #     If we go to `left` on N move, we don't want to go to `right` on N+1 move.

    #     This prevents infinite reccursion when we have equal hevristics.
    #     """
    #     opposite_moves = {
    #         'left': 'right',
    #         'right': 'left',
    #         'up': 'down',
    #         'down': 'up'
    #     }

    #     self.banned_move = opposite_moves[last_move]

    def calculate_next_node(self):
        hevristics = []

        possible_moves = self.move()

        for move, target_number in possible_moves.items():
            if target_number:
                manhattan_distance = self.manhattan(target_number)

                if manhattan_distance == 0:
                    """
                    If the element is already on its place - don't touch it.
                    """
                    self.fixed_elements.add(target_number)

                else:
                    hevristics.append((target_number,
                                       self.distance + manhattan_distance,
                                       move))

        random.shuffle(hevristics)

        best_hevristic_val = min([val for _, val, _ in hevristics])\

        import ipdb; ipdb.set_trace()

        for number, hevristic_val, move in hevristics:
            if hevristic_val == best_hevristic_val:
                old_grid = self.reorder_grid(number)

                checkpoint = "{}\nNext move: {}".format(old_grid, move)
                self.history.append(checkpoint)

                # self.ban_next_move(last_move=move)

                """
                Stop the loop on the first occured possition.

                If we don't the algorithm will swap all elements with equal
                hevristics with the moving element (0).
                """
                break

    def add_initially_fixed_elements(self):
        """
        If there are elements that are on there place
        in the initially generated grid, we add them to the
        `fixed_elements`
        """
        for number in range(1, self.max_element_value):
            if self.manhattan(number) == 0:
                self.fixed_elements.add(number)

    def play(self):
        self.add_initially_fixed_elements()

        while self.grid != self.final_grid:
            self.calculate_next_node()
            self.update_distance()


if __name__ == '__main__':
    table = Table(3)
    table.play()
