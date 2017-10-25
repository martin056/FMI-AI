MOVE_LEFT = 1
MOVE_RIGHT = 2
MOVE_LEFT_WITH_JUMP = 3
MOVE_RIGHT_WITH_JUMP = 4

MOVE_STEPS = {
    MOVE_LEFT: -1,
    MOVE_RIGHT: 1,
    MOVE_LEFT_WITH_JUMP: -2,
    MOVE_RIGHT_WITH_JUMP: 2,
}


def generate_swamp(frogs_count, left_frog, right_frog):
    left = frogs_count * left_frog
    right = frogs_count * right_frog

    return "{}_{}".format(left, right)


def generate_initial_swamp(frogs_count):
    return generate_swamp(frogs_count, '>', '<')


def generate_final_swamp(frogs_count):
    return generate_swamp(frogs_count, '<', '>')


def feng_shui_swamp(swamp, steps):
    """
    Returns if the old swamp can be ordered by the rules of Feng shui.

    The swamp Feng shui rules are:
      * The rock can't go to a index where frog is looking in the opposite direction of it's move.
      * The rock can't go outside of the swamp (it's index can't be < 0 or > of swamps length)
    """
    current_rock_index = swamp.find('_')

    new_rock_place = current_rock_index + steps

    max_possible_place = len(swamp) - 1

    if new_rock_place > max_possible_place or new_rock_place < 0:
        return False

    if current_rock_index > new_rock_place:
        return swamp[new_rock_place] == '>'

    if current_rock_index < new_rock_place:
        return swamp[new_rock_place] == '<'


def move_rock(swamp, steps):
    rock = swamp.find('_')

    new_swamp = list(swamp)
    new_swamp[rock] = new_swamp[rock + steps]
    new_swamp[rock + steps] = '_'

    return ''.join(new_swamp)


def reorder_swamp(swamp, move_steps):
    new_swamp = move_rock(swamp, move_steps)

    return new_swamp


def frogs_game(n):
    initial_swamp = generate_initial_swamp(n)
    final_swamp = generate_final_swamp(n)

    final_path = []

    def tail_rec(current_swamp):
        if current_swamp == final_swamp:
            final_path.append(current_swamp)
            return current_swamp

        for move_steps in MOVE_STEPS.values():
            if feng_shui_swamp(current_swamp, move_steps):
                swamp = reorder_swamp(current_swamp, move_steps)

                path = tail_rec(swamp)

                if path:
                    final_path.append(current_swamp)
                    return True

        return False

    tail_rec(initial_swamp)

    return final_path


if __name__ == '__main__':
    import time

    start = time.time()

    final_path = frogs_game(20)
    final_path.reverse()

    print("{} sec execution time".format(time.time() - start))

    print('\n'.join(final_path))
