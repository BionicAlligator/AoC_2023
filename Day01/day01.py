TESTING = False
PART = 2
OUTPUT_TO_CONSOLE = False

DIGITS_AS_STRINGS = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


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


def extract_digits(inputs):
    return [[char for char in line if char.isdigit()] for line in inputs]


def generate_calibration_values(digits):
    calibration_values = []

    for line in digits:
        calibration_value_string = line[0] + line[-1]
        calibration_values.append(int(calibration_value_string))

    return calibration_values


def replace_char_at_pos(string, index, new_char):
    return string[:index] + new_char + string[index + 1:]


def find_digit_string_first_occurrence(digit, string, first_match):
    first_digit_pos = string.find(DIGITS_AS_STRINGS[digit - 1])

    if first_match['pos'] > first_digit_pos >= 0:
        first_match = {'pos': first_digit_pos, 'digit_string': DIGITS_AS_STRINGS[digit - 1], 'digit': str(digit)}

    return first_match


def find_digit_string_last_occurrence(digit, string, last_match):
    last_digit_pos = string.rfind(DIGITS_AS_STRINGS[digit - 1])

    if last_match['pos'] < last_digit_pos >= 0:
        last_match = {'pos': last_digit_pos, 'digit_string': DIGITS_AS_STRINGS[digit - 1], 'digit': str(digit)}

    return last_match


def replace_first_digit_string_if_any(string):
    first_match = {'pos': float('inf')}

    for digit in range(1, len(DIGITS_AS_STRINGS) + 1):
        first_match = find_digit_string_first_occurrence(digit, string, first_match)

    if 'digit_string' in first_match.keys():
        return replace_char_at_pos(string, first_match['pos'], first_match['digit'])

    return string


def replace_last_digit_string_if_any(string):
    last_match = {'pos': float('-inf')}

    for digit in range(1, len(DIGITS_AS_STRINGS) + 1):
        last_match = find_digit_string_last_occurrence(digit, string, last_match)

    if 'digit_string' in last_match.keys():
        return replace_char_at_pos(string, last_match['pos'], last_match['digit'])

    return string


def part1(inputs):
    digits = extract_digits(inputs)
    log(digits)

    calibration_values = generate_calibration_values(digits)

    return sum(calibration_values)


def part2(inputs):
    parsed_inputs = []

    for orig_line in inputs:
        log(f"{orig_line=}")

        new_line = replace_first_digit_string_if_any(orig_line)
        new_line = replace_last_digit_string_if_any(new_line)

        log(f"{new_line=}\n")
        parsed_inputs.append(new_line)

    return part1(parsed_inputs)


if TESTING:
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
else:
    inputs = read_input("input.txt")

    print("Part 1: ", part1(inputs))

    if PART == 2:
        print("Part 2: ", part2(inputs))
