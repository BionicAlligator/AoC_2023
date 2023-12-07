from collections import defaultdict
from functools import cmp_to_key

TESTING = False
PART = 1
OUTPUT_TO_CONSOLE = True

CARD_STRENGTHS = list(reversed(['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']))
HAND_TYPES = list(reversed(["High card", "One pair", "Two pair", "Three of a kind", "Full house", "Four of a kind", "Five of a kind"]))


class Hand:
    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = int(bid)
        self.hand_type = self.determine_type()

    def __str__(self):
        return f"Type: {self.hand_type}, Cards: {self.cards}, Bid: {self.bid}"

    def determine_type(self):
        card_counts = []

        for card_strength in CARD_STRENGTHS:
            cards_of_strength = len([card for card in self.cards if card == card_strength])
            card_counts.append(cards_of_strength)

        if 5 in card_counts:
            hand_type = "Five of a kind"
        elif 4 in card_counts:
            hand_type = "Four of a kind"
        elif 3 in card_counts:
            if 2 in card_counts:
                hand_type = "Full house"
            else:
                hand_type = "Three of a kind"
        elif 2 in card_counts:
            if card_counts.count(2) == 2:
                hand_type = "Two pair"
            else:
                hand_type = "One pair"
        else:
            hand_type = "High card"

        return hand_type


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
    hands = []

    for hand_string in inputs:
        card_string, bid = hand_string.rstrip().split(" ")
        cards = [*card_string]
        hand = Hand(cards, bid)
        log(f"{str(hand)}")
        hands.append(hand)

    return hands


def compare(hand1, hand2):
    for card_index in range(0, 5):
        hand1_card_strength = CARD_STRENGTHS.index(hand1.cards[card_index])
        hand2_card_strength = CARD_STRENGTHS.index(hand2.cards[card_index])

        if hand1_card_strength > hand2_card_strength:
            return -1
        elif hand2_card_strength > hand1_card_strength:
            return 1

    return 0


def sorted_by_strength(hands):
    return sorted(hands, key=cmp_to_key(compare))


def part1(inputs):
    log(f"{HAND_TYPES=}, {CARD_STRENGTHS=}")

    mixed_hands = parse_input(inputs)

    hands_by_type = defaultdict(list)

    for hand in mixed_hands:
        hands_by_type[hand.hand_type].append(hand)

    sorted_hands_by_type = {}

    for hand_type, hands in hands_by_type.items():
        sorted_hands_by_type.update({hand_type: sorted_by_strength(hands)})

    log(f"{sorted_hands_by_type=}")

    hands_in_order = []

    for hand_type in HAND_TYPES:
        hands_in_order.extend(sorted_hands_by_type.get(hand_type, []))

    log("Hands in order:")
    for hand in hands_in_order:
        log(f"  {hand}")

    winnings = 0

    for index, hand in enumerate(list(reversed(hands_in_order))):
        winnings += hand.bid * (index + 1)

    return winnings


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
