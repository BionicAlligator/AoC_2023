import sys
from copy import deepcopy

TESTING = False
PART = 2
OUTPUT_TO_CONSOLE = True


class Tile:
    def __init__(self, tile_type):
        self.tile_type = tile_type
        self.onward_path = None
        self.caching = False

    def __str__(self):
        return f'{self.tile_type}'

    def cache_onward_path(self, grid, y, x):
        if self.tile_type == '|':
            onward_path1 = follow_path(grid, (y - 1, x), (-1, 0), [])
            onward_path2 = follow_path(grid, (y + 1, x), (1, 0), [])
            self.onward_path = onward_path1.union(onward_path2)
        elif self.tile_type == '-':
            onward_path1 = follow_path(grid, (y, x - 1), (0, -1), [])
            onward_path2 = follow_path(grid, (y, x + 1), (0, 1), [])
            self.onward_path = onward_path1.union(onward_path2)


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


def print_path(grid, path):
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if (y, x) in path:
                log("#", end="")
            else:
                log(".", end="")

        log("")


def within_bounds(grid, y, x):
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])


def follow_path(grid, start_point, direction, visited):
    path = set()

    if (start_point, direction) in visited:
        return path

    visited.append((start_point, direction))

    y, x = start_point
    dir_y, dir_x = direction

    if not within_bounds(grid, y, x):
        return path

    path.add((y, x))

    tile = grid[y][x]

    while tile.tile_type == '.':
        y += dir_y
        x += dir_x

        if within_bounds(grid, y, x):
            visited.append(((y, x), direction))
            path.add((y, x))
            tile = grid[y][x]
        else:
            return path

    match tile.tile_type:
        case '/':
            new_dir_y = -dir_x
            new_dir_x = -dir_y
            new_direction = (new_dir_y, new_dir_x)

            onward_path = follow_path(grid, (y + new_dir_y, x + new_dir_x), new_direction, visited)
            return path.union(onward_path)

        case '\\':
            new_dir_y = dir_x
            new_dir_x = dir_y
            new_direction = (new_dir_y, new_dir_x)

            onward_path = follow_path(grid, (y + new_dir_y, x + new_dir_x), new_direction, visited)
            return path.union(onward_path)

        case '|':
            if dir_x == 0:
                onward_path = follow_path(grid, (y + dir_y, x + dir_x), direction, visited)
                return path.union(onward_path)
            else:
                if tile.onward_path:
                    return path.union(tile.onward_path)

                if tile.caching:
                    return path

                tile.cache_onward_path(grid, y, x)
                return path.union(tile.onward_path)

                # onward_path1 = follow_path(grid, (y - 1, x), (-1, 0), visited)
                # onward_path2 = follow_path(grid, (y + 1, x), (1, 0), visited)
                # # tile.onward_path = onward_path1.union(onward_path2)
                # return path.union(onward_path1).union(onward_path2)

        case '-':
            if dir_y == 0:
                onward_path = follow_path(grid, (y + dir_y, x + dir_x), direction, visited)
                return path.union(onward_path)
            else:
                if tile.onward_path:
                    return path.union(tile.onward_path)

                if tile.caching:
                    return path

                tile.cache_onward_path(grid, y, x)
                return path.union(tile.onward_path)

                # onward_path1 = follow_path(grid, (y, x - 1), (0, -1), visited)
                # onward_path2 = follow_path(grid, (y, x + 1), (0, 1), visited)
                # # tile.onward_path = onward_path1.union(onward_path2)
                # return path.union(onward_path1).union(onward_path2)

    log(f"Unknown Tile Type: Aborting")
    exit(1)


def clear_cached_onward_paths(grid):
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            tile.onward_path = None


def part1(inputs):
    grid = parse_input(inputs)
    print_grid(grid, False)
    path = follow_path(grid, (0, 0), (0, 1), [])
    return len(path)


def part2(inputs):
    max_energised_tiles = 0

    grid = parse_input(inputs)

    for start_y in range(len(grid)):
        if start_y % 10 == 0:
            log(f"{start_y=}")

        max_energised_tiles = max(max_energised_tiles, len(follow_path(grid, (start_y, 0), (0, 1), [])))
        max_energised_tiles = max(max_energised_tiles, len(follow_path(grid, (start_y, len(grid[0]) - 1), (0, -1), [])))

    for start_x in range(len(grid[0])):
        if start_x % 10 == 0:
            log(f"{start_x=}")

        path_length = len(follow_path(grid, (0, start_x), (1, 0), []))
        if start_x == 3:
            log(f"{path_length =}")
        max_energised_tiles = max(max_energised_tiles, len(follow_path(grid, (0, start_x), (1, 0), [])))
        max_energised_tiles = max(max_energised_tiles, len(follow_path(grid, (len(grid) - 1, start_x), (-1, 0), [])))

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
