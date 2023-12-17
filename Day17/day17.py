# NOT WORKING.  Attempt at an A* approach with object to represent nodes
# Switched to standard Dijkstra using priority queue of tuples instead (see Day17b.py)

from copy import copy

TESTING = False
PART = 1
OUTPUT_TO_CONSOLE = True


class Node:
    def __init__(self, pos, heat_loss, end):
        self.y, self.x = pos
        self.heat_loss = heat_loss
        end_y, end_x = end
        self.min_heat_loss_to_end = abs(end_y - self.y) + abs(end_x - self.x)
        self.heat_loss_from_start = float('inf')
        self.predecessor = None
        self.direction_tracker = ((0, 0), float('inf'))

    def __str__(self):
        return self.heat_loss

    def heat_loss_via_node(self):
        return self.heat_loss_from_start + self.min_heat_loss_to_end


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
    factory = (len(inputs) - 1, len(inputs[0]) - 1)
    city = [[Node((y, x), int(heat_loss), factory) for x, heat_loss in enumerate(row)] for y, row in enumerate(inputs)]
    return city


def get_best_node(node_list):
    lowest_heat_loss = float('inf')
    best_node = None

    for node in node_list:
        if node.heat_loss_via_node() <= lowest_heat_loss:
            lowest_heat_loss = node.heat_loss_via_node()
            best_node = node

    return best_node


def get_possible_next_nodes(city, current):
    NEIGHBOUR_OFFSETS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    neighbours = []

    (dir_y, dir_x), num_steps = current.direction_tracker

    for offset_y, offset_x in NEIGHBOUR_OFFSETS:
        if (-dir_y, -dir_x) != (offset_y, offset_x):
            if not (num_steps == 3 and (dir_y, dir_x) == (offset_y, offset_x)):
                neighbour_y = current.y + offset_y
                neighbour_x = current.x + offset_x

                if 0 <= neighbour_y < len(city) and 0 <= neighbour_x < len(city[0]):
                    neighbours.append(city[current.y + offset_y][current.x + offset_x])

    return neighbours


def extract_path_from_start(node):
    path = []

    while node:
        path.append(node)
        node = node.predecessor

    return list(reversed(path))


def print_path_on_city(city, path):
    for y, row in enumerate(city):
        for x, node in enumerate(row):
            on_path = False

            for path_node in path:
                if (path_node.y, path_node.x) == (y, x):
                    on_path = True

            log(".", end="") if on_path else log(f"{node.heat_loss}", end="")

        log("")


def find_best_path(city, start, end):
    start.heat_loss_from_start = 0

    open_list = [start]

    while open_list:
        current = get_best_node(open_list)
        log(f"{(current.y, current.x)}")

        open_list.remove(current)

        if current == end:
            log(f"Found path to factory with heat loss of {end.heat_loss_from_start}")
            return extract_path_from_start(end)

        neighbours = get_possible_next_nodes(city, current)

        for neighbour in neighbours:
            tentative_heat_loss_to_neighbour = current.heat_loss_from_start + neighbour.heat_loss

            (dir_y, dir_x), num_steps = current.direction_tracker

            new_dir_y = neighbour.y - current.y
            new_dir_x = neighbour.x - current.x

            if new_dir_y == dir_y and new_dir_x == dir_x:
                neighbour_direction_tracker = ((dir_y, dir_x), num_steps + 1)
            else:
                neighbour_direction_tracker = ((new_dir_y, new_dir_x), 1)

            if (tentative_heat_loss_to_neighbour < neighbour.heat_loss_from_start or
                    (tentative_heat_loss_to_neighbour == neighbour.heat_loss_from_start and
                     neighbour.direction_tracker[1] > neighbour_direction_tracker[1])):
                neighbour.predecessor = current
                neighbour.heat_loss_from_start = tentative_heat_loss_to_neighbour
                neighbour.direction_tracker = neighbour_direction_tracker

                if neighbour not in open_list:
                    open_list.append(neighbour)

            # If the number of steps taken to get here is less, it should also be explored regardless
            elif (tentative_heat_loss_to_neighbour - neighbour.heat_loss_from_start < 50) and neighbour.direction_tracker[1] > neighbour_direction_tracker[1]:
                neighbour = copy(neighbour)

                neighbour.predecessor = current
                neighbour.heat_loss_from_start = tentative_heat_loss_to_neighbour
                neighbour.direction_tracker = neighbour_direction_tracker

                if neighbour not in open_list:
                    open_list.append(neighbour)

    log("NO PATH FOUND")
    exit(1)


def heat_loss_along_path(path):
    total_heat_loss = 0
    return total_heat_loss


def part1(inputs):
    city = parse_input(inputs)
    lavafall = city[0][0]
    factory = city[len(city) - 1][len(city[0]) - 1]

    path = find_best_path(city, lavafall, factory)

    print_path_on_city(city, path)

    return factory.heat_loss_from_start


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
