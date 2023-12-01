TESTING = False
PART = 2
OUTPUT_TO_CONSOLE = False


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


def part1(inputs):
    sum_of_calibration_values = 0

    digits = [[char for char in line if char.isdigit()] for line in inputs]
    log(digits)

    for line in digits:
        calibration_value_string = line[0] + line[-1]
        calibration_value = int(calibration_value_string)
        sum_of_calibration_values += calibration_value

    return sum_of_calibration_values


def part2(inputs):
    DIGITS_AS_STRINGS = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

    parsed_inputs = []

    for orig_line in inputs:
        log(f"{orig_line=}")
        line = orig_line

        first_match = {'pos': float('inf')}
        last_match = {'pos': float('-inf')}

        new_line = line

        for digit in range(1, len(DIGITS_AS_STRINGS) + 1):
            first_digit_pos = line.find(DIGITS_AS_STRINGS[digit - 1])
            last_digit_pos = line.rfind(DIGITS_AS_STRINGS[digit - 1])

            if first_match['pos'] > first_digit_pos >= 0:
                first_match = {'pos': first_digit_pos, 'digit_string': DIGITS_AS_STRINGS[digit - 1], 'digit': str(digit)}

            if last_match['pos'] < last_digit_pos >= 0:
                last_match = {'pos': last_digit_pos, 'digit_string': DIGITS_AS_STRINGS[digit - 1], 'digit': str(digit)}

        if 'digit_string' in first_match.keys():
            new_line = new_line[:first_match['pos']] + first_match['digit'] + new_line[first_match['pos'] + 1:]

        if 'digit_string' in last_match.keys():
            new_line = new_line[:last_match['pos']] + last_match['digit'] + new_line[last_match['pos'] + 1:]

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
