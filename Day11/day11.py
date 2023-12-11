TESTING = False
PART = 2
OUTPUT_TO_CONSOLE = True

EXPANSION_MULTIPLIER = 1000000


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


def print_universe(universe):
    for row in universe:
        for sector in row:
            log(sector, end="")

        log("")


def transpose(input_list):
    return [[row[i] for row in input_list] for i in range(len(input_list[0]))]


def expand_universe_in_one_dimension(inputs, universe_is_old=False):
    expanded_universe = []

    for row in inputs:
        if all(element in ['.', '$'] for element in row):
            if universe_is_old:
                expanded_universe.append(['$'] * len(row))
            else:
                expanded_universe.append(row)
                expanded_universe.append(row)
        else:
            expanded_universe.append(row)

    return expanded_universe


def expand_universe(inputs, universe_is_old=False):
    expanded_universe_x = expand_universe_in_one_dimension(inputs, universe_is_old)
    expanded_universe_x_transposed = transpose(expanded_universe_x)
    expanded_universe_transposed = expand_universe_in_one_dimension(expanded_universe_x_transposed, universe_is_old)
    expanded_universe = transpose(expanded_universe_transposed)
    return expanded_universe


def extract_galaxies(universe):
    galaxies = []

    for y, row in enumerate(universe):
        for x, sector in enumerate(row):
            if sector == "#":
                galaxies.append((y, x))

    return galaxies


def extract_old_galaxies(universe):
    galaxies = []

    y = 0

    for row in universe:
        x = 0

        if all(element == '$' for element in row):
            y += EXPANSION_MULTIPLIER
        else:
            for sector in row:
                if sector == '$':
                    x += EXPANSION_MULTIPLIER
                else:
                    if sector == '#':
                        galaxies.append((y, x))

                    x += 1

            y += 1

    return galaxies


def measure_distances_between(galaxies):
    shortest_paths = []
    galaxies_to_pop = len(galaxies) - 1

    for _ in range(galaxies_to_pop):
        galaxy1 = galaxies.pop()

        for galaxy2 in galaxies:
            shortest_paths.append(abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1]))

    return shortest_paths


def part1(inputs):
    expanded_universe = expand_universe(inputs)
    print_universe(expanded_universe)
    galaxies = extract_galaxies(expanded_universe)
    inter_galactic_shortest_paths = measure_distances_between(galaxies)
    return sum(inter_galactic_shortest_paths)


def part2(inputs):
    expanded_universe = expand_universe(inputs, True)
    print_universe(expanded_universe)
    galaxies = extract_old_galaxies(expanded_universe)
    inter_galactic_shortest_paths = measure_distances_between(galaxies)
    return sum(inter_galactic_shortest_paths)


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
