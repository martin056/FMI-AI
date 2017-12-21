import random


def get_random_color(pastel_factor=0.5):
    return [(x + pastel_factor) / (1.0 + pastel_factor)
            for x in [random.uniform(0, 1.0) for i in [1, 2, 3]]]


def color_distance(c1, c2):
    return sum([abs(x[0] - x[1]) for x in zip(c1, c2)])


def generate_new_color(existing_colors, pastel_factor=0.5):
    max_distance = None
    best_color = None

    for i in range(0, 100):
        color = get_random_color(pastel_factor=pastel_factor)
        if not existing_colors:
            return tuple(color)

        best_distance = min([color_distance(color, c) for c in existing_colors])

        if not max_distance or best_distance > max_distance:
            max_distance = best_distance
            best_color = color

    return tuple(best_color)


def generate_k_random_colors(k):
    colors = []

    for _ in range(k):
        colors.append(generate_new_color(colors, pastel_factor=0.9))

    return colors
