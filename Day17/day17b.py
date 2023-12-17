from heapq import heapify, heappop, heappush

TESTING = False
PART = 2
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
    city = [[int(heat_loss) for heat_loss in row] for row in inputs]
    return city


def find_path_with_lowest_heat_loss(city, start, end, ultra_crucible=False):
    NEIGHBOUR_OFFSETS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    done = set()
    frontier = []
    heappush(frontier, (0, start, ((0, 0), 0)))

    while frontier:
        heat_loss_from_start, pos, direction_tracker = heappop(frontier)
        y, x = pos
        (dir_y, dir_x), num_steps = direction_tracker

        if (pos, direction_tracker) in done:
            continue

        done.add((pos, direction_tracker))

        if pos == end:
            if ultra_crucible and num_steps < 4:
                continue

            return heat_loss_from_start

        for offset in NEIGHBOUR_OFFSETS:
            if (-dir_y, -dir_x) == offset:
                continue

            if ultra_crucible:
                if (dir_y, dir_x) == offset:
                    if num_steps == 10:
                        continue
                else:
                    if 0 < num_steps < 4:
                        continue
            elif (dir_y, dir_x) == offset and num_steps == 3:
                continue

            offset_y, offset_x = offset
            neighbour_y = y + offset_y
            neighbour_x = x + offset_x

            if 0 <= neighbour_y < len(city) and 0 <= neighbour_x < len(city[0]):
                neighbour_heat_loss = city[neighbour_y][neighbour_x]
                neighbour_heat_loss_from_start = heat_loss_from_start + neighbour_heat_loss

                if (dir_y, dir_x) == offset:
                    new_direction_tracker = (offset, num_steps + 1)
                else:
                    new_direction_tracker = (offset, 1)

                heappush(frontier, (neighbour_heat_loss_from_start, (neighbour_y, neighbour_x), new_direction_tracker))

    print("NOT FOUND")
    exit(1)


def part1(inputs):
    city = parse_input(inputs)
    lavapool = (0, 0)
    factory = (len(city) - 1, len(city[0]) - 1)
    total_heat_loss = find_path_with_lowest_heat_loss(city, lavapool, factory)
    return total_heat_loss


def part2(inputs):
    city = parse_input(inputs)
    lavapool = (0, 0)
    factory = (len(city) - 1, len(city[0]) - 1)
    total_heat_loss = find_path_with_lowest_heat_loss(city, lavapool, factory, True)
    return total_heat_loss


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
