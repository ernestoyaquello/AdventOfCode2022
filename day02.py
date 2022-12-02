import input

PROBLEM_NUMBER = 2

ROCK = 1; PAPER = 2; SCISSORS = 3
LOSS = 0; DRAW = 3; WIN = 6
RESULTS = {
    ROCK: {ROCK: DRAW, PAPER: WIN, SCISSORS: LOSS},
    PAPER: {ROCK: LOSS, PAPER: DRAW, SCISSORS: WIN},
    SCISSORS: {ROCK: WIN, PAPER: LOSS, SCISSORS: DRAW},
}

def execute(is_part_two):
    input_lists = input.read_lists(problem_number = PROBLEM_NUMBER)
    return part_1(input_lists) if not is_part_two else part_2(input_lists)

def part_1(input_lists):
    hand_decoder = {'A': ROCK, 'B': PAPER, 'C': SCISSORS, 'X': ROCK, 'Y': PAPER, 'Z': SCISSORS}
    rounds = [(hand_decoder[first_hand_encoded], hand_decoder[last_hand_encoded]) for first_hand_encoded, last_hand_encoded in input_lists]
    return sum(last_hand + RESULTS[first_hand][last_hand] for first_hand, last_hand in rounds)

def part_2(input_lists):
    hand_decoder = {'A': ROCK, 'B': PAPER, 'C': SCISSORS}
    expected_result_decoder = {'X': LOSS, 'Y': DRAW, 'Z': WIN}
    first_hand_to_expected_result = [(hand_decoder[first_hand_encoded], expected_result_decoder[expected_result_encoded]) for first_hand_encoded, expected_result_encoded in input_lists]
    return sum(next(last_hand + result for last_hand, result in RESULTS[first_hand].items() if result == expected_result) for first_hand, expected_result in first_hand_to_expected_result)

print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))