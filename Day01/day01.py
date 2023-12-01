TESTING = False
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


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def part1(inputs):
    sum = 0

    digits = [[char for char in line if char.isdigit()] for line in inputs]
    log(digits)

    for line in digits:
        num_string = line[0] + line[-1]
        num = int(num_string)
        sum += num

    return sum

def part2(inputs):
    new_inputs = []
    digits_as_strings = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

    for old_line in inputs:
        log(f"{old_line=}")
        line = old_line

        first_match = {'pos': 999999999999}
        last_match = {'pos': -1}

        new_line = line

        for num in range(1, len(digits_as_strings) + 1):
            first_num_pos = line.find(digits_as_strings[num - 1])
            last_num_pos = line.rfind(digits_as_strings[num - 1])

            if first_match['pos'] > first_num_pos >= 0:
                first_match = {'pos': first_num_pos, 'num_string': digits_as_strings[num - 1], 'num': str(num)}

            if last_match['pos'] < last_num_pos:
                last_match = {'pos': last_num_pos, 'num_string': digits_as_strings[num - 1], 'num': str(num)}

        if 'num_string' in first_match.keys():
            new_line = new_line[:first_match['pos']] + first_match['num'] + new_line[first_match['pos'] + 1:]

        if 'num_string' in last_match.keys():
            new_line = new_line[:last_match['pos']] + last_match['num'] + new_line[last_match['pos'] + 1:]

        log(f"{new_line=}\n")

        new_inputs.append(new_line)

    return part1(new_inputs)


if TESTING:
    print("Part 1")
    tests = read_tests("sampleInput.txt")

    for expected, inputs in tests:
        # actual = part1(inputs)
        actual = part2(inputs)

        if expected == str(actual):
            print(f"Passed: {inputs} -> {actual}\n")
        else:
            print(f"Failed: {inputs} -> {actual}, expected {expected}\n")
else:
    inputs = read_input("input.txt")

    print("Part 1: ", part1(inputs))
    print("Part 2: ", part2(inputs))
