from shapely import Polygon, Point

TESTING = False
PART = 1
OUTPUT_TO_CONSOLE = True


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
    dig_plan = []

    for instruction in inputs:
        direction, distance, colour = instruction.split(" ")
        colour = colour.strip('(#)')
        dig_plan.append((direction, int(distance), colour))

    return dig_plan


def dig_trench(dig_plan):
    trench_length = 0
    min_y = min_x = float('inf')
    max_y = max_x = float('-inf')
    y = x = 0
    coords = [(y, x)]

    for dir, dist, _ in dig_plan:
        trench_length += dist
        match dir:
            case 'R': x += dist
            case 'L': x -= dist
            case 'D': y += dist
            case 'U': y -= dist

        min_y = min(y, min_y)
        min_x = min(x, min_x)
        max_y = max(y, max_y)
        max_x = max(x, max_x)

        coords.append((y, x))

    return Polygon(coords), trench_length, (min_y, min_x, max_y, max_x)


def volume(trench, trench_length, bounds):
    min_y, min_x, max_y, max_x = bounds

    lagoon_volume = 0

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if trench.contains(Point(y, x)):
                lagoon_volume += 1

    return lagoon_volume + trench_length


# TODO: Use Pick's theorem instead of Shapely Polygon.contains
# The latter is slow for a large polygon
def part1(inputs):
    dig_plan = parse_input(inputs)
    trench, trench_length, bounds = dig_trench(dig_plan)
    return volume(trench, trench_length, bounds)


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
