from collections import deque

TESTING = False
PART = 2
OUTPUT_TO_CONSOLE = True

OFFSETS = {'>': (0, 1), '<': (0, -1), 'v': (1, 0), '^': (-1, 0)}


class Node:
    def __init__(self, pos, desc, neighbour_coords):
        y, x = pos
        self.y = y
        self.x = x
        self.desc = desc
        self.neighbour_coords = neighbour_coords
        self.neighbours = {}

    def __str__(self):
        return f"({self.x}, {self.y})"

    def link(self, nodes_by_coord):
        # if self.desc in OFFSETS:
        #     offset_y, offset_x = OFFSETS[self.desc]
        #     neighbour_coord = (self.y + offset_y, self.x + offset_x)
        #     self.neighbours = [nodes_by_coord[neighbour_coord]]
        # else:
        for neighbour_coord in self.neighbour_coords:
            self.neighbours.update({nodes_by_coord[neighbour_coord]: 1})

    def add_shortcut(self, neighbour):
        dest = neighbour
        prev = self

        nodes_on_route = []

        while len(dest.neighbours) == 2:
            nodes_on_route.append(dest)

            path_length_to_dest = self.neighbours.pop(dest)

            next_neighbour = [{node: path_length + path_length_to_dest}
                               for node, path_length in dest.neighbours.items()
                               if node != prev][0]

            self.neighbours.update(next_neighbour)
            prev = dest
            dest, path_increment = next_neighbour.popitem()

        return dest, path_increment, nodes_on_route


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


def parse_input(grid):
    nodes_by_coord = {}

    for y, row in enumerate(grid):
        for x, desc in enumerate(row):
            if grid[y][x] == '#':
                continue

            neighbour_coords = []

            for offset_y, offset_x in OFFSETS.values():
                neighbour_y = y + offset_y
                neighbour_x = x + offset_x

                if 0 <= neighbour_y < len(grid) and 0 <= neighbour_x < len(row) and grid[neighbour_y][neighbour_x] != '#':
                    neighbour_coords.append((neighbour_y, neighbour_x))

            nodes_by_coord.update({(y, x): Node((y, x), desc, neighbour_coords)})

    for node in nodes_by_coord.values():
        node.link(nodes_by_coord)

    start_node = nodes_by_coord[(0, 1)]
    end_node = nodes_by_coord[(len(grid) - 1, len(grid[0]) - 2)]

    return nodes_by_coord.values(), start_node, end_node


def find_longest_path(current, end):
    longest_path_length = 0
    longest_path = []

    to_check = deque([(0, current, [current])])

    while to_check:
        steps, current, path = to_check.pop()

        if current == end:
            if steps > longest_path_length:
                longest_path_length = steps
                longest_path = path
                log(f"Path found of length {longest_path_length}, still to check: {len(to_check)}")
                continue

        neighbour_info = current.neighbours.copy()

        for neighbour, path_increment in neighbour_info.items():
            if neighbour in path:
                continue

            new_path = path.copy()

            if len(neighbour.neighbours) == 2:
                neighbour, path_increment, nodes_on_route = current.add_shortcut(neighbour)
                new_path.extend(nodes_on_route)

            new_path.append(neighbour)

            to_check.append((steps + path_increment, neighbour, new_path))

    return longest_path_length, longest_path


def display_path(grid, path):
    node_coords = []

    for node in path:
        node_coords.append((node.y, node.x))

    for y, row in enumerate(grid):
        for x, desc in enumerate(row):
            if (y, x) in node_coords:
                log(".", end="")
            elif desc in ".<>v^":
                log(" ", end="")
            else:
                log(desc, end="")

        log("")


def part1(inputs):
    nodes, start_node, end_node = parse_input(inputs)
    return find_longest_path(start_node, end_node)


def part2(inputs):
    nodes, start_node, end_node = parse_input(inputs)
    longest_path_length, longest_path = find_longest_path(start_node, end_node)
    display_path(inputs, longest_path)
    return longest_path_length


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
