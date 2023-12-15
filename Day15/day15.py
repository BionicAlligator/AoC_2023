import re
from collections import OrderedDict

TESTING = False
PART = 2
OUTPUT_TO_CONSOLE = True


class Instruction:
    def __init__(self, groups):
        self.label = groups[0]
        self.box = apply_hash(self.label)
        self.operation = "insert" if groups[1] == '=' else "remove"

        if self.operation == "insert":
            self.lens = int(groups[2])
        else:
            self.lens = None

    def __str__(self):
        if self.operation == "insert":
            return f"Insert lens {self.lens} with label {self.label} into box {self.box}"
        else:
            return f"Remove lens with label {self.label} from box {self.box}"


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


def parse_input(inputs, hash_check=True):
    steps = inputs[0].split(",")

    instructions = []

    for step in steps:
        result = re.search(r'^([a-z]+)([=-])(\d*)$', step)
        instructions.append(Instruction(result.groups()))

    return steps if hash_check else instructions


def apply_hash(step):
    hash_value = 0

    log(f"{step}")

    for char in step:
        hash_value += ord(char)
        hash_value *= 17
        hash_value %= 256

    return hash_value


def hash_sequence(init_sequence):
    return [apply_hash(step) for step in init_sequence]


def initialise_facility(instructions):
    boxes = [OrderedDict() for box_num in range(256)]

    for instruction in instructions:
        box = boxes[instruction.box]

        match instruction.operation:
            case "insert":
                box.update({instruction.label: instruction.lens})

            case "remove":
                box.pop(instruction.label, None)

    return boxes


def focusing_power(boxes):
    total_power = 0

    for box_num, box in enumerate(boxes):
        slot_num = 1

        for lens, power in box.items():
            total_power += (box_num + 1) * slot_num * power
            slot_num += 1

    return total_power


def part1(inputs):
    init_sequence = parse_input(inputs)
    hashed_sequence = hash_sequence(init_sequence)
    return sum(hashed_sequence)


def part2(inputs):
    instructions = parse_input(inputs, False)

    for instruction in instructions:
        log(f"{instruction}")

    boxes = initialise_facility(instructions)

    return focusing_power(boxes)


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
