import re

TESTING = False
PART = 2
OUTPUT_TO_CONSOLE = True

CUBES_CONSTRAINT = {'red': 12, 'green': 13, 'blue': 14}


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


def extract_cube_info(cube_details):
    cubes = {}

    for cube in cube_details:
        cube_info = re.search('(\d+) ([a-z]+)', cube)
        num_cubes, colour = cube_info.groups()

        cubes[colour] = int(num_cubes)

    return cubes


def extract_draw_info(draw_details):
    draws = []

    for draw in draw_details:
        cube_details = draw.split(",")

        draws.append(extract_cube_info(cube_details))

    return draws


def extract_game_info(inputs):
    games = {}

    for game in inputs:
        game_info = re.search('Game (\d+):(.*)', game)
        game_id = int(game_info.group(1))
        draw_details = game_info.group(2).split(";")

        games[game_id] = extract_draw_info(draw_details)

    return games


def display_game_info(games):
    for game_ID, draws in games.items():
        log(f"Game {game_ID}: ", end="")

        for draw in draws:
            for colour, num_cubes in draw.items():
                log(f"{num_cubes} {colour}", end=",")

            log("", end=";")

        log("")


def determine_min_cubes(games):
    min_cubes = {}

    for game_id, draws in games.items():
        min_red = min_green = min_blue = 0

        for draw in draws:
            min_red = max(min_red, draw.get('red', 0))
            min_green = max(min_green, draw.get('green', 0))
            min_blue = max(min_blue, draw.get('blue', 0))

        min_cubes[game_id] = {'red': min_red, 'green': min_green, 'blue': min_blue}

    return min_cubes


def determine_possible_games(games, constraint):
    possible_games = []

    max_red = constraint['red']
    max_green = constraint['green']
    max_blue = constraint['blue']

    min_cubes = determine_min_cubes(games)

    for game_id in games:
        min_game_cubes = min_cubes[game_id]

        if (    (min_game_cubes['red'] <= max_red) and
                (min_game_cubes['green'] <= max_green) and
                (min_game_cubes['blue'] <= max_blue)):
            possible_games.append(game_id)

    return possible_games


def determine_cube_set_powers(min_cubes):
    powers = []

    for cube_set in min_cubes.values():
        power = cube_set['red'] * cube_set['green'] * cube_set['blue']
        powers.append(power)

    return powers


def part1(inputs):
    games = extract_game_info(inputs)
    display_game_info(games)
    possible_games = determine_possible_games(games, CUBES_CONSTRAINT)
    return sum(possible_games)


def part2(inputs):
    games = extract_game_info(inputs)
    min_cubes = determine_min_cubes(games)
    powers = determine_cube_set_powers(min_cubes)
    return sum(powers)


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
