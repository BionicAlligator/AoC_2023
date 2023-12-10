from shapely.geometry import Point, Polygon

TESTING = False
PART = 2
OUTPUT_TO_CONSOLE = True


class Node:
    def __init__(self, y, x, char):
        self.neighbour_coords = []
        self.neighbours = []
        self.is_visited = False
        self.is_enclosed = False
        self.distance_from_start = float("inf")

        self.y = y
        self.x = x
        self.char = char

        if char == "S":
            self.is_start_node = True
            self.distance_from_start = 0
        else:
            self.is_start_node = False

        self.determine_neighbours()

    def __str__(self):
        return (f"Coords: {self.y, self.x}  Start Node: {self.is_start_node}  "
                f"Enclosed: {self.is_enclosed}  Visited: {self.is_visited}")

    def is_neighbour(self, y, x):
        return True if (y, x) in self.neighbour_coords else False

    def determine_neighbours(self):
        match self.char:
            case "|":
                self.neighbour_coords.append((self.y - 1, self.x))
                self.neighbour_coords.append((self.y + 1, self.x))
            case "-":
                self.neighbour_coords.append((self.y, self.x - 1))
                self.neighbour_coords.append((self.y, self.x + 1))
            case "L":
                self.neighbour_coords.append((self.y - 1, self.x))
                self.neighbour_coords.append((self.y, self.x + 1))
            case "J":
                self.neighbour_coords.append((self.y - 1, self.x))
                self.neighbour_coords.append((self.y, self.x - 1))
            case "7":
                self.neighbour_coords.append((self.y + 1, self.x))
                self.neighbour_coords.append((self.y, self.x - 1))
            case "F":
                self.neighbour_coords.append((self.y + 1, self.x))
                self.neighbour_coords.append((self.y, self.x + 1))

    def determine_start_node_neighbours(self, nodes):
        for node_row in nodes:
            for node in node_row:
                if node.is_neighbour(self.y, self.x):
                    self.neighbour_coords.append((node.y, node.x))

    def connect(self, nodes):
        for neighbour_y, neighbour_x in self.neighbour_coords:
            if 0 <= neighbour_y < len(nodes) and 0 <= neighbour_x < len(nodes[0]):
                self.neighbours.append(nodes[neighbour_y][neighbour_x])

    def visit(self, distance_from_start):
        self.is_visited = True

        if self.distance_from_start > distance_from_start:
            self.distance_from_start = distance_from_start

        for neighbour in self.neighbours:
            if not neighbour.is_visited:
                return neighbour

        for neighbour in self.neighbours:
            if neighbour.is_start_node:
                return neighbour

    def determine_if_enclosed(self, node_polygon):
        if not self.is_visited:
            self.is_enclosed = Point(self.y, self.x).within(node_polygon)


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
    nodes = []
    start_node = None

    for y, line in enumerate(inputs):
        nodes.append([])

        for x, char in enumerate(line):
            nodes[y].append(Node(y, x, char))

            if nodes[y][x].is_start_node:
                start_node = nodes[y][x]

    start_node.determine_start_node_neighbours(nodes)

    return nodes, start_node


def connect_nodes(nodes):
    for node_row in nodes:
        for node in node_row:
            node.connect(nodes)

    return nodes


def walk_tunnel(nodes, start_node):
    node_coords = []

    start_node.is_visited = True
    current_node = start_node.neighbours[0]
    distance_from_start = 1

    while current_node != start_node:
        current_node = current_node.visit(distance_from_start)
        distance_from_start += 1
        node_coords.append((current_node.y, current_node.x))

    return nodes, distance_from_start, Polygon(node_coords)


def determine_enclosed_nodes(nodes, node_polygon):
    for node_row in nodes:
        for node in node_row:
            node.determine_if_enclosed(node_polygon)

    return nodes


def print_map(nodes):
    warnings = []
    unvisited_enclosed_nodes = 0

    for node_row in nodes:
        for node in node_row:
            if node.is_visited:
                log(node.char, end="")
            elif node.is_enclosed:
                unvisited_enclosed_nodes += 1
                log("I", end="")
            else:
                log("O", end="")

            if node.is_visited and node.is_enclosed:
                warnings.append(f"WARNING: Marked as Visited and Enclosed: {node}")

        log("")

    log(f"Number of Unvisited Enclosed nodes = {unvisited_enclosed_nodes}")

    for warning in warnings:
        log(warning)


def count_enclosed_nodes(nodes):
    enclosed_count = 0

    for node_row in nodes:
        for node in node_row:
            if node.is_enclosed and not node.is_visited:
                enclosed_count += 1

    return enclosed_count


def part1(inputs):
    nodes, start_node = parse_input(inputs)

    nodes = connect_nodes(nodes)

    nodes, distance_from_start, _ = walk_tunnel(nodes, start_node)

    return distance_from_start // 2


def part2(inputs):
    nodes, start_node = parse_input(inputs)

    nodes = connect_nodes(nodes)

    nodes, distance_from_start, node_polygon = walk_tunnel(nodes, start_node)

    nodes = determine_enclosed_nodes(nodes, node_polygon)

    print_map(nodes)

    return count_enclosed_nodes(nodes)


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
