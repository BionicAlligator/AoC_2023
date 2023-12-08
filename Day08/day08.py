import re
from math import lcm

TESTING = False
PART = 2
OUTPUT_TO_CONSOLE = True


class Node:
    def __init__(self, name, left, right):
        self.name = name
        self.left = left
        self.right = right
        self.is_start_node = self.name[2] == 'A'
        self.is_end_node = self.name[2] == 'Z'
        self.steps_to_end = -1

    def calc_steps_to_end(self, nodes, instructions):
        steps = 0
        instruction_index = 0
        current_node = self

        while not current_node.is_end_node:
            turn = instructions[instruction_index]
            next_node_name = current_node.left if turn == 'L' else current_node.right
            current_node = nodes[next_node_name]
            instruction_index = (instruction_index + 1) % len(instructions)
            steps += 1

        self.steps_to_end = steps


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
        elif line.strip() == "":
            pass
        else:
            inputs.append(line.rstrip())

    return tests


def read_input(filename):
    file = open(filename, "r")
    lines = [line.rstrip() for line in file if line.rstrip()]
    return lines


def parse_maps(inputs):
    nodes = {}
    instructions = inputs[0]

    for line in inputs[1:]:
        name, left, right = re.findall(r'\b\w{3}\b', line)
        nodes.update({name: Node(name, left, right)})

    return nodes, instructions


def walk_map(nodes, instructions):
    steps = 0
    instruction_index = 0
    next_node_name = 'AAA'

    while not next_node_name == "ZZZ":
        current_node = nodes[next_node_name]
        turn = instructions[instruction_index]
        next_node_name = current_node.left if turn == 'L' else current_node.right
        instruction_index = (instruction_index + 1) % len(instructions)
        steps += 1

    return steps


def part1(inputs):
    nodes, instructions = parse_maps(inputs)
    return walk_map(nodes, instructions)


def part2(inputs):
    nodes, instructions = parse_maps(inputs)

    start_nodes = [node for node in nodes.values() if node.is_start_node]

    for node in start_nodes:
        node.calc_steps_to_end(nodes, instructions)

    steps_to_end = [node.steps_to_end for node in start_nodes]

    return lcm(*steps_to_end)


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
