TESTING = False
PART = 2
OUTPUT_TO_CONSOLE = False

TOTAL_SPINS = 1000000000


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
    return [[pos for pos in row] for row in inputs]


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
    return [(row_num + 1, column_num)
            for row_num, row in enumerate(reversed(platform))
            for column_num, pos in enumerate(row)
            if pos == rock_type]


def calc_load(rock_positions):
    return sum([y for y, _ in rock_positions])


def spin_platform(platform):
    tilted_platform = tilt(platform, "north")
    tilted_platform = tilt(tilted_platform, "west")
    tilted_platform = tilt(tilted_platform, "south")
    tilted_platform = tilt(tilted_platform, "east")
    return tilted_platform


def fast_forward_to_end(platform_string, spin_num, spin_results):
    tilted_platform, last_here_spin_num = spin_results[platform_string]
    spins_between_cycles = spin_num - last_here_spin_num
    spin_num = TOTAL_SPINS - (TOTAL_SPINS - last_here_spin_num) % spins_between_cycles
    return spin_num, tilted_platform


def part1(inputs):
    platform = parse_input(inputs)
    platform_tilted_north = tilt(platform)
    round_rock_positions = extract_rock_positions(platform_tilted_north)
    return calc_load(round_rock_positions)


def part2(inputs):
    platform = parse_input(inputs)

    spin_results = {}
    been_here_before = False
    spin_num = 0

    while spin_num < TOTAL_SPINS:
        platform_string = convert_to_string(platform)

        if not been_here_before and platform_string in spin_results:
            been_here_before = True
            spin_num, platform = fast_forward_to_end(platform_string, spin_num, spin_results)
        else:
            platform = spin_platform(platform)
            spin_results.update({platform_string: (platform, spin_num)})

        spin_num += 1

    round_rock_positions = extract_rock_positions(platform)

    return calc_load(round_rock_positions)


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
