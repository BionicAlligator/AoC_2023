TESTING = False
PART = 1
OUTPUT_TO_CONSOLE = False


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
        elif line.strip() == "END":  # "END" means end of test specification
            tests.append((expected, inputs.copy()))
            inputs = []
        else:
            inputs.append(line.rstrip())

    return tests


def parse_input(inputs):
    patterns = []
    pattern_rows = []

    for line in inputs:
        if line == "":
            patterns.append(pattern_rows)
            pattern_rows = []
        else:
            pattern_rows.append(line)

    patterns.append(pattern_rows)
    return patterns


def read_input(filename):
    file = open(filename, "r")
    lines = [line.rstrip() for line in file]
    return lines


def transpose(pattern):
    transposed_pattern = list(map(list, zip(*pattern)))

    transposed_pattern_strings = []

    for row in transposed_pattern:
        row_as_string = "".join(row)
        transposed_pattern_strings.append(row_as_string)

    return transposed_pattern_strings


def find_reflections(pattern, vertical=False):
    if vertical:
        log("Vertical: ", end="")
        pattern = transpose(pattern)
    else:
        log("Horizontal: ", end="")

    for index in range(1, len(pattern)):
        reflectable_rows = min(index, len(pattern) - index)

        forward_image = "".join(pattern[index:index + reflectable_rows])
        backward_image = "".join(reversed(pattern[index - reflectable_rows:index]))

        if forward_image == backward_image:
            log(f"{forward_image} == {backward_image}  ", end="")
            log(f"MATCH: {index}")
            return index

    log("No matches")
    return 0


def part1(inputs):
    patterns = parse_input(inputs)

    total = 0

    for pattern in patterns:
        horizontal_reflections = find_reflections(pattern, False)
        vertical_reflections = find_reflections(pattern, True)

        if horizontal_reflections == 0 and vertical_reflections == 0:
            print(f"No matches: {pattern}")

        total += horizontal_reflections * 100 + vertical_reflections

    return total


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
