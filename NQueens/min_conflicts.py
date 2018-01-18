import random


def nqueens(nr, file):
    show(min_conflicts(list(range(nr)), nr), nr, file)


def show(soln, nr, file):
    for i in range(nr):
        row = ['_'] * nr

        for col in range(nr):
            if soln[col] == nr - 1 - i:
                row[col] = 'Q'

        file.write(' '.join(row))
        file.write('\n')


def min_conflicts(soln, nr, iters=300):
    def random_pos(li, filt):
        return random.choice([i for i in range(nr) if filt(li[i])])

    for k in range(iters):
        confs = find_conflicts(soln, nr)

        if sum(confs) == 0:
            return soln

        col = random_pos(confs, lambda elt: elt > 0)
        vconfs = [hits(soln, nr, col, row) for row in range(nr)]
        soln[col] = random_pos(vconfs, lambda elt: elt == min(vconfs))

    raise ValueError("Incomplete solution: try more iterations.")


def find_conflicts(soln, nr):
    return [hits(soln, nr, col, soln[col]) for col in range(nr)]


def hits(soln, nr, col, row):
    total = 0

    for i in range(nr):
        if i == col:
            continue

        if soln[i] == row or abs(i - col) == abs(soln[i] - row):
            total += 1

    return total


if __name__ == '__main__':
    size = input('Choose N: ')
    solutions = input('How many solutions do you want to find: ')

    with open('solutions.txt', 'w') as f:
        for iterration in range(1, int(solutions) + 1):
            f.write('Solution {}\n'.format(iterration))
            nqueens(int(size), f)
            f.write('\n\n')
