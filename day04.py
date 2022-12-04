import input

PROBLEM_NUMBER = 4

def execute(is_part_two):
    range_pairs = [[list(map(int, range_pair.split('-'))), list(map(int, range_pair2.split('-')))] for range_pair, range_pair2 in input.read_lists(problem_number = PROBLEM_NUMBER, item_separator = ',')]
    return part_1(range_pairs) if not is_part_two else part_2(range_pairs)

def part_1(range_pairs):
    return sum(1 for first, second in range_pairs if (second[0] >= first[0] and second[1] <= first[1]) or (first[0] >= second[0] and first[1] <= second[1]))

def part_2(range_pairs):
    return sum(1 for first, second in range_pairs if (first[0] >= second[0] and first[0] <= second[1]) or (first[1] >= second[0] and first[1] <= second[1]) or (second[0] > first[0] and second[1] < first[1]))

print("Part 1: " + str(execute(is_part_two = False)))
print("Part 2: " + str(execute(is_part_two = True)))