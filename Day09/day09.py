TESTING = False
PART = 2
OUTPUT_TO_CONSOLE = True


class Sequence:
    def __init__(self, values):
        self.values = values
        self.next_sequence = None

    def first_value(self):
        return self.values[0]

    def last_value(self):
        return self.values[-1]

    def calc_differences(self):
        differences = []

        for index in range(1, len(self.values)):
            diff = self.values[index] - self.values[index - 1]
            differences.append(diff)

        self.next_sequence = Sequence(differences)

    def extend(self):
        if not all(value == 0 for value in self.values):
            self.calc_differences()
            self.next_sequence.extend()

            self.values.insert(0, self.first_value() - self.next_sequence.first_value())
            self.values.append(self.last_value() + self.next_sequence.last_value())
        else:
            self.values.insert(0, 0)
            self.values.append(0)


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
    sequences = []

    for line in inputs:
        values = [int(value) for value in line.split()]
        sequences.append(Sequence(values))

    return sequences


def part1(inputs):
    total = 0

    sequences = parse_input(inputs)

    for sequence in sequences:
        sequence.extend()
        total = total + sequence.last_value()

    return total


def part2(inputs):
    total = 0

    sequences = parse_input(inputs)

    for sequence in sequences:
        sequence.extend()
        total = total + sequence.first_value()

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
