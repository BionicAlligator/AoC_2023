from collections import deque

TESTING = False
PART = 1
OUTPUT_TO_CONSOLE = True

NUM_STEPS = 6 if TESTING else 64


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


def walk(garden, start):
    OFFSETS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    HEIGHT = len(garden)
    WIDTH = len(garden[0])

    reachable = {start: 0}
    unreachable = set()
    to_check = deque([(start, 0)])

    while to_check:
        (plot_y, plot_x), steps = to_check.popleft()

        if steps >= NUM_STEPS:
            continue

        for y, x in OFFSETS:
            next_plot_y = plot_y + y
            next_plot_x = plot_x + x

            if not (0 <= next_plot_y < HEIGHT and 0 <= next_plot_x < WIDTH):
                continue

            if garden[next_plot_y][next_plot_x] == '#':
                unreachable.add((next_plot_y, next_plot_x))
                continue

            next_coord = (next_plot_y, next_plot_x)

            if next_coord in reachable or next_coord in unreachable:
                continue

            if (next_plot_y + next_plot_x) % 2:
                unreachable.add(next_coord)
            else:
                reachable.update({next_coord: steps + 1})

            to_check.append((next_coord, steps + 1))

    return reachable, unreachable


def part1(inputs):
    garden,start = parse_input(inputs)
    reachable, unreachable = walk(garden, start)
    return len(reachable)


def part2(inputs):
    return


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
