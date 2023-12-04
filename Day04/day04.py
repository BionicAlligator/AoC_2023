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


def parse_scratchcard_info(inputs):
    scratchcards = []

    for card in inputs:
        numbers = card.split(": ")[1].split(" | ")
        winning_numbers = numbers[0].split()
        our_numbers = numbers[1].split()
        scratchcards.append([winning_numbers, our_numbers])

    return scratchcards


def evaluate_scratchcards(scratchcards):
    scratchcard_values = []

    for winning_numbers, our_numbers in scratchcards:
        our_winners = [num for num in our_numbers if num in winning_numbers]
        log(our_winners)
        if len(our_winners) > 0:
            scratchcard_values.append(2**(len(our_winners) - 1))

    return scratchcard_values

def part1(inputs):
    scratchcards = parse_scratchcard_info(inputs)
    scratchcard_values = evaluate_scratchcards(scratchcards)
    return sum(scratchcard_values)


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
