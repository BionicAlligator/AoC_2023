import re
from copy import deepcopy

TESTING = False
PART = 2
OUTPUT_TO_CONSOLE = True


class Block:
    def __init__(self, x_range, y_range, z_range):
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range
        self.overlapping_blocks = []
        self.supporting_blocks = []
        self.supports = set()

    def intersects(self, other_block):
        if intersect(self.x_range, other_block.x_range) and intersect(self.y_range, other_block.y_range):
            return True

        return False

    # Generate list of blocks that overlap in x,y plane, sorted by stop z val
    def determine_overlapping_blocks(self, blocks):
        for block in blocks:
            if block == self:
                continue

            if self.intersects(block):
                self.overlapping_blocks.append(block)

        self.overlapping_blocks.sort(key=lambda b: b.z_range.stop)

    def settle(self):
        #   Set current block's start z val to equal stop z val of the block in the list that has
        #     the highest stop z val lower than or equal to the current block's start z val.
        block_immediately_below = None

        for block in self.overlapping_blocks:
            if block.z_range.stop - 1 == self.z_range.start:
                log("UNEXPECTED: Overlapping Z ranges")
                exit(1)

            if block.z_range.stop > self.z_range.start:
                break
            else:
                block_immediately_below = block

        drop = self.z_range.start - block_immediately_below.z_range.stop
        self.z_range = range(self.z_range.start - drop, self.z_range.stop - drop)

        # Record as 'supporting_blocks' all blocks in the list that have a stop z val one lower than
        #   the new start z val of the current block
        # Each supporting block also records that it supports this block
        for block in self.overlapping_blocks:
            if block.z_range.stop == self.z_range.start and block.z_range.start > 0:
                self.supporting_blocks.append(block)
                block.supports.add(self)


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


def intersect(range1, range2):
    return range(max(range1.start, range2.start), min(range1.stop, range2.stop)) or None


def parse_input(inputs):
    blocks = []

    min_y = min_x = float('inf')
    max_y = max_x = float('-inf')

    for row in inputs:
        nums = [int(num_string) for num_string in re.findall(r'\d+', row)]

        x_range = range(min(nums[0], nums[3]), max(nums[0], nums[3]) + 1)
        y_range = range(min(nums[1], nums[4]), max(nums[1], nums[4]) + 1)
        z_range = range(min(nums[2], nums[5]), max(nums[2], nums[5]) + 1)

        min_x = min(x_range.start, min_x)
        max_x = max(x_range.stop, max_x)
        min_y = min(y_range.start, min_y)
        max_y = max(y_range.stop, max_y)

        blocks.append(Block(x_range, y_range, z_range))

    floor = Block(range(min_x, max_x), range(min_y, max_y), range(0, 1))
    blocks.append(floor)

    return blocks, floor


def settle(blocks):
    # Sort blocks by start z val (lowest first)
    blocks.sort(key=lambda b: b.z_range.start)

    for block in blocks[1:]:
        block.determine_overlapping_blocks(blocks)
        block.settle()

    return


def extract_disintegrable_blocks(blocks):
    # A block can be disintegrated if:
    #   1. It is not supporting any other block
    #   2. It is one of several blocks supporting a block  AND  it is not also the only block supporting another block

    disintegrable_blocks = set()
    single_support_blocks = set()

    for block in blocks[1:]:
        # This block is not supporting any others
        if len(block.supports) == 0:
            disintegrable_blocks.add(block)

        # If there are multiple blocks supporting this one, they are potential candidates for disintegration
        if len(block.supporting_blocks) > 1:
            disintegrable_blocks.update(block.supporting_blocks)
        # If this block is supported by a single block then that supporting block can not be disintegrated
        elif len(block.supporting_blocks) == 1:
            single_support_blocks.add(block.supporting_blocks[0])

    # Remove any blocks that are the only support blocks from the candidates for disintegration
    for block in single_support_blocks:
        if block in disintegrable_blocks:
            disintegrable_blocks.remove(block)

    return disintegrable_blocks


def analyse_chain_reactions(blocks, disintegrable_blocks):
    total_falling_blocks = 0

    for block in blocks[1:]:
        if block in disintegrable_blocks:
            continue

        will_fall = set([block])
        to_check = set(block.supports)

        while to_check:
            check_block = to_check.pop()

            if all(b in will_fall for b in check_block.supporting_blocks):
                will_fall.add(check_block)
                to_check.update(set(check_block.supports))

        # The -1 is to account for the disintegrated block (which doesn't actually fall)
        total_falling_blocks += len(will_fall) - 1

    return total_falling_blocks


def part1(inputs):
    blocks, floor = parse_input(inputs)
    settle(blocks)
    disintegrable_blocks = extract_disintegrable_blocks(blocks)
    return len(disintegrable_blocks)


def part2(inputs):
    blocks, floor = parse_input(inputs)
    settle(blocks)
    disintegrable_blocks = extract_disintegrable_blocks(blocks)
    return analyse_chain_reactions(blocks, disintegrable_blocks)


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
