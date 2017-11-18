import random
import math


ITEM_WEIGHTS = [
    90, 130, 1530, 500, 150, 680, 270, 390, 230, 520, 110,
    320, 240, 480, 730, 420, 430, 220, 70, 180, 40, 300, 900, 2000
]


ITEM_VALUES = [
    150, 35, 200, 160, 60, 45, 60, 40, 30, 10, 70,
    30, 15, 10, 40, 70, 75, 80, 20, 12, 50, 10, 1, 150,
]


class GeneticAlgorithm:
    def __init__(self, item_weights, item_values, max_capacity, population_length):
        self.item_weights = item_weights
        self.item_values = item_values
        self.max_capacity = max_capacity
        self.population_length = population_length

        self.items_length = len(self.item_weights)

    def generate_random_population(self):
        def generate_random_member():
            member = [random.randint(0, 1) for _ in range(self.items_length)]
            member_heuristics = self.fitness_function(child=member)

            if member_heuristics > 0:
                return member

            return generate_random_member()

        return [generate_random_member() for _ in range(self.population_length)]

    def fitness_function(self, child):
        child_weight = self.get_child_weight(child)

        if child_weight > self.max_capacity:
            return -1

        return self.get_child_value(child)

    def get_child_weight(self, child):
        return sum([self.item_weights[i] for i, el in enumerate(child) if el == 1])

    def get_child_value(self, child):
        return sum([self.item_values[i] for i, el in enumerate(child) if el == 1])

    def mutate(self, child):
        # TODO: Be smarter with the if-else
        mutation_item_index = random.randint(0, self.items_length - 1)
        if child[mutation_item_index] == 0:
            child[mutation_item_index] = 1
        else:
            child[mutation_item_index] = 0

        return child

    def crossover(self, father, mother):
        separator_index = random.randint(0, self.items_length - 1)

        brother = father[:separator_index] + mother[separator_index:]
        sister = mother[:separator_index] + father[separator_index:]

        if self.fitness_function(brother) > 0:
            return brother
        elif self.fitness_function(sister) > 0:
            return sister
        else:
            self.crossover(father, mother)

    def crossover_and_mutate(self, father, mother):
        child = self.crossover(father, mother)
        do_mutation = random.randint(1, 100) < 5

        if do_mutation:
            child = self.mutate(child)

        if self.fitness_function(child) > 0:
            return child

        return self.crossover_and_mutate(father, mother)

    def get_best_members(self, population):
        best_members_length = math.ceil(len(population) * .2)
        return population[:best_members_length]

    def get_members_for_crossover(self, population):
        sorted_population = sorted(population,
                                   reverse=True,
                                   key=lambda member: self.get_child_value(member))

        best_members = self.get_best_members(sorted_population)
        # randomly pick random memeber from other bad members
        if random.randint(1, 100) < 3:
            best_members_length = math.ceil(len(population) * .2)
            bad_member = random.choice(sorted_population[best_members_length:])
            best_members.append(bad_member)

        return best_members

    def selection(self, population):
        members = self.get_members_for_crossover(population)
        new_population = []

        for _ in range(self.population_length):
            father = random.choice(members)
            mother = random.choice(members)

            child = self.crossover_and_mutate(father, mother)

            new_population.append(child)

        return self.get_best_members(new_population)


def solve_knapsack(n):
    genetic_algorithm = GeneticAlgorithm(item_weights=ITEM_WEIGHTS,
                                         item_values=ITEM_VALUES,
                                         max_capacity=5000,
                                         population_length=100)

    result = []
    best_score = 0

    for _ in range(n):
        population = genetic_algorithm.generate_random_population()
        selection = genetic_algorithm.selection(population)
        result.append(selection)

    for population in result:
        best_members = genetic_algorithm.get_best_members(population)
        best_members_values = [genetic_algorithm.get_child_value(m) for m in best_members]
        new_best_score = sorted(best_members_values)[-1]

        if best_score < new_best_score:
            best_score = new_best_score

        print("Current Best Score: ", best_score)

    return best_score


if __name__ == '__main__':
    n = input('How many times do you want to find a solution of the problem: ')
    score = solve_knapsack(int(n))

    print("Score: ", score)
