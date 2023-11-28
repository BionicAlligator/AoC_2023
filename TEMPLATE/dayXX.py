TESTING = True
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


def part1(inputs):
    return


if TESTING:
    print("Part 1")
    tests = read_tests("sampleInput.txt")

    for expected, inputs in tests:
        actual = part1(inputs)

        if expected == str(actual):
            print(f"Passed: {inputs} -> {actual}\n")
        else:
            print(f"Failed: {inputs} -> {actual}, expected {expected}\n")
else:
    inputs = read_input("input.txt")

    print("Part 1: ", part1(inputs))
