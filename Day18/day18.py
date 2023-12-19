from shapely import Polygon, Point, area

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
    # y1 = x1 = 0
    coords = [(y, x)]
    # coords1 = [(y1, x1)]

    for instruction_num in range(len(dig_plan)):
        dir, dist, colour = dig_plan[instruction_num]
        prev_dir = dig_plan[(instruction_num - 1) % len(dig_plan)][0]
        next_dir = dig_plan[(instruction_num + 1) % len(dig_plan)][0]

        # trench_length += dist
        match (prev_dir, dir, next_dir):
            case 'D', 'R', 'D':
                x += dist
            case 'D', 'R', 'U':
                x += (dist - 1)
            case 'U', 'R', 'D':
                x += (dist + 1)
            case 'U', 'R', 'U':
                x += dist

            case 'D', 'L', 'D':
                x -= dist
            case 'D', 'L', 'U':
                x -= (dist + 1)
            case 'U', 'L', 'D':
                x -= (dist - 1)
            case 'U', 'L', 'U':
                x -= dist

            case 'R', 'D', 'R':
                y += dist
            case 'R', 'D', 'L':
                y += (dist + 1)
            case 'L', 'D', 'R':
                y += (dist - 1)
            case 'L', 'D', 'L':
                y += dist

            case 'R', 'U', 'R':
                y -= dist
            case 'R', 'U', 'L':
                y -= (dist - 1)
            case 'L', 'U', 'R':
                y -= (dist + 1)
            case 'L', 'U', 'L':
                y -= dist

            case prev, curr, next:
                log(f"UNEXPECTED: {prev} -> {curr} -> {next}")

        coords.append((y, x))
        # coords1.append((y1, x1))

    log(f"{coords=}")
    return Polygon(coords)


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
    trench = dig_trench(dig_plan)
    return int(area(trench))


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
