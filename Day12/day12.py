import re

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
    springs = []
    patterns = []

    for row in inputs:
        spring_string, broken_spring_string = row.split(" ")

        springs.append(spring_string.replace('.', 'g').replace('?', 'u').replace('#', 'b'))

        broken_springs = broken_spring_string.split(',')

        pattern = "g*?"

        for index, spring in enumerate(broken_springs):
            if index == len(broken_springs) - 1:
                pattern += "b{" + spring + "}g*?$"
            else:
                pattern += "b{" + spring + "}g+?"

        patterns.append(pattern)

    return springs, patterns


def generate_spring_arrangements(spring_row):
    spring_arrangements = []

    if 'u' not in spring_row:
        return [spring_row]

    for spring_arrangement in generate_spring_arrangements(spring_row[1:]):
        if spring_row[0] == 'u':
            spring_arrangements.append("g" + spring_arrangement)
            spring_arrangements.append("b" + spring_arrangement)
        else:
            spring_arrangements.append(spring_row[0] + spring_arrangement)

    return spring_arrangements


def determine_possible_arrangements(springs, patterns):
    possible_arrangements = []

    for row_num in range(len(springs)):
        possible_arrangements.append([])

        spring_row = springs[row_num]
        pattern = patterns[row_num]

        all_spring_arrangements = generate_spring_arrangements(spring_row)

        for spring_arrangement in all_spring_arrangements:
            if re.match(pattern, spring_arrangement):
                possible_arrangements[row_num].append(spring_arrangement)

    return possible_arrangements


def count_possible_arrangements(possible_arrangements):
    total = 0

    for spring_row_arrangements in possible_arrangements:
        total += len(spring_row_arrangements)

    return total


def part1(inputs):
    springs, patterns = parse_input(inputs)
    possible_arrangements = determine_possible_arrangements(springs, patterns)
    return count_possible_arrangements(possible_arrangements)


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
