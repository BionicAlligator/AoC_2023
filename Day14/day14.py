TESTING = False
PART = 2
OUTPUT_TO_CONSOLE = False

TOTAL_SPINS = 1000000000

tilt_result_cache = {}
spin_result_cache = {}


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


def reverse_rows(platform):
    return [list(reversed(row)) for row in platform]


def convert_to_string(platform):
    return "".join((pos for row in platform for pos in row))


def tilt(platform, direction="north"):
    if direction == "north":
        platform = transpose(platform)
    if direction == "east":
        platform = reverse_rows(platform)
    if direction == "south":
        platform = reverse_rows(transpose(platform))

    platform_string = convert_to_string(platform)

    if (direction, platform_string) in tilt_result_cache:
        tilted_platform = tilt_result_cache[(direction, platform_string)]
    else:
        tilted_platform = []

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

        tilt_result_cache.update({(direction, platform_string): tilted_platform})

    if direction == "north":
        tilted_platform = transpose(tilted_platform)
    if direction == "east":
        tilted_platform = reverse_rows(tilted_platform)
    if direction == "south":
        tilted_platform = reverse_rows(tilted_platform)
        tilted_platform = transpose(tilted_platform)

    log(f"{direction}: {tilted_platform}")

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
    platform = parse_input(inputs)

    been_here_before = False

    spin_num = 0

    while spin_num < TOTAL_SPINS:
        if spin_num % 1000000 == 0:
            print(f"{spin_num=}")

        platform_string = convert_to_string(platform)

        if not been_here_before and platform_string in spin_result_cache:
            been_here_before = True
            tilted_platform, last_here_spin_num = spin_result_cache[platform_string]
            spins_between_cycles = spin_num - last_here_spin_num
            spin_num = TOTAL_SPINS - (TOTAL_SPINS - last_here_spin_num) % spins_between_cycles
        else:
            tilted_platform = tilt(platform, "north")
            tilted_platform = tilt(tilted_platform, "west")
            tilted_platform = tilt(tilted_platform, "south")
            tilted_platform = tilt(tilted_platform, "east")

            spin_result_cache.update({platform_string: (tilted_platform, spin_num)})

        if platform == tilted_platform:
            break

        platform = tilted_platform

        spin_num += 1

    round_rock_positions = extract_rock_positions(platform)
    load = calc_load(round_rock_positions)

    return load


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
