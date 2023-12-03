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
            inputs.append(line)

    return tests


def read_input(filename):
    file = open(filename, "r")
    lines = [line for line in file]
    return lines


def walk_schematic(inputs):
    schematic_numbers = []
    schematic_number_positions = {}
    engine_part_positions = set()
    potential_gears = set()

    next_schematic_number_index = 0

    for y, line in enumerate(inputs):
        schematic_number = ""

        for x, char in enumerate(line):
            if char.isdigit():
                schematic_number += char
                schematic_number_positions.update({(y, x): next_schematic_number_index})
            else:
                if schematic_number:
                    schematic_numbers.append({'Number': int(schematic_number), 'IsPartNum': False})
                    next_schematic_number_index += 1
                    schematic_number = ""

                if char not in ['.', '\n']:
                    engine_part_positions.add((y, x))

                    if char == '*':
                        potential_gears.add((y, x))

    return schematic_numbers, schematic_number_positions, engine_part_positions, potential_gears


def tag_part_numbers(schematic_numbers, schematic_number_positions, engine_part_positions):
    for part_pos_y, part_pos_x in engine_part_positions:
        for check_pos_y in range(part_pos_y - 1, part_pos_y + 2):
            for check_pos_x in range(part_pos_x - 1, part_pos_x + 2):
                if (check_pos_y, check_pos_x) in schematic_number_positions:
                    schematic_number_index = schematic_number_positions[(check_pos_y, check_pos_x)]
                    schematic_numbers[schematic_number_index]['IsPartNum'] = True

    return schematic_numbers


def extract_part_numbers(schematic_numbers):
    part_numbers = []

    for schematic_num in schematic_numbers:
        if schematic_num['IsPartNum']:
            part_numbers.append(schematic_num['Number'])

    return part_numbers


def extract_gear_ratios(schematic_numbers, schematic_number_positions, potential_gears):
    gear_ratios = []

    for part_pos_y, part_pos_x in potential_gears:
        adjacent_schematic_number_indices = set()

        for check_pos_y in range(part_pos_y - 1, part_pos_y + 2):
            for check_pos_x in range(part_pos_x - 1, part_pos_x + 2):
                if (check_pos_y, check_pos_x) in schematic_number_positions:
                    schematic_number_index = schematic_number_positions[(check_pos_y, check_pos_x)]
                    adjacent_schematic_number_indices.add(schematic_number_index)

        if len(adjacent_schematic_number_indices) == 2:
            gear_ratio = 1

            for schematic_number_index in adjacent_schematic_number_indices:
                gear_ratio *= schematic_numbers[schematic_number_index]['Number']

            gear_ratios.append(gear_ratio)

    return gear_ratios


def calc_gear_ratios(gears):
    return []


def part1(inputs):
    schematic_numbers, schematic_number_positions, engine_part_positions, _ = walk_schematic(inputs)
    schematic_numbers = tag_part_numbers(schematic_numbers, schematic_number_positions, engine_part_positions)
    part_numbers = extract_part_numbers(schematic_numbers)
    return sum(part_numbers)


def part2(inputs):
    schematic_numbers, schematic_number_positions, _, potential_gears = walk_schematic(inputs)
    gear_ratios = extract_gear_ratios(schematic_numbers, schematic_number_positions, potential_gears)
    return sum(gear_ratios)


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
