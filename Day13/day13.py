TESTING = False
PART = 2
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


def read_input(filename):
    file = open(filename, "r")
    lines = [line.rstrip() for line in file]
    return lines


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


def transpose(pattern):
    return ["".join(row) for row in map(list, zip(*pattern))]


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


def find_smudges(pattern, vertical=False):
    if vertical:
        log("Vertical: ", end="")
        pattern = transpose(pattern)
    else:
        log("Horizontal: ", end="")

    potential_smudge_rows = []

    for index in range(1, len(pattern)):
        reflectable_rows = min(index, len(pattern) - index)

        forward_image = "".join(pattern[index:index + reflectable_rows])
        backward_image = "".join(reversed(pattern[index - reflectable_rows:index]))

        if abs(forward_image.count('#') - backward_image.count('#')) == 1:
            diff_indices = []

            for pos in range(len(forward_image)):
                if forward_image[pos] != backward_image[pos]:
                    diff_indices.append(pos)

            if len(diff_indices) == 1:
                log(f"Smudge found at ({index}, {diff_indices[0]})")
                return index

    log("No smudge found")
    return 0


def part1(inputs):
    patterns = parse_input(inputs)

    total = 0

    for pattern in patterns:
        horizontal_reflection = find_reflections(pattern, False)
        vertical_reflection = find_reflections(pattern, True)

        if horizontal_reflection == 0 and vertical_reflection == 0:
            print(f"No matches: {pattern}")

        total += horizontal_reflection * 100 + vertical_reflection

    return total


def part2(inputs):
    patterns = parse_input(inputs)

    total = 0

    for pattern in patterns:
        orig_horizontal_reflection = find_reflections(pattern, False)
        orig_vertical_reflection = find_reflections(pattern, True)

        if orig_horizontal_reflection == 0 and orig_vertical_reflection == 0:
            print(f"No matches: {pattern}")

        new_horizontal_reflection = find_smudges(pattern, False)
        new_vertical_reflection = find_smudges(pattern, True)

        total += new_horizontal_reflection * 100 + new_vertical_reflection

    return total


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
