import re

TESTING = False
PART = 1
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


def extract_game_info(inputs):
    games = {}

    for game in inputs:
        game_regex = re.compile(r'Game (\d+):(.*)')
        game_info = game_regex.search(game)
        game_ID = int(game_info.group(1))
        draw_details = game_info.group(2).split(";")

        draws = []
        for draw in draw_details:
            dice = draw.split(",")

            draw = {}
            for die_type in dice:
                die_regex = re.compile(r'(\d+) ([a-z]+)')
                die_info = die_regex.search(die_type)
                num_dice, colour = die_info.groups()

                draw[colour] = int(num_dice)

            draws.append(draw)

        games[game_ID] = draws

    return games


def display_game_info(games):
    for game_ID, draws in games.items():
        log(f"Game {game_ID}: ", end="")

        for draw in draws:
            for colour, num_dice in draw.items():
                log(f"{num_dice} {colour}", end=",")

            log("", end=";")

        log("")


def determine_possible_games(games, constraint):
    possible_games = []

    max_red = constraint['red']
    max_green = constraint['green']
    max_blue = constraint['blue']

    for game_id, draws in games.items():
        min_red = min_green = min_blue = 0

        for draw in draws:
            min_red = max(min_red, draw.get('red', 0))
            min_green = max(min_green, draw.get('green', 0))
            min_blue = max(min_blue, draw.get('blue', 0))

        if (min_red <= max_red) and (min_green <= max_green) and (min_blue <= max_blue):
            possible_games.append(game_id)

    return possible_games


def part1(inputs):
    games = extract_game_info(inputs)
    display_game_info(games)
    possible_games = determine_possible_games(games, {'red': 12, 'green': 13, 'blue': 14})
    return sum(possible_games)


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
