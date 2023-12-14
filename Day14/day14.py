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


def parse_input(inputs):
    platform = []

    for y, row in enumerate(inputs):
        platform.append([])

        for x, pos in enumerate(row):
            platform[y].append(pos)

    return platform


def transpose(platform):
    return [[row[i] for row in platform] for i in range(len(platform[0]))]


def tilt(platform, direction="north"):
    tilted_platform = []

    if direction == "north":
        platform = transpose(platform)

        for row_num, row in enumerate(platform):
            tilted_platform.append([])
            empty_positions = []

            for column_num, pos in enumerate(row):
                match pos:
                    case '#':
                        empty_positions = []
                        tilted_platform[row_num].append('#')

                    case '.':
                        empty_positions.append(column_num)
                        tilted_platform[row_num].append('.')

                    case 'O':
                        if len(empty_positions) > 0:
                            new_rock_pos = empty_positions.pop(0)
                            tilted_platform[row_num][new_rock_pos] = 'O'
                            empty_positions.append(column_num)
                            tilted_platform[row_num].append('.')
                        else:
                            tilted_platform[row_num].append('O')

        tilted_platform = transpose(tilted_platform)

    log(f"{tilted_platform}")

    return tilted_platform


def extract_rock_positions(platform, rock_type='O'):
    rock_positions = []

    for row_num, row in enumerate(reversed(platform)):
        for column_num, pos in enumerate(row):
            if pos == rock_type:
                rock_positions.append((row_num + 1, column_num))

    log(f"{rock_positions =}")

    return rock_positions


def calc_load(rock_positions):
    total = 0

    for y, x in rock_positions:
        total += y

    return total


def part1(inputs):
    platform = parse_input(inputs)
    platform_tilted_north = tilt(platform)
    round_rock_positions = extract_rock_positions(platform_tilted_north)
    return calc_load(round_rock_positions)


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
