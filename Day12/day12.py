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


def parse_input(inputs, folded=False):
    springs = []
    broken_springs = []
    patterns = []
    num_damaged_springs = []

    for row in inputs:
        spring_string, broken_spring_string = row.split(" ")

        if folded:
            spring_string = ((spring_string + "?") * 5)[0:-1]
            broken_spring_string = ((broken_spring_string + ",") * 5)[0:-1]

        springs.append(spring_string.replace('.', 'g').replace('?', 'u').replace('#', 'b'))

        broken_springs_on_row = [int(num) for num in broken_spring_string.split(',')]

        broken_springs.append(broken_springs_on_row)

        # num_damaged_springs.append(sum(broken_springs_on_row))

        # pattern = "g*?"
        #
        # for index, num_springs in enumerate(broken_springs_on_row):
        #     if index == len(broken_springs_on_row) - 1:
        #         pattern += "b{" + str(num_springs) + "}g*?$"
        #     else:
        #         pattern += "b{" + str(num_springs) + "}g+?"
        #
        # patterns.append(pattern)

    return springs, broken_springs, patterns, num_damaged_springs


# def generate_spring_arrangements(spring_row, num_damaged_springs):
#     spring_arrangements = []
#
#     if len(spring_row) < num_damaged_springs:
#         return []
#
#     if 'u' not in spring_row:
#         if spring_row.count('b') == num_damaged_springs:
#             return [spring_row]
#         else:
#             return []
#
#     if spring_row[0] in ['u', 'b']:
#         for spring_arrangement in generate_spring_arrangements(spring_row[1:], num_damaged_springs - 1):
#             spring_arrangements.append("b" + spring_arrangement)
#
#     if spring_row[0] != 'b':
#         for spring_arrangement in generate_spring_arrangements(spring_row[1:], num_damaged_springs):
#             spring_arrangements.append("g" + spring_arrangement)
#
#     return spring_arrangements


def generate_spring_arrangements(spring_row, broken_spring_row, string_so_far):
    if spring_row == "":
        return [string_so_far]

    spring_arrangements = []

    num_broken_springs = sum(broken_spring_row)

    if num_broken_springs + len(broken_spring_row) - 1 > len(spring_row):
        return []

    if num_broken_springs > spring_row.count('b') + spring_row.count('u'):
        return []

    if spring_row == 'g':
        if num_broken_springs == 0:
            return ["g"]
        else:
            return []

    if len(broken_spring_row) == 0:
        if spring_row.count('b') > 0:
            return []
        else:
            return [spring_row.replace('u', 'g')]

    if (len(broken_spring_row) == 1 and
            re.match('^[bu]{' + str(num_broken_springs) + '}$', spring_row)):
        return [spring_row.replace('u', 'b')]

    this_char = spring_row[0]

    match this_char:
        case 'g':
            string_so_far += "g"
            spring_arrangements.extend(generate_spring_arrangements(spring_row[1:], broken_spring_row, string_so_far))

        case 'b':
            num_broken = broken_spring_row[0]

            if re.match('^[bu]{' + str(num_broken) + '}[gu]', spring_row):
                string_so_far += ('b' * num_broken) + 'g'
                spring_arrangements.extend(
                    generate_spring_arrangements(spring_row[num_broken + 1:],
                                                 broken_spring_row[1:],
                                                 string_so_far))
            else:
                return []
        case 'u':
            if len(broken_spring_row) > 0:
                num_broken = broken_spring_row[0]

                if re.search('^[bu]{' + str(num_broken) + '}[gu]', spring_row):
                    string_so_far_assuming_broken = string_so_far + ('b' * num_broken) + 'g'

                    sub_arrangements = generate_spring_arrangements(spring_row[num_broken + 1:],
                                                                    broken_spring_row[1:],
                                                                    string_so_far_assuming_broken)
                    spring_arrangements.extend(sub_arrangements)

            string_so_far_assuming_good = string_so_far + "g"

            spring_arrangements.extend(
                generate_spring_arrangements(spring_row[1:],
                                             broken_spring_row,
                                             string_so_far_assuming_good))

    return spring_arrangements


def determine_possible_arrangements(springs, broken_springs, patterns, num_damaged_springs):
    possible_arrangements = []

    for row_num in range(len(springs)):
        possible_arrangements.append([])

        spring_row = springs[row_num]
        broken_spring_row = broken_springs[row_num]
        # pattern = patterns[row_num]
        # damaged_spring_count = num_damaged_springs[row_num]

        possible_arrangements.append(generate_spring_arrangements(spring_row, broken_spring_row, ""))

        # all_spring_arrangements = generate_spring_arrangements(spring_row, damaged_spring_count)
        #
        # for spring_arrangement in all_spring_arrangements:
        #     if re.match(pattern, spring_arrangement):
        #         possible_arrangements[row_num].append(spring_arrangement)

    return possible_arrangements


def count_possible_arrangements(possible_arrangements):
    total = 0

    for spring_row_arrangements in possible_arrangements:
        total += len(spring_row_arrangements)

    return total


def part1(inputs):
    springs, broken_springs, patterns, num_damaged_springs = parse_input(inputs)
    possible_arrangements = determine_possible_arrangements(springs, broken_springs, patterns, num_damaged_springs)
    return count_possible_arrangements(possible_arrangements)


def part2(inputs):
    return 0


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
