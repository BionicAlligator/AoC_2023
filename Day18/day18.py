from shapely import Polygon, area

TESTING = False
PART = 2
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


def parse_input(inputs, use_hex=False):
    DIRECTION_MAP = {0: 'R', 1: 'D', 2: 'L', 3: 'U'}

    dig_plan = []

    if not use_hex:
        for instruction in inputs:
            direction, distance, _ = instruction.split(" ")
            dig_plan.append((direction, int(distance)))
    else:
        for instruction in inputs:
            _, _, inst = instruction.split(" ")
            inst = inst.strip('(#)')

            direction = DIRECTION_MAP[int(inst[5])]
            distance = int(inst[:5], 16)

            dig_plan.append((direction, int(distance)))

    return dig_plan


def dig_trench(dig_plan):
    y = x = 0
    coords = [(y, x)]

    for instruction_num in range(len(dig_plan)):
        dir, dist = dig_plan[instruction_num]
        prev_dir = dig_plan[(instruction_num - 1) % len(dig_plan)][0]
        next_dir = dig_plan[(instruction_num + 1) % len(dig_plan)][0]

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

    log(f"{coords=}")
    return Polygon(coords)


def part1(inputs):
    dig_plan = parse_input(inputs)
    trench = dig_trench(dig_plan)
    return int(area(trench))


def part2(inputs):
    dig_plan = parse_input(inputs, True)
    trench = dig_trench(dig_plan)
    return int(area(trench))


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
