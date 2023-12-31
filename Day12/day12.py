import re

TESTING = False
PART = 2
OUTPUT_TO_CONSOLE = False

possible_arrangement_cache = {}


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


def parse_input(inputs, folded=False):
    springs = []
    damage_reports = []

    for row in inputs:
        spring_row, damage_report = row.split(" ")

        if folded:
            spring_row = "?".join([spring_row] * 5)
            damage_report = ",".join([damage_report] * 5)

        springs.append(spring_row.replace('.', 'g').replace('?', 'u').replace('#', 'b'))

        broken_springs_on_row = [int(num) for num in damage_report.split(',')]

        damage_reports.append(broken_springs_on_row)

    return springs, damage_reports


def all_broken_springs_accounted_for(spring_row, broken_spring_row, num_broken_springs):
    return ((len(broken_spring_row) == 0 and
             spring_row.count('b') == 0) or
            (len(broken_spring_row) == 1 and
             re.match('^[bu]{' + str(num_broken_springs) + '}$', spring_row)))


def unaccounted_for_broken_springs(spring_row, broken_spring_row):
    return len(broken_spring_row) == 0 and spring_row.count('b') > 0


def insufficient_broken_springs(spring_row, broken_spring_row):
    return len(broken_spring_row) > 0 and spring_row == ""


def insufficient_springs_remaining(spring_row, broken_spring_row, num_broken_springs):
    return num_broken_springs + len(broken_spring_row) - 1 > len(spring_row)


def insufficient_potentially_broken_springs_remaining(spring_row, num_broken_springs):
    return num_broken_springs > spring_row.count('b') + spring_row.count('u')


def generate_spring_arrangements(spring_row, broken_spring_row):
    global possible_arrangement_cache

    broken_spring_row_tuple = tuple(broken_spring_row)

    if (spring_row, broken_spring_row_tuple) in possible_arrangement_cache:
        return possible_arrangement_cache[(spring_row, broken_spring_row_tuple)]

    num_broken_springs = sum(broken_spring_row)

    if all_broken_springs_accounted_for(spring_row, broken_spring_row, num_broken_springs):
        return 1

    if unaccounted_for_broken_springs(spring_row, broken_spring_row):
        return 0

    if insufficient_broken_springs(spring_row, broken_spring_row):
        return 0

    if insufficient_springs_remaining(spring_row, broken_spring_row, num_broken_springs):
        return 0

    if insufficient_potentially_broken_springs_remaining(spring_row, num_broken_springs):
        return 0

    this_char = spring_row[0]
    num_possible_arrangements = 0

    match this_char:
        case 'g':
            num_possible_arrangements = generate_spring_arrangements(
                spring_row[1:],
                broken_spring_row)

        case 'b':
            num_broken = broken_spring_row[0]

            if re.match('^[bu]{' + str(num_broken) + '}[gu]', spring_row):
                num_possible_arrangements = generate_spring_arrangements(
                    spring_row[num_broken + 1:],
                    broken_spring_row[1:])
            else:
                return 0

        case 'u':
            num_broken = broken_spring_row[0]

            if re.search('^[bu]{' + str(num_broken) + '}[gu]', spring_row):
                num_possible_arrangements = generate_spring_arrangements(
                    spring_row[num_broken + 1:],
                    broken_spring_row[1:])

            num_possible_arrangements += generate_spring_arrangements(
                spring_row[1:],
                broken_spring_row)

    possible_arrangement_cache.update({(spring_row, broken_spring_row_tuple): num_possible_arrangements})

    return num_possible_arrangements


def determine_possible_arrangements(springs, broken_springs):
    num_possible_arrangements = 0

    for row_num in range(len(springs)):
        # if row_num % 10 == 0:
        log(f"{row_num=}")

        spring_row = springs[row_num]
        broken_spring_row = broken_springs[row_num]

        num_possible_arrangements += generate_spring_arrangements(spring_row, broken_spring_row)

    return num_possible_arrangements


def part1(inputs):
    springs, broken_springs = parse_input(inputs)
    num_possible_arrangements = determine_possible_arrangements(springs, broken_springs)
    return num_possible_arrangements


def part2(inputs):
    springs, broken_springs = parse_input(inputs, True)
    num_possible_arrangements = determine_possible_arrangements(springs, broken_springs)
    return num_possible_arrangements


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
