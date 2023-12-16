import sys
from copy import deepcopy

TESTING = False
PART = 2
OUTPUT_TO_CONSOLE = True


class Tile:
    def __init__(self, tile_type):
        self.tile_type = tile_type
        self.beams = {(0, 1): 0, (0, -1): 0, (1, 0): 0, (-1, 0): 0}

    def __str__(self):
        return f'{self.tile_type} {self.beams[(0, 1)]}> {self.beams[(0, -1)]}< {self.beams[(1, 0)]}v {self.beams[(-1, 0)]}^'

    def energy_level(self, direction=None):
        if direction:
            return self.beams[direction]
        else:
            return sum(self.beams.values())


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
    grid = []

    for y, row in enumerate(inputs):
        grid.append([])

        for x, tile in enumerate(row):
            grid[y].append(Tile(tile))

    return grid


def print_grid(grid, verbose=False):
    for row in grid:
        for tile in row:
            if verbose:
                log(f"{tile}  ", end="")
            else:
                log(f"{tile.tile_type}", end="")

        log("")


def track_beam(grid, start_point, direction):
    y, x = start_point
    dir_y, dir_x = direction

    if y < 0 or x < 0 or y >= len(grid) or x >= len(grid[0]):
        return grid

    tile = grid[y][x]

    if tile.energy_level(direction) > 0:
        return grid

    tile.beams[direction] += 1

    while tile.tile_type == '.':
        next_y = y + dir_y
        next_x = x + dir_x

        if next_y < 0 or next_x < 0 or next_y >= len(grid) or next_x >= len(grid[0]):
            return grid

        y = next_y
        x = next_x

        tile = grid[y][x]

        if tile.energy_level(direction) > 0:
            return grid

        tile.beams[direction] += 1

    match tile.tile_type:
        case '/':
            new_dir_y = -dir_x
            new_dir_x = -dir_y
            new_direction = (new_dir_y, new_dir_x)

            return track_beam(grid, (y + new_dir_y, x + new_dir_x), new_direction)

        case '\\':
            new_dir_y = dir_x
            new_dir_x = dir_y
            new_direction = (new_dir_y, new_dir_x)

            return track_beam(grid, (y + new_dir_y, x + new_dir_x), new_direction)

        case '|':
            if dir_x == 0:
                return track_beam(grid, (y + dir_y, x + dir_x), direction)
            else:
                grid = track_beam(grid, (y - 1, x), (-1, 0))
                return track_beam(grid, (y + 1, x), (1, 0))

        case '-':
            if dir_y == 0:
                return track_beam(grid, (y + dir_y, x + dir_x), direction)
            else:
                grid = track_beam(grid, (y, x - 1), (0, -1))
                return track_beam(grid, (y, x + 1), (0, 1))

    return grid


def count_energised_tiles(grid):
    total = 0

    for row in grid:
        for tile in row:
            if tile.energy_level() > 0:
                total += 1

    return total


def part1(inputs):
    grid = parse_input(inputs)
    print_grid(grid, False)
    grid = track_beam(grid, (0, 0), (0, 1))
    print_grid(grid, True)
    return count_energised_tiles(grid)


def part2(inputs):
    max_energised_tiles = 0

    grid = parse_input(inputs)

    for start_y in range(len(grid)):
        if start_y % 10 == 0:
            log(f"{start_y=}")

        test_grid = deepcopy(grid)
        test_grid = track_beam(test_grid, (start_y, 0), (0, 1))
        max_energised_tiles = max(max_energised_tiles, count_energised_tiles(test_grid))

        test_grid = deepcopy(grid)
        test_grid = track_beam(test_grid, (start_y, len(grid[0]) - 1), (0, -1))
        max_energised_tiles = max(max_energised_tiles, count_energised_tiles(test_grid))

    for start_x in range(len(grid[0])):
        if start_x % 10 == 0:
            log(f"{start_x=}")

        test_grid = deepcopy(grid)
        test_grid = track_beam(test_grid, (0, start_x), (1, 0))
        max_energised_tiles = max(max_energised_tiles, count_energised_tiles(test_grid))

        test_grid = deepcopy(grid)
        test_grid = track_beam(test_grid, (len(grid) - 1, start_x), (-1, 0))
        max_energised_tiles = max(max_energised_tiles, count_energised_tiles(test_grid))

    return max_energised_tiles


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
