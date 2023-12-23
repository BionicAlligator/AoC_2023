# TODO: Fix this - think I have a bug either in the way I am solving the quadratic formula, or in the way I am applying it afterwards

import math
from collections import deque

TESTING = False
PART = 2
OUTPUT_TO_CONSOLE = True

PART_1_NUM_STEPS_TESTING = 6
PART_1_NUM_STEPS = 64
PART_2_NUM_STEPS_TESTING = 5000
PART_2_NUM_STEPS = 26501365


def log(message, end="\n"):
    if OUTPUT_TO_CONSOLE:
        print(message, end=end)


def read_tests(test_filename):
    tests = []
    inputs = []
    expected = ""

    file = open(test_filename, "r")

    for line in file:
        if line.lstrip().startswith("="):  # Line with equals sign at beginning or end means it is the expected output
            expected = line.split("=")[1].lstrip()
        elif line.rstrip().endswith("="):
            expected = line.split("=")[0].rstrip()
        elif not line.strip():  # Blank line means end of test specification
            tests.append((expected, inputs.copy()))
            inputs = []
        else:
            inputs.append(line.rstrip())

    return tests


def read_input(filename):
    file = open(filename, "r")
    lines = [line.rstrip() for line in file]
    return lines


def parse_input(inputs):
    garden = []

    for y, row in enumerate(inputs):
        garden.append([])

        for x, feature in enumerate(row):
            if feature == 'S':
                start = (y, x)
                feature = '.'

            garden[y].append(feature)

    return garden, start


def walk(garden, start, num_steps):
    OFFSETS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    HEIGHT = len(garden)
    WIDTH = len(garden[0])

    reachable = {}
    unreachable = set()
    to_check = deque([(start, 0)])

    while to_check:
        (plot_y, plot_x), steps = to_check.popleft()

        if steps >= num_steps:
            continue

        for y, x in OFFSETS:
            next_plot_y = plot_y + y
            next_plot_x = plot_x + x

            if garden[next_plot_y % HEIGHT][next_plot_x % WIDTH] == '#':
                unreachable.add((next_plot_y, next_plot_x))
                continue

            next_coord = (next_plot_y, next_plot_x)

            if next_coord in reachable or next_coord in unreachable:
                continue

            if (next_plot_y + next_plot_x) % 2 != (num_steps % 2):
                unreachable.add(next_coord)
            else:
                reachable.update({next_coord: steps + 1})

            to_check.append((next_coord, steps + 1))

    return reachable, unreachable


def solve_quadratic(point1, point2, point3):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3

    # a * x1^2 + b * x1 + c = y1
    # a * x2^2 + b * x2 + c = y2
    # a * x3^2 + b * x3 + c = y3
    #
    # y2 - y1 = (x2^2 - x1^2) * a + (x2 - x1) * b , so b = (-(x2^2 - x1^2) * a) / (x2 - x1) = ((x1^2 - x2^2) / (x2 - x1)) * a
    # y3 - y2 = (x3^2 - x2^2) * a + (x3 - x2) * b = (x3^2 - x2^2) * a + (x3 - x2) * ((x1^2 - x2^2) / (x2 - x1)) * a
    #         = a * ((x3^2 - x2^2) + ((x3 - x2) * ((x1^2 - x2^2) / (x2 - x1)))
    # so a = (y3 - y2) / ((x3^2 - x2^2) + ((x3 - x2) * ((x1^2 - x2^2) / (x2 - x1))))
    #
    # d = y3 - y2
    # e = x3^2 - x2^2
    # f = x3 - x2
    # g = x1^2 - x2^2
    # h = x2 - x1
    #
    # a = d / (e + (f * (g / h)))
    # b = (g / h) * a
    # c = y1 - a * x1^2 - b * x1

    d = y3 - y2
    e = (x3 ** 2) - (x2 ** 2)
    f = x3 - x2
    g = (x1 ** 2) - (x2 ** 2)
    h = x2 - x1

    a = d / (e + (f * (g / h)))
    b = (g / h) * a
    c = y1 - (a * (x1 ** 2)) - (b * x1)

    return a, b, c


def part1(inputs):
    NUM_STEPS = PART_1_NUM_STEPS_TESTING if TESTING else PART_1_NUM_STEPS

    garden, start = parse_input(inputs)
    reachable, unreachable = walk(garden, start, NUM_STEPS)
    return len(reachable)


def part2(inputs):
    NUM_STEPS = PART_2_NUM_STEPS_TESTING if TESTING else PART_2_NUM_STEPS

    garden, start = parse_input(inputs)
    start_y = start[0]

    # Get first three values to solve polynomial equation
    reachable, unreachable = walk(garden, start, start_y)
    num_reachable_1 = len(reachable)
    log(f"{num_reachable_1} with {start_y} steps")

    reachable, unreachable = walk(garden, start, start_y + len(garden))
    num_reachable_2 = len(reachable)
    log(f"{num_reachable_2} with {start_y + len(garden)} steps")

    reachable, unreachable = walk(garden, start, start_y + (2 * len(garden)))
    num_reachable_3 = len(reachable)
    log(f"{num_reachable_3} with {start_y + 2 * len(garden)} steps")

    # a, b, c = solve_quadratic((start_y, num_reachable_1),
    #                           (start_y + len(garden), num_reachable_2),
    #                           (start_y + (2 * len(garden)), num_reachable_3))

    a, b, c = solve_quadratic((0, num_reachable_1),
                              (1, num_reachable_2),
                              (2, num_reachable_3))

    max_range = NUM_STEPS // len(garden)

    # return (a * (NUM_STEPS ** 2)) + (b * NUM_STEPS) + c
    return (a * (max_range ** 2)) + (b * max_range) + c


def run_tests():
    tests = read_tests("sample_input_part_" + str(PART) + ".txt")

    print(f"Test Results for Part {PART}")

    passed = failed = 0

    for expected, inputs in tests:
        actual = part1(inputs) if PART == 1 else part2(inputs)

        if expected == str(actual):
            passed += 1
            print(f"Passed: {inputs} -> {actual}\n")
        else:
            failed += 1
            print(f"Failed: {inputs} -> {actual}, expected {expected}\n")

    print(f"Passed: {passed}, Failed: {failed}")


def run_for_real():
    inputs = read_input("input.txt")

    print("Part 1: ", part1(inputs))

    if PART == 2:
        print("Part 2: ", part2(inputs))


if TESTING:
    run_tests()
else:
    run_for_real()
