import random
import math
from copy import deepcopy

"""
The solution uses `Simulated Annealing`
"""


class Blacksmith:
    def __init__(self, temp, queens_places):
        self.temp = temp
        self.queens_places = queens_places

        self.annealing_rate = 0.95
        self.max_forge_tries = 1e6

    def stabilize_temp(self):
        # Temperature may go too low. That's the purpose of the annealing rate.
        self.temp = max(self.temp * self.annealing_rate, 0.01)

    def get_collisions_number(self, queens_places):
        collisions = 0

        for i in range(len(queens_places)):
            for j in range(i + 1, len(queens_places)):
                if queens_places[i] == queens_places[j]:
                    collisions += 1

                offset = j - i  # helper for the diagonals

                in_diag1 = queens_places[i] == queens_places[j] - offset
                in_diag2 = queens_places[i] == queens_places[j] + offset

                if in_diag1 or in_diag2:
                    collisions += 1

        return collisions

    def move_random_queen(self, queens_places):
        rand_row = random.randint(0, len(queens_places) - 1)
        rand_col = random.randint(0, len(queens_places) - 1)

        queens_places[rand_row] = rand_col

        return queens_places

    def forge(self, queens_places, heuristics):
        nailing = True

        while nailing:
            queens_places_copy = deepcopy(queens_places)
            new_queens_places = self.move_random_queen(queens_places_copy)

            new_heuristics = self.get_collisions_number(new_queens_places)

            if new_heuristics < heuristics:
                # The blacksmith has done good enough job
                nailing = False
            else:
                # How bad the blacksmith hit the anvil?
                delta_error = heuristics - new_heuristics
                # The probability must stay in [0, 1]
                accept_probability = min(1, math.exp(delta_error / self.temp))
                # random.random() returns random float in [0 ,1]
                # We may accept the bad job of the blacksmith eventhough it has higher heuristcs
                nailing = random.random() <= accept_probability

        return new_queens_places, new_heuristics

    def annealing(self):
        queens_places = self.queens_places

        heuristics = self.get_collisions_number(queens_places)
        steps = 0

        while heuristics > 0:
            queens_places, heuristics = self.forge(queens_places, heuristics)
            self.stabilize_temp()

            # The algorith may got "stucked" (plateau)
            if steps >= self.max_forge_tries:
                print("Plateau occured :@")
                queens_places = None
                break

            steps += 1

        return queens_places


class Board:
    def __init__(self, size):
        self.given_number = size
        self.max_number = size ** 2
        self.initial_queens_places = []  # where is each Q in each column
        self.initial_grid = self.generate_random_grid()

        self.blacksmith = Blacksmith(self.max_number, self.initial_queens_places)

    def __draw_empty_grid(self):
        grid = []
        empty_boxes = ['_' for _ in range(self.max_number)]

        for _ in range(self.given_number):
            grid.append(empty_boxes[:self.given_number])
            empty_boxes = empty_boxes[self.given_number:]

        return grid

    def generate_random_grid(self):
        grid = self.__draw_empty_grid()

        for row in grid:
            col = random.randint(0, self.given_number - 1)
            row[col] = 'Q'
            # helper
            self.initial_queens_places.append(col)

        return grid

    def solve_puzzle(self):
        solution = self.blacksmith.annealing()
        grid = None

        if solution is not None:
            grid = self.draw_solution(solution)

        return grid

    def draw_solution(self, solution):
        grid = self.__draw_empty_grid()

        for Q_row, Q_col in enumerate(solution):
            grid[Q_row][Q_col] = 'Q'

        return grid


if __name__ == '__main__':
    board_size = input("Choose board size: ")
    solutions_size = input("Choose how many times do you want to start the algorithm: ")

    board = Board(int(board_size))

    print("Calculating...")

    with open('result.txt', 'w') as f:
        f.write("Starting grid:\n")
        for row in board.initial_grid:
            f.write("{}\n".format(row))
        f.write("\n\nALGORITH RESULTS\n\n")

    iterration = 0

    with open('result.txt', 'a') as f:
        while iterration < int(solutions_size):
            iterration += 1
            solution = board.solve_puzzle()

            iterration_header = "Iterration {}\n".format(iterration)
            print(iterration_header)
            f.write(iterration_header)

            if solution is not None:
                print("solution!")
                for row in solution:
                    f.write("{}\n".format(row))
            else:
                f.write("The algorithm got stucked. Solution not found...")

            f.write('\n')

    print("Open `result.txt` to check the results!")
